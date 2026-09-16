"""Tests for the parts that must behave identically on every replay."""

from __future__ import annotations

import math

import pytest
from pydantic import ValidationError

from reqdecide.adapters.github_issues import (
    IssueComment,
    IssueRecord,
    RejectionTheme,
    build_corpus,
    classify_rejection_theme,
    looks_like_feature_request,
    map_issue,
    normalize_payload,
    stratified_audit_sample,
)
from reqdecide.policy import AdmissionProposal, CriticFlags, decide, expected_costs
from reqdecide.schema import (
    Action,
    CostModel,
    Decision,
    DecisionLabel,
    Project,
    Requirement,
    SuperClass,
    TurnInput,
    UncertaintySignal,
    super_class_of,
)
from reqdecide.uncertainty import (
    Interpretation,
    cluster_texts,
    estimate_uncertainty,
    shannon_entropy,
)


def make_decision(label: DecisionLabel, action: Action, **kwargs) -> Decision:
    return Decision(
        candidate_text="Staff must log in with company SSO.",
        label=label,
        action=action,
        confidence=0.8,
        rationale="test",
        **kwargs,
    )


class TestSchema:
    def test_super_classes_collapse_nine_labels_into_three(self):
        assert super_class_of(DecisionLabel.CLARIFY) is SuperClass.HOLD
        assert super_class_of(DecisionLabel.UNJUSTIFIED) is SuperClass.BLOCK
        assert super_class_of(DecisionLabel.ACCEPT) is SuperClass.ACCEPT

    def test_label_and_action_must_agree(self):
        with pytest.raises(ValidationError):
            make_decision(DecisionLabel.REJECT, Action.ADMIT)

    def test_ask_requires_a_question(self):
        with pytest.raises(ValidationError):
            make_decision(DecisionLabel.CLARIFY, Action.ASK)
        assert make_decision(DecisionLabel.CLARIFY, Action.ASK, questions=["Which users?"])

    def test_duplicate_must_name_its_twin(self):
        with pytest.raises(ValidationError):
            make_decision(DecisionLabel.DUPLICATE, Action.BLOCK)

    def test_requirement_without_accept_decision_is_unrepresentable(self):
        blocked = make_decision(DecisionLabel.UNJUSTIFIED, Action.BLOCK)
        with pytest.raises(ValidationError):
            Project(
                title="Leave portal",
                decisions=[blocked],
                requirements=[Requirement(decision_id=blocked.id, text="Put it on a blockchain.")],
            )

    def test_trace_coverage_is_total_when_every_requirement_has_an_accept(self):
        accepted = make_decision(DecisionLabel.ACCEPT, Action.ADMIT)
        project = Project(
            title="Leave portal",
            decisions=[accepted],
            requirements=[Requirement(decision_id=accepted.id, text="Staff log in with SSO.")],
        )
        assert project.trace_coverage() == 1.0
        assert project.orphan_requirements() == []


class TestUncertainty:
    def test_entropy_is_zero_when_every_reading_agrees(self):
        assert shannon_entropy([8]) == 0.0

    def test_entropy_is_maximal_when_every_reading_differs(self):
        assert shannon_entropy([1, 1, 1, 1]) == pytest.approx(math.log(4))

    def test_paraphrases_cluster_together(self):
        texts = [
            "Staff sign in using the company single sign-on.",
            "Employees log in through company single sign-on.",
            "The site should look modern and colourful.",
        ]
        assert len(cluster_texts(texts)) == 2

    def test_agreeing_readings_are_not_flagged_ambiguous(self):
        readings = [Interpretation("Users export the report as PDF.", 0.9)] * 6
        signal = estimate_uncertainty(readings)
        assert signal.n_clusters == 1
        assert signal.normalized_entropy == 0.0
        assert signal.is_ambiguous is False
        assert signal.mean_confidence == pytest.approx(0.9)

    def test_disagreeing_readings_are_flagged_ambiguous(self):
        readings = [
            Interpretation("The report exports as a PDF file."),
            Interpretation("The dashboard refreshes every minute."),
            Interpretation("Managers receive an email digest."),
            Interpretation("Data synchronises with the payroll system."),
        ]
        signal = estimate_uncertainty(readings)
        assert signal.n_clusters == 4
        assert signal.normalized_entropy == pytest.approx(1.0)
        assert signal.is_ambiguous is True


