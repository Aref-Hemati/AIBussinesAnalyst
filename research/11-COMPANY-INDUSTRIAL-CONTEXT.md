# Company / industrial context

This is the **field-study advantage**. Most LLM4RE papers are lab-only (Zadenoori ~7% field; Cheng ~1.3% production).

Do **not** paste secrets, personal data, or identifiable client names into public files.

Last updated: 2026-09-16.

## Why the company matters for the paper

We already have:

- Real non-technical stakeholders
- Real org hard rules (SSO, personnel codes, RTL/Persian UI, audit, Excel export, HR/finance IDs)
- Real artifacts: RFP files, certificate-of-origin style systems, leave-request forms
- A running BA prototype (Dify) with **version freeze** — rare in literature (management 6.8%)

The paper should be framed as:

> *An industrial evaluation of an agentic BA for conversational elicitation, critique, and validation*

not as:

> *We imported a Dify YAML.*

## What we can collect (after permission)

For each project/case:

| Field | Public? | Notes |
|-------|---------|-------|
| Anonymized dialogue | if approved | Replace org/product names |
| Decision gold labels | derived | Created by BA, not raw secrets |
| Counts (how many reqs, turns) | usually OK | |
| Org rule **types** | OK | “SSO required” not the IdP hostname |
| Screenshots of internal systems | **no** unless scrubbed |

## Ethics / publication checklist

- [ ] Written permission from employer
- [ ] Anonymization protocol (names, IDs, volumes, vendors)
- [ ] Stakeholder consent if identifiable quotes
- [ ] Separate **public example dialogues** (synthetic but realistic) so the artifact works without company data
- [ ] No credentials in git (already in `.gitignore`)

## Domain hooks for the critic (examples, not confidential)

These are the kinds of challenges a company BA must make — they should appear in `exp-unjustified-10`:

- Native Android vs responsive web already required by design system
- WhatsApp / Telegram vs official notification channel
- Blockchain vs existing audit log + RBAC
- “1 million users” vs current org size
- Public Google login vs SSO + 8-digit personnel code
- “AI must always be correct” vs human review responsibility

## How industrial cases map to RQs

| Company activity | RQ |
|------------------|----|
| Messy stakeholder chat in Persian | RQ1, RQ3 |
| Uploaded RFP vs org rules | RQ2, M4 |
| Freeze version for a sprint | RQ5 |
| HTML demo from draft | product only (mention as downstream, not a claim) |
