# Artifact locations

Canonical map of **kept** research artifacts. Raw paper dumps are **not** kept (see ingest rule).

Last updated: 2026-09-16.

## Ingest rule (raw papers)

1. User drops a paper into [`papers/raw/`](papers/raw/README.md) (PDF, HTML+`_files/`, or TXT) and says so.
2. Agent reads it and writes/updates `papers/<nn>-*.md` with **problem, method, results (tables/numbers), limitations, what we can beat, figures**.
3. Important figures are copied to [`figures/baselines/`](figures/README.md) (or `figures/paper/` if ours).
4. Related work / numbers-to-beat files are refreshed (`02`, `06`, `07` as needed).
5. **Delete the file(s) from `papers/raw/`** (including HTML `_files/` folders). Raw is an inbox, not an archive.
6. Log the read in [`logs/reading-log.md`](logs/reading-log.md).

Do not leave copyrighted PDFs in git. The durable record is our notes + extracted figures we actually cite.

## Where things live

| Kind | Path | Notes |
|------|------|--------|
| Trail index | [`README.md`](README.md) | Start here |
| Working title, RQs, related work, method, eval | `00`–`08`, `10`–`12` | |
| Papers still needed | [`09-PAPERS-NEEDING-FULL-TEXT.md`](09-PAPERS-NEEDING-FULL-TEXT.md) | Also has ingest rule |
| Paper notes | [`papers/00-INDEX.md`](papers/00-INDEX.md) | One MD per paper |
| Raw inbox | [`papers/raw/`](papers/raw/README.md) | Empty except README after processing |
| Baseline figures (other papers) | [`figures/baselines/`](figures/README.md) | Caption with source; never claim as ours |
| Our experiment plots | `figures/experiments/` | After runs |
| Paper-ready figures | `figures/paper/` | Polished |
| Experiment / reading logs | [`logs/`](logs/README.md) | |
| Original idea dump | [`notes/source-notes-original-idea.md`](notes/source-notes-original-idea.md) | |
| Public dataset plan | [`12-PUBLIC-DATASET.md`](12-PUBLIC-DATASET.md) | L0–L2 |
| Company context | [`11-COMPANY-INDUSTRIAL-CONTEXT.md`](11-COMPANY-INDUSTRIAL-CONTEXT.md) | No secrets |
| Dify product | repo root `business-analyst-fa-chatflow.dify.yml`, `WORKFLOW.md` | Not the paper |
| Research code | repo root [`src/reqdecide/`](../src/reqdecide), [`tests/`](../tests), `pyproject.toml` | Map in [`08-SOFTWARE-AND-IMPLEMENTATION.md`](08-SOFTWARE-AND-IMPLEMENTATION.md) |
| Fetched corpora (V1–V3) | repo root `data/` | **Git-ignored.** Rebuild with the adapters; never commit issue dumps |
| Validation ladder V1–V4 | [`06-EVALUATION-FRAMEWORK.md`](06-EVALUATION-FRAMEWORK.md) | Which tier compares against whose numbers |

## Extracted baseline figures (kept)

| File | Source paper |
|------|----------------|
| `figures/baselines/zadenoori-fig-eval-methods.png` | Zadenoori LLM4RE SLR — task × eval method (elicitation field n=1) |
| `figures/baselines/zadenoori-fig-io-artefacts.png` | Zadenoori — input × output artefacts |
| `figures/baselines/zadenoori-fig1-scheme.svg` | Zadenoori Fig. 1 conceptual scheme |
| `figures/baselines/zadenoori-fig2-search.svg` | Zadenoori Fig. 2 search funnel |
| `figures/baselines/ontoagent-fig1.png` | OntoAgent architecture |
| `figures/baselines/ontoagent-fig2.png` | OntoAgent induction-size curve |
| `figures/baselines/ontoagent-fig3.png` | OntoAgent turn-level IRE |
| `figures/baselines/llmrei-fig1.png` | LLMREI-short dialogue |
| `figures/baselines/llmrei-fig4.png` | LLMREI recall boxplots |
| `figures/baselines/guide-fig1.png` | GUIDE GUI (out of core scope) |

## Paper notes vs raw

| Paper | Notes file | Raw dump |
|-------|------------|----------|
| Zadenoori LLM4RE SLR | `papers/01-zadenoori-llm4re-slr-2025.md` | **deleted** after extract (2026-09-16) |
