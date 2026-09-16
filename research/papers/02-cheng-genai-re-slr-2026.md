# Cheng et al. — Generative AI for Requirements Engineering: SLR

- **Cite:** Cheng et al. *Generative AI for Requirements Engineering: A Systematic Literature Review*. Software: Practice and Experience, 2026. DOI [10.1002/spe.70029](https://doi.org/10.1002/spe.70029). arXiv:2409.06741
- **Read:** 2026-09-16 (arXiv + Wiley snippets)
- **Our use:** strongest evidence that **management** and **production** are empty — our freeze/trace + company deploy

## Problem

GenAI-RE grew too fast for narrative reviews. Need classification across lifecycle, prompts, eval, industry.

## Method

772 initial hits → **238** papers (2019–May 2025) after screening + snowballing. QA mean ~3.79/4.

## Results

### Lifecycle attention

| Phase | Share |
|-------|-------|
| Analysis | **30.0%** |
| Elicitation | **22.1%** |
| Specification | **22.1%** |
| Validation | **19.0%** |
| Management | **6.8%** |

GPT-family in **67.3%** of applications.

### Challenges (co-occurring triad)

| Challenge | Papers mentioning |
|-----------|-------------------|
| Reproducibility | 66.8% |
| Hallucinations | 63.4% |
| Interpretability | 57.1% |
| Co-occurrence of the three | ~35% |

### Industry

| Stage | Share |
|-------|-------|
| Early-stage / vision / PoC | **90.3%** |
| Prototype / experimental deploy | 8.4% |
| Production-grade | **1.3%** |

Tools publicly released: **23.9%**. Datasets often used but not shared.

Prompt examples available in >80% of studies (better than Zadenoori’s code-sharing era, different corpus).

Evaluation still precision/recall/F1 heavy; weak RE-specific metrics (traceability, ambiguity resolution, stakeholder alignment).

## Roadmap they propose (aligns with us)

1. Stronger evaluation foundations and benchmarks
2. Governance-aware development (fairness, privacy, interpretability)
3. Move beyond isolated tasks to operational workflows

## How we use it

- Intro: “only 1.3% production; we evaluate in a company workflow.”
- RQ5: management 6.8% → versioning/trace is a real hole, not a side feature.
- Discussion: we must report prompts, model ids, and failure modes (hallucination of org rules).

**Do not** claim we “beat” this paper. We operationalize its roadmap.
