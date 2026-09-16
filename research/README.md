# Research workspace — Agentic AI Business Analyst

This folder is the **canonical research trail** for the journal paper and the open-source tool. Implementation lives at the repo root (`business-analyst-fa-chatflow.dify.yml`, `WORKFLOW.md`). Research thinking, papers, numbers to beat, and experiment logs live here.

> Do not treat the Dify chatflow as the paper. The chatflow is a vehicle. The scientific contribution is the **requirement-decision loop** (elicit → critique → negotiate → validate → specify → trace) evaluated in an industrial setting.

## Goals (locked)

| Priority | Goal | Success looks like |
|----------|------|--------------------|
| 1 | **Journal paper** with a strong idea, not an implementation report | Clear RQs, baselines, metrics, industrial evidence |
| 2 | **Open-source software** that reviewers and practitioners can run | GitHub repo + reproducible evaluation scripts |
| 3 | **Industrial usefulness** at the company | Real (anonymized) cases, BA agreement, reduced ambiguity |

**Competitive artifact (almost as important as the industrial study):** a public **decision-labeled dialogue dataset**. OntoAgent competes with ReqElicitGym (101); TSE competes with 13,958 user stories. We cannot compete on title keywords. We compete with **gold decisions**. See [12-PUBLIC-DATASET.md](12-PUBLIC-DATASET.md).

Parked extra goals:

- Requirement graph + change-impact analysis
- Dify + standalone dual implementation

## Working title (frozen 2026-09-16)

> **From Conversational Stakeholder Input to Validated Software Requirements: An Industrial Evaluation of an Agentic Business Analyst with Interactive Critique**

That is the original title plus the one missing scientific word: **critique**. It keeps industrial evaluation (rare field data) and the BA persona, and it no longer reads as a passive pipeline.

Do **not** use the all-in-one stuffed title *“Challenging the Stakeholder: An Industrial Evaluation of Trustworthy Agentic Requirements Engineering through Interactive Critique and Validation.”* Too long, “trustworthy” is unearned until we have guarantees, and “challenging the stakeholder” sounds adversarial rather than professional BA work.

RQ in one line (not a title): *Can an AI agent decide whether a stakeholder statement should become a requirement?*

Rejected alternatives stay in [00-VISION-AND-GOALS.md](00-VISION-AND-GOALS.md).

## Git commits

When the user says **commit**, do it without waiting for a message. Split and describe by the agent’s judgment (why, not a file dump). One or more commits is fine. Never push unless asked. Never commit `.env` or credentials.

## Raw paper inbox

If the user puts a file in [`papers/raw/`](papers/raw/README.md): extract a full paper note, copy needed figures, **then delete the dump**. Locations: [`ARTIFACTS.md`](ARTIFACTS.md).

Academic search terms (not “AI Business Analyst”):

- LLM-based Requirements Engineering (LLM4RE)
- Agentic Requirements Engineering
- Conversational / interactive requirements elicitation
- Requirement critique / negotiation / validation
- Knowledge-augmented RE (RAG + org constraints)

## Start here (read in this order)

1. [00-VISION-AND-GOALS.md](00-VISION-AND-GOALS.md) — idea, gap, what is / is not novel
2. [01-RESEARCH-QUESTIONS.md](01-RESEARCH-QUESTIONS.md) — RQs and claims we must be able to defend
3. [02-RELATED-WORKS.md](02-RELATED-WORKS.md) — landscape + how we differ
4. [03-CONTRIBUTIONS.md](03-CONTRIBUTIONS.md) — paper contributions vs engineering contributions
5. [04-JOURNEY-AND-ACTION-PLAN.md](04-JOURNEY-AND-ACTION-PLAN.md) — phases, checkpoints, what to do next
6. [05-NOVEL-METHODS.md](05-NOVEL-METHODS.md) — methods to invent / combine / test
7. [13-METHOD-CRAC.md](13-METHOD-CRAC.md) — frozen admission-control formulation the code implements
8. [06-EVALUATION-FRAMEWORK.md](06-EVALUATION-FRAMEWORK.md) — metrics, baselines, V1–V4 ladder
9. [07-RESULTS-LOG.md](07-RESULTS-LOG.md) — **empty until we run experiments** — numbers, graphs, logs
10. [08-SOFTWARE-AND-IMPLEMENTATION.md](08-SOFTWARE-AND-IMPLEMENTATION.md) — Dify today, target architecture, GitHub plan
11. [09-PAPERS-NEEDING-FULL-TEXT.md](09-PAPERS-NEEDING-FULL-TEXT.md) — papers we could not fully read
12. [10-GLOSSARY.md](10-GLOSSARY.md)
13. [11-COMPANY-INDUSTRIAL-CONTEXT.md](11-COMPANY-INDUSTRIAL-CONTEXT.md)
14. [12-PUBLIC-DATASET.md](12-PUBLIC-DATASET.md) — how we compete: gold Decision dialogues, not title keywords
15. [ARTIFACTS.md](ARTIFACTS.md) — where kept files live; raw inbox is deleted after extract

