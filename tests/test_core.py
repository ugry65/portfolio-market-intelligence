import json

import pytest

from portfolio_intelligence.engines import AlertEngine, PortfolioImpactEngine, PortfolioPosition
from portfolio_intelligence.exporter import build_payload
from portfolio_intelligence.models import Signal, SourceStatus


def test_signal_validation() -> None:
    with pytest.raises(ValueError):
        Signal(
            signal_id="bad",
            title="Bad",
            summary="Bad",
            category="test",
            severity="info",
            confidence=1.1,
            freshness=1.0,
            occurred_at="2026-01-01T00:00:00+00:00",
        )


def test_direct_portfolio_match() -> None:
    engine = PortfolioImpactEngine()
    impacts = engine.evaluate(
        title="ASML publishes results",
        summary="Company update",
        tags=(),
        positions=(PortfolioPosition("ASMF.F", "ASML Holding", 0.04, aliases=("ASML",)),),
    )
    assert impacts[0].ticker == "ASMF.F"
    assert impacts[0].direct is True
    assert impacts[0].relevance == 1.0


def test_alert_and_export_are_serializable() -> None:
    signal = Signal(
        signal_id="s1",
        title="Test",
        summary="Test",
        category="macro",
        severity="warning",
        confidence=0.9,
        freshness=0.9,
        occurred_at="2026-01-01T00:00:00+00:00",
    )
    decision = AlertEngine().classify(signal)
    assert decision.status in {"alert", "watch", "information"}
    payload = build_payload((signal,), (SourceStatus("test", "ok"),))
    json.dumps(payload)
    assert payload["schema_version"] == "0.1.0"
