# National Road Network and BC Digital Road Atlas roadless areas (issue #4)

Issue #4 asked for one provincial road dataset through the same pipeline, with
a vehicle-road filter, compared with OSM and the paper. I chose the National
Road Network (NRN, Statistics Canada) because it covers every province and
territory in one schema, so it also tests the harmonization pattern 13 times
and addresses the NT and NU discrepancy in note 04. The BC Digital Road Atlas (a provincial dataset with
resource roads) is the second dataset, in the last section. Alberta Human
Footprint is not done.

Run: `run_regions.py nrn all`, current NRN GeoPackages (English) from
`geo.statcan.gc.ca/nrn_rrn/`, paper method (1 km buffer, StatCan 2016 land
mask, EPSG:3347). All 13 ran; 7.5 minutes of compute for the national run.
OSM is the 1 January 2021 snapshot from note 09.

## Vehicle-road filter

NRN `ROADCLASS` is a functional class, not a surface or use class. Every
`ROADSEG` feature is a road for motor vehicles; ferries are a separate layer
(not read) and there are no pedestrian or trail classes to remove. So the
filter is an exclusion list that defaults to empty (`EXCLUDED_ROADCLASS` in
`nrn_roadless.py`). Resource / Recreation (a narrow resource-access road) stays in.

The one class that matters is `Winter` (ice and snow roads): 2,786 km of
7,173 km in NT. With Winter roads the NT total is within 3% of
the paper's NRN figure (7,401 km); without them it is 4,387 km. The merged
layer in note 04 holds 5,317 km of NRN in NT, so it probably dropped
the Winter class (not checked in the merge code). This likely resolves finding 1
of note 04 for NT: the difference is the Winter class, not a different download. NU is 1,097 km here, against 912 km in the paper and
1,261 km in the merged layer; NRN edition differences are the likely cause but
unchecked. Elsewhere Winter roads are small (Alberta 40 segments, Ontario 234).

## Results

| Jurisdiction | NRN km | OSM roadless km2 | NRN roadless km2 | OSM % | NRN % | Diff (pp) | NRN patches | OSM patches |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| British Columbia | 91,219 | 746,876 | 823,011 | 81.4 | 89.7 | +8.3 | 3,748 | 5,679 |
| Alberta | 239,762 | 362,751 | 380,201 | 56.7 | 59.4 | +2.7 | 7,306 | 8,070 |
| Saskatchewan | 249,914 | 355,652 | 359,408 | 56.3 | 56.8 | +0.6 | 8,001 | 8,024 |
| Manitoba | 86,224 | 523,702 | 534,844 | 83.4 | 85.2 | +1.8 | 2,315 | 2,380 |
| Ontario | 260,398 | 744,339 | 743,852 | 75.9 | 75.9 | 0.0 | 10,328 | 9,893 |
| Quebec | 146,949 | 1,274,859 | 1,348,915 | 86.4 | 91.4 | +5.0 | 6,872 | 8,176 |
| New Brunswick | 36,053 | 32,009 | 34,764 | 43.0 | 46.6 | +3.7 | 1,738 | 1,796 |
| Nova Scotia | 51,983 | 11,800 | 12,464 | 20.5 | 21.7 | +1.2 | 2,607 | 2,575 |
| Prince Edward Island | 7,090 | 347 | 359 | 5.8 | 6.0 | +0.2 | 401 | 406 |
| Newfoundland and Labrador | 20,290 | 360,671 | 372,526 | 90.7 | 93.7 | +3.0 | 2,398 | 2,767 |
| Yukon | 6,411 | 440,922 | 445,302 | 96.8 | 97.7 | +1.0 | 69 | 115 |
| Northwest Territories | 7,173 | 1,267,294 | 1,265,403 | 99.2 | 99.1 | -0.1 | 983 | 966 |
| Nunavut | 1,097 | 2,007,658 | 2,009,702 | 99.9 | 100.0 | +0.1 | 15,797 | 15,818 |

## Findings

