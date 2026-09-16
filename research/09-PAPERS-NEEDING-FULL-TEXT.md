# Papers we could not fully read

Please paste **full text** or drop a file into `research/papers/raw/` and tell me. Until then, notes stay abstract-level and must not be over-cited as if we read the methods.

Last updated: 2026-09-16.

## Ingest rule (raw → notes → delete)

When a file appears in `research/papers/raw/`:

1. Read it fully (PDF, HTML+`_files/`, or TXT).
2. Write/update `research/papers/<id>-*.md` with problem, method, results, limitations, numbers to beat, and how we differ.
3. Copy important figures to `research/figures/baselines/` and register them in [`ARTIFACTS.md`](ARTIFACTS.md).
4. Refresh this list, `02-RELATED-WORKS.md`, and `logs/reading-log.md`.
5. **Delete the raw dump** (including HTML sidecar folders). Raw is an inbox, not an archive.

Do not ask the user to keep the original in `raw/` after extraction.

## How to give me a paper

1. Paste text in chat, **or**
2. Put a `.pdf` / `.html` / `.txt` under `research/papers/raw/` and name it in chat.

I will also extract **result tables and important figures** when images are available.

## High priority (closest to our idea)

| Paper | Why we need the full text | What we have |
|-------|---------------------------|--------------|
| **Virtual Software Engineer Agent for Product Requirement Engineering and Management Using GPT-4.1 and CoT**, IEEE ICCCI 2025, [10.1109/iccci65070.2025.11158389](https://doi.org/10.1109/iccci65070.2025.11158389) | Closest conversational “virtual engineer”; need BLEU/METEOR/ROUGE tables, prompts, limitations | Abstract only |
| **Automated Software Requirements Elicitation: A Systematic Mapping Study**, MDPI Information 2026, 17(8):777 | Confirm 51% / 23% / 8% funnel and industrial 14%; need figures | Abstract + OSF summary; HTML/PDF fetch timed out |
| **QUARE: Quality-Aware RE through Multi-Agent Dialectic Negotiation**, RE 2026 | Protocol details, baselines (MARE, iReDev), whether they reject requirements | Abstract (98.2% compliance, etc.) |
| **From Business Meetings to Requirement Artifacts: MARARE** [10.1145/3786167.3788405](https://doi.org/10.1145/3786167.3788405) | Live multi-agent meeting BA; tiny n=5 but close | Abstract |
| **LLMREI original RE’25 paper** (Korn et al., interview chatbots) | Prompt text for fair baseline reimplementation | OntoAgent’s re-reported numbers + our saved figures |

## High priority (evaluation / quality)

| Paper | Why | What we have |
|-------|-----|--------------|
| **Can LLMs Generate User Stories…?** TSE 2026 paywall version vs arXiv 2507.15157 | We used arXiv HTML — check camera-ready numbers | Strong arXiv coverage |
| **Advancing RE with LLMs**, Ellsel & Stark, Procedia CIRP 2025, [10.1016/j.procir.2025.08.120](https://doi.org/10.1016/j.procir.2025.08.120) | Exact GPT-4o vs human % on quality | Abstract + snippets (~69.5% mentioned in secondary pages — **unverified**) |
| **ReqNet**, 2025, [10.1007/s40747-025-02143-w](https://link.springer.com/article/10.1007/s40747-025-02143-w) | Document/RFP extraction baseline | Not read |
| **From issue titles to requirements**, REJ 2026, [10.1007/s00766-026-00462-z](https://link.springer.com/article/10.1007/s00766-026-00462-z) | Prompt strategies from informal text | Not read |
| **Supporting Stakeholder Requirements Expression with LLM Revisions** (Hannover) | Human expression + LLM revision — adjacent to critique | Not read |
| **A Methodology for Systematic Evaluation of LLMs in RE with No Ground Truth**, Systems 2026, [10.3390/systems14060598](https://doi.org/10.3390/systems14060598) | May solve industrial eval without gold specs | Not read |

## RE 2026 / human factors (validation loop)

| Paper | Why |
|-------|-----|
| **Under Pressure: Navigating Human Factors in AI-Supported Requirements Validation** | Directly about validation — our 8% gap |
| **Debugging Requirements Interview Scripts: A Framework for Quality Assessment** | Question quality — complements TKQR |

## Other listed sources (lower priority but cite-carefully)

| Paper | URL | Status |
|-------|-----|--------|
| Integrating LLM capabilities into the RE process | https://doi.org/10.1016/j.dte.2026.100098 | Not read |
| Enhancing SRE with LMs and prompting (ACL SRW 2025) | https://aclanthology.org/2025.acl-srw.31/ | Not read |
| Using ChatGPT in SRE: A Comprehensive Review (2024) | (user list; locate PDF) | Not read as full text this pass |
| Large Language Model for RE SLR (Sciety / RS 5589929) | https://sciety.org/articles/activity/10.21203/rs.3.rs-5589929/v1 | May overlap Zadenoori; check |
| Business Analyst’s Guide to Agentic AI Requirements | https://modernanalyst.com/.../ID/7213/... | Practitioner; skim later |
| Formal RE and LLMs two-way roadmap | IST 2025 PDF **was retrieved** — notes in `papers/10-ferrari-formal-re-llms-2025.md` |

## Accessible and already summarized (do not re-send unless camera-ready differs)

- Zadenoori et al. LLM4RE SLR — notes in `papers/01` (raw HTML **deleted** after extract, 2026-09-16)
- Cheng et al. GenAI RE SLR — arXiv:2409.06741 / SPE 70029
- Hemmat et al. Frontiers 2025 — open
- Yin et al. LLM+Agent 2026 — Sage/IOS page retrieved
- OntoAgent — arXiv:2605.05828
- ReqElicitGym — arXiv:2602.18306
- Quattrocchi et al. user stories — arXiv:2507.15157
- RECOVER — arXiv:2411.19552
- Ferrari & Spoletini IST 2025 — CNR PDF

## Figures we already keep

See [`figures/README.md`](figures/README.md) and [`ARTIFACTS.md`](ARTIFACTS.md).
