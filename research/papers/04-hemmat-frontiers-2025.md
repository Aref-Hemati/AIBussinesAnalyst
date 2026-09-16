# Hemmat et al. — Research directions for LLMs in software requirement engineering

- **Cite:** A. Hemmat, M. Sharbaf, S. Kolahdouz-Rahimi, K. Lano, S. Y. Tehrani. *Research directions for using LLM in software requirement engineering: a systematic review*. Frontiers in Computer Science, 7:1519437, 2025. [10.3389/fcomp.2025.1519437](https://doi.org/10.3389/fcomp.2025.1519437)
- **Read:** 2026-09-16 (open HTML)
- **Our use:** future-work checklist; human-in-the-loop hybrid as recommended direction

## Scope

Systematic mapping of NLP/LLM applications in SRE: model types, I/O, tasks, tuning, prompting, challenges.

## Directions they highlight

1. Better evaluation metrics and benchmarks
2. Domain-specific fine-tuning
3. Advanced prompt engineering
4. Integration with existing RE tools/workflows
5. Reliability, consistency, hallucination control
6. **Hybrid / human-in-the-loop** with traditional tools

## Challenges

Domain knowledge gaps; incomplete/inconsistent outputs; context window limits; **validation difficulty**; formatting/structure errors.

## Our stance

We follow (1), (4), (5), (6) in v1. We **defer** (2) fine-tuning until we have labeled Decision data from industrial cases.

Human-in-the-loop for us is not “the BA edits the FRD at the end.” It is **confirmation of decisions and freeze** (SMS 8% gap).
