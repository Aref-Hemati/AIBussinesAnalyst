"""Typed model of the requirement admission-control loop.

The gate that matters is in ``Project``: a requirement may not exist unless an
ACCEPT decision produced it. Everything else here is bookkeeping around that.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


class DecisionLabel(str, Enum):
    """Fine-grained outcome for one candidate statement."""

    ACCEPT = "ACCEPT"
    CLARIFY = "CLARIFY"
    REJECT = "REJECT"
    DUPLICATE = "DUPLICATE"
    CONFLICTING = "CONFLICTING"
    AMBIGUOUS = "AMBIGUOUS"
    OUT_OF_SCOPE = "OUT-OF-SCOPE"
    UNJUSTIFIED = "UNJUSTIFIED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT-EVIDENCE"


class SuperClass(str, Enum):
    """Scoring granularity for small samples.

    Nine-way F1 needs support we will not have industrially, so results are led
    by these three and the nine labels appear in error analysis.
    """

    ACCEPT = "ACCEPT"
    HOLD = "HOLD"
    BLOCK = "BLOCK"


SUPER_CLASS_OF: dict[DecisionLabel, SuperClass] = {
    DecisionLabel.ACCEPT: SuperClass.ACCEPT,
    DecisionLabel.CLARIFY: SuperClass.HOLD,
    DecisionLabel.AMBIGUOUS: SuperClass.HOLD,
    DecisionLabel.INSUFFICIENT_EVIDENCE: SuperClass.HOLD,
    DecisionLabel.REJECT: SuperClass.BLOCK,
    DecisionLabel.OUT_OF_SCOPE: SuperClass.BLOCK,
    DecisionLabel.UNJUSTIFIED: SuperClass.BLOCK,
    DecisionLabel.DUPLICATE: SuperClass.BLOCK,
    DecisionLabel.CONFLICTING: SuperClass.BLOCK,
}


def super_class_of(label: DecisionLabel) -> SuperClass:
    return SUPER_CLASS_OF[label]


class Action(str, Enum):
    """What the agent does next, chosen by the cost-sensitive rule."""

    ADMIT = "ADMIT"
    ASK = "ASK"
    BLOCK = "BLOCK"


class RequirementKind(str, Enum):
    FUNCTIONAL = "FR"
    NON_FUNCTIONAL = "NFR"
    BUSINESS_RULE = "BR"
    CONSTRAINT = "CONSTRAINT"


class RequirementStatus(str, Enum):
    DRAFT = "draft"
    CLARIFIED = "clarified"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"
    FROZEN = "frozen"


class SourceSpan(BaseModel):
    """Where a claim came from: a chat turn, or an offset in an uploaded file."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["message", "file"] = "message"
    ref: str = Field(description="message id, or file name")
    start: int | None = None
    end: int | None = None
    quote: str | None = None


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: _new_id("msg"))
    role: Literal["stakeholder", "analyst", "system"]
    text: str
    created_at: datetime = Field(default_factory=_utcnow)


class OrgRule(BaseModel):
    """A company hard rule the critic may cite when blocking."""

    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    tags: list[str] = Field(default_factory=list)


class UncertaintySignal(BaseModel):
    """Output of ``reqdecide.uncertainty``.

    ``interpretation_entropy`` measures disagreement between readings of the
    utterance, which is what a clarifying question can fix. ``mean_confidence``
    measures how sure the model is about each reading. Low confidence with low
    entropy means the model lacks knowledge, and asking the stakeholder will not
    supply it; retrieve org rules instead.
    """

    model_config = ConfigDict(extra="forbid")

    n_samples: int = Field(ge=1)
    n_clusters: int = Field(ge=1)
    cluster_sizes: list[int] = Field(default_factory=list)
    interpretation_entropy: float = Field(ge=0.0, description="Shannon entropy in nats")
    normalized_entropy: float = Field(ge=0.0, le=1.0)
    mean_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    dominant_interpretation: str | None = None
    interpretations: list[str] = Field(default_factory=list)

    @property
    def is_ambiguous(self) -> bool:
        """Genuine ambiguity: readings disagree rather than the model being unsure."""
        return self.n_clusters > 1 and self.normalized_entropy >= 0.5


class CostModel(BaseModel):
    """Costs the admission rule trades off.

    Sweeping these produces the risk-coverage curve rather than a single tuned
    operating point.
    """

    model_config = ConfigDict(extra="forbid")

    wrong_admit: float = Field(default=1.0, gt=0, description="unjustified requirement enters the spec")
    wrong_block: float = Field(default=1.0, gt=0, description="a real need is refused")
    ask: float = Field(default=0.15, ge=0, description="one stakeholder question")


