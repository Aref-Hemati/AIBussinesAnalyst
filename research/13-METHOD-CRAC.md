# Method: Calibrated Requirement Admission Control (CRAC)

Status: **method freeze for implementation**. Change only if an RQ or a validation-tier protocol changes.  
Last updated: 2026-09-16.

Code: [`src/reqdecide/schema.py`](../src/reqdecide/schema.py), [`uncertainty.py`](../src/reqdecide/uncertainty.py), [`policy.py`](../src/reqdecide/policy.py).  
Validation: [`06-EVALUATION-FRAMEWORK.md`](06-EVALUATION-FRAMEWORK.md) (V1–V4 ladder).

## Claim this method is allowed to make

With the stakeholder in the loop, an agent that **admits, asks, or blocks** each statement under a question budget produces higher-precision specifications than vanilla or prompted LLMs, without collapsing recall of real needs.

The scientific object is not “we wrapped an LLM.” It is a **selective-prediction rule** over requirement candidates.

## What is not new

| Already published | What they own |
|-------------------|---------------|
| OntoAgent / ReqElicitGym | *What to ask* to cover implicit slots (IRE, TKQR) |
| Yin 2026 | Conflict, duplicate, priority on existing demand sources |
| CLAM / CLAMBER / Intent-Sim | *When to ask* vs guess, in QA not RE |
| WONTFIX studies | Why GitHub issues get declined |

## What is new (keep this list short)

1. **Interpretation entropy, not model confidence.** Sample K readings of the utterance, cluster them, take the entropy of the cluster distribution. Disagreement among readings is ambiguity (ask the stakeholder). Agreement plus low confidence is ignorance (retrieve org rules; do not nag).
2. **Cost-sensitive admission.** Three explicit costs: wrong admit, wrong block, one question. The operating point is a **curve**, not a single accuracy.
3. **Hard schema gate.** A requirement that does not trace to an ACCEPT decision is unrepresentable (`Project` validator). That is Ferrari’s structured-constraint idea at the cheap end.

Multi-agent orchestration is a *mechanism*. It is not listed as a contribution.

## Loop

```
utterance
  → K independent readings
  → interpretation entropy
  → critics (duplicate, conflict, org-rule, evidence, necessity)
  → expected-cost rule under remaining question budget
  → ADMIT | ASK | BLOCK
  → only ADMIT may write a requirement
  → freeze requires a human confirm
```

Hard constraints fire before the cost rule: duplicate, conflict, org-rule. Ambiguity with budget remaining spends a question. Ambiguity with no budget **refuses to admit** rather than guessing.

## Decision labels vs scoring

Nine labels live on the object. Scoring for small *n* uses three super-classes:

| Super-class | Labels | Action |
|-------------|--------|--------|
| ACCEPT | ACCEPT | admit |
| HOLD | CLARIFY, AMBIGUOUS, INSUFFICIENT-EVIDENCE | ask |
| BLOCK | REJECT, OUT-OF-SCOPE, UNJUSTIFIED, DUPLICATE, CONFLICTING | block |

## How this is allowed to be compared

See the V1–V4 ladder in [`06-EVALUATION-FRAMEWORK.md`](06-EVALUATION-FRAMEWORK.md). Short version:

- V1 and V2: same public splits / same gym as published numbers, with the zero-shot vs supervised and IRE 0.32 vs 0.69 caveats written in that file.
- V3: first public baseline on maintainer outcomes; we do not invent those labels.
- V4: industrial κ only.

## What we will not claim

- Beating PassionNet/SR-BERT *as specialists* on V1.
- Quoting OntoAgent’s 0.69 IRE without a controlled re-run.
- That `wontfix` is a gold BLOCK without the theme filter and the 200-issue audit.
- That the agent replaces a human BA.