- **NRN gives more roadless land than OSM almost everywhere** (+0 to +8 pp):
  OSM maps resource and low-use roads that NRN omits. BC is the extreme: NRN
  holds 91,219 km against 735,796 km in the merged layer (note 04), so NRN
  misses most BC resource roads and its roadless figure (89.7%) is not a usable
  estimate. QC (+5 pp), NB, NL and AB show the same pattern. NRN is a floor on
  road length, and so a ceiling on roadless area, wherever it lacks resource roads.
- **Edition age varies widely.** BC 14.0, MB 6.0 and NL 7.0 are
  packaged files dated October 2018; SK 15.0 is dated February 2025. The
  newest `REVDATE` is 2010 (NL), 2012 (MB), 2023 (PE) and 2024 to 2025
  elsewhere (BC and SK have no usable `REVDATE`). MB and NL are therefore
  comparable to OSM 2021 only loosely; the NRN there is older than the OSM snapshot.
- **Ontario and Saskatchewan agree with OSM** (within 0.6 pp), where both are
  reasonably complete. Nova Scotia agrees within 1.2 pp (note 06).
- **The paper's Table 4 values for these provinces are not in our notes**, so
  no comparison with the paper was made beyond NS (note 06) and the NT and NU
  road length above. That comparison needs the paper's tables entered by hand.

## BC Digital Road Atlas

`bcdra_roadless.py [--strict]`, DRA Master Partially-Attributed Roads, full
province geodatabase (258 MB) downloaded anonymously from the BC object store,
edition stamped 2026-10-30. Licence is "Access Only", free of charge, not an
open licence (note 02); not resolved. The layer has 1,880,540 segments and
756,161 km. The attribute names differ from the catalogue: the class field is
`RD_CLASS`, with `FEAT_TYPE` and `RD_SURFACE`.

Default filter is the paper's DRA exclusions mapped to `RD_CLASS`: ferry,
driveway, pedestrian, proposed, runway, water. `--strict` also drops trail
(36,806 km) and `RD_SURFACE` decommissioned or rehabilitated.

| BC source | Road km | Roadless km2 | Roadless % | Patches |
| --- | --- | --- | --- | --- |
| NRN 14.0 (2018) | 91,219 | 823,011 | 89.7 | 3,748 |
| OSM 2021 | not recorded | 746,876 | 81.4 | 5,679 |
| DRA, paper exclusions | 739,084 | 494,471 | 53.9 | 11,358 |
| DRA, strict | 702,313 | 502,908 | 54.8 | 11,481 |

- The DRA total (739,084 km) is 6% under the paper's DRA figure for BC (788,946
  km), a newer edition and different exclusions being possible causes (unchecked).
- BC roadless area is 28 points lower with the DRA than with OSM and 36 lower
  than with the NRN. OSM and the NRN both miss most BC resource roads, so
  their BC figures should not be used. The DRA is the only one of the three
  that is plausibly complete, but it has not been checked against imagery, and
  its roads include old and overgrown ones (overgrown is 44,613 km and stays
  in both variants).
- The filter choice matters little here: dropping trails and decommissioned
  roads adds 0.9 points. Class `unclassified` (304,854 km) is kept; it is not
  an exclusion in the paper.
- Run time is about 15 minutes per variant, because of the 1.8 million
  segments. This is the first input where tiling or a simplified buffer may be
  worth considering.
- The paper's BC roadless area is not in our notes, so no comparison with it.

## Harmonization pattern for further datasets

A new dataset needs only a loader: read the road layer, drop non-vehicle
classes with an explicit documented list, reproject to EPSG:3347, return a
GeoDataFrame. `roadless_patches`, `summarize`, the boundary and the resumable
runner are shared. `nrn_roadless.py` (about 30 lines) is the template; the
runner selects the source by label (`nrn` or a snapshot date). The DRA loader
(`bcdra_roadless.py`) follows the same shape with its own filter and a
standalone entry point. The loader test
is in `tests/test_roadless.py`.

## Limits

- The DRA is not archived either; record the edition with results.
- No NRN edition is archived at the download URL, so a rerun gets whatever is
  current; record the edition (`NRN_<prov>_<ed>_GPKG_en.gpkg`) with results.
- The NRN licence (OGL-Canada per the catalogue) was not read in full.
- Nothing is checked against imagery.
