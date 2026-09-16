# Journey and action plan

This file is the **path lock**. If we wander, we come back here.

Last updated: 2026-09-16.  
Current phase: **P0 — freeze RQs and evaluation before building more agents.**

## Path-lock questions (every new idea)

1. Which RQ in [`01-RESEARCH-QUESTIONS.md`](01-RESEARCH-QUESTIONS.md) does this answer?
2. Did a paper in [`papers/`](papers/00-INDEX.md) already do it?
3. How do we measure it ([`06`](06-EVALUATION-FRAMEWORK.md))?
4. Where is the number stored ([`07`](07-RESULTS-LOG.md))?

If (1) is empty → product backlog only ([`08`](08-SOFTWARE-AND-IMPLEMENTATION.md)).

## Where we are now (honest)

| Asset | State | Paper value |
|-------|-------|-------------|
| Persian Dify BA chatflow | Working prototype (rules, RFP files, draft, freeze, HTML demo) | Industrial vehicle; **not** yet critic/decision |
| Company org hard rules | Encoded as conversation variable | Strong RAG/domain hook |
| Research notes | This `research/` tree (created 2026-09-16) | Trail is now explicit |
| Decision taxonomy | Specified on paper, **not implemented** | Core gap |
| Evaluation harness | Not started | Blocks the paper |
| Anonymized industrial cases | Not collected | Blocks the strong paper |
| Public Python tool | Not started | Blocks artifact |

The company Dify app currently **records** requirements more than it **rejects** them. That is the opposite of RQ2. First implementation increment should be the Decision node, not more LLM branches.

## Phases

### P0 — Research freeze (1–2 weeks) — **NOW**

- [x] Capture idea + literature into markdown
- [ ] You supply missing PDFs listed in [`09-PAPERS-NEEDING-FULL-TEXT.md`](09-PAPERS-NEEDING-FULL-TEXT.md)
- [ ] Confirm company permission for anonymized cases (legal/ethics)
- [ ] Freeze RQ1–RQ5 wording
- [ ] Freeze JSON schema for Requirement Decision + Project model
- [ ] Choose target venue class (conference checkpoint vs journal direct)

**Exit:** RQs + metrics + schema agreed; no more architecture doodling without mapping to RQs.

### P1 — Minimal critic loop (research code, not only Dify)

Build the smallest system that can support RQ2:

1. Conversation agent (can start from current BA prompt)
2. Extract candidate statements
3. **Decision classifier + rationale** (the product)
4. One clarification question if CLARIFY
5. Structured JSON spec update
6. Human-readable Markdown FRD

Do **not** start with 8 specialist agents. Add agents only if ablation shows gain (QUARE’s lesson: protocol > sprawl; OntoAgent’s lesson: ontology/structure > extra free-form).

**Exit:** 10 scripted dialogues where Vanilla accepts blockchain/WhatsApp/1M users and Agentic-BA challenges them.

### P2 — Evaluation harness

- Replay scripts
- Score vs gold decisions
- Compute P/R/F1, κ, IRE/TKQR if using ReqElicitGym
- Log tokens, turns, time
- Plot: turn vs completeness; confusion matrix

**Exit:** `research/07-RESULTS-LOG.md` has **real numbers** from a toy set.

### P3 — Baselines

Implement or wrap:

| System | How |
|--------|-----|
| A Vanilla | same model, “write an SRS” |
| B Prompted BA | single BA system prompt, no explicit decision object |
| C Agentic | P1 loop |
| Optional D | OntoAgent-style slot questions **without** reject |
| Optional E | Yin-style conflict/priority **without** live interview |

Ablation inside C: critic off / RAG off / question-budget off.

### P4 — Public benchmark + industrial cases (in parallel)

- Run on **ReqElicitGym** (101 website scenarios) so we can sit next to OntoAgent numbers
- Collect **N ≥ 8–12** anonymized company cases (leave request, certificate of origin, etc.) with a human BA gold spec + gold decisions
- Ethics: consent, strip names, systems, volumes that identify the org

**Exit:** two evaluation worlds (public + industrial). Journals love this pairing.

### P5 — Human study

- 2+ professional BAs label decisions (κ)
- Stakeholders rate usefulness (secondary)
- Time-to-validated-spec vs manual BA (if feasible)

### P6 — Paper write-up

Order of writing (do not start with Implementation):

1. Related work + gap (already drafted in `02`)
2. Method (decision + loop)
3. Evaluation design
4. Results (from `07`)
5. Discussion / error analysis
6. Then implementation appendix + artifact

### P7 — Open-source release

- English-first GitHub README
- Company Persian Dify remains a downstream distribution
- Evaluation scripts + example dialogues
- License + model-provider abstraction (no hard OpenRouter-only)

## Suggested extra goals (parked, not current path)

| Idea | RQ | Park until |
|------|----|------------|
| Requirement graph impact analysis | RQ5 | After freeze works in research code |
| Formal constraints / LTL snippets | Ferrari roadmap | Paper v2 |
| Multi-quality dialectic (QUARE-like) | extra | Only if NFRs become the industrial pain |
| GUI/HTML demo | none | Product only (already in Dify) |
| Meeting-bot (MARARE-like) | none | Different paper |

## Weekly cadence (suggested)

| Week | Output |
|------|--------|
| 1 | Schema + 10 adversarial dialogues + gold labels |
| 2 | Decision loop MVP + first confusion matrix |
| 3 | Vanilla vs Prompted vs Agentic on those 10 |
| 4 | ReqElicitGym subset (20 scenarios) |
| 5–6 | Industrial cases (as permission allows) |
| 7 | Human BA labeling |
| 8 | Draft paper skeleton with real tables |

## Risks that knock us off the path

| Risk | Symptom | Counter |
|------|---------|---------|
| Demo-driven | More Dify nodes, no metrics | P0 rule |
| Multi-agent sprawl | 8 agents, no ablation | Max 3 roles until P3 |
| BLEU worship | “Our ROUGE is higher” | Decision accuracy first |
| Unreleased company data | Paper stays toy | Anonymized public examples anyway |
| Model chasing | Swap GPT every week | Freeze one model per experiment, report name+date |
| Context switching | New side paper ideas | Put them under P7 parked list |

## Decision log

| Date | Decision | Why |
|------|----------|-----|
| 2026-09-16 | Scientific novelty = Requirement Decision + critique, not “AI BA” branding | Literature already has conversational extractors |
| 2026-09-16 | Multi-agent is mechanism | Too common to be the claim |
| 2026-09-16 | Do not lead with Dify | Tool-lock weakens journal contribution |
| 2026-09-16 | Industrial evaluation is the differentiator | 1.3% production in Cheng SLR |
| 2026-09-16 | Freeze title: original + “with Interactive Critique” | Keep field-study signal; add novelty word; reject stuffed all-in-one and “Challenging the Stakeholder” as header |
| 2026-09-16 | Public decision-labeled dataset is a first-class competitive artifact, not a leftover | Other papers win on gyms/US corpora; industrial n will be small |
| 2026-09-16 | On “please commit”, agent chooses split and messages | Keep the trail in git without blocking on commit-message drafting |
| 2026-09-16 | Raw papers: extract notes + figures, then **delete** the dump | Avoid git-bloating copyrighted PDFs; `ARTIFACTS.md` holds locations |

Add rows as we go. Do not delete rows — strike-through superseded decisions.
