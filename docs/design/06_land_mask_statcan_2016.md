# Land mask: StatCan 2016 provincial boundary reproduces the paper (Nova Scotia)

Follows `05_osm_prototype_nova_scotia.md`, which left the paper's land mask as
an open question. Status: experiment on one province; not yet the pipeline
default.

## Finding

Using the Statistics Canada 2016 provincial boundary instead of the
geoBoundaries polygon brings the patch metrics close to Table 4 of Poley et al.
(2022). Same method, same 2021-01-01 Geofabrik snapshot, Nova Scotia only,
compared with the paper's OSM row:

| Metric | Paper (OSM, April 2021) | StatCan 2016 (local file) | geoBoundaries |
| --- | --- | --- | --- |
| Land area, km2 | 57,534 | 57,534 | not recorded |
| Roadless area, km2 | 11,545 | 11,800 | 11,728 |
| Percent roadless | 20 | 20.5 | 20.5 |
| Patches | 2,459 | 2,575 | 3,816 |
| Mean patch, km2 | 4.7 | 4.6 | not recorded |
| Median patch, km2 | 0.24 | 0.2 | not recorded |
| Maximum patch, km2 | 1,266 | 1,274 | not recorded |

- Land area matches the paper to the km2, which is strong evidence the paper
  used this boundary (or one derived from it).
- Patch count falls from 3,816 to 2,575, within 5% of the paper. The coastal
  slivers flagged in note 05 came from the geoBoundaries coastline, not from
  the method.
- Roadless area is 2.2% above the paper, a little further than geoBoundaries.
  The April 2021 snapshot is unavailable (Geofabrik keeps 1 January snapshots),
  so a residual gap is expected.
- Patch count, mean and median are now usable as secondary checks, not only
  roadless area and percent.

## Evidence the paper does not name its mask

The paper and its supplement give the buffer (1 km both sides), software
(ArcMap 10.7) and projection (NAD83 CSRS, Lambert Conformal Conic), but name no
boundary file and describe no coastline handling. The identification above is
an inference from the land-area match, not a statement by the authors.

## The boundary file

`data/external/poley2022/canada_linear_features/Stats Canada Country Shapefile/lpr_000b16a_e.shp`
holds 13 provincial and territorial polygons (field `PRUID`; Nova Scotia is
12) in the file's Lambert Conformal Conic projection. It ships in the Poley
2021 compilation (see `03_poley_baseline_dataset.md`).

`lpr_000b16a_e` is the 2016 **Cartographic** Boundary File: clipped to the
detailed coastline (Nova Scotia is 666 polygons, 189,811 vertices, 54 MB for
all of Canada). The matching **Digital** Boundary File is `lpr_000a16a_e`,
which extends into coastal water (Nova Scotia is 2 polygons, 76,209 km2, 2 MB).
Only the cartographic file gives the paper's 57,534 km2, so it is the one to
use. Downloading from StatCan: Provinces/territories, Cartographic Boundary
File, ArcGIS (.shp), English.

## Provenance and licence

Decision recorded in `docs/decisions/0003-statcan-boundary-default.md`: the
StatCan file is the default, geoBoundaries the fallback.

Licence (checked 2026-11-18 at <https://www.statcan.gc.ca/en/reference/licence>):
the Statistics Canada Open Licence grants a worldwide, royalty-free,
non-exclusive right to use, reproduce, publish and freely distribute the
Information (data files and maps included), on conditions: reproduce it
accurately, do not misrepresent it or its source, do not link it with other
data to identify individuals or organizations, and do not use Statistics
Canada's name or logos without authorization. The boundary files page and the
download carry no licence text; the licence applies through the 2016 reference
guide ("Use of this publication is governed by the Statistics Canada Open
Licence Agreement"). A third-party mirror of the guide lists OGL-Canada 2.0
instead; both are permissive, but only the first is from Statistics Canada.

Attribution to use:

- Redistributing the file: "Source: Statistics Canada, Boundary Files, 2016
  Census, Catalogue no. 92-160-X. Reproduced and distributed on an 'as is'
  basis with the permission of Statistics Canada."
- Outputs derived from it (roadless-area results): "Adapted from Statistics
  Canada, Boundary Files, 2016 Census, Catalogue no. 92-160-X. This does not
  constitute an endorsement by Statistics Canada of this product."

Handling: the file stays a manual download into `data/raw/` (StatCan returns
403 to automated clients; do not work around it) and is not committed, because
nothing needs it in the repo. The licence would permit committing it with the
first attribution.

## Next steps

- BC, AB, ON and QC are being run with this boundary (see the province
  results note) to check the pattern holds beyond Nova Scotia.
- Done: `fetch_inputs.py boundary <province>` extracts the province from the
  StatCan zip by `PRENAME` (ADR 0003).
- Revisit whether a minimum patch size is still wanted (deferred in note 05);
  the sliver problem largely disappears with this mask.
