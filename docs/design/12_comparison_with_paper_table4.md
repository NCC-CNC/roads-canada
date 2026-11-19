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
  disagreement. Mostly explained, see "Alberta gap" below.

## Alberta gap

Our road length is 13% above the paper's (443,275 against 391,825 km). The 2023
HFI metadata (section 4.3) says it added two road types, ROAD-VEGETATED
(34,356 km) and ROAD-VEGETATED-OSE (8,507 km), access dispositions with no
detectable road surface. `abhfi_diagnostics.py` and a run without those two
types give:

| Variant | Road km | Roadless % | Patches | Mean km2 | Largest km2 | Over 1,000 km2 |
| --- | --- | --- | --- | --- | --- | --- |
| Paper (ABHFP) | 391,825 | 47.0 | 9,332 | 32.1 | 91,101 | 32 |
| 2023, paper exclusion | 443,275 | 36.4 | 12,092 | 19.2 | 32,128 | 23 |
| 2023, minus the two new types | 401,342 | 43.7 | 9,780 | 28.6 | 36,877 | 32 |
| 2023, strict (also minus winter) | 398,892 | 44.2 | 9,670 | 29.3 | 75,739 | 26 |

The paper's roadless cell is restored from the printed 47% (note 04); its mean
patch size times patch count (299,557 km2) agrees with it.

- **Length is a weak guide.** A road beside an existing one removes little new
  land; an isolated one removes up to 2 km2 per km. Unique roadless loss per
  class (land that is roadless only if the class is absent): vegetated 1.17
  km2 per km (39,196 km2 from 7.6% of road length), truck trail 0.55,
  vegetated-OSE 0.46, winter 0.70, unimproved 0.27, gravel 0.12, paved and
  other 0.06. Vegetated roads are also the most isolated class (median 780 m
  to the nearest other class, 25% beyond 2 km).
- **The two new types explain most of the gap** (36.4 to 43.7%, and the
  patch count and the count over 1,000 km2 return to the paper's range).
- **The rest is one large block.** The paper's largest patch is 91,101 km2;
  ours is 36,877 km2 (75,739 in strict). In the strict run's largest patch,
  294 km of ROAD-WINTER (source ABMI22, no year) alone cut it from 75,739 to
  36,879 km2; vegetated roads add 5,529 km (52,317 alone) and vegetated-OSE
  4,446 km (70,002 alone). A block that intact in the paper's 2018 edition
  was split in 2023 by roads that edition probably did not hold.
  That is an inference: only the 2018 edition itself can confirm it.
- **Not recoverable from the data.** Only 3% of road segments carry a `YEAR`
  and 377,000 km carry `SOURCE` ABMI22 (the 2022 rewrite), so a 2018 cut
  cannot be rebuilt. The 2018 edition would need requesting from ABMI.

## Consequences for #4

- The pipeline needs no change to match the published method.
- Differences from the paper in provincial datasets come from newer source
  editions, not from the method. Report the edition with every figure.
- The headline figure for Alberta is a rule choice (note 15): default, strict or
  minus the new types. Ontario's gap is
  an edition difference that cannot be tested; treat our current-edition figure
  as the estimate.
