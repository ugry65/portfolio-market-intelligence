from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

Severity = Literal["info", "watch", "warning", "critical"]
Direction = Literal["positive", "negative", "mixed", "neutral"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Evidence:
    source_id: str
    title: str
    url: str | None = None
    published_at: str | None = None
    excerpt: str | None = None
    source_type: str = "unknown"


@dataclass(frozen=True)
class SourceStatus:
    source_id: str
    status: Literal["ok", "degraded", "failed", "disabled"]
    checked_at: str = field(default_factory=utc_now_iso)
    message: str | None = None
    item_count: int = 0


@dataclass(frozen=True)
class PortfolioImpact:
    ticker: str
    relevance: float
    direction: Direction
    rationale: str
    estimated_weight: float | None = None
    direct: bool = True

    def __post_init__(self) -> None:
        if not 0 <= self.relevance <= 1:
            raise ValueError("relevance must be between 0 and 1")
        if self.estimated_weight is not None and not 0 <= self.estimated_weight <= 1:
            raise ValueError("estimated_weight must be between 0 and 1")


@dataclass(frozen=True)
class Signal:
    signal_id: str
    title: str
    summary: str
    category: str
    severity: Severity
    confidence: float
    freshness: float
    occurred_at: str
    detected_at: str = field(default_factory=utc_now_iso)
    tags: tuple[str, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    portfolio_impacts: tuple[PortfolioImpact, ...] = ()
    data_quality: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (("confidence", self.confidence), ("freshness", self.freshness)):
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1")

    @property
    def priority_score(self) -> float:
        severity_weight = {"info": 0.25, "watch": 0.5, "warning": 0.75, "critical": 1.0}
        portfolio_relevance = max(
            (impact.relevance for impact in self.portfolio_impacts), default=0.0
        )
        score = (
            severity_weight[self.severity] * 0.35
            + self.confidence * 0.25
            + self.freshness * 0.15
            + portfolio_relevance * 0.25
        )
        return round(score, 4)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["priority_score"] = self.priority_score
        return payload
