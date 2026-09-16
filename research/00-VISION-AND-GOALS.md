# Vision and goals

Status: **locked for v1 of the paper** (update only if an RQ changes).  
Last updated: 2026-09-16.

## Working title (frozen)

> **From Conversational Stakeholder Input to Validated Software Requirements: An Industrial Evaluation of an Agentic Business Analyst with Interactive Critique**

The original title was kept almost intact: industrial evaluation + BA persona + conversational → validated spec. The only addition is **with Interactive Critique**, so a reader does not think this is another extract-and-dump pipeline.

**Rejected as title** (keep as keywords in abstract, not the header):

| Candidate | Why not the title |
|-----------|-------------------|
| All-in-one *Challenging the Stakeholder: An Industrial Evaluation of Trustworthy Agentic RE…* | Too long; “challenging the stakeholder” sounds combative; “trustworthy” is unearned without formal guarantees |
| Option 2 *Trustworthy Agentic Requirements Engineering: …* | Fine as an **academic running header**, weaker as the main title (hides the BA role and the from–to story) |
| Option 3 *Challenging the Stakeholder: …* | Hook is memorable but the wrong first impression for RE (BAs collaborate; they do not “challenge the stakeholder” as identity) |

Abstract still says: critique, reject, negotiate, decision, industrial. Title does not need every keyword.

## What we are building (product)

A conversational **AI Business Analyst** that does not dump stakeholder wishes into an FRD.

It behaves like a professional BA:

- understands messy, multi-source, often non-technical input
- asks targeted follow-up questions
- **challenges** unjustified, infeasible, redundant, or conflicting requests
- detects ambiguity, scope creep, missing actors, missing business value
- produces a **validated** structured specification
- keeps **traceability** from utterance → decision → requirement → story → acceptance criterion
- respects **organization hard rules** (SSO, RTL/Persian UI, existing systems, regulations)

Current company prototype already has: org hard rules, RFP file ingest, draft accumulation, **version freeze**, HTML demo. That is useful engineering. It is not yet the paper.

## What we are claiming scientifically (paper)

Not: “LLMs can write requirements.” That is already known.

Yes:

> An agentic BA can **decide** whether a stakeholder statement should become a requirement, and iterative critique + clarification **improves** requirement quality versus vanilla and prompted LLMs, including in an industrial workflow.

## Why this is still valuable in 2026

The field is busy. Closest systems:

| System | What it does well | What it does not do (our opening) |
|--------|-------------------|-----------------------------------|
| Yin et al. 2026 | Multi-source normalize → parse → conflict → priority; 80.4% P / 79.7% R | Not a live BA interview; does not *reject* unjustified stakeholder wishes in conversation |
| Virtual SE Agent (ICCCI 2025) | Conversational extraction with GPT-4.1 + CoT | Similarity to expert docs (BLEU/ROUGE), not critique / necessity |
| OntoAgent (2026) | Ontology-guided *what to ask*; +33% IRE, +21% TKQR | Coverage of implicit slots, not “should this exist?” |
| LLMREI (RE’25) | Interview chatbots (long/short prompts) | Free-form; weak on style/NFR; no reject/negotiate |
| Quattrocchi TSE 2026 | Generate + assess user stories | Simulated interviews; lower diversity; weaker acceptance criteria |
| RECOVER (TSE 2025) | Extract requirements from existing transcripts | Post-hoc extraction, not live challenge |
| QUARE (RE 2026) | Multi-agent dialectic on quality attributes | Quality-attribute negotiation, not BA necessity critique |
| Cheng SPE 2026 | Map of 238 GenAI-RE papers | Shows **management 6.8%**, **production 1.3%** |

The gap is the **full BA loop**, especially:

**necessity / business-value critique + iterative stakeholder validation + industrial evaluation + traceability / versioning.**

Our company setting is an academic advantage most papers lack (Zadenoori: 7% field studies; Cheng: 1.3% production).

## Dual publication strategy

```
                    ┌─────────────────────────────┐
                    │  Journal paper (primary)    │
                    │  method + experiment        │
                    └─────────────┬───────────────┘
                                  │
           ┌──────────────────────┼──────────────────────┐
           ▼                      ▼                      ▼
   Open-source tool         Industrial case          Optional later:
   (GitHub artifact)        (anonymized)             requirement graph,
                                                     formal checks, dataset
```

Paper without runnable software is weaker in 2026 (reviewers expect artifacts).  
Software without evaluation is a blog post, not a journal paper.

## Goals in priority order

### G1 — Journal paper (must)

Target venues (ambition descending; pick after first results):

| Venue type | Examples | Fit |
|------------|----------|-----|
| Top SE journal | IEEE TSE, TOSEM, EMSE, IST, JSS, REJ | Strongest if industrial study is solid |
| Strong specialist | Requirements Engineering Journal, SPE | Natural home |
| Fast conference first | RE, REFSQ, ESEM, ICSE SEIP | Good if we need a checkpoint |

Minimum paper shape:

1. Problem + gap (this file + related work)
2. Method: Requirement Decision + critic loop
3. Implementation (enough to reproduce)
4. Experiment: 3 systems × industrial and/or ReqElicitGym-style cases
5. Human BA agreement
6. Error analysis
7. Artifact

### G2 — Open-source software (must)

Users should be able to:

- run a BA interview in English (and keep Persian for the company fork)
- get a structured project model (JSON + Markdown)
- see ACCEPT / CLARIFY / REJECT with reasons
- export FRD / user stories / acceptance criteria / trace matrix

License: MIT or Apache-2.0 (decide before first public commit of the research code).

### G3 — Public decision dataset (elevate: this is how we compete)

Not a side artifact. OntoAgent is citable because of **ReqElicitGym**; TSE 2026 is citable because of **13,958 labeled stories**. Our industrial n will be small. A public set of dialogues with gold `ACCEPT/CLARIFY/REJECT/…` labels is what other groups can rerun.

Details: [12-PUBLIC-DATASET.md](12-PUBLIC-DATASET.md). Seed: `exp-unjustified-10`.

### G4 — Suggested extra goals (high value)

| Extra goal | Why it is valuable | When |
|------------|--------------------|------|
| **Requirement graph + impact analysis** | Management is only 6.8% of GenAI-RE work | After v1 paper method is stable |
| **Domain RAG from org systems** | Differentiates from generic GPT BA | Parallel with company deployment |
| **Formal / constrained specs** | Ferrari & Spoletini IST 2025 roadmap | v2, not v1 |
| **Eval harness like ReqElicitGym** | Reproducible comparison vs OntoAgent / LLMREI | As soon as critic loop exists |

## Non-goals for the first paper

- “We invented multi-agent RE.” Multi-agent is the **mechanism**.
- Beating GPT at writing fluent FR-01 sentences.
- Full formal verification of generated requirements.
- Replacing human BAs. The claim is **assistance + measurable quality gain**.
- GUI generation (GUIDE/Figma figure in `figures/baselines/` is adjacent SE, not our core).

## Positioning sentence (use in abstracts)

A conversational AI Business Analyst that does not merely extract stakeholder requirements, but **reasons over them**, challenges questionable requirements, detects ambiguity/redundancy/conflicts, asks targeted clarification questions, and iteratively constructs a **validated, traceable** requirements specification — evaluated against vanilla LLM prompting and human BA judgment, including industrial cases.
