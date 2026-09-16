# Results log (numbers, graphs, experiment artifacts)

**This file stays empty of claims until a run exists.**  
Do not paste hoped-for numbers. Date every row.

Last updated: 2026-09-16.

## How to add a result

1. Tag the git commit / prompt hash
2. Name the experiment (`exp-unjustified-10`, `gym-20`, `industrial-leave-01`, …)
3. Fill a table below
4. Drop plots under `figures/experiments/<exp-id>/`
5. Link raw logs from `logs/`
6. Update [04-JOURNEY-AND-ACTION-PLAN.md](04-JOURNEY-AND-ACTION-PLAN.md) decision log if the result changes the path

## Baseline numbers from literature (not our results)

Copied here so graphs have a comparison band. Sources in [`papers/`](papers/00-INDEX.md).

| Source | Metric | Value |
|--------|--------|-------|
| Yin 2026 | Precision | 80.4% |
| Yin 2026 | Recall | 79.7% |
| Yin 2026 | F1 | 0.89 |
| Yin 2026 | Redundant proposals removed | 22 (17.3% contribution) |
| OntoAgent | IRE | 0.69 |
| OntoAgent | TKQR | 0.59 |
| LLMREI-short | IRE / TKQR | 0.39 / 0.49 |
| LLMREI-long | IRE / TKQR | 0.38 / 0.09 |
| Mistake-guided | IRE / TKQR | 0.52 / 0.48 |
| RECOVER | Turn P / R | 63% / 77% |
| RECOVER | Conversation BLEU vs expert | 78.82% |
| TSE 2026 | Claude Opus quality κ | 0.87 |
| TSE 2026 | US reject GT / students / Claude | 9.43 / 14.64 / 16.55 % |
| QUARE | Compliance coverage | 98.2% |
| MARARE | Coverage | 80.0 ± 11.2% |
| MARARE | Hallucination | 14.3 ± 6.2% |

## Our experiments

### exp-unjustified-10

Status: **not run**  
Model: _TBD_  
Commit: _TBD_

| Metric | Vanilla A | Prompted B | Agentic C |
|--------|-----------|------------|-----------|
| Unjustified-acceptance % | | | |
| Completeness (gold needs) | | | |
| False-reject % | | | |
| Mean challenge questions | | | |

Plots: _none yet_

### gym-20 (ReqElicitGym subset)

Status: **not run**

| System | IRE | TKQR |
|--------|-----|------|
| Vanilla | | |
| Prompted | | |
| Agentic | | |
| OntoAgent (published) | 0.69 | 0.59 |

### industrial-n

Status: **not collected**

| Case id | Domain | Turns | Gold reqs | Notes |
|---------|--------|-------|-----------|-------|
| | | | | |

## Visual results checklist (paper figures we will need)

| Fig | Content | Status |
|-----|---------|--------|
| F1 | Architecture (decision loop) | not drawn |
| F2 | Example dialogue: Vanilla vs Agentic on blockchain/WhatsApp | not drawn |
| F3 | Completeness vs turn (like OntoAgent fig 3) | not run |
| F4 | Confusion matrix of decisions | not run |
| F5 | Three-system bar chart of core metrics | not run |
| F6 | Ablation bars | not run |
| F7 | Trace graph screenshot | not built |
| F8 | Training/inference **logs** (loss only if we fine-tune; otherwise token/cost/turn logs) | not run |

## Log graphs (runtime, not ML loss)

Until we fine-tune, “graph of logs” means:

- turns vs completeness
- tokens per case
- cost per validated spec
- latency per critic call
- freeze events over a project

Store CSV in `logs/<exp-id>/metrics.csv`. Plot with a small Python script later (do not paste huge CSV here).
