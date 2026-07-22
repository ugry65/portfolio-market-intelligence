from __future__ import annotations

import json
from pathlib import Path

from portfolio_intelligence.adapters import SourceAdapter, StaticSignalAdapter
from portfolio_intelligence.deduplication import deduplicate_signals
from portfolio_intelligence.engines import PortfolioPosition
from portfolio_intelligence.models import Evidence, Signal
from portfolio_intelligence.pipeline import IntelligencePipeline
from portfolio_intelligence.portfolio_loader import load_portfolio_csv, load_portfolio_json


def make_signal(signal_id: str, title: str, confidence: float = 0.8) -> Signal:
    return Signal(
        signal_id=signal_id,
        title=title,
        summary="ASML semiconductor outlook changed.",
        category="company",
        severity="warning",
        confidence=confidence,
        freshness=0.9,
        occurred_at="2026-07-22T08:00:00+00:00",
        tags=("semiconductor",),
        evidence=(Evidence(source_id=signal_id, title=title),),
    )


def test_json_loader_accepts_percent_weights(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.json"
    path.write_text(
        json.dumps(
            {
                "positions": [
                    {"ticker": "ASML", "name": "ASML Holding", "weight": 60},
                    {"ticker": "MSFT", "name": "Microsoft", "weight": 40},
                ]
            }
        ),
        encoding="utf-8",
    )
    result = load_portfolio_json(path)
    assert [position.weight for position in result.positions] == [0.6, 0.4]
    assert result.warnings == ()


def test_csv_loader_reports_weight_gap(tmp_path: Path) -> None:
    path = tmp_path / "portfolio.csv"
    path.write_text(
        "ticker,name,weight,aliases,themes\nASML,ASML Holding,0.25,ASML NV,semiconductor|AI\n",
        encoding="utf-8",
    )
    result = load_portfolio_csv(path)
    assert result.positions[0].themes == ("semiconductor", "AI")
    assert "not approximately 1.0" in result.warnings[0]


def test_deduplication_keeps_strongest_and_unions_evidence() -> None:
    signals = (
        make_signal("a", "ASML outlook weakens", 0.7),
        make_signal("b", "ASML outlook weakens!", 0.9),
    )
    merged = deduplicate_signals(signals)
    assert len(merged) == 1
    assert merged[0].confidence == 0.9
    assert len(merged[0].evidence) == 2


def test_pipeline_enriches_and_classifies() -> None:
    positions = (
        PortfolioPosition(
            ticker="ASML",
            name="ASML Holding",
            weight=0.12,
            aliases=("ASML NV",),
            themes=("semiconductor",),
        ),
    )
    adapter = StaticSignalAdapter("manual", (make_signal("a", "ASML outlook weakens"),))
    signals, statuses, decisions = IntelligencePipeline().run((adapter,), positions)
    assert statuses[0].status == "ok"
    assert signals[0].portfolio_impacts[0].ticker == "ASML"
    assert decisions[signals[0].signal_id].status in {"watch", "alert"}


class FailingAdapter(SourceAdapter):
    source_id = "broken"

    def fetch(self):
        raise RuntimeError("source unavailable")


def test_pipeline_preserves_adapter_failure() -> None:
    signals, statuses, decisions = IntelligencePipeline().run((FailingAdapter(),), ())
    assert signals == ()
    assert decisions == {}
    assert statuses[0].status == "failed"
    assert "source unavailable" in (statuses[0].message or "")
