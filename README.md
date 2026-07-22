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

## Jelenlegi működő vertikális szelet

```text
SourceAdapter
    ↓
normalizált Signal + SourceStatus
    ↓
portfólióillesztés
    ↓
deduplikáció
    ↓
prioritási és alert-besorolás
    ↓
portfolio-intelligence.json export
```

A jelenlegi implementáció tartalmazza:

- forrásadapter-szerződést és kontrollált statikus adaptert;
- JSON- és CSV-portfólióbetöltést;
- közvetlen ticker-, cégnév- és témakapcsolat felismerést;
- determinisztikus, azonos napi esemény-deduplikációt;
- adapterhibák megőrzését `SourceStatus` rekordként;
- `information`, `watch` és `alert` besorolást;
- determinisztikus JSON-exportot és unit teszteket.

## Helyi futtatás

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
python scripts/generate_demo.py
```

A biztonságos portfólióbemeneti példa az `examples/portfolio.example.json` fájlban található. Valós portfólióadatot, API-kulcsot vagy szerverkonfigurációt nem szabad a repositoryba commitolni.

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

## Státusz

A repository fejlesztési alapverzió. Produkciós adatforrás, API-kulcs vagy személyes portfólióadat még nincs benne.