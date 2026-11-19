# Provincial road datasets: ON, QC, NS, YT (issue #4)

Continues note 10 (NRN, BC DRA, Alberta HFI). Same pipeline and method (1 km
buffer, StatCan 2016 land mask, EPSG:3347); each dataset is a loader with a
documented exclusion list and a `--strict` upper-bound variant, run through
`single_dataset.run`. Compiled 2026-11-19. All downloads are the current
edition, which the sources do not archive, so record the date with results.

## Results

| Jurisdiction and dataset | Road km | Roadless km2 | Roadless % | OSM 2021 % | NRN % | Patches |
| --- | --- | --- | --- | --- | --- | --- |
| Ontario, ORN + MNR roads | 461,020 | 652,027 | 66.5 | 75.9 | 75.9 | 13,377 |
| Ontario, strict | 455,211 | 654,099 | 66.7 | | | 13,423 |
| Quebec, RQTT | 657,573 | 1,034,381 | 70.1 | 86.4 | 91.4 | 13,229 |
| Quebec, strict | 656,662 | 1,034,556 | 70.1 | | | 13,248 |
| Nova Scotia, NSTDB roads | 110,351 | 5,396 | 9.4 | 20.5 | 21.7 | 1,267 |
| Nova Scotia, strict | 109,925 | 5,405 | 9.4 | | | 1,276 |
| Yukon, Road Network + Forest Resource Roads | 8,759 | 444,466 | 97.5 | 96.8 | 97.7 | 95 |
| Yukon, strict | 8,359 | 444,529 | 97.6 | | | 95 |

Per-run results are in `data/processed/<label>/<slug>/stats.json` (ignored by
git), with labels `on`, `qc`, `ns`, `yt` and a `_strict` suffix.

## Datasets and filters

- **Ontario** (`on_roadless.py`): ORN Road Net Element (585,333 segments,
  264,611 km) and MNR Road Segments (314,738 segments, 196,573 km, nearly all
  Resource / Recreation class), both from the LIO ArcGIS service under the
  Open Government Licence - Ontario, fetched by the new `fetch_inputs.py arcgis`.
  Default drops ORN FERRY CONNECTION only (the paper lists no Ontario
  exclusions); strict also drops ORN VIRTUAL ROAD (connectors, 2,845 km) and MNR
  segments that are destroyed, planted or Closed. The combined length is
  17% below the paper's ORN + MNRF figure (552,538 km); not explained.
- **Quebec** (`qc_roadless.py`): Referentiel quebecois du transport terrestre,
  layer Reseau_routier (656,523 km as downloaded), CC-BY 4.0 with attribution.
  Default drops Rue pietonne (the paper's exclusion) and Liaison maritime
  (ferries); strict also drops Chemin prive and Saisonnier. Length is 2% above
  the paper's AQreseau+ (644,738 km). The forest road classes (`Cls_CheFor`,
  coded 01 to 05, NF, NC, HI, IN) are kept whole because their coding is not
  documented in the files and was not looked up.
- **Nova Scotia** (`ns_roadless.py`): NSTDB Roads, Trails and Rails road line
  layer (336,702 features, Nova Scotia open data resource `a6gf-w68e`,
  OGL-Nova Scotia), fetched by the new `fetch_inputs.py socrata`. Default is the
  paper's list (driveway, ferry crossing, foot bridge, railroad, trail, walk,
  water access); strict adds abandoned roads, driveway and trail bridges,
  TRACK - Addressed (no vehicular traffic) and the status-unknown placeholder.
  Length is 2% above the paper's NSTDB (107,867 km). TRACK is 57,113 km of it.
- **Yukon** (`yt_roadless.py`): Yukon Road Network (8,164 km) and Forest
  Resource Roads 50k (595 km), GeoYukon ArcGIS services. Licence not verified.
  Default keeps everything; strict drops Winter and Driveway network types and
  Trail forest roads.

## Findings

- **The same pattern as BC and Alberta:** wherever a dataset with resource or
  low-use roads exists, roadless area is much lower than from OSM and the NRN:
  Ontario -9.4 points against both, Quebec -16 against OSM and -21 against the
  NRN, Nova Scotia -11 against OSM and -12 against the NRN. These three NRN
  figures are ceilings on roadless area, not estimates.
- **Filters barely matter** in these four (at most 0.2 points between default and
  strict), unlike Alberta (7.8 points).
- **Yukon is the exception:** 97.5% with the territorial data, within 1 point
  of OSM (96.8%) and the NRN (97.7%). The Yukon Road Network (8,164 km) is shorter than the
  paper's OSM figure (13,489 km), so it does not hold the tracks OSM maps; the
  97.5% is probably still too high, and no better Yukon source was found.
- **Run time:** Ontario and Quebec took about 9 to 10 minutes per variant
  (900,000 and 1.5 million segments); Nova Scotia and Yukon under 2 minutes.

## Not done, and why

| Jurisdiction | Dataset in note 02 | Outcome |
| --- | --- | --- |
| New Brunswick | Forest Roads (IRIU portal) | Resolved in note 13: the portal now serves it and it is on Socrata (gnb.socrata.com udwq-sw5i). |
| Manitoba | Manitoba Road Network 2023 | 1,476 provincial route lines, not a full network. Not useful. |
| Saskatchewan | Updated Road Network (SURN) | It is NRN-derived: 250,991 km against 249,914 km in the NRN. No new roads. Not run. |
| Prince Edward Island | PEI NRN service | A newer NRN edition (19,758 segments); would change the NRN result by under 1 point. Not run. |
| Newfoundland and Labrador | Resource Access Roads | No download or REST endpoint found (GeoAtlas returns 404 for service paths). Needs the geoatlas viewer or a direct request to the department. |
| Northwest Territories | Transportation_LCC Roads | Community roads, 6,103 km (1,843 km of Winter), less than the NRN's 7,173 km. Fetched but not run; adds little. |
| Nunavut | None | NRN and OSM only. |

So NL, NB, MB, SK, PE, NT and NU rely on the NRN and OSM results in notes 09 and
10. For NB and NL those are ceilings on roadless area.

## Limits

- No result here is checked against imagery or against the paper's roadless
  areas (not in our notes).
- Licences: Ontario, Quebec and Nova Scotia are open licences; Yukon unverified.
- Sources keep no history, so none of these can be rerun for an earlier date.
