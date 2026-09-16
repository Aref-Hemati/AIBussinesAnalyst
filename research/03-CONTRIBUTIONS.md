# Contributions

Split **scientific** vs **engineering**. Reviewers punish papers that confuse the two.

Last updated: 2026-09-16.

## Scientific contributions (paper)

### C1 — Requirement Decision as a first-class RE artifact

We treat each stakeholder statement as a **decision problem**, not as raw material for FR-xx generation.

Contribution: a taxonomy + policy that maps utterances to `{ACCEPT, CLARIFY, REJECT, ...}` with a stored rationale, evidence pointers, and next action (question, alternative, or exclusion).

This is measurable (accuracy, κ, confusion matrix). That makes it a research contribution.

### C2 — Critique-and-elicit loop (not extract-and-dump)

A closed loop:

1. Interpret utterance in context (org rules, current spec, prior decisions)
2. Critique: ambiguity, conflict, redundancy, necessity, feasibility, scope, evidence
3. If needed: **one targeted question or a negotiated alternative**
4. Only then: write/update a structured requirement
5. Ask the stakeholder to confirm the decision, not only the wording

Novelty vs OntoAgent: they maximize implicit-slot coverage. We maximize **justified** coverage. Asking more is not always better.

Novelty vs Yin: they mediate conflicts among existing demand sources. We mediate **live** stakeholder over-scoping.

### C3 — Evaluation protocol that the field is missing

A three-system experiment plus human BA gold labels, with industrial cases:

- System A: Vanilla LLM
- System B: Prompt-engineered BA (single strong prompt)
- System C: Agentic BA (decision + critic + optional specialists)

Metrics mix: classic IR (P/R/F1), QUS semantic quality, IRE/TKQR, **decision accuracy**, trace completeness, time-to-validated-spec.

This answers Cheng/Zadenoori’s complaint: lab-only, surface metrics, no production.

### C4 — Domain-grounded BA (industrial knowledge)

Optional but strong if the company allows it: RAG over org hard rules, existing systems, prior frozen versions, terminology.

This is **not** “we used RAG” as novelty (Yin already did). The contribution is **showing that grounding changes ACCEPT/REJECT decisions** (e.g. reject native Android if responsive web + SSO already satisfies policy).

## Engineering contributions (software / GitHub)

These support C1–C4. They are listed in the artifact appendix, not as the abstract’s main claim.

| E# | Artifact |
|----|----------|
| E1 | Open-source conversational BA producing a structured **project model** (JSON schema) |
| E2 | Dify chatflow (Persian, company) + portable Python/agent implementation |
| E3 | Version freeze already in the company DSL — maps to RE **management** |
| E4 | Evaluation harness (replay dialogues, score decisions, plot logs) |
| E5 | Anonymization guidelines + example cases |

## Structured project model (output contribution)

Final output is not “an SRS blob.” It is a typed model:

```
Project
 ├── BusinessGoals[]
 ├── Stakeholders[] / Actors[]
 ├── Scope { in, out }
 ├── FunctionalRequirements[]
 ├── NonFunctionalRequirements[]
 ├── BusinessRules[]
 ├── Constraints[]
 ├── Assumptions[]
 ├── Dependencies[]
 ├── Risks[]
 ├── UserStories[] + AcceptanceCriteria[]
 ├── Priorities[]
 ├── Traceability[]     // utterance_id → decision_id → req_id → story_id → ac_id
 ├── OpenQuestions[]
 └── VersionHistory[]   // freeze events
```

Each requirement carries:

- `decision` + `decision_rationale`
- `source_spans` (chat turns / file offsets)
- `status`: draft | clarified | accepted | rejected | frozen
- `conflicts_with[]`
- `business_objective_id` (nullable — null ⇒ UNJUSTIFIED)

## What would make reviewers say “incremental”

- Reporting only fluency / BLEU against an expert FRD
- Showing one cherry-picked chat transcript
- Claiming multi-agent as the invention
- No human BA comparison
- No rejection examples

## Contribution sentence for the abstract (draft)

We contribute (i) a requirement-decision taxonomy and critic–elicit loop that treats necessity, conflict, and evidence as first-class outcomes; (ii) a structured, traceable specification model with stakeholder validation in the loop; and (iii) an empirical comparison of vanilla, prompted, and agentic BA systems, including industrial cases and human BA agreement.
