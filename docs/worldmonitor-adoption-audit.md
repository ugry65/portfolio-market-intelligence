# World Monitor átvételi és licenc-audit

Dátum: 2026-07-21

Forrásprojekt: `koala73/worldmonitor`

## 1. Licenc

A World Monitor GNU Affero General Public License v3.0 vagy újabb licenc alatt áll.

Ennek gyakorlati következménye, hogy a World Monitorból közvetlenül átvett vagy abból származtatott kód esetén:

- meg kell őrizni a szerzői és licencértesítéseket;
- a módosításokat és azok dátumát egyértelműen jelezni kell;
- a származékos művet AGPL-kompatibilis feltételekkel kell terjeszteni;
- hálózaton keresztül használt módosított változatnál a megfelelő forráskódot a felhasználók számára hozzáférhetővé kell tenni;
- az interaktív felület megfelelő jogi értesítéseit meg kell őrizni vagy megjeleníteni, ahol ez alkalmazandó.

Ez nem jogi tanács. Közvetlen kódátvétel előtt szükség esetén külön jogi ellenőrzés indokolt.

## 2. Döntés

A projekt első fázisában nem másolunk át World Monitor-forrásfájlokat.

A választott megközelítés: **clean-room jellegű, saját implementáció**, amely kizárólag nyilvánosan megfigyelhető funkcionális és architekturális ötletekből indul ki.

## 3. Hasznosítható koncepciók

### Átvehető mintaként, saját implementációval

- több adatforrás egységes adapterrétege;
- események normalizálása közös adatsémába;
- források közötti korreláció;
- téma- és országintelligencia pontszámok;
- időbélyegzett AI-összefoglalók;
- több dashboard kiszolgálása egy közös backendből;
- lokális AI-modell opcionális támogatása;
- eseményidővonal és katalizátornaptár;
- forrás- és megbízhatósági metaadatok;
- degradált működés, amikor egy adatforrás kiesik.

### Portfólióspecifikusan saját fejlesztés

- portfolio impact engine;
- pozíció-, szektor-, téma-, földrajzi és devizahatás;
- profitvédelmi és stop-alert logika;
- watchlist-rangsorolás;
- ETF-átfedés és koncentrációelemzés;
- tézisváltozás és döntési státusz;
- meglévő dashboard JSON-séma exportja;
- `data_quality` és bizonytalansági jelzések.

### Nem prioritás

- katonai térkép;
- repülő- és hajókövetés;
- 3D földgömb;
- vizuális effektusok;
- a portfóliószempontból irreleváns geopolitikai widgetek.

## 4. Közvetlen komponensátvétel feltételei

Egy World Monitor-fájl vagy modul csak akkor kerülhet be, ha mindegyik feltétel teljesül:

1. pontos fájl- és szerzői eredet dokumentált;
2. a licenc- és attribution-követelmények dokumentáltak;
3. a modul elkülöníthetősége és licenchátása felmért;
4. nincs benne titok, API-kulcs, személyes adat vagy harmadik fél által korlátozott tartalom;
5. az átvételt külön architektúradöntés engedélyezi;
6. tesztek igazolják, hogy nem változtatja meg a meglévő dashboard számítási autoritását.

## 5. Első fejlesztési sorrend

1. közös esemény- és bizonyítékséma;
2. RSS/hírforrás adapter interfész;
3. makroadat-adapter interfész;
4. portfólió- és watchlist-kontextus beolvasása;
5. téma-intelligencia prototípus;
6. portfólióhatás prototípus;
7. brief-generálás;
8. elkülönített JSON export;
9. csak ezután dashboard-integráció.

## 6. Biztonsági korlátok

- API-kulcs nem kerülhet repositoryba;
- `.env` fájl nem commitolható;
- valódi személyes portfólióadat csak külön döntéssel tárolható;
- automatikus kereskedési funkció nem készül;
- a meglévő `dashboard-data.json` szerződés nem változik hallgatólagosan;
- hiányzó adatból nem képezhető kitalált érték.
