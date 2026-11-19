# New Brunswick: NBRN plus Forest Roads (issue #4)

Compiled 2026-11-19. Retry of the NB source search in note 11. The paper used
no provincial dataset for NB or NL (its Table 2 lists only GRIP, gROADS, OSM,
SC and NRN), so there is no paper figure to compare with.

## What changed

The IRIU portal that returned 401 now loads. Its Forest Roads dataset (roads
not maintained by the transportation department whose main purpose is access
to forest resources) is a Socrata dataset on gnb.socrata.com (`udwq-sw5i`,
New Brunswick Open Government Licence, 181,432 features), fetched with
`fetch_inputs.py socrata gnb.socrata.com udwq-sw5i nb_forest_roads`. The public
road network is the NBRN v10.2 file geodatabase from GeoNB (31,362 km, same
licence), which has only a few Crown-land resource road classes, so the two are
combined (`nb_roadless.py`).

## Result

| Source | Road km | Roadless km2 | Roadless % | Patches |
| --- | --- | --- | --- | --- |
| OSM 2021 | | 32,009 | 43.0 | 1,796 |
| NRN | 36,053 | 34,764 | 46.6 | 1,738 |
| NBRN + Forest Roads | 124,675 | 2,497 | 3.4 | 1,538 |

Per-run results are in `data/processed/nb/new-brunswick/stats.json`.

## Findings

- **OSM and the NRN overstate NB roadless area by about 40 points**, the
  largest gap of any province (BC 28, AB 20). Forest Roads adds 93,313 km, more
  than the NBRN and NRN together.
- **Checked for double counting:** 72 exact duplicate geometries; dissolving
  gives 93,113 km, so the length is real, about 1.3 km/km2.
- **Caveat:** the layer has geometry only (no class, status or date), so
  disused or overgrown roads cannot be filtered out. 3.4% is therefore a floor
  on roadless area, as the strict variants elsewhere are a ceiling. Nothing is
  checked against imagery.
- **NBRN is the current edition (updated 2026-11-19) and is not archived.**
  Record the date with results.

## Newfoundland and Labrador

Still no download. The Resource Access Roads layer (Fisheries, Forestry and
Agriculture) is only in the GeoAtlas viewer; `geoatlas.gov.nl.ca` has no REST
path, `gis.gov.nl.ca` returned 503, and the open data hub search returned
nothing. The help file gives ResourceRoads@gov.nl.ca as the contact, so the
next step is a direct request.
