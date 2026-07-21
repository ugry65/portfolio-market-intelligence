# Portfolio Market Intelligence

A befektetési portfóliót, watchlistet és piaci környezetet támogató intelligencia-réteg.

## Cél

A projekt feladata a piaci, makrogazdasági, híralapú és tematikus adatok összegyűjtése, értékelése és portfólióhatássá alakítása. A rendszer nem kereskedik automatikusan, és nem módosítja a meglévő dashboard számítási vagy JSON-szerződését.

## Alapelvek

- a backend az egyetlen számítási autoritás;
- a frontend csak megjelenít;
- hiányzó vagy bizonytalan adatot nem találunk ki;
- minden következtetéshez forrás, időbélyeg és megbízhatósági jelzés tartozik;
- tény, számítás, becslés, feltételezés és elemzői vélemény elkülönül;
- nincs automatikus vételi vagy eladási megbízás;
- a meglévő `dashboard-data.json` séma csak külön architektúradöntéssel változhat.

## Tervezett modulok

```text
sources
  ├── market data
  ├── macro data
  ├── news and filings
  ├── ETF issuer data
  └── portfolio and watchlist context
          ↓
normalization and evidence layer
          ↓
correlation and theme intelligence
          ↓
portfolio impact engine
          ↓
briefs, alerts and dashboard export
```

## World Monitor kapcsolat

A `koala73/worldmonitor` projekt inspirációs és kutatási forrás. Licence GNU AGPL-3.0. Emiatt közvetlen forráskód csak dokumentált licencvizsgálat után kerülhet ebbe a repositoryba.

Elsődleges stratégia:

1. általános architekturális minták átvétele;
2. permisszív licencű külső könyvtárak közvetlen használata;
3. saját, független implementáció a portfólióspecifikus modulokhoz;
4. AGPL-kód elkülönítése vagy mellőzése, amíg a licenckövetkezményeket kifejezetten nem vállaljuk.

Részletek: [`docs/worldmonitor-adoption-audit.md`](docs/worldmonitor-adoption-audit.md)

## Kezdeti státusz

A repository jelenleg kutatási és architekturális alap. Produkciós adatforrás, API-kulcs vagy személyes portfólióadat még nincs benne.
