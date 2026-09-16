# Yin, Cui, Luan — LLM+Agent RE for multi-source heterogeneous demands

- **Cite:** D. Yin, Z. Cui, L. Luan. *LLM+Agent-Based Requirement Engineering for Multi-Source and Heterogeneous User Demands*. Frontiers in Artificial Intelligence and Applications, vol. 415 (CECNet 2025), pp. 46–56, 2026. [10.3233/FAIA251514](https://doi.org/10.3233/FAIA251514)
- **Read:** 2026-09-16 (Sage full page)
- **Closest paper** to our *architecture*, not to our *live critique* story
- **Numbers to beat / compare**

## Problem

User demands arrive from PMs, app stores, social, customer service. Heterogeneity, noise, semantic inconsistency, redundancy → wasted R&D.

Standalone GPT hallucinates and lacks domain grounding.

## Method

### Data sources (5)

1. Project requirement pool (statuses: clarify → released)
2. End-user feedback (stores + CS)
3. Industry/market reports
4. Legal/compliance
5. Smart-home app functional/NFR JSON (demo product)

### Dynamic RAG

- Embed in ChromaDB
- **RIND** trigger: token uncertainty × max attention × non-stopword; threshold **θ = 0.6**
- Cosine retrieve into agent context

### Four-level agents

| Level | Agent | Job |
|-------|-------|-----|
| 1 | Existing Requirement Sorting + User Feedback | Normalize to JSON; tag release vs review state |
| 2 | Requirement Analysis | Strip emotion; extract function points; RAG vs demo app |
| 3 | Conflict Mediation | Illegal vs RAG; conflict with released/review items; count user-feedback issues |
| 4 | Priority Assessment | Weighted score; JSON backlog |

Priority (Eq. 4):

`Contribution = 0.6 * LCR + 0.3 * (UFI / user issues) + 0.1 * MF`

LCR = legal compliance; UFI = user-feedback issues; MF = mandatory features.

### Expert voting

12 experts (4 PMO, 2 architects, 2 RD, 4 managers). Experts listed **95** key requirements. System generated **105** to-be-reviewed.

Match grades: exact=1 TP, partial=0.5, possible=0.2, none=0.

## Results (beat carefully — different task)

**Table 1 (per expert precision/recall)** — average:

- Precision **80.4%**
- Recall **79.7%**
- Conclusion also reports **F1 = 0.89** vs BERT and standalone GPT-4 on demand extraction (same section; slightly different wording than Table 1 — cite both)

Per-expert precision range ~73.8%–85.9% (see paper Table 1).

**Table 2 redundancy**

| Released | Reviewing | User feedback | Proposed redundant | Contribution rate |
|----------|-----------|---------------|--------------------|-------------------|
| 231 | 56 | 71 | **22** | **17.3%** |

Conclusion: **~18%** fewer redundant feature proposals.

## What they did well (steal)

- Typed JSON between agents
- Conflict agent with explicit rules
- Expert panel protocol (we should copy n and roles if possible)
- Legal weight in priority
- Industrial dataset

## What they did **not** do (our opening)

- No conversational stakeholder interview
- No “why do you want this?” necessity critic
- Conflicts are among *existing corpus items*, not live over-scoping
- Evaluation is match-to-key-needs, not Decision-class accuracy
- No trace from a single utterance to a reject rationale shown to the user
- Conclusion’s F1 0.89 vs BERT/GPT-4 needs the same split if we ever compare extraction-only

## How we might beat them (honest)

We will **not** beat 80.4% on their smart-home corpus. We can:

- Report analog **redundancy suppression** in live interviews
- Add **unjustified-acceptance** which they do not measure
- Show **stakeholder-in-the-loop** validation (their experts vote after the fact)

## Figures

Paper Figure 1 (overall architecture) — save if you export the PDF image to `../figures/baselines/yin-fig1.jpg`.
