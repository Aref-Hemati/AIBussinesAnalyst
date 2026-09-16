# ReqElicitGym — Evaluation environment for conversational elicitation

- **Cite:** Jin et al. *ReqElicitGym: An Evaluation Environment for Interview Competence in Conversational Requirements Elicitation*. arXiv:2602.18306
- **Read:** 2026-09-16 (PDF extract)
- **Our use:** **public benchmark** so we are comparable to OntoAgent/LLMREI without waiting for company data

## Design

- **101** elicitation scenarios, **10** application domains (website-focused in OntoAgent use)
- Each item: Initial Req (underspecified) vs Final Req; gap = **Implicit Req**
- **Oracle user:** GPT-5.1, answers grounded in implicit requirements
- **Task evaluator:** LLM-as-judge, turn-level implicit-requirement capture
- Metrics include **Implicit Requirement Elicitation Rate (IRE)** and process-aware stats (OntoAgent adds TKQR)

## Validation of the gym itself

33 real interview dialogues, 555 turns:

| Component | Cohen’s κ vs humans |
|-----------|---------------------|
| Oracle user disclosure behavior | **0.73** |
| Task evaluator vs experts | **0.72** |

Substantial agreement (Landis & Koch).

## How we should use it

1. Implement a Gym adapter in `eval/`
2. Run Vanilla / Prompted / Agentic with max turns = 20 (OntoAgent protocol)
3. Report IRE, TKQR, **plus** our Decision metrics (Gym may not label UNJUSTIFIED — we may need to **inject** unjustified distractors into initial reqs)

Injection idea: append “also use blockchain and support 1 million users” to Initial Req; gold = those are NOT implicit needs unless in Final Req. That turns Gym into an RQ2 test.

## Caveat

Simulated stakeholders are calmer and more consistent than real ones (RECOVER’s noisy meetings). D3 industrial cases remain mandatory for the journal story.
