# Automated Software Requirements Elicitation: A Systematic Mapping Study (2026)

- **Cite:** *Automated Software Requirements Elicitation: A Systematic Mapping Study*. Information (MDPI), 2026, 17(8):777. https://www.mdpi.com/2078-2489/17/8/777
- **OSF:** https://doi.org/10.17605/osf.io/fzmbw
- **Read:** 2026-09-16 **abstract / OSF summary only** — full PDF timed out. **Treat 51/23/8 as reported in secondary summaries; confirm on PDF.**
- **Our use:** the funnel that justifies critique + validation as the research gap

## Corpus

74 peer-reviewed studies, 2021–2025, PRISMA, five databases. Classified by AI technique, textual source, elicitation activity, domain.

Two source families of similar size: (1) user feedback + agile artifacts, (2) formal documentation.

## Headline results

| Automation depth | Share of approaches |
|------------------|---------------------|
| Identify requirements | mature; often F1 ≥ 0.8 |
| **Structure** identified requirements | **~51%** |
| **Consolidate** | **~23%** |
| **Engineer stakeholder validation into the loop** | **~8%** |

Other:

- Fine-tuned encoder models still outperform larger generative models **on pure identification**
- LLMs help on long regulatory text, multilingual feedback, structured outputs
- Custom datasets **77%**
- Industrial validation **14%**
- NFR coverage skewed

## Interpretation for our paper

A basic system that maps

`“customers upload documents” → FR-01 upload`

is **identification** — the saturated part of the funnel.

Our BA is aimed at the thin end: **structure + consolidate + validate**, with an extra layer the SMS barely sees: **refuse / negotiate**.

## TODO when PDF arrives

- [ ] Copy exact table of elicitation activities
- [ ] Save funnel figure under `../figures/baselines/`
- [ ] Confirm 51/23/8 wording is theirs, not a paraphrase
- [ ] List the 8% validation papers — we must cite and differentiate
