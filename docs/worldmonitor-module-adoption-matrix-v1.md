# World Monitor module adoption matrix — v1

Date: 2026-07-21

## Decision summary

The source repository `koala73/worldmonitor` is licensed under AGPL-3.0. Directly copying or adapting its source code into this project could bring the resulting covered work under AGPL obligations, including source-availability duties for modified software used over a network.

For this project the default decision is therefore:

- reuse ideas, interfaces, data-flow patterns and mature third-party libraries;
- implement portfolio-specific business logic independently;
- do not copy World Monitor source files unless a separate, explicit licensing decision is recorded;
- keep the existing portfolio dashboard schema and backend-authoritative calculation model unchanged.

## Classification legend

- **A — Reuse as independent dependency:** use the underlying third-party library or public API directly, after checking its own license and terms.
- **B — Clean-room reimplementation:** reproduce the capability from documented behaviour and general engineering patterns, without copying source code or distinctive implementation details.
- **C — Further licence/data-terms review:** potentially useful, but source, dataset or service terms must be checked before implementation.
- **D — Exclude:** not useful for the investment-dashboard objective or introduces disproportionate complexity/risk.

## Module-level adoption matrix

| World Monitor area / observed repository element | Portfolio relevance | Category | Decision | Proposed portfolio equivalent |
|---|---:|---|---|---|
| `src/services/signal-aggregator.ts` | Very high | B | Reimplement independently | `SignalAggregator` combining market, macro, company, ETF and news signals with source attribution and confidence |
| `src/app/data-loader.ts` | Very high | B | Reimplement independently | Deterministic ingestion orchestrator with adapters, timestamps, retries, freshness and data-quality flags |
| `src/shared/pipeline-registry-store.ts` | High | B | Reimplement independently | Registry of enabled pipelines, run state, last-success time and degraded-source status |
| `src/workers/analysis.worker.ts` | High | A/B | Use standard worker/job technology, write our own analysis logic | Background analysis jobs for scoring, deduplication, embeddings and brief generation |
| `src/workers/vector-db.ts` and RAG tests | Medium-high | A/B/C | Use an independent vector store/library; review provider terms | Searchable evidence archive for news, filings, ETF documents and prior thesis notes |
| `src/components/LatestBriefPanel.ts` | Very high | B | Rebuild as a native portfolio component | Daily/weekly portfolio intelligence brief with facts, estimates, alerts and evidence links |
| risk-score API and CII scoring tests | Very high conceptually | B | Reimplement scoring from first principles | Portfolio Risk Score, Theme Risk Score and Position Attention Score; no direct CII formula copy |
| event/threat timeline panels and tests | High | B | Reimplement independently | Catalyst and risk-event timeline by asset, sector, theme and portfolio impact |
| news/feed date-ranking tests | High | B | Rebuild deterministic ranking rules | Effective-date normalization, source time, publication time, event time, freshness decay |
| markets-news wiring tests | High | B | Reimplement portfolio-specific correlation | Link market moves and news to holdings, sectors, regions and themes |
| notification relay and digest jobs | High | A/B/C | Use standard scheduler/messaging stack; inspect provider terms | Scheduled digest and threshold alerts; no automatic trading |
| browser-bundle secret guard tests | Very high | B | Adopt the security requirement, implement our own tests | CI guard ensuring API keys and private portfolio data never enter frontend bundles |
| blocked-storage-services tests | High | B | Adopt the principle | Prevent unsupported or insecure client-side persistence of sensitive data |
| analytics / telemetry | Medium | A/C | Use privacy-conscious independent tooling only if needed | Operational telemetry, not investment tracking; disabled by default for personal use |
| unified settings component | Medium | B | Rebuild a smaller version | Provider settings, source enable/disable, alert thresholds and AI mode |
| multiple dashboard variants | High conceptually | B | Adopt architecture, not code | One intelligence backend serving portfolio, watchlist and research dashboard views |
| AI summaries / local AI patterns | High | A/B/C | Use OpenAI or local model APIs under their own terms; custom prompts and validation | Evidence-bound brief generator with fact/estimate/opinion separation |
| RSS and curated news-source architecture | Very high | A/B/C | Use RSS libraries and feeds directly; review each source’s usage terms | Source registry, feed adapters, deduplication, entity tagging, relevance scoring |
| finance radar / market-data integrations | Very high | A/B/C | Use chosen market-data APIs directly; do not copy integration code | Prices, indices, FX, rates, commodities, ETF metrics and economic series adapters |
| country intelligence concept | Medium | B | Translate the concept, do not copy formula | Country/region exposure risk score driven by portfolio weights and current signals |
| plugin/data-source architecture | Very high | B | Reimplement a typed adapter interface | Replaceable adapters for prices, FX, macro, filings, news and AI providers |
| consumer-price panel/core | Medium | A/B/C | Use official CPI data APIs; implement our own transform | Inflation monitor mapped to portfolio sectors, bonds, gold and currencies |
| Telegram intelligence | Low-medium | C | Defer pending source-quality, legal and operational review | Optional alternative-source adapter; not part of MVP |
| local storage and caching patterns | High | A/B | Use standard cache/database libraries independently | Server-side cache with provenance, TTL, stale status and reproducible snapshots |
| desktop/Tauri application | Low | D for initial phases | Exclude from MVP | Web/backend workflow is sufficient; reconsider only for secure local/private operation |
| global map and map-layer definitions | Low | D | Exclude | Geographic exposure charts and tables are sufficient |
| aircraft, vessel, conflict and military layers | None | D | Exclude | No investment-dashboard requirement |
| supply-chain route explorer | Medium, long term | B/C | Defer; reimplement only for selected themes | Semiconductor, energy, shipping and commodity supply-chain risk module |
| commodity/gold layers | High for existing portfolio | A/B/C | Use market and official data directly; own scoring | Gold, silver, copper, uranium and miner-theme intelligence modules |
| consumer/pro commercial modules | Low | D/C | Exclude unless separately justified | No billing, public SaaS or lead-generation scope in current project |

