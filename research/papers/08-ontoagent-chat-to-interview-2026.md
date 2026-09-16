# OntoAgent — From Chat to Interview: Agentic elicitation with an experience ontology

- **Cite:** D. Jin, Z. Jin, et al. *From Chat to Interview: Agentic Requirements Elicitation with an Experience Ontology*. arXiv:2605.05828 / RE 2026 pipeline
- **Code (anon):** https://anonymous.4open.science/r/TypoAgent-RE2026
- **Read:** 2026-09-16 arXiv HTML
- **Role:** **SOTA structured interviewer** — we must compare on IRE/TKQR and *add* necessity critique
- **Figures saved:** `../figures/baselines/ontoagent-fig1.png` (pipeline), `ontoagent-fig2.png` (induction size), `ontoagent-fig3.png` (turn IRE)

## Problem

Free-form LLM interviews miss **implicit** requirements and ask redundant/generic questions. Experienced analysts follow a hidden cognitive structure.

## Method

1. **Induce ontology** from domain requirement texts: Aspect (expert-fixed) → Dimension (LLM merge-heavy) → Slot `<key, question>`
2. **Interview loop:** ParseUser → ScoreOnto → ReRankOnto → GatePrune → QuestionGen
3. Stop: no eligible slots or max turns (20 in experiments)

Decouples *what to ask* (ontology) from *how to ask* (LLM wording).

## Results (numbers to beat on the same gym)

Eval: **ReqElicitGym**, 101 website scenarios.

### Table II overall

| Approach | IRE | TKQR |
|----------|-----|------|
| Non-CoT | 0.13 | 0.09 |
| CoT | 0.08 | 0.19 |
| LLMREI-short (RE’25) | 0.39 | **0.49** |
| LLMREI-long (RE’25) | 0.38 | 0.09 |
| Mistake-guided prompt (RE’25) | **0.52** | 0.48 |
| **OntoAgent** | **0.69 (↑33%)** | **0.59 (↑21%)** |

Relative % vs best baseline on that metric.

### Table III ablation (GPT-5.1 backbone)

| Variant | IRE | TKQR |
|---------|-----|------|
| Base LLM | 0.13 | 0.09 |
| + Experience Ontology | 0.41 | 0.34 |
| + ScoreOnto | 0.58 | 0.37 |
| + ReRankOnto | 0.64 | 0.52 |
| + GatePrune | 0.69 | 0.59 |

Ontology is the largest jump.

### Table IV backbones (robustness)

IRE 0.55–0.68; TKQR 0.47–0.74 across Claude Opus 4.5, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5, GLM-4.7, Qwen3 235B. Architecture > single model (same moral as QUARE).

### Table V aspect IRE

Style is the killer dimension for free-form models (often <0.01 to 0.17). OntoAgent style IRE **0.55**. Interaction 0.74, content 0.64.

### Induction size (Fig 3 / our `ontoagent-fig2.png`)

5→15 samples: IRE 0.69→0.73; at 20 samples TKQR drops 0.60→0.57 (bloated search space).

### Human eval (n=6 SE students, Likert 1–7)

| | Effectiveness | Efficiency | Adaptability |
|--|---------------|------------|--------------|
| LLMREI-short | 4.58 | 4.92 | 5.14 |
| LLMREI-long | 4.47 | 3.26 | 4.74 |
| Mistake-guided | 5.11 | 5.26 | 5.08 |
| OntoAgent | **5.87 (↑15%)** | **5.79 (↑10%)** | **6.12 (↑19%)** |

Turn plots (`ontoagent-fig3.png`): OntoAgent climbs earlier (turns 3–5) and plateaus higher; baselines stagnate.

## Threats they note

Gym is websites; greedy decoding; baseline reimplementation; small human n.

## Gap vs us

OntoAgent assumes the slot **should be elicited**. A stakeholder who says “put it on blockchain” would get *better blockchain slots*, not a challenge.

**Combination to test (K4 in novel methods):** OntoAgent-like completeness **after** our Decision says ACCEPT or CLARIFY-for-missing-info — never for UNJUSTIFIED.

If we run ReqElicitGym, we **must** report IRE/TKQR in the same table. If we lose IRE but win unjustified-precision, that is still a paper — say so explicitly.
