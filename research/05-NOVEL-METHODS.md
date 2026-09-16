# Novel methods to invent, combine, and test

Innovative ≠ ungrounded. Each idea below is **checked against 2025–2026 papers**. Status: proposed → to test → adopted / rejected.

Last updated: 2026-09-16.

The admission-control formulation that the code implements is frozen in [`13-METHOD-CRAC.md`](13-METHOD-CRAC.md). The numbered methods below remain the ablation menu.

## Design principle

Combine **three published strengths** that have not been evaluated together as a BA:

| Strength | Source | What we add |
|----------|--------|-------------|
| Structured questioning (what to ask) | OntoAgent | Only ask after a decision of CLARIFY |
| Conflict + priority + RAG | Yin et al. 2026 | Apply in **live** dialogue, not only batch feedback |
| Semantic quality assessment | Quattrocchi TSE; Ellsel CIRP | Run **before** ACCEPT, not only on a finished backlog |
| Transcript extraction | RECOVER | Inverse: we generate the transcript **and** the spec |
| Dialectic protocol | QUARE | Dialectic on **necessity/scope**, not only quality attributes |
| Version/management | rare (6.8%) + our Dify freeze | Trace + immutable versions as first-class |

## M1 — Requirement Decision Object (core, test first)

**Idea:** Every candidate is a typed object, not a sentence in a list.

```json
{
  "id": "cand-17",
  "utterance_id": "t-12",
  "text": "We need blockchain",
  "decision": "UNJUSTIFIED",
  "confidence": 0.81,
  "business_objective_id": null,
  "questions": ["What fraud or audit problem does blockchain solve that signed audit logs do not?"],
  "alternatives": ["Append-only audit log with RBAC"],
  "org_rule_refs": ["security.audit-log"],
  "conflicts_with": []
}
```

**Why novel enough:** papers extract or ask; few persist a **reject class with an alternative**.

**Check vs literature:** Yin resolves conflicts among existing items; OntoAgent never rejects a requested feature for lack of value; QUARE negotiates quality trade-offs.

**Experiment:** gold labels on 50 planted unjustified requests. Metric: reject/clarify recall without destroying true requirements (false reject).

## M2 — Two-budget questioning policy

**Idea:** Separate budgets:

- `B_cover` — questions that fill missing slots (OntoAgent-like)
- `B_challenge` — questions that attack necessity, evidence, feasibility

Stop when both budgets are met **or** stakeholder confirms freeze.

**Why:** OntoAgent’s TKQR rewards early key questions; unconstrained challenge can nag. A budget makes the BA professional, not inquisitorial.

**Test:** same IRE with fewer challenge turns; stakeholder Likert “felt challenged but not blocked.”

## M3 — Evidence gate for quantitative NFRs

**Idea:** Any number (users, SLA, TPS, “real-time”) is `INSUFFICIENT-EVIDENCE` until a source is given (current volume, contract, regulation).

Example: “1 million users” → ask peak concurrency / current baseline / which year.

**Check:** quality papers assess clarity; they do not gate **evidence**.

**Test:** planted numeric claims; % correctly gated vs Vanilla (which will happily write NFR-01).

## M4 — Org-rule critic (domain-aware BA)

**Idea:** RAG/retrieve org hard rules *before* ACCEPT.

If rule says SSO + personnel code login, reject “also add Google login on the public internet” or mark CONFLICTING.

Already partially present in the Dify `org_hard_rules` variable — **promote it from prompt spice to a decision input**.

**Check:** Yin uses legal/compliance in a **priority weight** (0.6), not as a conversational reject. Cheng notes RAG is still a minority pattern in older LLM4RE (Zadenoori: 6%).

**Test:** paired cases with/without rule retrieval; decision accuracy on policy conflicts.

## M5 — Contradiction graph (live Yin)

**Idea:** Maintain an embedding/index of accepted requirements. New ACCEPT is checked for:

