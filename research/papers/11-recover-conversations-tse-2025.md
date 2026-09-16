# RECOVER — Requirements from stakeholders’ conversations (TSE 2025)

- **Cite:** G. Voria, F. Casillo, C. Gravino, G. Catolino, F. Palomba. *RECOVER: Toward Requirements Generation from Stakeholders’ Conversations*. IEEE TSE, 2025. [10.1109/tse.2025.3572056](https://doi.org/10.1109/tse.2025.3572056) arXiv:2411.19552
- **Read:** 2026-09-16
- **Role:** best **post-hoc extraction** paper; opposite timing to our live BA

## Method

Pipeline over conversation **turns**: detect requirement-relevant turns → generate system requirements with LLM → expert still needed to drop hallucinations.

Compared with engineers’ oracle and with ChatGPT-on-full-transcript.

## Results

### Turn classification

| | |
|--|--|
| Precision | **63%** (39 TP / 62 predicted) |
| Recall | **77%** (39/51 relevant) |

Recall-oriented by design (misses worse than extras).

### Turn-level generation vs wording

| Metric | Mean |
|--------|------|
| BLEU | **5.39%** |
| ROUGE | 38.53% |
| METEOR | 41.87% |

Wording diverges; semantics better than BLEU suggests.

### Whole-conversation vs expert oracle

| | RECOVER | ChatGPT (full convo) |
|--|---------|----------------------|
| BLEU | **78.82%** | lower |
| METEOR | **39.09%** | — |
| ROUGE | — | **43.96%** (higher overlap, weaker BLEU) |

Structured pipeline beat a single prompt on BLEU/METEOR.

Practitioners: useful **but** want post-validation.

In-vivo industrial transcripts: noisy, still applicable (see paper for details).

## Gap vs us

RECOVER assumes the conversation **already happened** (possibly with a human BA). We **are** the interviewer and we try to prevent bad requirements from entering the transcript.

If we ever extract from uploaded meeting notes, RECOVER is the baseline for that mode (Dify file path).

## Lesson

Do not make BLEU the headline. Their own turn-level BLEU is tiny. We will use decision F1 + human BA.
