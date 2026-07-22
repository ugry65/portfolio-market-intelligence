from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from datetime import datetime

from .models import Evidence, Signal


_WHITESPACE = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^a-z0-9 ]+")


def canonical_text(value: str) -> str:
    value = value.casefold().strip()
    value = _NON_WORD.sub(" ", value)
    return _WHITESPACE.sub(" ", value).strip()


def signal_fingerprint(signal: Signal) -> str:
    day = signal.occurred_at[:10]
    basis = "|".join(
        (
            canonical_text(signal.title),
            canonical_text(signal.category),
            day,
        )
    )
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:20]


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def deduplicate_signals(signals: tuple[Signal, ...]) -> tuple[Signal, ...]:
    """Merge same-day, same-category signals with the same canonical title.

    The strongest signal is retained. Evidence, tags, impacts, and data-quality
    notes are unioned without fabricating new conclusions.
    """

    groups: dict[str, list[Signal]] = {}
    for signal in signals:
        groups.setdefault(signal_fingerprint(signal), []).append(signal)

    merged: list[Signal] = []
    for fingerprint, group in groups.items():
        strongest = max(
            group,
            key=lambda item: (item.priority_score, item.confidence, _timestamp(item.detected_at)),
        )
        evidence_by_key: dict[tuple[str, str, str | None], Evidence] = {}
        for item in group:
            for evidence in item.evidence:
                evidence_by_key[(evidence.source_id, evidence.title, evidence.url)] = evidence

        impacts_by_ticker = {}
        for item in group:
            for impact in item.portfolio_impacts:
                current = impacts_by_ticker.get(impact.ticker)
                if current is None or impact.relevance > current.relevance:
                    impacts_by_ticker[impact.ticker] = impact

        merged.append(
            replace(
                strongest,
                signal_id=fingerprint,
                tags=tuple(sorted({tag for item in group for tag in item.tags})),
                evidence=tuple(evidence_by_key.values()),
                portfolio_impacts=tuple(
                    sorted(impacts_by_ticker.values(), key=lambda item: (-item.relevance, item.ticker))
                ),
                data_quality=tuple(
                    sorted({note for item in group for note in item.data_quality})
                ),
            )
        )

    return tuple(sorted(merged, key=lambda item: (-item.priority_score, item.occurred_at)))