class TestGithubAdapter:
    def maintainer(self, body: str) -> IssueComment:
        return IssueComment(body=body, author_association="MEMBER")

    def test_bug_reports_are_not_requirement_admission(self):
        issue = IssueRecord(repo="a/b", number=1, title="Crash on save", labels=["bug"])
        assert looks_like_feature_request(issue) is False

    def test_feature_intent_is_read_from_label_or_title(self):
        assert looks_like_feature_request(IssueRecord(repo="a/b", number=2, title="Dark mode", labels=["enhancement"]))
        assert looks_like_feature_request(IssueRecord(repo="a/b", number=3, title="Please add dark mode"))
        assert looks_like_feature_request(IssueRecord(repo="a/b", number=4, title="Dark mode", labels=["Suggestion"]))

    def test_themes_come_with_the_phrase_that_triggered_them(self):
        theme, evidence = classify_rejection_theme("This is out of scope for the core library.")
        assert theme is RejectionTheme.OUT_OF_SCOPE
        assert "out of scope" in evidence.lower()

    def test_completed_issue_maps_to_accept(self):
        issue = IssueRecord(
            repo="a/b", number=4, title="Add dark mode", labels=["enhancement"],
            state="closed", state_reason="completed",
        )
        decision = map_issue(issue)
        assert decision.label is DecisionLabel.ACCEPT

    def test_out_of_scope_closure_maps_to_out_of_scope(self):
        issue = IssueRecord(
            repo="a/b", number=5, title="Add a chat client", labels=["enhancement"],
            state="closed", state_reason="not_planned",
            comments=[self.maintainer("Sorry, this is out of scope for this project.")],
        )
        decision = map_issue(issue)
        assert decision.label is DecisionLabel.OUT_OF_SCOPE
        assert decision.decision_relevant is True

    def test_capacity_closure_is_kept_out_of_gold_but_flagged(self):
        issue = IssueRecord(
            repo="a/b", number=6, title="Add plugin API", labels=["enhancement", "wontfix"],
            state="closed", state_reason="not_planned",
            comments=[self.maintainer("We do not have the time for this. Pull requests welcome.")],
        )
        decision = map_issue(issue)
        assert decision.theme is RejectionTheme.NO_CAPACITY
        assert decision.decision_relevant is False
        assert decision.needs_audit is True
        assert build_corpus([issue]) == []

    def test_policy_wide_feature_freeze_is_out_of_scope(self):
        issue = IssueRecord(
            repo="a/b",
            number=8,
            title="Add a QUERY method",
            labels=["Feature Request"],
            state="closed",
            state_reason="not_planned",
            comments=[IssueComment(body="Requests is not accepting feature requests.", author_association="NONE")],
        )
        decision = map_issue(issue)
        assert decision.label is DecisionLabel.OUT_OF_SCOPE
        assert decision.decision_relevant is True

    def test_open_untouched_issue_yields_no_gold_label(self):
        issue = IssueRecord(repo="a/b", number=7, title="Add dark mode", labels=["enhancement"])
        assert map_issue(issue) is None

    def test_repo_specific_info_needed_aliases_map_to_hold(self):
        for label in ("need-info", "info-needed", "Needs More Info"):
            issue = IssueRecord(
                repo="a/b",
                number=9,
                title="Add dark mode",
                labels=["enhancement", label],
            )
            decision = map_issue(issue)
            assert decision.label is DecisionLabel.CLARIFY
            assert decision.super_class is SuperClass.HOLD

    def test_overlapping_fetches_are_deduplicated(self):
        issue = IssueRecord(
            repo="a/b",
            number=10,
            title="Add dark mode",
            labels=["enhancement"],
            state="closed",
            state_reason="completed",
        )
        assert len(build_corpus([issue, issue])) == 1

    def test_github_null_body_is_normalized(self):
        payload = normalize_payload(
            {"repo": "a/b", "number": 11, "title": "Feature", "body": None}
        )
        assert IssueRecord.model_validate(payload).body == ""

    def test_audit_sample_is_deterministic_and_bounded(self):
        issues = [
            IssueRecord(
                repo="a/b", number=n, title=f"Add feature {n}", labels=["enhancement"],
                state="closed", state_reason="completed",
            )
            for n in range(50)
        ]
        decisions = build_corpus(issues)
        first = stratified_audit_sample(decisions, n=10)
        second = stratified_audit_sample(decisions, n=10)
        assert len(first) == 10
        assert [d.number for d in first] == [d.number for d in second]


def _turn(text: str, budget: int = 3) -> TurnInput:
    return TurnInput(utterance=text, question_budget_remaining=budget)


def _proposal(p_need: float) -> AdmissionProposal:
    return AdmissionProposal(p_need=p_need, rationale="model hunch")


class TestPolicy:
    def test_duplicate_blocks_without_asking(self):
        decision = decide(
            _turn("Staff must log in with SSO."),
            _proposal(0.95),
            flags=CriticFlags(duplicate_of="req-1"),
        )
        assert decision.label is DecisionLabel.DUPLICATE
        assert decision.action is Action.BLOCK

    def test_high_entropy_asks_when_budget_remains(self):
        uncertainty = UncertaintySignal(
            n_samples=4,
            n_clusters=4,
            cluster_sizes=[1, 1, 1, 1],
            interpretation_entropy=1.386,
            normalized_entropy=1.0,
            interpretations=["A", "B", "C", "D"],
        )
        decision = decide(_turn("Make it user-friendly."), _proposal(0.7), uncertainty=uncertainty)
        assert decision.action is Action.ASK
        assert decision.label is DecisionLabel.AMBIGUOUS
        assert decision.questions

    def test_high_entropy_without_budget_refuses_to_admit(self):
        uncertainty = UncertaintySignal(
            n_samples=4,
            n_clusters=4,
            cluster_sizes=[1, 1, 1, 1],
            interpretation_entropy=1.386,
            normalized_entropy=1.0,
            interpretations=["A", "B", "C", "D"],
        )
        decision = decide(
            _turn("Make it user-friendly.", budget=0),
            _proposal(0.9),
            uncertainty=uncertainty,
        )
        assert decision.action is Action.BLOCK
        assert decision.label is DecisionLabel.REJECT

    def test_confident_need_is_admitted(self):
        decision = decide(_turn("Staff must log in with company SSO.", budget=0), _proposal(0.95))
        assert decision.label is DecisionLabel.ACCEPT
        assert decision.action is Action.ADMIT

    def test_confident_non_need_is_blocked(self):
        decision = decide(_turn("Put the audit trail on a blockchain.", budget=0), _proposal(0.05))
        assert decision.action is Action.BLOCK

    def test_asking_is_cheaper_than_guessing_when_p_need_is_near_half(self):
        costs = expected_costs(0.5, CostModel())
        assert costs["ASK"] < costs["ADMIT"]
        assert costs["ASK"] < costs["BLOCK"]
        decision = decide(_turn("Maybe we need a mobile app."), _proposal(0.5))
        assert decision.action is Action.ASK