- duplicate (DUPLICATE)
- opposite constraint (CONFLICTING)
- scope expansion vs frozen version (scope creep)

On conflict, present **alternatives** (QUARE-like one-round dialectic): keep A, keep B, or synthesize.

**Test:** Yin-style redundant-proposal reduction; we should aim to **beat 18%** on live interviews (different setting — report carefully).

## M6 — Completeness critic with a domain ontology

**Idea:** Do not copy OntoAgent’s website ontology blindly. Induce a **company/domain** ontology from frozen versions + past RFPs (leave, certificates, HR forms).

Then: after a cluster of ACCEPTs, run completeness: missing actor? missing error path? missing audit?

**Check:** OntoAgent showed style/NFR slots are what free-form LLMs miss (style IRE 0.55 vs ≤0.17). Our org systems will miss **exception/audit/RBAC** more than “style.”

**Test:** missing-requirement rate vs human BA checklist.

## M7 — User story as intermediate, FRD as freeze artifact

**Idea:** TSE 2026: LLMs match coverage but miss acceptance criteria and diversity.

Pipeline:

```
utterance → decision → canonical requirement
                      → user story + AC (only if ACCEPT)
                      → freeze to versioned FRD
```

Do not jump conversation → FRD in one generation (Vanilla failure mode).

**Test:** AC compliance rate vs TSE rejection-rate numbers (humans ~9–15% reject, LLMs often worse).

## M8 — Decision-aware generation (anti-hallucinated FR)

**Idea:** The spec generator **may not emit a requirement without an ACCEPT decision id**. Hard schema constraint.

This is the cheapest high-value method. Ferrari & Spoletini argue formal/structured constraints make LLMs trustworthy; a JSON schema is the lightweight end of that roadmap.

**Test:** count of “orphan” requirements (should be 0).

## M9 — Human-BA-in-the-loop freeze (validation 8% gap)

**Idea:** SMS: only 8% engineer stakeholder validation. We make freeze a **protocol**:

1. Agent proposes version diff (added/rejected/open questions)
2. Stakeholder or BA must confirm
3. Only then `current_version_number++` (already in Dify)

**Paper angle:** validation is not a Likert at the end; it is an **operation in the method**.

## M10 — Three-system causal experiment (methodological novelty)

Not an algorithm, but a contribution: most papers show one system. We pre-register A/B/C.

Optional fourth: **human BA unaided** on a subset (expensive, gold).

## Combinations worth testing (priority order)

| ID | Combination | Expected gain | Risk |
|----|-------------|---------------|------|
| K1 | M1+M8 | No unjustified FR in output | Over-reject |
| K2 | K1+M3 | Numeric NFR quality | Annoyance |
| K3 | K2+M4 | Company specificity | RAG noise |
| K4 | K3+M6 | Completeness | Extra turns |
| K5 | K4+M5 | Conflict/redundancy | Latency/cost |
| K6 | +M2 budgets | Usability | Missing slots |

**Do not jump to K6.** Ablate in this order (OntoAgent-style incremental table).

## Methods we should **not** spend v1 time on

| Tempting idea | Why wait |
|---------------|----------|
| 8 specialist agents from day one | QUARE/MARARE already occupy “many agents”; we need a **decision** |
| Fine-tuning a local LLM | Zadenoori/Hemmat list it as a direction; needs data we do not have yet |
| Full FM/model checking | Ferrari roadmap is v2 |
| GUI generation (GUIDE figure) | Different research area |
| Meeting transcription BA | MARARE’s paper; different input modality |

## Next experiment (smallest innovative test)

**Name:** `exp-unjustified-10`

10 short dialogues mixing valid needs + unjustified extras (blockchain, WhatsApp, 1M users, native Android, “AI that is always correct”).

Score Vanilla / Prompted / Agentic on:

- # unjustified items that became FRs (lower better)
- # true needs missed (lower better)
- # challenge questions that were on-point (human rated)

If Agentic does not win this, do not add more agents — fix the critic prompt/schema.
