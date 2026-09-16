# Research questions and claims

Status: **draft v1 — freeze before writing the paper introduction**.  
Last updated: 2026-09-16.

Every experiment, agent, and Dify node must map to at least one RQ. If it does not, it is a product feature ([08-SOFTWARE-AND-IMPLEMENTATION.md](08-SOFTWARE-AND-IMPLEMENTATION.md)).

## One-sentence claim

An agentic BA with an explicit **Requirement Decision** (accept / clarify / reject) improves requirement quality, reduces unjustified scope, and increases stakeholder-validated completeness compared with vanilla and prompt-only LLMs.

## Research questions

### RQ1 — Quality of elicitation from non-technical stakeholders

**Can an agentic system improve the quality of requirements elicited from non-technical stakeholders compared with vanilla LLM and prompt-engineered BA?**

- Independent variable: system (Vanilla / Prompted / Agentic-BA)
- Dependent: completeness, precision, ambiguity, QUS semantic scores, human BA rating
- Why it matters: elicitation is crowded; **quality under realistic stakeholders** is not

### RQ2 — Filtering / critique (the distinctive RQ)

**Can the agent correctly decide whether a stakeholder statement should become a requirement?**

Decision labels:

| Label | Meaning |
|-------|---------|
| ACCEPT | Clear, in-scope, justified, feasible enough to specify |
| CLARIFY | Missing evidence, ambiguous, or underspecified |
| REJECT | Out of scope, unjustified, infeasible, or harmful |
| DUPLICATE | Semantically covered by an existing requirement |
| CONFLICTING | Contradicts an accepted requirement or hard rule |
| UNJUSTIFIED | No business objective / no stakeholder |
| INSUFFICIENT-EVIDENCE | Quantitative claim without basis (e.g. “1 million users”) |
| OUT-OF-SCOPE | Explicitly deferred or excluded |
| AMBIGUOUS | Multiple interpretations; not yet a requirement |

Metrics: decision accuracy vs human BA gold labels; precision/recall per class; Cohen’s κ.

This is the RQ we should **lead** with. Extraction is solved enough. **Necessity reasoning** is not.

### RQ3 — Iterative questioning

**Does iterative AI-driven questioning reduce ambiguity and incompleteness versus one-shot generation?**

- Compare: one-shot FRD vs N-turn interview then FRD
- Metrics: ambiguity count before/after; missing-slot rate; IRE (implicit requirement elicitation); TKQR (turn-discounted key question rate)
- Baselines to beat: OntoAgent IRE **0.69**, TKQR **0.59**; LLMREI-short IRE **0.39**; mistake-guided IRE **0.52**

We should report IRE/TKQR **and** our own decision metrics. OntoAgent optimizes “ask the right missing slot.” We optimize “ask whether it should exist, then fill slots.”

### RQ4 — Comparison with humans

**How does the AI BA compare with conventional LLM prompting and/or professional human BAs?**

- Human BA agreement on decisions and on final spec quality
- Time-to-validated-spec
- Over-acceptance rate (AI too eager) and over-rejection rate (AI too strict)
- User (stakeholder) satisfaction — secondary, not the main claim

### RQ5 — Traceability and management

**Can the resulting requirements maintain traceability from stakeholder statement → decision → requirement → acceptance criterion (and frozen version)?**

This is strategically important: Cheng et al. find **management only 6.8%** of GenAI-RE work. Our Dify version-freeze is a real hook.

Metrics: % requirements with a source utterance; % with a decision record; impact completeness when a requirement is withdrawn.

## Hypotheses (falsifiable)

| ID | Hypothesis |
|----|------------|
| H1 | Agentic-BA completeness ≥ Prompted ≥ Vanilla on the same stakeholder input |
| H2 | Agentic-BA has **higher precision** (fewer unjustified requirements) than Vanilla, even if recall is similar |
| H3 | Decision-class κ with human BAs ≥ 0.60 (substantial) on ACCEPT vs not-ACCEPT; harder on CLARIFY subtypes |
| H4 | After critique turns, ambiguity defects drop vs the one-shot spec |
| H5 | Stakeholders accept fewer “blockchain / 1M users / WhatsApp” style items without justification under Agentic-BA |
| H6 | Trace links from utterance to requirement exist for ≥ 95% of ACCEPT decisions |

If H2 fails (the agent just generates more text), the paper is weak.

## What we will **not** claim

- Superhuman BA replacement
- Formal correctness of all generated requirements (v1)
- Domain-general ontology as good as OntoAgent on websites without induction data
- Multi-agent architecture as the scientific novelty

## Mapping RQs → paper sections

| RQ | Method section | Evaluation | Result artifact |
|----|----------------|------------|-----------------|
| RQ1 | Spec generator + interview | Quality metrics vs 3 systems | Tables in `07` |
| RQ2 | Requirement Critic + Decision | Confusion matrix vs BA gold | Main figure |
| RQ3 | Question policy | IRE/TKQR + ambiguity delta | Dialogue plots |
| RQ4 | Same systems + human raters | κ, Likert, time | Human study table |
| RQ5 | Requirement store + freeze | Trace coverage | Graph / matrix |

## Primary vs secondary story

**Primary story:** Requirement Decision + critique (RQ2, RQ3).  
**Secondary story:** Industrial field evaluation + traceability (RQ1, RQ4, RQ5).  
**Not the story:** Number of agents.
