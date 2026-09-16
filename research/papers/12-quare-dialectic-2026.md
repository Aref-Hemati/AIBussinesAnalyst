# QUARE — Quality-Aware RE via multi-agent dialectic negotiation (RE 2026)

- **Cite:** *QUARE: Quality-Aware Requirements Engineering through Multi-Agent Dialectic Negotiation*. RE 2026 Research Papers. https://conf.researchr.org/details/RE-2026/RE-2026-Research-Papers/19/...
- **Read:** **abstract only**
- **Role:** strongest 2026 *protocol* paper for multi-agent RE; we steal dialectic, not “more requirements”

## Claimed method

Five specialist agents — Safety, Efficiency, Green, Trustworthiness, Responsibility — plus orchestrator.

Dialectical loop: proposal → critique → synthesis. Then KAOS goal models with topology validation + RAG against industry standards.

## Claimed results

| Metric | Value |
|--------|-------|
| Compliance coverage | **98.2%** (+105% vs both baselines) |
| Semantic preservation | **94.9%** (+2.3 pp vs best baseline) |
| Verifiability | **4.96 / 5.0** |
| Volume | **25–43% more requirements** than other multi-agent RE frameworks |

Cases: MARE, iReDev benchmarks + industrial autonomous-driving spec.

Message: **architecture and explicit interaction protocol beat model scale.**

## How this interacts with our claim

- **Agree:** protocol > “just GPT.”
- **Disagree as success metric:** “more requirements” can be scope creep. Our H2 is precision / justified-ness.
- **Reuse:** one-round dialectic when CONFLICTING (keep A / keep B / synthesize).
- **Difference:** they negotiate *quality attributes*; we negotiate *necessity and scope* with the stakeholder, not only among agents.

Need full text for baselines, prompts, and whether stakeholders sit in the loop.
