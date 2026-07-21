# Portfolio Market Intelligence – kezdeti architektúra v0.1

## Rendszerhatár

Ez a repository önálló intelligencia- és kutatási réteg. Nem helyettesíti a meglévő `portfolio-dashboard` vagy `watchlist-dashboard` backendjét, és kezdetben nem írja közvetlenül azok produkciós adatfájljait.

## Fő komponensek

```text
src/
  adapters/
    market/
    macro/
    news/
    filings/
    etf/
  domain/
    events/
    evidence/
    themes/
    portfolio/
    watchlist/
  engines/
    correlation/
    theme_intelligence/
    portfolio_impact/
    briefing/
  exporters/
    research_json/
    dashboard_bridge/
  quality/
  config/

tests/
  unit/
  integration/
  fixtures/

docs/
```

## Adatfolyam

1. Az adapterek külső adatot olvasnak.
2. A normalizáló réteg közös esemény- és bizonyítéksémát hoz létre.
3. A minőségellenőrzés jelzi a frissességet, hiányt, konfliktust és bizonytalanságot.
4. A korrelációs motor összekapcsolja a piaci, makro- és híreseményeket.
5. A téma-intelligencia motor tematikus állapotot számít.
6. A portfólióhatás-motor a saját pozíciókra és watchlistre vetíti a hatást.
7. A brief-generátor tényeket, becsléseket és elemzői véleményt elkülönítve állít elő.
8. Az exporterek külön kutatási JSON-t készítenek; produkciós dashboard-export csak explicit integráció után engedélyezett.

## Kezdeti közös objektumok

### Evidence

- `source_id`
- `source_type`
- `source_url`
- `published_at`
- `retrieved_at`
- `freshness_status`
- `confidence`
- `licence_or_terms`
- `raw_reference`

### IntelligenceEvent

- `event_id`
- `event_type`
- `title`
- `summary`
- `entities`
- `themes`
- `countries`
- `sectors`
- `tickers`
- `direction`
- `magnitude_estimate`
- `time_horizon`
- `evidence_ids`
- `data_quality`

### PortfolioImpact

- `portfolio_item_id`
- `event_id`
- `impact_direction`
- `impact_strength`
- `time_horizon`
- `thesis_effect`
- `action_category`
- `confidence`
- `rationale`

## Integrációs szabály

A meglévő dashboard csak olyan adatot kap, amely:

- determinisztikusan előállítható vagy egyértelműen becslésként jelölt;
- forrással és időbélyeggel rendelkezik;
- átment a data-quality ellenőrzésen;
- megfelel a meglévő JSON-sémának;
- nem számoltat újra semmit a frontenddel.

## Következő technikai döntések

- programozási nyelv és futtatási környezet;
- elsődleges piaci adatforrások;
- RSS/híraggregáció megoldása;
- tárolási forma: fájl, SQLite vagy más lokális adatbázis;
- AI-szolgáltató és költségkorlát;
- ütemezés és hibakezelés;
- tesztadatok és fixture-politika.
