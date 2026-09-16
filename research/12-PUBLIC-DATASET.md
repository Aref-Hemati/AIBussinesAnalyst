# Public dataset — how we compete

Last updated: 2026-09-16.

A reviewer does not cite a clever title. They cite a **reproducible task**. If our industrial sample is 8–12 cases, we still need something others can download.

## What others already own

| Paper | Public-ish resource | What it measures |
|-------|---------------------|------------------|
| OntoAgent / ReqElicitGym | 101 website scenarios, implicit vs final reqs | IRE, TKQR (did you **ask the missing slot**?) |
| Quattrocchi TSE 2026 | 13,958 generated user stories + 153 quality labels | Coverage, diversity, QUS |
| Yin 2026 | Private SaaS/smart-home corpus | P/R of extracted demands |
| RECOVER | Replication package + transcripts | Extract from **past** meetings |

Nobody releases **gold labels for “should this utterance become a requirement?”** That is our dataset niche.

## Scope (keep it narrow)

Name (working): **ReqDecide** (or `exp-unjustified` as the seed split).

Each item is a **short stakeholder dialogue** plus a gold **Decision** per candidate statement — not a full SRS.

```
dialogue (5–20 turns)
  candidate statements[]
    gold_decision ∈ {ACCEPT, CLARIFY, REJECT,
                     DUPLICATE, CONFLICTING, AMBIGUOUS,
                     OUT-OF-SCOPE, UNJUSTIFIED, INSUFFICIENT-EVIDENCE}
    gold_rationale (one sentence)
    gold_requirement?  # only if ACCEPT
```

**v1 paper can score three super-classes** even if the schema has nine labels:

| Super-class | Includes | Why |
|-------------|----------|-----|
| ACCEPT | ACCEPT | Should enter the spec |
| HOLD | CLARIFY, AMBIGUOUS, INSUFFICIENT-EVIDENCE | Ask, do not write FR-xx yet |
| BLOCK | REJECT, OUT-OF-SCOPE, UNJUSTIFIED, DUPLICATE, CONFLICTING | Must not become a new FR as stated |

Nine-way F1 is a stretch until support is balanced. Reviewers will destroy a 9-class table with n=10. **Advertise 3-way + error analysis of subtypes.**

## Three layers (compete on all three if we can)

| Layer | Size target | Language | Purpose |
|-------|-------------|----------|---------|
| **L0 seed** `exp-unjustified-10` | 10 scripted adversarial chats | English (public) | Debug the critic; not the only evidence |
| **L1 public benchmark** | 40–80 dialogues, multiple domains | English | What GitHub ships; comparable like a mini-gym |
| **L2 industrial** | 8–12 anonymized company cases | Persian → English gloss | The “industrial evaluation” in the title |

L0 is necessary. L1 is what lets other papers cite us. L2 is what makes journals take us seriously. **Do not wait for L2 to build L0/L1.**

## What “scope” of the dataset should cover

Not random apps. Cover **decision types**, or the critic looks cherry-picked.

| Decision we want gold for | Planted example (public, fictional) |
|---------------------------|-------------------------------------|
| ACCEPT | “Staff must log in with the company SSO.” |
| CLARIFY / AMBIGUOUS | “Make it user-friendly.” |
| INSUFFICIENT-EVIDENCE | “Support 10 million concurrent users.” |
| UNJUSTIFIED | “Put the audit trail on a blockchain.” |
| OUT-OF-SCOPE | “Also ship a consumer TikTok clone.” |
| CONFLICTING | “No passwords” vs “SSO with OTP.” |
| DUPLICATE | Same upload feature stated twice |
| REJECT (infeasible / harmful) | “The AI analysis is never wrong; no human review.” |

Domains for L1 (public, not company IP): leave/HR, document portal, booking, internal dashboard — close enough to company work that transfer is plausible.

## How this competes (reader view)

- Vs OntoAgent: they maximize implicit coverage; we add **BLOCK/HOLD** labels they do not have. We can still *also* run IRE on Gym.
- Vs Vanilla LLM papers: same dialogues, three systems, decision F1.
- Vs Yin: we cannot share their industrial dump; we share a **task definition** others can extend.

## What not to put in the public set

Company system names, real volumes, personnel IDs, un-anonymized RFP text. Those stay in L2 or stay unpublished.

## Next concrete slice

`exp-unjustified-10` is L0. It must include mixed **valid** needs so the agent cannot win by rejecting everything (recall trap).
