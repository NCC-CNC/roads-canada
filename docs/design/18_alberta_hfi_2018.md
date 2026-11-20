# Alberta HFI 2018 reproduces the paper (issue #4)

Run 2026-11-20 with `abhfi_roadless.py --2018` on the ABMI Human Footprint
Inventory 2018 (v1, `HFI_2018_v1.gdb`, last modified 2020-05-15), supplied by
the paper's lead author. Layer `o03_Roads_Centerlines_HFI2018` (1,080,346
lines). Same method as note 12 (1 km buffer, StatCan 2016 land mask,
EPSG:3347). Nothing is checked against imagery.

## Result

| Variant | Road km | Roadless % | Patches | Mean km2 | Largest km2 | Over 1,000 km2 |
| --- | --- | --- | --- | --- | --- | --- |
| Paper (ABHFP) | 391,825 | 47.0 | 9,332 | 32.1 | 91,101 | 32 |
| 2018, paper exclusion | 386,824 | 46.5 | 9,209 | 32.3 | 90,931 | 32 |
| 2018, strict (also minus winter) | 381,778 | 47.6 | 8,990 | 33.9 | 138,286 | 25 |
| 2023, paper exclusion (note 12) | 443,275 | 36.4 | 12,092 | 19.2 | 32,128 | 23 |

With the paper's exclusion (airport runways only) the 2018 edition lands within
0.5 points of the paper on roadless share, within 1.4% on patch count and
within 0.2% on the largest patch. This confirms note 12's inference: the gap
between our 2023 run and the paper is an edition effect, not a method
difference. The 2018 file holds 56,000 km less road than 2023.

## Schema differences from 2023

- `FEATURE_TY` has 26 values and no `ROAD-VEGETATED` or `ROAD-VEGETATED-OSE`.
  It has `TRUCK-TRAIL`, `TRAIL-ATV`, `ROAD-WINTER-ACCESS`, `ROAD-WINTER-ROAD`
  and `FORD-WINTER-XING`.
- Strict for 2018 therefore drops the three winter types only.
- Every row carries `YEAR` 2018 and `SOURCE` ABMI18, so a 2018 cut is clean,
  unlike 2023 (note 12).
- The geodatabase CRS is NAD83 / Alberta 10-TM (Forest); the loader reprojects.

## Consequences

- Alberta now validates against Table 4. Note 12's "mostly explained" becomes
  explained.
- The headline (ADR 0004) is still the current edition. The 2023 run is the
  up-to-date figure; the 2018 run is the like-for-like check against the paper
  and the baseline for change over time (2018 to 2023: 46.5% to 36.4%; note 12
  attributes most of that to road types mapped in 2023, not to new construction). Which of the
  two the project reports for Alberta is the owner's call.
- Alberta headline (decided 2026-11-19, owner): report the current edition
  (2023) as the headline, and show the 2018 run as the figure comparable with
  the paper.

## Licence (read 2026-11-20, for issue #32)

- **Metadata section 9** (2018 PDF) splits the data into three classes:
  proprietary-sourced ("shall not be used or reproduced in whole or in part or
  in any form"), open-sourced, and ABMI-sourced. The last two may be
  reproduced in any form for educational, data collection or non-profit
  purposes with acknowledgement of the source; no resale without written
  permission from the ABMI.
- **We cannot tell which class a road row belongs to.** In the roads layer
  1,047,791 of 1,080,346 lines (373,611 of 392,116 km) have a null `SOURCE`;
  the rest are ABMI00, 16, 17 and 18. Open-sourced base features are tagged
  BASEFE elsewhere in the metadata (Government of Alberta Open Data Licence),
  and no road row carries that tag.
- **ABMI Terms and Conditions** (abmi.ca/abmi-home/terms-and-conditions): the
  ABMI must be acknowledged as the source; no licence is named; no general
  redistribution terms for data; products are provided as is.
- **What this allows us:** publishing area statistics and maps derived from the
  data, with acknowledgement, is within the non-profit terms. Redistributing the
  roads layer itself is not cleared, and may be barred for any proprietary part.
  This project does not redistribute it (`data/raw/` is ignored).
- **Citation** (metadata section 8): ABMI Human Footprint Inventory:
  Wall-to-Wall Human Footprint Inventory. 2018. Edmonton, AB: Alberta
  Biodiversity Monitoring Institute and Alberta Human Footprint Monitoring
  Program, March 2020.
- Open question for the ABMI: which road rows, if any, are proprietary-sourced.
