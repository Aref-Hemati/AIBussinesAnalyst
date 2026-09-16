# Evaluation framework

If we cannot measure it, it is not a paper contribution.

Last updated: 2026-09-16.

## Experimental systems

| ID | Name | Definition | Controls |
|----|------|------------|----------|
| A | Vanilla LLM | Same model. Prompt: “Produce an SRS / user stories from the following.” No critic. | model, temperature, max turns=1 unless user continues |
| B | Prompted BA | Single BA system prompt (challenge verbally) but **no** Decision object, no schema gate | same model |
| C | Agentic BA | Decision object + critic + schema gate (+ RAG if enabled) | same model |
| C− | Ablations | C without critic / without RAG / without question budget | one factor at a time |

**Freeze the model** for a result table (name, version, date, temperature). Changing models mid-table invalidates comparisons (Cheng: reproducibility 66.8%).

## Datasets

### D1 — Adversarial micro-set (build this week)

~10–20 scripted stakeholder chats designed to trigger unjustified scope. Gold labels by us, then by a BA.

Purpose: debug RQ2. Not for the journal’s only evidence.

### D2 — ReqElicitGym (public)

101 website scenarios; implicit vs initial requirements; oracle user + LLM-as-judge (κ 0.73 / 0.72 vs humans).

Purpose: comparable IRE / TKQR vs OntoAgent / LLMREI.

Caveat: simulated user; website domain. Report as **external benchmark**, not industrial proof.

### D3 — Industrial anonymized cases (the paper-maker)

Target: 8–12 real elicitation sessions or reconstructed sessions from existing RFPs at the company.

For each case:

- raw stakeholder input (chat and/or RFP excerpt)
- org rules that applied
- gold Decision labels
- gold spec (human BA)
- frozen version if available

Permission + anonymization required ([11-COMPANY-INDUSTRIAL-CONTEXT.md](11-COMPANY-INDUSTRIAL-CONTEXT.md)).

### D4 — User-story quality subset

Reuse QUS criteria from TSE 2026 on generated stories (optional second study).

## External validation ladder (V1–V4)

Added 2026-09-16. This is the answer to the first objection a reviewer will raise: *“you invented the taxonomy, wrote the dialogues, labeled them, and your agent won.”* Three of the four tiers use data we did not create, and two allow direct comparison with published numbers.

| Tier | Data | Who else has numbers | Comparison type |
|------|------|----------------------|-----------------|
| **V1** | Conflict / duplicate pairs (WorldVista, UAV, PURE→THEMAS+Mashbot, OPENCOSS), DAMIR-PURE ambiguity | SR-BERT transfer learning, PassionNet, S3CDA (Malik et al. compilation) | **Direct**, same fixed public splits |
| **V2** | ReqElicitGym / ReqElicitBench — 101 scenarios, oracle user, judge | ReqElicitGym empirical study; OntoAgent | **Direct**, same environment and metrics |
| **V3** | GitHub feature requests with maintainer outcomes | Nobody, for this task | **We set the first public baseline** |
| **V4** | 8–12 anonymized industrial cases (D3) | Nobody | Human agreement only |

### V1 — Zero-shot generalist vs supervised specialist

Run the conflict, duplicate, and ambiguity critics in **pairwise mode** on the public splits and report next to the published macro-F1 / conflict-F1.

State the framing explicitly in the paper, because it is the honest one:

> Prior results come from models **trained on the task**. CRAC is a **general zero-shot decision policy** with no task-specific training. The claim is comparable component skill without supervision, not a new state of the art.

Threats to write in the same paragraph:

- Several conflicts are **synthetic**, crafted by Malik et al. along INCOSE guidelines, not naturally occurring.
- Class imbalance is extreme (conflict:neutral up to **1:367** on OPENCOSS), so macro-F1 and conflict-F1 both go in the table; accuracy does not.
- Pairwise mode is a **different input form** from live dialogue. It validates the critic, not the loop.

### V2 — Standardized protocol head-to-head

