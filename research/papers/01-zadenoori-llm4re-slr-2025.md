# Zadenoori et al. — LLMs for Requirements Engineering: A Systematic Literature Review

- **Cite:** M. A. Zadenoori, J. Dąbrowski, W. Alhoshan, L. Zhao, A. Ferrari. *Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review*. arXiv:2509.11446, 2025.
- **URL:** https://arxiv.org/abs/2509.11446
- **Venue:** preprint (authors note it is preliminary; no full cross-check yet)
- **Read:** 2026-09-16 from arXiv HTML
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

Shift vs NLP4RE: from defect detection/classification → cognitively heavy elicitation & validation.

Input artifacts still dominated by SRS (38%), but issues/feedback (12%) and legal (9%) growing.

Output diversity includes interview scripts/questionnaires (5%) — adjacent to our question policy.

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
