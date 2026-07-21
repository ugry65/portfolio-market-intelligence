# Portfolio Intelligence JSON v0.1

## Purpose

This file is separate from the production portfolio dashboard schema. It contains evidence-backed market intelligence and must not overwrite `dashboard-data.json`.

Default output name:

`portfolio-intelligence.json`

## Top-level fields

- `schema_version`: semantic schema version.
- `generated_at`: UTC generation timestamp.
- `data_quality`: source-level failure and degradation summary.
- `source_statuses`: status records for every configured source.
- `signals`: descending priority order.

## Signal requirements

Every signal must include:

- stable `signal_id`;
- title and concise summary;
- category and severity;
- confidence and freshness in the range 0–1;
- occurrence and detection timestamps;
- zero or more evidence records;
- zero or more portfolio impacts;
- explicit data-quality flags where applicable;
- deterministic `priority_score`;
- deterministic alert classification.

## Safety rules

1. Missing data must remain missing; it must not be inferred silently.
2. AI-generated statements, when later introduced, require evidence references and a separate confidence field.
3. Portfolio weights are inputs from the portfolio backend, not recalculated by the intelligence frontend.
4. ETF look-through exposure must identify its holdings source and effective date.
5. A failed source must remain visible in `data_quality` and `source_statuses`.
6. Synthetic/demo data must always carry a `synthetic_demo_data` flag.

## Compatibility

The production dashboard may later consume this file as a secondary read-only source. Any merge into `dashboard-data.json` requires a separately versioned schema decision and must preserve the existing dashboard contract.
