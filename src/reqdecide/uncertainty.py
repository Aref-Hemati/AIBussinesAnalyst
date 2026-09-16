"""Interpretation entropy: separating an ambiguous statement from an unsure model.

A clarifying question is only worth a stakeholder's patience when the readings
of an utterance genuinely disagree. If every sample says the same thing and the
model is merely unsure, asking will not help; retrieving org rules will.

So we sample K independent readings, cluster them semantically, and take the
entropy of the cluster distribution. High entropy means ambiguity. Low entropy
with low self-reported confidence means missing knowledge.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Protocol, Sequence

from .schema import UncertaintySignal

INTERPRETATION_PROMPT = """You are reading one statement from a stakeholder during a requirements interview.

Conversation so far:
{context}

Stakeholder statement:
{utterance}

State, in one sentence, what concrete capability this person is asking the software to provide. Commit to a single reading even if the statement is vague; do not hedge and do not list alternatives.

Reply with JSON only:
{{"reading": "<one sentence>", "confidence": <number between 0 and 1>}}
"""

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Two similarity functions need two thresholds. Content-word overlap between
# genuine paraphrases sits far lower than embedding cosine does, so sharing one
# number would either split paraphrases or merge unrelated readings.
DEFAULT_JACCARD_THRESHOLD = 0.35
DEFAULT_EMBED_THRESHOLD = 0.82

_STOPWORDS = frozenset(
    """
    a an and are as at be by can could for from has have in into is it its may must not of on or
    should shall so that the their them there they this to use used user users want wants was we
    what when where which will with would you your system software application able allow allows
    """.split()
)


class GenerateFn(Protocol):
    """Minimal LLM interface, so no vendor SDK leaks into the method."""

    def __call__(self, prompt: str) -> str: ...


class EmbedFn(Protocol):
    def __call__(self, texts: Sequence[str]) -> Sequence[Sequence[float]]: ...


@dataclass(frozen=True)
class Interpretation:
    text: str
    confidence: Optional[float] = None


def prompt_hash(prompt: str = INTERPRETATION_PROMPT) -> str:
    """Record this with every decision so a result table stays reproducible."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def _tokens(text: str) -> frozenset[str]:
    return frozenset(t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS)


def jaccard(a: str, b: str) -> float:
    """Content-word overlap. The offline default when no embedder is supplied."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _parse_interpretation(raw: str) -> Interpretation:
    """Tolerate a model that wraps JSON in prose or fences."""
    text = raw.strip()
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            payload = json.loads(match.group(0))
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict):
            reading = str(payload.get("reading", "")).strip()
            confidence = payload.get("confidence")
            if isinstance(confidence, (int, float)):
                confidence = min(1.0, max(0.0, float(confidence)))
            else:
                confidence = None
            if reading:
                return Interpretation(text=reading, confidence=confidence)
    return Interpretation(text=text)


def sample_interpretations(
    utterance: str,
    generate: GenerateFn,
    k: int = 8,
    context: str = "",
    prompt_template: str = INTERPRETATION_PROMPT,
) -> list[Interpretation]:
    """Draw K independent readings. The caller's ``generate`` must be sampling,
    not greedy, or every draw is identical and entropy is meaningless."""
    if k < 1:
        raise ValueError("k must be at least 1")
    prompt = prompt_template.format(context=context or "(start of interview)", utterance=utterance)
    samples: list[Interpretation] = []
    for _ in range(k):
        samples.append(_parse_interpretation(generate(prompt)))
    return samples


def resolve_threshold(threshold: Optional[float], embed: Optional[EmbedFn]) -> float:
    if threshold is not None:
        return threshold
    return DEFAULT_EMBED_THRESHOLD if embed is not None else DEFAULT_JACCARD_THRESHOLD


def cluster_texts(
    texts: Sequence[str],
    threshold: Optional[float] = None,
    similarity: Optional[Callable[[str, str], float]] = None,
    embed: Optional[EmbedFn] = None,
) -> list[list[int]]:
    """Greedy single-link clustering into groups of equivalent readings.

    Deterministic and dependency-free, which matters more here than optimality:
    K is small, and the cluster count feeds a published metric.
    """
    if not texts:
        return []

    cutoff = resolve_threshold(threshold, embed)

    if embed is not None:
        vectors = list(embed(texts))

        def sim(i: int, j: int) -> float:
            return cosine(vectors[i], vectors[j])
    else:
        fn = similarity or jaccard

        def sim(i: int, j: int) -> float:
            return fn(texts[i], texts[j])

    clusters: list[list[int]] = []
    for idx in range(len(texts)):
        for cluster in clusters:
            if any(sim(idx, member) >= cutoff for member in cluster):
                cluster.append(idx)
                break
        else:
            clusters.append([idx])
    return clusters


def shannon_entropy(counts: Iterable[int]) -> float:
    """Entropy of a cluster distribution, in nats."""
    sizes = [c for c in counts if c > 0]
    total = sum(sizes)
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log(c / total) for c in sizes)


def estimate_uncertainty(
    interpretations: Sequence[Interpretation],
    threshold: Optional[float] = None,
    similarity: Optional[Callable[[str, str], float]] = None,
    embed: Optional[EmbedFn] = None,
) -> UncertaintySignal:
    """Turn K readings into the signal the admission rule consumes."""
    if not interpretations:
        raise ValueError("at least one interpretation is required")

    texts = [i.text for i in interpretations]
    clusters = cluster_texts(texts, threshold=threshold, similarity=similarity, embed=embed)
    sizes = sorted((len(c) for c in clusters), reverse=True)

    entropy = shannon_entropy(sizes)
    ceiling = math.log(len(texts)) if len(texts) > 1 else 0.0
    normalized = entropy / ceiling if ceiling > 0 else 0.0

    confidences = [i.confidence for i in interpretations if i.confidence is not None]
    mean_confidence = sum(confidences) / len(confidences) if confidences else None

    largest = max(clusters, key=len)
    dominant = texts[largest[0]]

    return UncertaintySignal(
        n_samples=len(texts),
        n_clusters=len(clusters),
        cluster_sizes=sizes,
        interpretation_entropy=entropy,
        normalized_entropy=min(1.0, normalized),
        mean_confidence=mean_confidence,
        dominant_interpretation=dominant,
        interpretations=texts,
    )


def measure(
    utterance: str,
    generate: GenerateFn,
    k: int = 8,
    context: str = "",
    threshold: Optional[float] = None,
    embed: Optional[EmbedFn] = None,
) -> UncertaintySignal:
    """Sample and score in one call."""
    samples = sample_interpretations(utterance, generate, k=k, context=context)
    return estimate_uncertainty(samples, threshold=threshold, embed=embed)


__all__ = [
    "DEFAULT_EMBED_THRESHOLD",
    "DEFAULT_JACCARD_THRESHOLD",
    "EmbedFn",
    "GenerateFn",
    "INTERPRETATION_PROMPT",
    "Interpretation",
    "resolve_threshold",
    "cluster_texts",
    "cosine",
    "estimate_uncertainty",
    "jaccard",
    "measure",
    "prompt_hash",
    "sample_interpretations",
    "shannon_entropy",
]
