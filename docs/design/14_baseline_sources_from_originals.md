# Baseline-only sources, rebuilt from the original providers (issue #4)

Compiled 2026-11-19. Note 13 listed sources that the paper's merged baseline
used but that our pipeline lacked. The baseline file is the paper's data, so it
is not a pipeline input; instead each source was traced to its original
provider (the baseline metadata names them) and loaded from there. Nothing here
reads `canada_linear_features`.

## Results

| Jurisdiction | Sources | Road km | Roadless km2 | Roadless % | OSM 2021 % | NRN % |
| --- | --- | --- | --- | --- | --- | --- |
| NL | NRN + Resource Access Roads | 48,168 | 350,586 | 88.2 | 90.7 | 93.7 |
| NL strict | drops ATV-only and Not Passable | 47,100 | 351,390 | 88.4 | | |
| MB | NRN + MLI 1:20,000 + BEAD roads | 274,882 | 484,650 | 77.2 | 83.4 | 85.2 |
| MB strict | also drops cart tracks, accessways, lanes | 216,397 | 504,939 | 80.5 | | |
| NT | NRN + BEAD roads | 19,779 | 1,258,327 | 98.5 | | 99.1 |

Per-run results are in `data/processed/{nl,nl_strict,mb,mb_strict,nt}/<slug>/stats.json`.
The paper has no roadless area for these jurisdictions (Table 4 covers five
provinces), so there is nothing to compare with.

## Sources

- **NL Resource Access Roads** (`nl_roadless.py`): two public ArcGIS Online
  services from the Department of Fisheries, Forestry and Agriculture
  (FFA_ResourceRoads_NF layer 2 and FFA_ResourceRoads_LB layer 0, 13,480
  features, 27,878 km, modified 2025-10-31), Open Government Licence -
  Newfoundland and Labrador. The earlier note 11 and 13 finding that no
  download exists was wrong: the layer is on the NL GeoHub.
- **MB MLI 1:20,000 transportation** (`mb_roadless.py`): public, OpenMB
  licence, `trn_bas_20k_ln` (522,373 lines, 171,317 km). Files date from 2009
  and MLI stopped updating in February 2022. About a third of its length is
  cart tracks (52,164 km), and it includes rail lines, footpaths and trails,
  which the loader drops.
- **BEAD roads** (`bead.py`, used for MB and NT): ECCC, Open Government Licence
  Canada, 2010 (zip) and 2015 (ArcGIS service) editions, Class Road only.

## Caveats

- **BEAD is raw.** The paper cleaned it by hand (dropping segments that did not
  follow a visible road and small unconnected pieces); that is not reproduced.
  The 2010 and 2015 editions overlap, so `road_km` double counts shared roads,
  but the union buffer does not.
- **The MB layer is old and fixed.** Treat MB as a 2009-vintage estimate plus
  BEAD; it cannot be refreshed.
- **MB default keeps cart tracks and accessways**, as the paper's baseline did
  (it classed them as track). The strict variant is an upper bound.
- Nothing is checked against imagery.

## Still without an original source

- **SK_HFP** (Saskatchewan Human Footprint): sent privately by FTP to the
  paper's authors. It was built from the NRN and a "State of the Forest"
  linear feature file; no public copy found. Contact `egis@gov.sk.ca`.
- **PEI forest roads**: a private file transfer from the PEI environment
  department. PEI's public road centreline layer (16,910 features) is
  provincial but duplicates the NRN's public roads, so it adds nothing.
- Statistics Canada, GRIP and gROADS are comparison datasets and not needed.
