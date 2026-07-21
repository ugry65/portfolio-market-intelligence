from portfolio_intelligence.engines import PortfolioImpactEngine, PortfolioPosition
from portfolio_intelligence.exporter import export_json
from portfolio_intelligence.models import Evidence, Signal, SourceStatus

positions = (
    PortfolioPosition("ASMF.F", "ASML Holding", 0.04, aliases=("ASML",), themes=("semiconductor", "AI")),
    PortfolioPosition("XAIX.DE", "Xtrackers Artificial Intelligence & Big Data", 0.02, themes=("AI", "semiconductor")),
)

impact_engine = PortfolioImpactEngine()
impacts = impact_engine.evaluate(
    title="ASML order outlook weakens",
    summary="Semiconductor equipment demand expectations softened.",
    tags=("semiconductor", "AI"),
    positions=positions,
)

signal = Signal(
    signal_id="demo-asml-001",
    title="ASML order outlook weakens",
    summary="A demonstration signal only; not current investment information.",
    category="company",
    severity="warning",
    confidence=0.85,
    freshness=0.95,
    occurred_at="2026-01-01T12:00:00+00:00",
    tags=("ASML", "semiconductor"),
    evidence=(Evidence("demo", "Synthetic demonstration evidence"),),
    portfolio_impacts=impacts,
    data_quality=("synthetic_demo_data",),
)

path = export_json(
    "output/portfolio-intelligence.json",
    (signal,),
    (SourceStatus("demo", "ok", item_count=1),),
)
print(path)
