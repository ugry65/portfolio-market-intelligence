from __future__ import annotations

from dataclasses import dataclass

from .models import PortfolioImpact, Signal


@dataclass(frozen=True)
class PortfolioPosition:
    ticker: str
    name: str
    weight: float
    aliases: tuple[str, ...] = ()
    themes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.weight <= 1:
            raise ValueError("weight must be between 0 and 1")


class PortfolioImpactEngine:
    """Deterministic first-pass matching; no AI inference and no invented exposure."""

    def evaluate(
        self,
        *,
        title: str,
        summary: str,
        tags: tuple[str, ...],
        positions: tuple[PortfolioPosition, ...],
    ) -> tuple[PortfolioImpact, ...]:
        haystack = " ".join((title, summary, *tags)).casefold()
        impacts: list[PortfolioImpact] = []

        for position in positions:
            identifiers = (position.ticker, position.name, *position.aliases)
            direct_match = any(identifier.casefold() in haystack for identifier in identifiers)
            matched_themes = [theme for theme in position.themes if theme.casefold() in haystack]

            if not direct_match and not matched_themes:
                continue

            relevance = 1.0 if direct_match else min(0.75, 0.35 + 0.1 * len(matched_themes))
            rationale = (
                "Direct instrument/company match."
                if direct_match
                else f"Theme match: {', '.join(matched_themes)}."
            )
            impacts.append(
                PortfolioImpact(
                    ticker=position.ticker,
                    relevance=relevance,
                    direction="neutral",
                    rationale=rationale,
                    estimated_weight=position.weight,
                    direct=direct_match,
                )
            )

        return tuple(sorted(impacts, key=lambda item: (-item.relevance, -float(item.estimated_weight or 0))))


@dataclass(frozen=True)
class AlertDecision:
    status: str
    reason: str
    priority_score: float


class AlertEngine:
    def classify(self, signal: Signal) -> AlertDecision:
        score = signal.priority_score
        if signal.severity == "critical" and score >= 0.75:
            return AlertDecision("alert", "Critical, high-priority portfolio signal.", score)
        if score >= 0.65:
            return AlertDecision("alert", "Priority threshold reached.", score)
        if score >= 0.45:
            return AlertDecision("watch", "Monitor; evidence is relevant but not urgent.", score)
        return AlertDecision("information", "No immediate portfolio action indicated.", score)
