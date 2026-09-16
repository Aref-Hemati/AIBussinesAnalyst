# Related works (synthesis)

This is the **paper-facing** related-work map. Per-paper detail lives in [`papers/`](papers/00-INDEX.md). Update this file when a new paper changes the gap.

Last literature sweep: 2026-09-16.

## How to read this map

We group work by **capability**, not by year. For each group: what they achieved, headline numbers, and the leftover that our BA must address.

```
Extraction ──► Generation ──► Quality check ──► Interview ──► Multi-agent process
     ▲                                                              │
     └──────── still missing: NECESSITY CRITIQUE + VALIDATED SPEC ─┘
```

## Surveys that define the gap

### Zadenoori et al., 2025 — LLM4RE SLR (74 studies, 2023–2024)

- [arXiv:2509.11446](https://arxiv.org/abs/2509.11446) — notes in `papers/01`; raw HTML deleted after extract
- LLM4RE shifted from NLP4RE’s defect detection/classification toward **elicitation and validation** (15 studies, **20%** each)
- Prompting: zero-shot 44%, few-shot 29%, **RAG 6%**, **interactive prompting 5%**
- GPT-family ~90%; **lab experiments 75%**, field studies **7%**
- Their task×method bubble chart: **requirements elicitation field studies = 1** (lab = 11). Validation field studies = 1 (lab = 12).
- 61% share code/prompts; only **16%** share datasets
- Tools exist (21) but most work is out-of-the-box, not end-to-end workflows

**Use in our paper:** “interactive elicitation in the field is almost absent.” Cite `zadenoori-fig-eval-methods.png`.

### Cheng et al., 2026 — GenAI for RE SLR (238 papers, 2019–May 2025)

- SPE [10.1002/spe.70029](https://doi.org/10.1002/spe.70029) / [arXiv:2409.06741](https://arxiv.org/abs/2409.06741)
- RE phase share: analysis **30.0%**, elicitation **22.1%**, specification **22.1%**, validation **19.0%**, **management 6.8%**
- GPT models **67.3%** of applications
- Challenge triad: reproducibility 66.8%, hallucinations 63.4%, interpretability 57.1% (co-occur ~35%)
- **90.3% early-stage**, 8.4% prototype, **1.3% production**
- Tools released 23.9%; many datasets used but not shared

**Use:** industrial evaluation + requirement management/versioning are rare. Our company freeze/versioning is a contribution hook.

### Automated Software Requirements Elicitation SMS, 2026 (74 studies, 2021–2025)

- MDPI Information 17(8):777 — [mdpi.com/2078-2489/17/8/777](https://www.mdpi.com/2078-2489/17/8/777)
- AI is good at **identifying** requirements (often F1 ≥ 0.8)
- Automation depth funnel: **51% structure**, **23% consolidate**, **8% stakeholder validation**
- 77% custom datasets; **14%** industrial validation
- Fine-tuned encoders still beat larger generative models on pure identification; LLMs win on long/multilingual/structured generation

**Use:** this is the single best quantitative justification for our validation/critique loop.

Full PDF was not retrieved in this pass — see [09-PAPERS-NEEDING-FULL-TEXT.md](09-PAPERS-NEEDING-FULL-TEXT.md).

### Hemmat et al., 2025 — Frontiers systematic review

- [10.3389/fcomp.2025.1519437](https://doi.org/10.3389/fcomp.2025.1519437)
- Directions: better metrics/benchmarks, domain fine-tuning, prompt engineering, tool integration, reliability, **human-in-the-loop hybrids**
- Challenges: domain gaps, incomplete/inconsistent outputs, validation difficulty, hallucinations

**Use:** our critic is a structured human-in-the-loop hybrid (AI proposes decisions, stakeholder/BA confirms).

## Closest systems (must compare in the paper)

### 1. Yin, Cui, Luan 2026 — LLM+Agent for heterogeneous user demands

- [10.3233/FAIA251514](https://doi.org/10.3233/FAIA251514)
- Four-level agents: standardize → parse → **conflict mediation** → **priority**
- Dynamic RAG (ChromaDB + RIND uncertainty trigger, θ=0.6)
- Smart-home / SaaS industrial data
- **Precision 80.4%, recall 79.7%, F1 0.89**; **22 redundant proposals**, contribution rate **17.3%** (~18% in conclusion)
- Expert panel n=12 vs 95 key requirements; system proposed 105 to-be-reviewed
- Priority formula: `0.6*legal + 0.3*user-feedback-share + 0.1*mandatory`

**Leftover:** batch processing of existing feedback, not a live BA that challenges a stakeholder in the moment. No ACCEPT/REJECT of *requested* features for lack of business value during dialogue.

**We borrow:** conflict agent, priority evidence, RAG grounding, expert-voting evaluation protocol.

### 2. Virtual Software Engineer Agent — GPT-4.1 + CoT (ICCCI 2025)

- [10.1109/iccci65070.2025.11158389](https://doi.org/10.1109/iccci65070.2025.11158389)
- Conversational agent incrementally derives structured requirements
- Evaluation: BLEU / METEOR / ROUGE-L vs expert docs at a Bangkok firm

**Leftover:** linguistic similarity ≠ BA quality. Full numeric tables not accessible (paywall). **Please paste PDF text** — [09](09-PAPERS-NEEDING-FULL-TEXT.md).

**We borrow:** conversational incremental derivation; we must **not** use BLEU as our primary metric (RECOVER already showed BLEU is a poor turn-level signal).

### 3. OntoAgent — From Chat to Interview (2026)

- [arXiv:2605.05828](https://www.alphaxiv.org/abs/2605.05828)
- Experience ontology (Aspect → Dimension → Slot); operations ParseUser, ScoreOnto, ReRankOnto, GatePrune
- ReqElicitGym: 101 website scenarios
- IRE **0.69** (+33% vs mistake-guided 0.52); TKQR **0.59** (+21% vs LLMREI-short 0.49)
- Style IRE: baselines ≤0.17, OntoAgent **0.55**
- Human Likert (n=6): effectiveness 5.87, efficiency 5.79, adaptability 6.12
- Ablation: ontology is the largest jump (IRE 0.13 → 0.41)

Figures saved: `figures/baselines/ontoagent-fig1.png` (architecture), `ontoagent-fig2.png` (induction-size curve), `ontoagent-fig3.png` (turn-level IRE).

**Leftover:** asks *missing* slots, does not reject unjustified slots. Website domain. Simulated oracle user.

**We borrow:** slot ontology + TKQR/IRE reporting. **We add:** necessity critic before slot filling.

### 4. LLMREI (Korn et al., RE’25) — interview chatbots

Referenced by OntoAgent and visible in our saved figures.

- Short vs long interview prompts
- OntoAgent numbers: LLMREI-short IRE 0.39 / TKQR 0.49; long IRE 0.38 / TKQR 0.09 (long is inefficient)
- `llmrei-fig4.png`: short prompt slightly higher elicited-recall median than long; partial-elicitation remains low

**Leftover:** free-form chat; redundant/generic early questions (OntoAgent’s motivation figure).

### 5. Quattrocchi, Pasquale, Spoletini, Baresi — TSE 2026

- IEEE TSE 52(5):1773–1790, [10.1109/TSE.2026.3670612](https://doi.org/10.1109/TSE.2026.3670612) / [arXiv:2507.15157](https://arxiv.org/html/2507.15157v1)
- 10 LLMs emulate analyst+customer interviews; **13,958** user stories
- Coverage vs GT (c=0.8): Claude 3 Sonnet/Opus **96.23%**; students **52.83%**; all LLMs together 98.11%
- Diversity: students **98.58%** vs best LLM Grok **74.74%**, Claude 3 Sonnet **44.23%**
- Quality assessment: Claude 3 Opus **κ=0.87** with codebook (beats inter-human ~0.74–0.78)
- Rejection rate (score=1 on any QUS criterion): GT **9.43%**, students **14.64%**, Claude 3 Opus **16.55%** — LLMs fail acceptance more often
- Defects: conjunctions, low feature specificity, weak rationale

**Leftover:** generation quality ≠ BA critique. Simulated customer. No industrial org constraints.

**We borrow:** QUS + codebook for the Critic; never claim “LLM US are as good as experts” without the diversity/AC caveat.

### 6. RECOVER — TSE 2025 (Voria, Palomba et al.)

- [10.1109/tse.2025.3572056](https://doi.org/10.1109/tse.2025.3572056) / [arXiv:2411.19552](https://arxiv.org/abs/2411.19552)
- Extract requirements from **existing** conversation turns
- Classifier: precision **63%**, recall **77%** (recall-oriented)
- Turn-level: BLEU mean 5.39%, ROUGE 38.53%, METEOR 41.87%
- Whole conversation vs expert: BLEU **78.82%**, METEOR 39.09%; ChatGPT higher ROUGE (43.96%) but worse BLEU
- Practitioners still want expert post-validation (hallucinations)

**Leftover:** not interactive; does not prevent bad requirements from being uttered into existence.

### 7. QUARE — RE 2026 (dialectic negotiation)

- [RE 2026 paper 19](https://conf.researchr.org/details/RE-2026/RE-2026-Research-Papers/19/QUARE-Quality-Aware-Requirements-Engineering-through-Multi-Agent-Dialectic-Negotiati)
- 5 quality agents (Safety, Efficiency, Green, Trustworthiness, Responsibility) + orchestrator
- 98.2% compliance coverage (+105% vs baselines), 94.9% semantic preservation, verifiability 4.96/5
- Generates 25–43% more requirements than other multi-agent RE frameworks
- Claim: architecture/protocol > model scale

**Leftover:** NFR/quality-attribute conflicts, not “do we need WhatsApp?” Full text not retrieved.

**We borrow:** explicit critique protocol; **we do not** treat “more requirements” as success (our H2 is precision).

### 8. MARARE — meetings to artifacts (2026)

- [10.1145/3786167.3788405](https://doi.org/10.1145/3786167.3788405)
- Real-time: one agent talks, others extract/verify
- 5 meetings (5–8 min): coverage 80.0±11.2%, similarity 0.86±0.05, hallucination 14.3±6.2%

**Leftover:** meeting capture, not BA challenge. Tiny sample.

## Other relevant strands

| Paper | Role for us |
|-------|-------------|
| Ferrari & Spoletini, IST 2025, *Formal RE and LLMs: a two-way roadmap* | v2: use lightweight formal/constrained checks to bound LLM BA; not v1 novelty |
| Ellsel & Stark, Procedia CIRP 2025, *Advancing RE with LLMs* | GPT-4o closest to humans on quality scoring — supports a Quality Agent |
| ReqElicitGym (Jin et al., arXiv:2602.18306) | **Use as public benchmark** alongside industrial cases; 101 scenarios, oracle κ=0.73, evaluator κ=0.72 |
| ReqNet (2025) | Extraction from unstructured documents — baseline for file/RFP path |
| Görer & Aydemir, RE 2024 | Interview **script** generation — preparation, not live critique |
| Ronanki et al., 2023 | ChatGPT assists elicitation — early prompted-BA baseline |
| Modern Analyst “BA Guide to Agentic AI Requirements” (practitioner) | Cite as practitioner framing, not academic evidence |

RE 2026 papers we should add when full text is available:

- *Under Pressure: Navigating Human Factors in AI-Supported Requirements Validation*
- *Debugging Requirements Interview Scripts: A Framework for Quality Assessment*

## Difference table (for the paper)

| Capability | Vanilla LLM | Prompted BA | Yin 2026 | OntoAgent | RECOVER | **Our target** |
|-----------|-------------|-------------|----------|-----------|---------|----------------|
| Extract from text | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| Live interview | weak | medium | ✗ | ✓ | ✗ (offline) | ✓ |
| Slot completeness | weak | weak | medium | **strong** | medium | strong |
| Reject unjustified req | ✗ | weak | partial (conflict) | ✗ | ✗ | **core** |
| Org hard rules / RAG | ✗ | optional | ✓ | domain ontology | ✗ | ✓ (company) |
| Stakeholder validation loop | ✗ | informal | expert vote after | simulated | expert after | **in-loop** |
| Trace + version freeze | ✗ | ✗ | PRD link field | ✗ | ✗ | ✓ |
| Industrial field study | rare | rare | SaaS batch | small human n=6 | in-vivo transcripts | **target** |

## Related-work writing rule

When drafting the paper:

1. Open with the two SLRs + the 51/23/8 funnel.
2. Then closest systems (Yin, OntoAgent, Virtual SE, TSE user stories, RECOVER).
3. Then: **none of them treat “should this be a requirement?” as a first-class, measured decision.**
4. Close with industrial rarity (1.3% production, 7% field).
