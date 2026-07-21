# Dependency and data-source register

Status values: `proposed`, `reviewing`, `approved`, `rejected`, `deferred`.

No dependency or provider is approved merely because another project uses it.

## Software dependencies

| Component | Purpose | Candidate | Licence | Security review | Status | Notes |
|---|---|---|---|---|---|---|
| Runtime | Backend processing | Python 3.12+ | PSF | pending | proposed | Initial recommendation |
| Data models | Validation and serialization | Pydantic | MIT | pending | proposed | Strict missing-data handling required |
| HTTP client | API retrieval | httpx | BSD-3-Clause | pending | proposed | Timeouts, retries and rate limiting required |
| Tests | Unit/integration tests | pytest | MIT | pending | proposed | Required from first code milestone |
| Local database | Snapshots and evidence metadata | SQLite | Public domain | pending | proposed | Do not store secrets in committed DB files |
| HTTP API | Optional later API | FastAPI | MIT | pending | deferred | Not needed for the initial file-based workflow |
| RSS parser | RSS/Atom ingestion | TBD | TBD | pending | reviewing | Select directly from original registry |
| Scheduler | Scheduled ingestion/digests | TBD | TBD | pending | deferred | Needed only after deterministic manual runs work |
| Vector store | Evidence semantic search | TBD | TBD | pending | deferred | Avoid premature complexity |
| AI SDK | Brief generation | OpenAI or local model client | provider-specific | pending | deferred | Evidence-bound outputs only |

## Data and service providers

| Source category | Candidate | Data required | Terms/licence status | Authentication | Status | Risks/limitations |
|---|---|---|---|---|---|---|
| Manual prices | Existing `manual_prices.csv` workflow | Current and manually verified prices | internal workflow | none | approved | Values must retain as-of timestamps |
| Manual FX | Existing `manual_fx_rates.csv` workflow | FX conversion rates | internal workflow | none | approved | Missing/stale rates must be reported |
| Central-bank FX | ECB or another official source | Reference FX rates | review required | usually none | proposed | Reference rates may not match transaction pricing |
| Macro | FRED / ECB / Eurostat / official agencies | Rates, inflation, growth, liquidity | review required | varies | proposed | Release dates and revision history must be retained |
| Market prices | TBD | Equities, ETFs, ETCs, indices, crypto | review required | likely | reviewing | Redistribution and delayed-data restrictions |
| ETF metadata | Issuer pages / regulated documents | TER, AUM, holdings, geography, sectors | review required per issuer | varies | proposed | Holdings frequency and licensing vary |
| Company filings | SEC and issuer/regulator sources | Reports and filings | review required | usually none | proposed | Entity matching and filing-version handling |
| News/RSS | Curated publisher feeds | Headlines, timestamps, summaries, links | review per source | usually none | reviewing | Copyright, caching and full-text restrictions |
| AI provider | OpenAI or local model | Summarization and structured inference | provider terms required | key/local | deferred | Privacy, retention, hallucination and cost |

## Mandatory review fields for every new provider

- provider and exact endpoint;
- data purpose;
- licence or terms URL;
- commercial/personal-use permission;
- caching and retention restrictions;
- redistribution restrictions;
- attribution requirements;
- rate limits;
- authentication and secret-storage method;
- timestamp semantics;
- expected update frequency;
- known coverage gaps;
- fallback behaviour;
- decision and review date.

## Prohibited until explicitly approved

- committing API keys or tokens;
- scraping a provider whose terms prohibit automated access;
- redistributing licensed market data in a public repository;
- treating delayed or estimated prices as real-time without a label;
- storing full copyrighted articles when only links/metadata are permitted;
- sending identifiable portfolio data to an AI provider without a specific privacy decision;
- allowing a data adapter to overwrite authoritative holdings or accounting data.
