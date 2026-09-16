"""Cost-sensitive admission: admit, ask, or block under a question budget.

The LLM may propose a label and a probability that the statement is a real need.
This module is the part that is allowed to override it. High interpretation
entropy spends a question instead of guessing. Duplicate and org-rule conflicts
block without asking. Everything else is an expected-cost comparison, so a
reviewer can sweep the three costs and see a curve rather than one tuned point.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schema import (
    Action,
    CostModel,
    Decision,
    DecisionLabel,
    SuperClass,
    TurnInput,
    UncertaintySignal,
    super_class_of,
)

AMBIGUITY_THRESHOLD = 0.5
CLOSE_COSTS_RATIO = 1.25


@dataclass(frozen=True)
class CriticFlags:
    """Deterministic facts the policy may trust more than the model's hunch."""

    duplicate_of: str | None = None
    conflicts_with: tuple[str, ...] = ()
    org_rule_ids: tuple[str, ...] = ()
    missing_evidence: bool = False
    unjustified: bool = False
    out_of_scope: bool = False
    infeasible: bool = False
    question: str | None = None
    alternative: str | None = None


@dataclass(frozen=True)
class AdmissionProposal:
    """What the generative side thinks, before the cost rule."""

    p_need: float
    label: DecisionLabel | None = None
    rationale: str = ""
    question: str | None = None


def expected_costs(p_need: float, costs: CostModel) -> dict[str, float]:
    """Immediate expected cost of each action, ignoring later turns.

    ASK is charged the question cost plus a residual: after the answer we still
    face the cheaper of admit/block, scaled by remaining uncertainty (1). That
    is deliberately conservative so asking is not free.
    """
    p = min(1.0, max(0.0, p_need))
    admit = (1.0 - p) * costs.wrong_admit
    block = p * costs.wrong_block
    residual = min(admit, block)
    ask = costs.ask + 0.5 * residual
    return {"ADMIT": admit, "ASK": ask, "BLOCK": block}


def _question_text(proposal: AdmissionProposal, flags: CriticFlags, fallback: str) -> str:
    return flags.question or proposal.question or fallback


def decide(
    turn: TurnInput,
    proposal: AdmissionProposal,
    uncertainty: UncertaintySignal | None = None,
    flags: CriticFlags | None = None,
) -> Decision:
    """Pick an action. Hard constraints first, then expected cost."""
    flags = flags or CriticFlags()
    p_need = min(1.0, max(0.0, proposal.p_need))
    costs = expected_costs(p_need, turn.costs)
    confidence = p_need if p_need >= 0.5 else 1.0 - p_need

    def make(
        label: DecisionLabel,
        rationale: str,
        *,
        questions: list[str] | None = None,
        extra_costs: dict[str, float] | None = None,
    ) -> Decision:
        action = {
            SuperClass.ACCEPT: Action.ADMIT,
            SuperClass.HOLD: Action.ASK,
            SuperClass.BLOCK: Action.BLOCK,
        }[super_class_of(label)]
        return Decision(
            candidate_text=turn.utterance,
            label=label,
            action=action,
            confidence=round(confidence, 4),
            rationale=rationale,
            questions=questions or [],
            alternatives=[flags.alternative] if flags.alternative else [],
            org_rule_refs=list(flags.org_rule_ids),
            conflicts_with=list(flags.conflicts_with),
            duplicate_of=flags.duplicate_of,
            evidence=[],
            uncertainty=uncertainty,
            expected_costs=extra_costs or costs,
            turn_index=turn.turn_index,
        )

    if flags.duplicate_of:
        return make(DecisionLabel.DUPLICATE, f"already covered by {flags.duplicate_of}")
    if flags.conflicts_with:
        return make(
            DecisionLabel.CONFLICTING,
            "conflicts with accepted requirement(s) " + ", ".join(flags.conflicts_with),
        )
    if flags.org_rule_ids and flags.out_of_scope:
        return make(
            DecisionLabel.OUT_OF_SCOPE,
            "blocked by org rule " + ", ".join(flags.org_rule_ids),
        )
    if flags.out_of_scope:
        return make(DecisionLabel.OUT_OF_SCOPE, "outside stated project scope")
    if flags.infeasible:
        return make(DecisionLabel.REJECT, "infeasible as stated")
    if flags.unjustified:
        if turn.may_ask:
            return make(
                DecisionLabel.CLARIFY,
                "no business objective yet; ask before writing a requirement",
                questions=[
                    _question_text(
                        proposal,
                        flags,
                        "Which business objective or stakeholder does this serve?",
                    )
                ],
            )
        return make(DecisionLabel.UNJUSTIFIED, "no business objective and no question budget left")

    if flags.missing_evidence:
        if turn.may_ask:
            return make(
                DecisionLabel.INSUFFICIENT_EVIDENCE,
                "quantitative claim without a source",
                questions=[
                    _question_text(
                        proposal,
                        flags,
                        "What current volume, contract, or measurement is that number based on?",
                    )
                ],
            )
        return make(DecisionLabel.REJECT, "numeric claim with no evidence and no budget to ask")

    ambiguous = bool(uncertainty and uncertainty.is_ambiguous)
    if ambiguous and turn.may_ask:
        return make(
            DecisionLabel.AMBIGUOUS,
            "interpretations of the utterance disagree; a question is cheaper than guessing",
            questions=[
                _question_text(
                    proposal,
                    flags,
                    "Which of these readings do you mean: "
                    + "; ".join((uncertainty.interpretations or [])[:3]),
                )
            ],
        )
    if ambiguous and not turn.may_ask:
        # Out of questions: refuse to invent a requirement from an ambiguous statement.
        return make(
            DecisionLabel.REJECT,
            "ambiguous and the question budget is exhausted; do not admit",
        )

    admit_cost, ask_cost, block_cost = costs["ADMIT"], costs["ASK"], costs["BLOCK"]
    cheapest = min(admit_cost, block_cost)
    close = (max(admit_cost, block_cost) / cheapest) <= CLOSE_COSTS_RATIO if cheapest > 0 else True

    if turn.may_ask and (ask_cost < cheapest or close):
        return make(
            DecisionLabel.CLARIFY,
            "admit and block costs are close; spend a question",
            questions=[
                _question_text(
                    proposal,
                    flags,
                    "Should this become a requirement, and if so who needs it?",
                )
            ],
        )

    if block_cost < admit_cost:
        return make(DecisionLabel.REJECT, "expected cost of admitting exceeds expected cost of blocking")
    return make(DecisionLabel.ACCEPT, "expected cost of blocking exceeds expected cost of admitting")


def sweep_ask_cost(
    p_need: float,
    ask_costs: list[float],
    wrong_admit: float = 1.0,
    wrong_block: float = 1.0,
) -> list[tuple[float, str]]:
    """Risk-coverage style sweep: which action wins as asking gets more expensive."""
    rows: list[tuple[float, str]] = []
    for ask in ask_costs:
        costs = expected_costs(p_need, CostModel(wrong_admit=wrong_admit, wrong_block=wrong_block, ask=ask))
        rows.append((ask, min(costs, key=costs.get)))
    return rows
