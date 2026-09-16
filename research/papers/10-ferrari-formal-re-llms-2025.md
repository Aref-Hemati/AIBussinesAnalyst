# Ferrari & Spoletini — Formal RE and LLMs: a two-way roadmap

- **Cite:** A. Ferrari, P. Spoletini. *Formal requirements engineering and large language models: A two-way roadmap*. Information and Software Technology, 181:107697, 2025. [10.1016/j.infsof.2025.107697](https://doi.org/10.1016/j.infsof.2025.107697)
- **PDF:** CNR IRIS (read 2026-09-16)
- **Type:** vision / roadmap, not an empirical bake-off
- **Our use:** v2 and discussion; lightweight “formal” = schema + constraints in v1

## Problem

LLMs do RE tasks well enough to be tempting, but correctness, fairness, trustworthiness are not guaranteed. Formal methods (FMs) have the opposite problem: trustworthy but unusable for most teams.

## Two roadmaps

1. **LLMs → make FMs usable:** help write formal specs, explain model-checker output, ACE-like controlled English, iterative prompting for models (they survey GPT for GRL, class diagrams, sequence diagrams — often plausible but wrong, worse with smells).
2. **FMs → make LLM-RE trustworthy:** check generated requirements/models/code against properties; constrain generation.

They extend their REFSQ 2024 vision paper.

Background includes LLM **agents** (tools, memory, multi-step) as the way complex tasks get done — relevant to our orchestrator.

## Examples in the paper

Handshake protocol: NL requirements (integrity, order, flow control) → PROMELA → Spin. Shows FM payoff and expertise barrier.

LLM side: generation can look right and still violate requirements, especially with ambiguity.

## What we take for v1 (without becoming an FM paper)

Ferrari’s trust problem is exactly **sycophantic FR generation**.

Our cheap end of roadmap 2:

- JSON schema (no FR without ACCEPT id)
- Org-rule predicates (“SSO required ⇒ reject public-only Google login”)
- Explicit contradictions stored as CONFLICTING

v2 (parked): AC → test skeletons; optional LTL for critical NFRs; Alloy for scope invariants.

**Do not** promise model checking in the first abstract.
