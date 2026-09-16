# Virtual Software Engineer Agent (GPT-4.1 + CoT) — ICCCI 2025

- **Cite:** *Virtual Software Engineer Agent for Product Requirement Engineering and Management Using GPT-4.1 and CoT*. IEEE ICCCI 2025. [10.1109/iccci65070.2025.11158389](https://doi.org/10.1109/iccci65070.2025.11158389)
- **Also:** NYCU academic hub record
- **Read:** **ABSTRACT ONLY** (paywall). See [`../09-PAPERS-NEEDING-FULL-TEXT.md`](../09-PAPERS-NEEDING-FULL-TEXT.md)
- **Role:** closest *conversational product-requirement agent* in the user’s original list

## What the abstract says

Capturing complete user requirements is hampered by ambiguity and labor cost. They build a **Virtual Software Engineer Agent** that talks to users and incrementally derives **structured software requirements** from unstructured input, using **GPT-4.1** and **Chain-of-Thought**.

Evaluation: compare agent output to **expert-written requirement documents** from a **Bangkok software firm**, using **BLEU, METEOR, ROUGE-L**.

Claim: potential to automate elicitation while keeping fidelity to user intent.

## Pipeline (from abstract)

```
User → Conversation → LLM Agent → Requirement extraction
     → Requirement engineering → Structured requirements
```

## Why this is not yet our paper

Linguistic overlap with an expert FRD does **not** measure:

- whether unjustified features were filtered
- whether the agent challenged the user
- traceability
- industrial process (freeze, org rules)

RECOVER already showed turn-level BLEU can be ~5% while still being useful. If this paper’s main tables are BLEU-only, we cite it as an incremental conversational extractor and **do not** compete on BLEU.

## Need from full text

- [ ] Exact BLEU/METEOR/ROUGE numbers (overall and per section)
- [ ] Number of projects / pages / participants
- [ ] Prompt / CoT template
- [ ] Whether the agent asks follow-ups or only converts
- [ ] Human evaluation besides n-gram overlap
- [ ] Limitations / error analysis
- [ ] Any reject/challenge behavior (likely none)

**Please paste the PDF.** Until then, cite cautiously: “a conversational GPT-4.1 agent evaluated with n-gram overlap against expert documents.”