## Third-party components that may be reused independently

The exact dependency inventory must be reviewed from `package.json` and lockfiles before any library is selected. The safe rule is to install required libraries from their original package registries and comply with each library's own licence, rather than copying vendored or World Monitor-specific wrapper code.

Likely independent categories include:

- HTTP client and retry libraries;
- RSS/Atom parsing;
- schema validation;
- task scheduling and queues;
- SQLite/PostgreSQL and migration tools;
- charting libraries;
- date/time normalization;
- vector databases and embedding clients;
- testing frameworks;
- structured logging;
- OpenTelemetry-compatible monitoring;
- official SDKs for chosen data and AI providers.

No package is approved solely by appearing in World Monitor. Every selected dependency needs a recorded licence and security check.

## Portfolio-specific modules that must be ours

These represent the unique value and should not be inherited from another project:

1. Portfolio impact engine
2. Position and theme exposure mapping
3. Portfolio Risk Score
4. Position Attention Score
5. Profit Protection Engine
6. Buy Opportunity Engine
7. Thesis-monitoring logic
8. Watchlist prioritization
9. Portfolio-aware news relevance scoring
10. Decision categories and dashboard status mapping
11. Data-quality policy and missing-data reporting
12. `dashboard-data.json` generation and schema validation

## Clean-room implementation rules

1. World Monitor source code must not be pasted into implementation prompts or copied into this repository.
2. Requirements may be derived from publicly observable behaviour, documentation and general architecture.
3. New names, interfaces, tests and algorithms must be portfolio-specific.
4. Each new module should include a short provenance note: `independent implementation; concept informed by public dashboard patterns`.
5. Third-party library licences and data-provider terms must be recorded in `docs/dependency-register.md`.
6. Facts, calculations, estimates and AI opinions must remain separately labelled in all generated outputs.
7. The frontend must not recompute authoritative portfolio values, weights, returns, statuses or alerts.
8. No automated order execution is permitted.

## Recommended MVP extraction order

### Phase 1 — Foundation

- typed source-adapter interface;
- source registry and run-status registry;
- normalized `Signal` and `Evidence` models;
- freshness, provenance and confidence fields;
- deterministic JSON output and schema tests;
- secret-leak CI tests.

### Phase 2 — Market and news ingestion

- prices and FX adapters;
- macro-series adapter;
- RSS/news ingestion;
- deduplication and entity tagging;
- asset/theme relevance mapping.

### Phase 3 — Portfolio intelligence

- signal aggregation;
- portfolio-impact scoring;
- catalyst timeline;
- position attention and theme risk scores;
- daily/weekly brief generator.

### Phase 4 — Dashboard integration

- extend only through a versioned, approved schema path;
- keep existing dashboard calculations backend-authoritative;
- add intelligence sections without changing existing position/accounting semantics;
- maintain data-quality and missing-source reports.

## Immediate implementation decision

The first code milestone should be a small, independent TypeScript or Python backend skeleton containing:

- `SourceAdapter` interface;
- `Signal`, `Evidence`, `SourceStatus` and `PortfolioImpact` models;
- a source registry;
- a deterministic signal aggregator stub;
- JSON schema validation;
- unit tests for provenance, freshness and missing-data handling.

This milestone contains no copied World Monitor source code and creates the base needed for later market, news and AI integrations.
