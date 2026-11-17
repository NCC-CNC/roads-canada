# OSM roadless-area prototype: Nova Scotia validation (issue #3)

## Method

`src/roadless/osm_roadless.py` follows Poley et al. (2022): drop OSM `fclass`
bridleway, cycleway, footway, path, pedestrian and steps; buffer the remaining
roads 1 km; subtract the buffer from the provincial land boundary; explode the
remainder into patches. Projection is EPSG:3347 (the paper used an unstated
Lambert Conformal Conic). Inputs are the Geofabrik Nova Scotia shapefile
extract (fetched November 2026) and the Nova Scotia polygon from geoBoundaries
CAN ADM1 (StatCan-derived, licence listed as Open Government Canada 2.0). Runtime is about
one minute.

## Result against Table 4 (OSM row)

| | Natural Earth 10m | geoBoundaries | Paper |
|---|---|---|---|
| Roadless area (km2) | 10,900 | 10,872 | 11,545 |
| Percent roadless | 19.1 | 19.0 | 20 |
| Patches | 2,006 | 3,726 | 2,459 |
| Patches under 1 km2 | not tallied | 81% | almost 77% |

## Matching the paper's OSM date

Geofabrik keeps public 1 January snapshots back to 2014 (`-YYMMDD-free.shp.zip`),
so the 2021 extract is not wholly lost, though April 2021 is unavailable.
Same method and geoBoundaries boundary:

| OSM snapshot | Roads kept | Roadless km2 | Percent | Patches |
|---|---|---|---|---|
| 2021-01-01 | 108,638 | 11,728 | 20.5 | 3,816 |
| 2022-01-01 | 111,894 | 11,625 | 20.3 | 3,817 |
| 2026-11 | 139,887 | 10,872 | 19.0 | 3,726 |
| Paper (April 2021) | | 11,545 | 20 | 2,459 |

Roadless area is within about 1 to 2% of the paper using a 2021 snapshot, so
the earlier 6% gap was OSM growth, not the method. Patch count stays high
because of coastal slivers (see below).

## Findings

- With the current extract, roadless area is about 6% below the paper under
  both boundaries. The 2021 snapshots remove most of that gap (table above), so
  OSM growth is the main cause.
- Patch count depends strongly on coastline detail. The detailed boundary adds
  many sliver patches (median patch about 0 km2). Counting only patches above
  0.01 km2 gives 2,331, near the paper's 2,459, but the paper states no minimum
  patch size, so this is a coincidence until shown otherwise.
- The paper's mean patch size (11,545 / 2,459, about 4.7 km2) and its
  statement that almost 77% of Nova Scotia patches are under 1 km2 are the
  better shape checks than raw patch count.
- April 2021 itself cannot be re-downloaded, but the 1 January 2021 and 2022
  snapshots bracket it. `02_data_sources.md` says daily extracts only; update it.

## How much the patch-count gap matters

On the 2021-01-01 snapshot, 3,075 of 3,816 patches are under 1 km2 and hold
only 363 of 11,728 km2 (3%). 1,923 of those touch the coastline, so most are
coastal slivers or small islands. Patches of at least 1 km2 number 741; the
paper implies about 565. Consequences:

- Roadless area and percent roadless are insensitive to slivers. Use them as
  the pass/fail validation metrics.
- Patch count, mean and median depend on the land mask. Report patches of at
  least 1 km2 as a secondary check, and do not expect an exact match.
- Change detection is unaffected, because the same mask is used on both dates.
- A proper test needs a rebuilt land mask (for example dropping islands or
  generalizing the coast before differencing), not clipping existing patches.

## Open questions

- Which land mask did the paper use (likely a provincial boundary clipped in
  ArcMap)? Unknown.
- Add a configurable minimum patch size? Deferred until the mask is settled.
