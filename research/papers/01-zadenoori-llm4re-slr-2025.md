# Zadenoori et al. — LLMs for Requirements Engineering: A Systematic Literature Review

- **Cite:** M. A. Zadenoori, J. Dąbrowski, W. Alhoshan, L. Zhao, A. Ferrari. *Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review*. arXiv:2509.11446, 2025.
- **URL:** https://arxiv.org/abs/2509.11446
- **Local copy:** raw HTML **deleted after extract** (2026-09-16). Kept figures: `../figures/baselines/zadenoori-*`
- **Venue:** preprint (authors note it is preliminary; no full cross-check yet)
- **Read:** 2026-09-16 from arXiv HTML; **re-read local HTML + result figures** the same day
- **Our use:** opening related-work evidence that elicitation/validation dominate, industry and interactive prompting do not

## Problem

NLP4RE historically focused on classification and defect detection. Generative LLMs change the task mix. Need a map of *how* LLMs are used in RE (tasks, prompts, eval).

## Method

Kitchenham SLR. Scopus query (11 Sep 2024) + venue-by-venue search (REJ, TSE, TOSEM, IST, JSS, EMSE, RE, REFSQ; 18 Dec 2024). **74** primary studies, mostly 2023–2024. CORE A*/A/B and Q1/Q2 plus selected workshops.

RQs: demographics; RE usage (task/phase/artifacts); prompt engineering; resources (models, data, tools); evaluation methods.

## Results (numbers to remember)

| Finding | Number |
|---------|--------|
| Primary studies | 74 |
| Conferences / workshops | 66% / 23% |
| Elicitation task share | ~20% |
| Validation task share | ~20% |
| Modeling | ~12% |
| Broader SE tasks | ~15% |
| V&V as phase | 16 studies, 22% |
| Zero-shot prompting | 44% |
| Few-shot | 29% |
| RAG | **6%** |
| Interactive prompting | **5%** |
| GPT-family models | ~90% |
| LLaMA | 15% |
| Share code/prompts | 61% |
| Share datasets | **16%** (12/74) |
| Lab experiments | **75–76%** |
| Field studies | **7%** |
| Proposed integrated tools | 21 tools (minority of papers) |

Search funnel (Fig. 2): Scopus 244 → title/abstract 136 → inclusion 62; venue search +12 → **74**.

**Exact task/phase counts (Tables 5–6):** elicitation **15 studies, 20%**; validation **15, 20%**; elicitation *phase* and V&V *phase* **16 each, 22%**. NLP4RE had analysis 42.7% and V&V only 4% — the lifecycle has flipped toward the human-heavy ends.

Input: SRS **28 / 38%**. Output includes interview scripts/questionnaires (**5%**) — adjacent to our question policy.

### Result figures we kept (from the HTML)

| File | What it shows | Use |
|------|---------------|-----|
| `../figures/baselines/zadenoori-fig-eval-methods.png` | Task × eval method bubbles | **Elicitation field studies = 1**; validation field studies = 1. Lab owns elicitation (11) and validation (12). |
| `../figures/baselines/zadenoori-fig-io-artefacts.png` | Input × output artefacts | Interview scripts almost empty (1). SRS→analysis reports is the dense cell. |
| `../figures/baselines/zadenoori-fig1-scheme.svg` | Conceptual data-extraction scheme | Optional related-work figure |
| `../figures/baselines/zadenoori-fig2-search.svg` | Search/filter pipeline | Methods appendix |

**This is stronger than “7% field studies.”** Among 74 papers, **live elicitation in the field is essentially one study.** That is the sentence for our industrial-evaluation claim.

## Limitations they admit

Preliminary; single-author screening with limited double-check. GPT-heavy literature may date quickly.

## Why we can beat / complement this (we are not competing with an SLR)

We **cite** it. Our empirical paper should:

- be a **field** study (their 7% gap)
- use **interactive** prompting as the object of study (their 5%)
- optionally RAG (their 6%)
- release prompts + some data (their 16% data gap)

## Quotes / takeaways for intro

Most studies test LLMs out-of-the-box rather than embedding them in multi-step stakeholder workflows. Future work: integrated workflows, formal methods, domain tools, usefulness besides raw performance.
