from __future__ import annotations

from dataclasses import replace

from .adapters import SourceAdapter
from .deduplication import deduplicate_signals
from .engines import AlertDecision, AlertEngine, PortfolioImpactEngine, PortfolioPosition
from .models import Signal, SourceStatus


class IntelligencePipeline:
    def __init__(
        self,
        *,
        impact_engine: PortfolioImpactEngine | None = None,
        alert_engine: AlertEngine | None = None,
    ) -> None:
        self.impact_engine = impact_engine or PortfolioImpactEngine()
        self.alert_engine = alert_engine or AlertEngine()

    def run(
        self,
        adapters: tuple[SourceAdapter, ...],
        positions: tuple[PortfolioPosition, ...],
    ) -> tuple[tuple[Signal, ...], tuple[SourceStatus, ...], dict[str, AlertDecision]]:
        collected: list[Signal] = []
        statuses: list[SourceStatus] = []

        for adapter in adapters:
            try:
                result = adapter.fetch()
            except Exception as exc:  # preserve source failure instead of hiding it
                statuses.append(
                    SourceStatus(
                        source_id=adapter.source_id,
                        status="failed",
                        message=f"{type(exc).__name__}: {exc}",
                    )
                )
                continue

            statuses.append(result.status)
            for signal in result.signals:
                impacts = signal.portfolio_impacts or self.impact_engine.evaluate(
                    title=signal.title,
                    summary=signal.summary,
                    tags=signal.tags,
                    positions=positions,
                )
                collected.append(replace(signal, portfolio_impacts=impacts))

        signals = deduplicate_signals(tuple(collected))
        decisions = {signal.signal_id: self.alert_engine.classify(signal) for signal in signals}
        return signals, tuple(statuses), decisions
