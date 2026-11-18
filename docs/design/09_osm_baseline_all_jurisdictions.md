# OSM roadless baseline, all 13 jurisdictions (issue #5 follow-up)

`run_regions.py 210101 all`: Geofabrik 1 January 2021 snapshot, paper method
(1 km buffer, StatCan 2016 land mask), EPSG:3347. All 13 ran with no errors.
Seconds are compute only, excluding download.

| Jurisdiction | Land km2 | Roadless km2 | Percent | Patches | Seconds |
| --- | --- | --- | --- | --- | --- |
| British Columbia | 917,733 | 746,876 | 81.4 | 5,679 | 91 |
| Alberta | 639,937 | 362,751 | 56.7 | 8,070 | 55 |
| Saskatchewan | 632,214 | 355,652 | 56.3 | 8,024 | 32 |
| Manitoba | 627,595 | 523,702 | 83.4 | 2,380 | 15 |
| Ontario | 980,244 | 744,339 | 75.9 | 9,893 | 138 |
| Quebec | 1,476,349 | 1,274,859 | 86.4 | 8,176 | 78 |
| New Brunswick | 74,525 | 32,009 | 43.0 | 1,796 | 15 |
| Nova Scotia | 57,534 | 11,800 | 20.5 | 2,575 | 29 |
| Prince Edward Island | 6,023 | 347 | 5.8 | 406 | 3 |
| Newfoundland and Labrador | 397,598 | 360,671 | 90.7 | 2,767 | 14 |
| Yukon | 455,687 | 440,922 | 96.8 | 115 | 3 |
| Northwest Territories | 1,277,219 | 1,267,294 | 99.2 | 966 | 2 |
| Nunavut | 2,010,567 | 2,007,658 | 99.9 | 15,818 | 13 |

## Findings

- Largest run was Ontario at 138 s, so tiling is not needed for a baseline.
  Whole-country compute is about 8 minutes. The earlier tiling worry applies
  to memory on other machines and to larger future inputs, not to this run.
- The BC, AB, ON and QC results match the figures in note 07 (same inputs).
  Nova Scotia matches the paper within 0.5% (note 06). The other provinces
  have not been compared with the paper: the paper's roadless areas are not in
  our notes for them, and its layers are not published.
- Nunavut (15,818 patches) and the northern territories reflect sparse OSM
  coverage as much as true roadlessness; OSM is thin there (note 04).
- Percentages for the territories are driven by what OSM has mapped, so treat
  them as upper bounds on roadless area.

Per-province outputs are in `data/processed/210101/<slug>/` (ignored by git).
