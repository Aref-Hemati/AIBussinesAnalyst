# Figures

## How we use figures

- `baselines/` — **other people’s** results/architectures (for related work and “numbers to beat”). Always caption with source.
- `experiments/` — **our** plots (created after runs). Named `exp-<id>-<what>.png`
- `paper/` — polished versions for the manuscript

Do not present a baseline figure as if it were our result.

## Currently stored baselines

| File | Source | What it shows | Use in our paper |
|------|--------|---------------|------------------|
| `baselines/ontoagent-fig1.png` | OntoAgent 2026 | Ontology induction + interview loop (ParseUser, Score/ReRank, GatePrune, QuestionGen) | Related-work architecture; contrast with our Decision-first loop |
| `baselines/ontoagent-fig2.png` | OntoAgent Fig. 3 | IRE rises then TKQR falls as induction samples grow 5→20 | Warn: bigger ontology ≠ better efficiency |
| `baselines/ontoagent-fig3.png` | OntoAgent Fig. 4 | Turn-level IRE on 6 scenarios; OntoAgent climbs faster | **Template for our F3** (completeness vs turn) |
| `baselines/llmrei-fig1.png` | LLMREI-short | Interview dialogue (roles, permissions, sync, integrations) | Example of elicitation-without-critique (accepts “real time” at face value) |
| `baselines/llmrei-fig4.png` | LLMREI | Boxplots: elicited vs partially elicited recall, long vs short prompts | Short prompts can beat long on recall; still lots of partial elicitation |
| `baselines/guide-fig1.png` | GUIDE GUI paper | Figma plugin / MD component generation | **Not core RE.** Only if we discuss HTML demo as downstream |
| `baselines/zadenoori-fig-eval-methods.png` | Zadenoori LLM4RE SLR | Task × empirical method. Elicitation **field study count = 1**; lab = 11 | Cite when we say industrial eval is rare *inside elicitation*, not only overall |
| `baselines/zadenoori-fig-io-artefacts.png` | Zadenoori LLM4RE SLR | Input×output. Interview scripts ≈ empty | Our dialogue→decision→spec path is not the crowded cell |
| `baselines/zadenoori-fig1-scheme.svg` | Zadenoori Fig. 1 | LLM4RE conceptual scheme | Optional |
| `baselines/zadenoori-fig2-search.svg` | Zadenoori Fig. 2 | Search funnel 244→74 | Optional |

## Figures we still want from PDFs

When you send PDFs, extract:

- [ ] Yin 2026 Figure 1 architecture + Tables 1–2 as images
- [ ] MDPI SMS automation-depth funnel (51/23/8)
- [ ] Cheng SPE lifecycle bar chart (30/22/22/19/6.8) and production 1.3%
- [ ] TSE 2026 diversity heatmaps and κ-vs-codebook
- [ ] QUARE dialectic diagram
- [ ] Virtual SE Agent architecture (ICCCI)

## Our paper figures (todo — see `../07-RESULTS-LOG.md`)

F1 Decision-loop architecture  
F2 Vanilla vs Agentic dialogue (blockchain/WhatsApp)  
F3 Completeness vs turn  
F4 Decision confusion matrix  
F5 Three-system metrics  
F6 Ablation  
F7 Trace graph  
F8 Cost/turn logs