Paper-by-paper notes: [papers/00-INDEX.md](papers/00-INDEX.md)

Figures from baselines: [figures/README.md](figures/README.md)

Experiment / reading logs: [logs/README.md](logs/README.md)

## North-star research question

> Can an LLM-based agentic system **autonomously perform business analysis** by interactively eliciting, **challenging**, validating, prioritizing, and formalizing stakeholder requirements — and can it **decide that some statements should not become requirements**?

## What the literature already covers (do not claim as novelty)

| Already studied | Typical output |
|-----------------|----------------|
| Requirement extraction | “Find requirements in this text” |
| User-story generation | “Generate US from a description / interview” |
| Quality checking | “Is this requirement clear / atomic?” |
| Transformation | “Convert to user story / formal spec” |
| Conversational elicitation | “Ask questions to obtain requirements” |
| Multi-agent RE | “Several agents process requirements” |

## The remaining gap (our target)

Identification is mature. **Consolidation, critique, stakeholder validation, and management** are not.

Evidence:

- Automated elicitation SMS (2026): ~**51%** structure identified requirements, **23%** consolidate, **8%** engineer stakeholder validation.
- Cheng et al. SPE (2026, 238 papers): analysis 30%, elicitation 22.1%, specification 22.1%, validation 19%, **management 6.8%**; **only 1.3%** reach production; **90.3%** early-stage.
- Zadenoori et al. arXiv (2025, 74 LLM4RE studies): elicitation & validation dominate; **75% lab experiments**, **7% field studies**; **elicitation field studies = 1** (their eval-method bubble chart); interactive prompting **5%**, RAG **6%**.

Our distinctive loop:

```
Stakeholder statement
        │
        ▼
 Requirement Decision
   ACCEPT | CLARIFY | REJECT
   (+ DUPLICATE | CONFLICTING | AMBIGUOUS
    | OUT-OF-SCOPE | UNJUSTIFIED
    | INSUFFICIENT-EVIDENCE | NEEDS-CLARIFICATION)
        │
        ▼
 Question / alternative / explanation
        │
        ▼
 Validated specification + traceability
```

## Numbers we must beat or compare against

See [06-EVALUATION-FRAMEWORK.md](06-EVALUATION-FRAMEWORK.md) for the full table. Headline baselines:

| System | Metric | Number |
|--------|--------|--------|
| Yin et al. 2026 (LLM+Agent, heterogeneous demands) | Precision / Recall / F1 | 80.4% / 79.7% / 0.89 |
| Yin et al. 2026 | Redundant proposals reduced | 17.3–18% |
| OntoAgent 2026 | IRE / TKQR | 0.69 / 0.59 |
| LLMREI-short (RE’25) | IRE / TKQR | 0.39 / 0.49 |
| Mistake-guided prompt (RE’25) | IRE / TKQR | 0.52 / 0.48 |
| RECOVER (TSE 2025) | Turn precision / recall | 63% / 77% |
| RECOVER | Conversation-level BLEU vs expert | 78.82% |
| Quattrocchi et al. TSE 2026 | Claude 3 Opus quality κ vs humans | 0.87 |
| Quattrocchi et al. | US rejection: GT / students / Claude | 9.43% / 14.64% / 16.55% |
| QUARE (RE 2026) | Compliance coverage | 98.2% |

## Implementation stance

- Not limited to Dify. Preferred research stack: Python agents + structured requirement store + optional Dify YAML mirror.
- Current company prototype: Persian BA chatflow with org hard rules, draft requirements, version freeze, HTML demo.
- Paper evaluation should include **vanilla LLM vs prompted BA vs agentic BA**.

## Path-lock rule

Whenever we add a new idea, answer these four questions in [04-JOURNEY-AND-ACTION-PLAN.md](04-JOURNEY-AND-ACTION-PLAN.md):

1. Does it help answer an RQ in `01`?
2. Is it already done by a paper in `papers/`?
3. How will we measure it (`06`)?
4. Where will the number / figure go (`07`)?

If the answer to (1) is no, it is a software feature, not a paper contribution. Keep it in `08`.
