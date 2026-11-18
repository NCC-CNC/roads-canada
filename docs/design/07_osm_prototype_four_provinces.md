# OSM roadless-area prototype: BC, AB, ON and QC (issue #3)

Extends `05_osm_prototype_nova_scotia.md`. Same script, same method, run on the
other four provinces in Table 4 of Poley et al. (2022).

## Inputs

- OSM: Geofabrik 1 January 2021 snapshots (`-210101-free.shp.zip`).
- Boundary: Statistics Canada 2016 provincial boundary
  (`lpr_000b16a_e.shp`, shipped with the Poley data compilation under
  `data/external/poley2022/`), filtered on PRUID (BC 59, AB 48, ON 35, QC 24).
  Its land areas match the paper's "Total area" column exactly, so it is the
  best available stand-in for the paper's mask. On Nova Scotia it also matched
  (57,534 km2). geoBoundaries was not run for these provinces.
- No code changes. Projection EPSG:3347, 1 km buffer, same OSM exclusion list.

## Table 4 targets, checked against the page image

Three cells lost leading digits in the PDF itself (the page image shows the
same gaps, so this is damage in the source, not in text extraction). They are
reconstructed from the percent cover and from mean patch size times patch
count, and agree on all three:

| Cell | As printed | Reconstructed | Check |
| --- | --- | --- | --- |
| AB OSM roadless km2 | 63,598 | 363,598 | 57% of 639,936 is 364,765; 44.3 x 8,217 is 364,000 |
| AB ABHFP roadless km2 | 99,382 | 299,382 | 47% of 639,936 is 300,770; 32.1 x 9,332 is 299,560 |
| ON GRIP roadless km2 | 02,546 | 902,546 | 92% of 980,243 is 901,824; 164.3 x 5,495 is 902,830 |

Only the AB OSM cell is used as a target below. The other two are not OSM.

## Result (OSM 2021-01-01 snapshot, StatCan 2016 boundary)

| Province | Roadless km2 | Paper km2 | Diff | Percent | Paper % | Patches | Paper patches |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC | 746,876 | 743,268 | +0.5% | 81.4 | 81 | 5,679 | 5,752 |
| AB | 362,751 | 363,598 (reconstructed) | -0.2% | 56.7 | 57 | 8,070 | 8,217 |
| ON | 744,338 | 743,338 | +0.1% | 75.9 | 76 | 9,893 | 9,509 |
| QC | 1,274,859 | 1,273,366 | +0.1% | 86.4 | 86 | 8,176 | 8,048 |

| Province | Mean km2 | Paper mean | Median km2 | Paper median | Max km2 | Paper max |
| --- | --- | --- | --- | --- | --- | --- |
| BC | 131.5 | 129.2 | 0.2 | 0.23 | 174,909 | 174,663 |
| AB | 45.0 | 44.3 | 1.2 | 1.26 | 87,956 | 88,028 |
| ON | 75.2 | 78.2 | 0.1 | 0.09 | 530,080 | 530,104 |
| QC | 155.9 | 158.2 | 0.4 | 0.40 | 818,243 | 818,325 |

Total area (land) in each run equals the paper's "Total area" column (BC
917,732; AB 639,936; ON 980,243; QC 1,476,348 km2).

## Findings

- Roadless area is within 0.5% of the paper in all four provinces, tighter
  than Nova Scotia's 1 to 2%. Percent cover rounds to the paper's value in all
  four.
- Patch count, mean, median and maximum also agree closely (patch count within
  4%, median and maximum nearly exact). With this boundary the large-province
  shape metrics reproduce, which supports the view that the Nova Scotia patch
  count gap comes from the land mask and coastline, not the method.
- The OSM 2021-01-01 snapshot is a close enough proxy for the paper's
  April 2021 extract at provincial scale.

## Resources

Peak memory and wall time on the 16 GB, 16-core workstation:

| Province | Roads kept | Wall time | Peak RSS |
| --- | --- | --- | --- |
| BC | 325,531 | 1.5 min | 2.2 GB |
| AB | 375,992 | 1.2 min | 2.2 GB |
| ON | 762,338 | 2.3 min | 4.1 GB |
| QC | 421,008 | 1.4 min | 2.7 GB |

The vector buffer and union approach in ADR 0002 held up for the largest
provinces. Ontario's 4.1 GB is the high-water mark; a national run would need
to go province by province or reconsider the raster fallback.

## Practical notes

- `fetch_inputs.py` used to write the download straight to its final name, so
  an interrupted download left a truncated zip that was later treated as
  complete (it happened once with Quebec). It now downloads to a `.part` file
  and renames on success. Files fetched before that change may still be
  truncated; check with `unzip -tq` or delete and refetch.
