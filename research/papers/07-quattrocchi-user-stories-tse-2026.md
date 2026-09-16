# Quattrocchi et al. — Can LLMs Generate User Stories and Assess Their Quality?

- **Cite:** G. Quattrocchi, L. Pasquale, P. Spoletini, L. Baresi. *Can LLMs Generate User Stories and Assess Their Quality?* IEEE Trans. Software Eng., 52(5):1773–1790, May 2026. [10.1109/TSE.2026.3670612](https://doi.org/10.1109/TSE.2026.3670612)
- **arXiv:** https://arxiv.org/html/2507.15157v1 (read 2026-09-16)
- **Venue strength:** **TSE** — cite heavily
- **Our use:** (1) US as intermediate representation; (2) codebook-based Quality Agent; (3) warning that LLMs have high coverage, low diversity, weaker AC

## Setup

Replicates Ferrari et al. interview-based learning (summer-camp CamperPlus, 53 GT user stories).

- 10 LLMs × 30 analyst instances + 1 customer instance
- Two 15-min-style interview rounds then 50 US each
- **13,958** LLM user stories vs 1,530 student US vs 53 GT

Models: Claude 3.5/3 Sonnet, Claude 3 Opus, Grok Beta, GPT-4, GPT-3.5 Turbo, LLaMA 3.1 8B/405B, Gemini 1.5 Flash/Pro.

QUS semantic criteria (3-point): Feature Specificity, Rationale Clarity, Problem-Oriented, Language Clarity, Internal Consistency.

Human codebook; 153 US labeled by 3 authors.

## Results to beat / respect

### Coverage of GT (Table II, cosine 0.8 / 0.85)

| Generator | c=0.8 | c=0.85 |
|-----------|-------|--------|
| Claude 3 Sonnet | **96.23** | 88.68 |
| Claude 3 Opus | **96.23** | 84.91 |
| Gemini 1.5 Pro | 90.57 | 77.36 |
| Llama 3.1 405B | 81.13 | 64.15 |
| GPT-4 | 75.47 | 43.40 |
| GPT-3.5 | 73.58 | 37.74 |
| Llama 3.1 8B | 58.49 | 16.98 |
| **All LLMs** | **98.11** | 98.11 |
| **Students** | **52.83** | 15.09 |

LLMs crush students on matching the *known* GT set — possibly conservative, pattern-copying.

### Diversity (Table III)

| Generator | Avg diversity % |
|-----------|-----------------|
| Students | **98.58** |
| Grok Beta | 74.74 |
| LLaMA 3.1 8B | 73.36 |
| GPT-4 | 62.21 |
| Claude 3 Opus | 55.35 |
| Claude 3 Sonnet | **44.23** |

High coverage + low diversity = **not a creative BA**.

### Detectability (GPTZero AI %)

Claude 3.5 Sonnet **18.86%** (more human-like than students 20.24%); Claude 3 Opus **80.01%**; GT **3.28%**.

### Quality assessment κ (with full codebook)

Claude 3 Opus **overall κ = 0.87** (FS 0.89, RC 0.86, PO 0.72, LC 0.92, IC 0.97) — **above inter-human ~0.74–0.78**.

Partial codebook sometimes beat full (Claude 3.5 0.86 vs 0.84; GPT-4 0.85 vs 0.78) — over-prompting can hurt.

LLaMA 3.1 8B max ~0.70.

### Rejection rate (any criterion = 1), Table VIII

| Source | Rejection % | Avg score |
|--------|-------------|-----------|
| Ground truth | **9.43** | 2.78 |
| Students | **14.64** | 2.70 |
| Claude 3 Opus (generated) | **16.55** | 2.78 |

LLM stories look fluent but **fail acceptance more often**. Defects: conjunctions, low specificity, weak rationale.

## Implications for us

1. **Do not** use “coverage vs GT” as the only success metric — we would look good and still be a bad BA.
2. **Do** reuse QUS + codebook inside the Critic before ACCEPT.
3. **Do** generate AC explicitly; TSE says this is where LLMs fail.
4. Customer was an LLM with GT in context — our industrial users will not be that consistent. Expect lower coverage.

## Figures in original

Study overview Fig. 1; diversity heatmaps Fig. 2; κ vs codebook Fig. 3. Save from PDF if needed for related-work slides — not our results.
