# Portfolio Market Intelligence — implementation roadmap v1

Date: 2026-07-21

## Objective

Build an independent portfolio-intelligence backend inspired by useful public dashboard patterns, without copying AGPL-covered World Monitor source code. The system supplements — but does not replace — the existing portfolio calculation backend and dashboard JSON contract.

## Architectural boundary

```text
External sources
  ├─ prices / FX
  ├─ macro data
  ├─ ETF and issuer data
  ├─ filings
  └─ news / RSS
        ↓
Portfolio Market Intelligence
  ├─ source adapters
  ├─ normalization
  ├─ evidence and provenance
  ├─ signal aggregation
  ├─ portfolio impact
  ├─ risk / catalyst scoring
  └─ AI brief generation
        ↓
Versioned intelligence output
        ↓
Existing portfolio backend / dashboard integration
```

The existing portfolio backend remains authoritative for holdings, cost basis, current value, returns, weights, risk flags, decision status and `data_quality` fields.

## Technology decision for MVP

Recommended initial stack:

- Python 3.12+
- Pydantic for strict models and validation
- pytest for tests
- httpx for HTTP clients
- SQLite for local development and reproducible snapshots
- JSON files for initial deterministic exports
- optional FastAPI only when an HTTP API becomes necessary

Reason: the existing portfolio update workflow is already backend/data-file oriented, and Python is suitable for financial data normalization, analysis and scheduled jobs. A frontend framework is not required for the first milestone.

## Milestone 0 — governance and safety

Deliverables:

- module adoption matrix;
- dependency and data-source register;
- clean-room implementation rules;
- secrets policy;
- data-retention and privacy rules;
- explicit prohibition of automatic trading.

Acceptance criteria:

- no World Monitor source files in the repository;
- no API keys or portfolio exports committed;
- every external dependency and data source has an owner, licence/terms status and usage purpose.

## Milestone 1 — core domain skeleton

Proposed structure:

```text
src/portfolio_intelligence/
  models/
    evidence.py
    signal.py
    source_status.py
    portfolio_impact.py
  adapters/
    base.py
    registry.py
  pipelines/
    normalize.py
    aggregate.py
  quality/
    freshness.py
    validation.py
  export/
    intelligence_json.py

tests/
  test_evidence.py
  test_freshness.py
  test_registry.py
  test_aggregation.py
  test_export_schema.py
```

Core models:

- `Evidence`: source, URL or identifier, observed time, published time, retrieved time, excerpt/hash, licence/terms tag;
- `Signal`: entity, signal type, direction, magnitude, confidence, horizon, evidence references;
- `SourceStatus`: latest run, latest success, freshness, degraded state, error category;
- `PortfolioImpact`: affected ticker/theme/sector/region, estimated impact, confidence, rationale and evidence;
- `DataQualityIssue`: missing, stale, conflicting, unverified or provider-limited.

Acceptance criteria:

- deterministic serialization;
- strict validation;
- no silent defaulting of missing financial facts;
- tests distinguish missing, zero and not-applicable values;
- every signal must reference evidence or be explicitly marked as model-generated inference.

## Milestone 2 — source adapters

Initial adapters:

1. manual market-price input compatible with the existing workflow;
2. manual FX-rate input;
3. one official macro source;
4. RSS/Atom news source;
5. optional issuer/ETF metadata source after terms review.

Adapter contract:

- `fetch()` retrieves raw data;
- `normalize()` creates typed records;
- `quality()` reports freshness and limitations;
- `provenance()` records source identity and retrieval metadata.

Acceptance criteria:

- provider failure does not corrupt prior valid snapshots;
- stale data remains visible and marked stale;
- conflicting values are retained with conflict metadata;
- source adapters cannot write directly into the dashboard JSON.

## Milestone 3 — news and evidence pipeline

Capabilities:

- feed registry;
- effective-date normalization;
- duplicate detection;
- ticker, company, ETF, sector, country and theme tagging;
- source-quality tiers;
- relevance scoring against current portfolio and watchlist;
- evidence archive.

Important rules:

- publication date and event date remain separate;
- syndicated copies should not count as independent confirmation;
- AI summaries cannot be treated as primary evidence;
- low-confidence entity matches must be flagged rather than forced.

## Milestone 4 — signal aggregation

Initial signal families:

- price and volatility;
- earnings/fundamental;
- macro sensitivity;
- regulatory/political;
- sector/theme momentum;
- technical condition;
- portfolio concentration;
- thesis-supporting and thesis-breaking events.

Aggregation principles:

- evidence count is not equal to evidence independence;
- recency decay varies by signal type;
- conflicting evidence lowers confidence;
- missing data lowers coverage, not necessarily the score itself;
- output includes score components and explanation.

## Milestone 5 — portfolio impact engine

Inputs:

- current portfolio positions and weights from the authoritative portfolio backend;
- normalized signals;
- sector, geography, currency and theme mappings;
- position-level decision statuses and monitoring flags.

Outputs:

- affected positions;
- direct and indirect exposure;
- estimated time horizon;
- confidence;
- portfolio-level concentration interaction;
- suggested review priority;
- no automatic buy/sell command.

Initial scores:

- Position Attention Score;
- Theme Risk Score;
- Portfolio Event Impact Score;
- Data Coverage Score.

## Milestone 6 — catalyst timeline and briefs

Catalyst timeline:

- earnings;
- central-bank and macro releases;
- ETF/index changes;
- regulatory decisions;
- known company events;
- user-defined thesis checkpoints.

Brief outputs:

- daily change brief;
- weekly portfolio intelligence review;
- position-specific thesis update;
- watchlist opportunity brief.

Every brief must separate:

- verified facts;
- calculations;
- estimates;
- assumptions;
- AI/analyst interpretation.

## Milestone 7 — dashboard integration

Integration should occur only after the intelligence output is stable.

Rules:

- do not alter the existing accounting logic;
- do not let the frontend recompute values or statuses;
- use a versioned intelligence section or separate JSON file first;
- preserve `data_quality` and missing-data reports;
- provide backward-compatible dashboard behaviour when intelligence data is unavailable.

Recommended first integration:

```text
data/portfolio-intelligence.json
```

Only after validation should selected fields be incorporated into the primary dashboard schema through a formal schema-version decision.

## Deferred capabilities

Not in MVP:

- map/globe visualization;
- aircraft, ship or military layers;
- desktop/Tauri app;
- Telegram intelligence;
- automated trading;
- public multi-user SaaS;
- billing and subscriptions;
- complex vector/RAG infrastructure before a sufficient evidence corpus exists.

## Definition of done for v0.1

- independent, tested source-adapter framework;
- evidence and signal models;
- one market/manual adapter, one macro adapter and one RSS adapter;
- freshness and source-status reporting;
- deterministic signal aggregation prototype;
- portfolio-impact stub using sample anonymized holdings;
- JSON schema and tests;
- no secrets or personal portfolio data committed;
- documented dependency and data-source licences/terms.
