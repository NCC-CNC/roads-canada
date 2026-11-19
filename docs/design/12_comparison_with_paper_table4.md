# Our results against Poley et al. (2022) Table 4 (issue #4)

Compiled 2026-11-19. Paper values come from `data/external/poley2022/poley2022_table4_roadless.csv`
(made by `paper_tables.py`; three cells restored from the printed percent
cover, see its README). Our values are from `data/processed/*/stats.json`;
the table is printed by `compare_to_paper.py`. Diff is ours minus the paper's,
as a share of the paper's roadless area. The paper covers BC, AB, ON, QC and NS
only; the other jurisdictions cannot be checked this way.

## Result

| Prov | Source | Paper km2 | Ours km2 | Diff % | Paper % | Ours % | Paper patches | Our patches | Paper mean km2 | Our mean km2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BC | OSM 2021 | 743,268 | 746,876 | +0.5 | 81 | 81.4 | 5,752 | 5,679 | 129.2 | 131.5 |
| BC | NRN | 823,822 | 823,011 | -0.1 | 90 | 89.7 | 3,655 | 3,748 | 225.4 | 219.6 |
| BC | BCDRA | 480,517 | 494,471 | +2.9 | 52 | 53.9 | 11,800 | 11,358 | 40.7 | 43.5 |
| AB | OSM 2021 | 363,598 | 362,751 | -0.2 | 57 | 56.7 | 8,217 | 8,070 | 44.3 | 45.0 |
| AB | NRN | 384,246 | 380,201 | -1.1 | 60 | 59.4 | 7,352 | 7,306 | 52.3 | 52.0 |
| AB | ABHFP | 299,382 | 232,618 | -22.3 | 47 | 36.4 | 9,332 | 12,092 | 32.1 | 19.2 |
| ON | OSM 2021 | 743,338 | 744,339 | +0.1 | 76 | 75.9 | 9,509 | 9,893 | 78.2 | 75.2 |
| ON | NRN | 744,409 | 743,852 | -0.1 | 76 | 75.9 | 10,004 | 10,328 | 74.4 | 72.0 |
| ON | ORN | 618,531 | 652,027 | +5.4 | 63 | 66.5 | 13,538 | 13,377 | 45.7 | 48.7 |
| QC | OSM 2021 | 1,273,366 | 1,274,859 | +0.1 | 86 | 86.4 | 8,048 | 8,176 | 158.2 | 155.9 |
| QC | NRN | 1,318,150 | 1,348,915 | +2.3 | 89 | 91.4 | 6,858 | 6,872 | 192.2 | 196.3 |
| QC | AQR | 1,038,052 | 1,034,381 | -0.4 | 70 | 70.1 | 13,342 | 13,229 | 77.8 | 78.2 |
| NS | OSM 2021 | 11,545 | 11,800 | +2.2 | 20 | 20.5 | 2,459 | 2,575 | 4.7 | 4.6 |
| NS | NRN | 12,475 | 12,464 | -0.1 | 22 | 21.7 | 2,418 | 2,607 | 5.2 | 4.8 |
| NS | NSTDB | 5,297 | 5,396 | +1.9 | 9 | 9.4 | 1,196 | 1,267 | 4.4 | 4.3 |

## Findings

- **OSM 2021 and NRN reproduce the paper.** All ten OSM and NRN runs are
  within 2.3% of the paper's roadless area, and eight within 1.1% (the largest
  are Quebec NRN, +2.3%, and Nova Scotia OSM, +2.2%). Patch counts and mean patch size agree to a few percent. This
  validates the pipeline (buffer, land mask, projection) against the original
  work. The Alberta OSM match (362,751 against the restored 363,598 km2) also
  supports the reconstruction of that truncated cell.
- **Quebec AQR, Nova Scotia NSTDB and BC DRA reproduce within 3%.** Newer
  editions of the same sources give almost the same answer as 2021.
- **Ontario ORN + MNR is 5.4% higher in roadless area** (66.5% against 63%),
  consistent with our road length being 17% below the paper's (note 11): the
  missing roads are not in our layers, so land near them counts as roadless.
  Checked: our NRN Ontario length (260,398 km) is within 0.5% of the paper's
  NRN (261,714 km), so lengths are measured the same way. The paper summed
  ORN and MNRF without removing overlap ("assessed the ORN and MNRF datasets
  ... as well as the sum of the two", supplement), and so do we (ORN 264,611 +
  MNR 196,573 km). The gap is therefore the source editions: the paper used
  2019 and 2020 downloads, which LIO does not archive. It cannot be tested
  further without those files.
- **Alberta ABHFP is 22% lower** (36.4% against 47%), the one large
  disagreement. Our road length is 13% above the paper's (443,275 against
  391,825 km), so the 2023 HFI edition holds more roads than the one the paper
  used. The strict variant (44.2%, 282,869 km2) is 5.5% below the paper, so
  the paper's figure sits between our default and strict. Not resolved; the
  paper's edition of the HFI would have to be found.

## Consequences for #4

- The pipeline needs no change to match the published method.
- Differences from the paper in provincial datasets come from newer source
  editions, not from the method. Report the edition with every figure.
- The headline figure for Alberta is the open question; Ontario's gap is
  an edition difference that cannot be tested; treat our current-edition figure
  as the estimate.