class Decision(BaseModel):
    """One admission-control decision about one candidate statement."""

    model_config = ConfigDict(extra="forbid", use_enum_values=False)

    id: str = Field(default_factory=lambda: _new_id("dec"))
    candidate_text: str
    label: DecisionLabel
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str

    source_spans: list[SourceSpan] = Field(default_factory=list)
    business_objective_id: str | None = Field(
        default=None, description="null on an ACCEPT is what UNJUSTIFIED means"
    )
    questions: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    org_rule_refs: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    duplicate_of: str | None = None
    evidence: list[str] = Field(default_factory=list)

    uncertainty: UncertaintySignal | None = None
    expected_costs: dict[str, float] = Field(default_factory=dict)

    model_name: str | None = None
    prompt_hash: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    turn_index: int | None = None

    @property
    def super_class(self) -> SuperClass:
        return super_class_of(self.label)

    @model_validator(mode="after")
    def _check_label_action_coherence(self) -> Decision:
        expected = {
            SuperClass.ACCEPT: Action.ADMIT,
            SuperClass.HOLD: Action.ASK,
            SuperClass.BLOCK: Action.BLOCK,
        }[self.super_class]
        if self.action is not expected:
            raise ValueError(
                f"label {self.label.value} implies action {expected.value}, got {self.action.value}"
            )
        if self.action is Action.ASK and not self.questions:
            raise ValueError("an ASK decision must carry at least one question")
        if self.label is DecisionLabel.DUPLICATE and not self.duplicate_of:
            raise ValueError("DUPLICATE must name the requirement it duplicates")
        if self.label is DecisionLabel.CONFLICTING and not self.conflicts_with:
            raise ValueError("CONFLICTING must name what it conflicts with")
        return self


class AcceptanceCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: _new_id("ac"))
    text: str


class Requirement(BaseModel):
    """A specification row. It cannot exist without the decision that admitted it."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: _new_id("req"))
    decision_id: str
    kind: RequirementKind = RequirementKind.FUNCTIONAL
    text: str
    status: RequirementStatus = RequirementStatus.DRAFT
    priority: Literal["must", "should", "could", "wont"] | None = None
    user_story: str | None = None
    acceptance_criteria: list[AcceptanceCriterion] = Field(default_factory=list)
    source_spans: list[SourceSpan] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    business_objective_id: str | None = None


class OpenQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: _new_id("q"))
    decision_id: str
    text: str
    answered: bool = False
    answer: str | None = None


class VersionRecord(BaseModel):
    """A freeze event: RE management, which the surveys show is rare."""

    model_config = ConfigDict(extra="forbid")

    number: int = Field(ge=1)
    created_at: datetime = Field(default_factory=_utcnow)
    confirmed_by: str | None = None
    requirement_ids: list[str] = Field(default_factory=list)
    added: list[str] = Field(default_factory=list)
    removed: list[str] = Field(default_factory=list)
    note: str | None = None


class TurnInput(BaseModel):
    """Everything the policy may look at for one stakeholder turn.

    Passing this explicitly keeps replay deterministic: the same TurnInput must
    yield the same decision for a fixed model and seed.
    """

    model_config = ConfigDict(extra="forbid")

    utterance: str
    project_id: str | None = None
    turn_index: int = Field(default=0, ge=0)
    history: list[Message] = Field(default_factory=list)
    org_rules: list[OrgRule] = Field(default_factory=list)
    accepted_requirements: list[Requirement] = Field(default_factory=list)
    prior_decisions: list[Decision] = Field(default_factory=list)
    question_budget_remaining: int = Field(default=3, ge=0)
    costs: CostModel = Field(default_factory=CostModel)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def may_ask(self) -> bool:
        return self.question_budget_remaining > 0


class Project(BaseModel):
    """The whole elicitation session, and the artifact we score."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: _new_id("prj"))
    title: str
    language: str = "en"
    org_rule_set_id: str | None = None

    messages: list[Message] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    versions: list[VersionRecord] = Field(default_factory=list)

    def decision_by_id(self, decision_id: str) -> Decision | None:
        return next((d for d in self.decisions if d.id == decision_id), None)

    def orphan_requirements(self) -> list[Requirement]:
        """Requirements with no ACCEPT decision behind them. Must stay empty."""
        accepted = {d.id for d in self.decisions if d.label is DecisionLabel.ACCEPT}
        return [r for r in self.requirements if r.decision_id not in accepted]

    def trace_coverage(self) -> float:
        """Share of requirements that trace back to an ACCEPT decision."""
        if not self.requirements:
            return 1.0
        return 1.0 - len(self.orphan_requirements()) / len(self.requirements)

    def decision_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for d in self.decisions:
            counts[d.label.value] = counts.get(d.label.value, 0) + 1
        return counts

    @model_validator(mode="after")
    def _no_orphan_requirements(self) -> Project:
        orphans = self.orphan_requirements()
        if orphans:
            ids = ", ".join(r.id for r in orphans)
            raise ValueError(
                "requirements without an ACCEPT decision are not representable: " + ids
            )
        return self


__all__ = [
    "SUPER_CLASS_OF",
    "AcceptanceCriterion",
    "Action",
    "CostModel",
    "Decision",
    "DecisionLabel",
    "Message",
    "OpenQuestion",
    "OrgRule",
    "Project",
    "Requirement",
    "RequirementKind",
    "RequirementStatus",
    "SourceSpan",
    "SuperClass",
    "TurnInput",
    "UncertaintySignal",
    "VersionRecord",
    "super_class_of",
]
