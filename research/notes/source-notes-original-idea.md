# Original idea notes (user research dump)

Captured 2026-09-16 from the project owner’s research conversation so the path is not lost in chat.

This is **source material**, not the paper. Normalized claims live in `00`–`06`.

## Product idea (kept)

User → conversational AI BA → analyze/clean/**challenge** requirements → structured spec → validation loop → freeze.

BA skills: understand, question, challenge, clarify, prioritize, detect contradiction/redundancy/scope creep/infeasibility, identify missing needs.

Output model: goals, actors, scope, FR/NFR, rules, constraints, stories, AC, trace, open questions.

Strongest intuition: **the AI should refuse to encode unjustified wishes** (blockchain, WhatsApp, 1M users) until business evidence exists.

## Academic framing they already converged on

- Do not title the science “I built an AI BA with an LLM.”
- Prefer: *Trustworthy Agentic RE through interactive elicitation, critique, and validation*
- Multi-agent = mechanism; critique/negotiation = contribution
- Company = experimental environment
- RQs they listed match our `01` (quality, unnecessary reqs, iterative questions, vs LLM/human, traceability)

## Papers they listed (now in `papers/`)

See `../papers/00-INDEX.md` and `../09-PAPERS-NEEDING-FULL-TEXT.md`.

## Architecture sketch they liked

Conversation → extraction → analysis (redundancy, conflict, necessity, completeness, feasibility, priority) → BA reasoning/negotiation → more questions or specification.

We **narrowed** that for v1: one Critic + Decision object first, specialists later ([04](../04-JOURNEY-AND-ACTION-PLAN.md)).