Both artifacts are available: the gym at [`jdm4pku/ReqElicitBench`](https://github.com/jdm4pku/ReqElicitBench), and OntoAgent’s replication package at `anonymous.4open.science/r/TypoAgent-RE2026`.

**Document the variance, do not cherry-pick it.** Published IRE numbers on the same gym disagree by a wide margin:

| Source | Reported IRE | Setting |
|--------|--------------|---------|
| ReqElicitGym empirical study | **0.32** (best of 7 LLMs) | Plain LLM interviewers, Non-CoT / CoT |
| OntoAgent | **0.69** (+33% over baselines), TKQR 0.59 | Ontology-guided agent |

Protocol rule for our table: fix one model, one temperature, one turn cap, and **re-run at least one published baseline ourselves** in that protocol. Report our controlled baseline beside both literature reference points. A single number lifted out of either paper is not a comparison.

Extension we release: **ReqElicitGym-Adv**, the same scenarios with an oracle user that also voices unjustified, out-of-scope, and unevidenced demands from a generator **frozen before** CRAC is run on it. Coverage-maximizing agents should degrade there; CRAC should not.

### V3 — First public baseline on natural maintainer decisions

Maintainer outcomes are decisions made by humans with real stakes, recorded before we existed.

| Observed outcome | Our label | Super-class |
|------------------|-----------|-------------|
| Implemented / merged / `state:accepted` | ACCEPT | ACCEPT |
| Closed `not_planned`, `wontfix` | REJECT / OUT-OF-SCOPE | BLOCK |
| Duplicate label or closing comment pointing at an existing issue | DUPLICATE | BLOCK |
| `needs-info`, awaiting-response, closed stale for silence | CLARIFY | HOLD |

Sources: `open-index/open-github-issues` (text, labels, `state_reason`, timelines), the WONTFIX figshare dataset (3,132 popular repos), GitReq for requirement-quality labels.

**Label noise is the main threat and the mitigation is not optional.** `wontfix` frequently means “no maintainer time,” which is *not* “this should not be a requirement.” Therefore:

1. Filter with the published eight-theme WONTFIX taxonomy; keep only decision-relevant themes (unnecessary, already implemented, out of scope, infeasible, duplicate) and drop capacity//staleness-only themes.
2. Hand-audit a **stratified sample of ~200 issues**, two annotators, and report **Cohen’s κ between the natural label and the human reading**. If κ is weak, V3 becomes a noisy-label study and is reported as such.

Since nobody has scored an agent on this task, comparison comes from baselines we run in the same harness — Vanilla, Prompted, and a TF-IDF or BERT classifier — plus the existing automated wontfix-identification work as a reference point. The data is public, so others can beat our number later. That is the point.

### V4 — Industrial ecological validity

No external leaderboard. Agreement statistics only:

- **Cohen’s κ** for two raters (AI vs BA, or BA vs BA).
- **Fleiss’ κ** when three or more BAs label the same cases.
- Report κ per super-class (ACCEPT / HOLD / BLOCK) as the headline and the nine-way confusion matrix as error analysis. Nine-way F1 with n=8–12 is not defensible.

This tier buys what Zadenoori shows is missing (elicitation field studies = 1), not leaderboard position.

## Metrics

### Core (must appear in the paper)

| Metric | RQ | Definition | Better |
|--------|----|------------|--------|
| Decision accuracy | RQ2 | Correct ACCEPT/CLARIFY/REJECT vs gold (macro-F1 per class) | ↑ |
| Cohen’s κ (AI vs BA) | RQ2, RQ4 | Agreement beyond chance | ↑ (≥0.60 substantial) |
| Precision of requirements | RQ1, RQ2 | Share of generated reqs that gold considers valid | ↑ |
| Recall / completeness | RQ1 | Share of gold reqs covered (semantic match, threshold calibrated like TSE 0.8) | ↑ |
| Unjustified-acceptance rate | RQ2 | Gold-REJECT items that became FRs | ↓ |
| False-reject rate | RQ2 | Gold-ACCEPT items rejected | ↓ |
| Ambiguity defect rate | RQ3 | QUS language-clarity or INCOSE smells | ↓ after dialogue |
| Trace coverage | RQ5 | % ACCEPT with utterance + decision ids | ↑ (~100%) |
| Orphan FR count | RQ2 | FRs without ACCEPT id | =0 |

### Comparative (to sit beside published numbers)

| Metric | Published number to beat / compare | Notes |
|--------|-------------------------------------|-------|
| IRE | OntoAgent **0.69**; mistake-guided **0.52**; LLMREI-short **0.39**; gym’s own best plain LLM **0.32** | Implicit coverage. Sources disagree — see V2 protocol rule |
| TKQR | OntoAgent **0.59**; LLMREI-short **0.49** | Efficiency of questions |
| P / R / F1 of extracted reqs | Yin **80.4 / 79.7 / 0.89** | Different task (batch multi-source) — **do not claim beat** without same data |
| Redundancy reduction | Yin **17.3–18%** | Report analogously: % duplicate proposals suppressed |
| Turn precision/recall | RECOVER **63% / 77%** | Only if we classify turns |
| US rejection rate | GT 9.43%; students 14.64%; Claude 16.55% | Lower reject after our AC critic |
| Quality κ | Claude 3 Opus **0.87** with codebook | Our Quality Agent should approach this |
| Industrial vs lab | Cheng **1.3% production**; Zadenoori **7% field** | Our D3 is the differentiator, not a number to beat |

### Secondary

- Turns to freeze
- Tokens / cost
- Stakeholder Likert (challenge quality, trust, time)
- BA Likert (would use in real project)
- Hallucination rate (invented actors, invented regulations) — Cheng 63.4% of papers worry about this

**Do not lead with BLEU.** RECOVER’s turn-level BLEU 5.39% shows wording overlap is the wrong story. If we report BLEU, it is appendix-only vs expert FRD.

## Semantic matching protocol (completeness)

Follow TSE 2026 calibration, do not invent a threshold blindly:

- Embed requirements (state model)
- Cosine ≥ **0.80** = covered (they found 72.5% human match)
- Also report ≥ **0.85** (95% human match, stricter)

Human spot-check 20 pairs per bin if we change the embedder.

## Human evaluation

| Task | Raters | Instrument |
|------|--------|------------|
| Gold decisions | ≥2 BAs | taxonomy in RQ2; resolve conflicts |
| Spec quality | same | completeness, correctness, usefulness 1–7 |
| Dialogue quality | stakeholders | challenge fairness, clarity, length |
| Agreement | compute κ | Landis & Koch interpretation |

OntoAgent human study was n=6 students — we should **not** copy that as our only human evidence. Prefer professional BAs even if n is smaller, plus the public benchmark.

## Experiment design (journal-ready)

### E1 — Three-system comparison (main)

For each case in D1 then D3:

1. Same stakeholder script (or same human, counterbalanced)
2. Run A, B, C
3. Independent BA scores outputs blind to condition
4. Report means + statistical test if n allows (Wilcoxon / bootstrap CIs if small n)

### E2 — Ablation (C only)

Critic, RAG, budget, ontology — incremental like OntoAgent Table III.

### E3 — Questioning process

Plot IRE (or completeness) **vs turn**, like `figures/baselines/ontoagent-fig3.png`.

This is a required visual for an elicitation paper.

### E4 — Error analysis

Qualitative codebook of failure modes:

- sycophancy (accepts everything)
- over-challenge (blocks obvious needs)
- missed NFR/audit
- RAG citing wrong rule
- hallucination of org systems

## Result tables we will fill in `07-RESULTS-LOG.md`

Copy these empty tables when an experiment finishes.

### Table: three systems (industrial or D1)

| Metric | Vanilla A | Prompted B | Agentic C |
|--------|-----------|------------|-----------|
| Completeness | | | |
| Precision | | | |
| Ambiguity defects | | | |
| Redundancy | | | |
| Conflicts remaining | | | |
| Unjustified-acceptance % | | | |
| Traceability % | | | |
| BA agreement κ | | | |
| User satisfaction | | | |

### Table: decision classes (C only)

| Class | P | R | F1 | Support |
|-------|---|---|----|---------|
| ACCEPT | | | | |
| CLARIFY | | | | |
| REJECT | | | | |
| DUPLICATE | | | | |
| CONFLICTING | | | | |
| UNJUSTIFIED | | | | |
| INSUFFICIENT-EVIDENCE | | | | |

## Validity threats (write early)

- **Construct:** Decision labels are subjective — mitigate with codebook + dual annotation (TSE did this).
- **Internal:** Prompt leakage, model drift — freeze prompts in git tags.
- **External:** One company, Persian domain, one Dify stack — mitigate with ReqElicitGym + English open-source tool.
- **Conclusion:** Small n industrial — report CIs, avoid overclaim vs Yin’s 80.4% on different data.

## Pre-registration lite

Before E1, write in `logs/experiment-log.md`:

- model + temperature
- prompt hashes
- inclusion of cases
- primary metric = **unjustified-acceptance ↓ without recall collapse**
