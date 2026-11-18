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

## Decision needed: provenance and licence

The pipeline currently fetches its boundary from a pinned geoBoundaries commit
(`fetch_inputs.py boundary`), which is reproducible and public. The StatCan
file is only available here through the compilation. Statistics Canada boundary
files are published under the Statistics Canada Open Licence (the 2016
reference guide in the download says use is governed by it; current terms at
<https://www.statcan.gc.ca/en/reference/licence>, not yet read). StatCan returned
403 to automated download earlier. Before making this the default:

1. Read the current Statistics Canada Open Licence terms. The boundary files
   page states no licence and the download has no licence file; the only
   statement is in the 2016 reference guide ("Use of this publication is
   governed by the Statistics Canada Open Licence Agreement"). Recorded in
   `02_data_sources.md` as unverified. Do not commit the file to the repo until
   confirmed.
2. The manual download from StatCan (Provinces/territories, Cartographic
   Boundary File, ArcGIS, English) is byte-identical to the copy in the Poley
   compilation (checked on the .shp, .dbf, .shx and .prj files), so either
   source works. Document it as a manual step; do not work around the 403.
   Cite as Statistics Canada, Boundary Files, 2016 Census, Catalogue no.
   92-160-X.
3. If it becomes the default, record it in an ADR and keep the geoBoundaries
   path as a fallback.

## Next steps

- BC, AB, ON and QC are being run with this boundary (see the province
  results note) to check the pattern holds beyond Nova Scotia.
- Add a boundary argument convention to `osm_roadless.py` documentation: the
  script takes any boundary file, so a province must be extracted first
  (filter `PRUID`; BC 59, AB 48, ON 35, QC 24).
- Revisit whether a minimum patch size is still wanted (deferred in note 05);
  the sliver problem largely disappears with this mask.
