# 03 The Poley 2021 Linear Features Compilation

Exploration of the road data compiled for Poley et al. (2022), for use as a
baseline and validation target. Compiled 2026-11-17 from the compilation's own
metadata PDFs and `ogrinfo` queries. Lengths are planar, from `Shape_Length`
in EPSG:3347. Nothing here has been checked against imagery.

## What it is

A folder of about 20 GB held locally in
`data/external/poley2022/canada_linear_features/` (gitignored). It is the
2021 Canada Linear Features Data Compilation, assembled by L. Poley with
R. Schuster and J. Ray, and holds three datasets plus a boundary file:

| Part | Content | Size | Notes |
| --- | --- | --- | --- |
| Canada Roads Merged Dataset | Roads for every province and territory, merged from the best available sources | 13 GB as shapefiles, 2 GB as `roads.gdb` | 7,138,352 features, about 3.18 million km |
| OSM trails | OSM features with `fclass` bridleway, cycleway, footway, path, pedestrian or steps | 626,660 features | The classes the paper removed from roads; has `osm_id` |
| Seismic lines | AB, BC (three layers), NT, SK, YK, plus a merged national file | 4.6 GB | See the seismic section |
| Boundaries | Statistics Canada 2016 provincial and territorial polygons | 13 polygons | Usable as a clip layer |

The compilation is not a release of the paper's results. The authors'
roadless-area layers and code are not published with the paper (see
`02_data_sources.md`).

## Do not use `all_roads_canada.shp`

The national shapefile is truncated. Its `.dbf` is 2,147,482,869 bytes, at the
2 GiB shapefile limit, and it holds 2,091,025 features, about 29% of the
total. The merged national seismic file hits the same limit and also failed
its CRC check on extraction. The 13 per-province shapefiles sum to exactly
7,138,352 features, matching `roads.gdb` (layer `roads_merge`), so use either
of those.

## Schema

Every layer has `SOURCE_DS`, `ORIG_CLASS`, `ORIG_ID`, `GEN_CLASS` and
`FLII_IMP`. BC adds `ID`. The geodatabase adds `ID` and `Shape_Length`. The
projection is NAD83 / Statistics Canada Lambert (EPSG:3347).

- `SOURCE_DS`: the source dataset, for example NRN, BC_DRA, OSM.
- `ORIG_CLASS` and `ORIG_ID`: the class and identifier in the source dataset.
- `GEN_CLASS`: the class generalized to the nearest OSM class.
- `FLII_IMP`: a fixed lookup from `GEN_CLASS`, taken from the Forest
  Landscape Integrity Index paper (Graham et al. 2020).

There are no construction, closure or status fields.

## Contents by source

| `SOURCE_DS` | Features | km | Dominant classes (share of km) |
| --- | --- | --- | --- |
| NRN | 1,512,078 | 858,951 | secondary 53%, residential 18%, track 14% |
| BC_DRA | 1,974,333 | 735,413 | unclassified 50%, track 39% |
| AQRESEAU | 926,034 | 483,025 | track 91% |
| OMNRF | 443,549 | 270,366 | track 99% |
| ORNE | 523,020 | 210,235 | residential 65%, primary 18% |
| AB_HFP | 451,597 | 152,068 | track 83% |
| OSM | 448,098 | 95,692 | service 43%, track 33% |
| MLI_20K_TL | 283,817 | 84,096 | track 82% |
| SK_HFP | 160,552 | 74,578 | track 100% |
| NSTDB | 198,373 | 66,927 | track 87% |
| NB_FORESTROADS | 123,109 | 64,359 | not broken out |
| STATSCAN | 46,197 | 36,826 | track 45%, residential 41% |
| Other (NB added, NL, BEAD 2010 and 2015, ORNE_RESREC, PEI, Yukon) | 47,595 | 48,361 | resource-road layers |

Findings:

- OSM supplies only about 3% of the length. Most of the baseline is
  government data, so an OSM-only pipeline will not reproduce it. The gap is
  itself a measure of what OSM misses.
- `track` is about half of all length (1.61 million km). The resource-road
  layers arrive almost entirely as `track`.

## Data quality issues

- `GEN_CLASS` casing is mixed. Motorway, Primary, Residential, Secondary,
  Service, Track, Trunk and Unknown each also appear in lowercase.
- Typos: `unclassifed` (940,943 features, 368,735 km) beside `unclassified`,
  and `seconday` (12,258 features) beside `secondary`.
- `_link` classes use both spaces and underscores (`primary link`,
  `secondary_link`), and `bus guideway` variants appear.
- Statistics Canada rows carry numeric codes in `ORIG_CLASS` with `GEN_CLASS`
  of Unknown.
- Half of BC DRA is `unclassified`, so the DRA's own class field is the
  better source there.
- The authors warn of residual duplicate lines from slightly offset sources,
  dangles, and roads that are no longer passable.
- Any pipeline using this baseline needs a class-normalization step first.

## How it was merged

Per the 2021 metadata, each jurisdiction was merged in priority order. Each
lower-priority source was erased inside a buffer (15 to 80 m, chosen per
dataset and region) around the layers already merged, then its road ends were
extended 30 to 150 m to rejoin intersections. A manual scan against imagery
followed each step. The authors state that "no general set of rules could be
developed" and that the process "required significant manual input".

| Jurisdiction | Sources, highest priority first |
| --- | --- |
| BC | DRA, OSM |
| AB | NRN, AB HFP, OSM, Statistics Canada |
| SK | NRN, Statistics Canada, OSM, SK HFP |
| MB | NRN, MLI, OSM, Statistics Canada, BEAD 2015, BEAD 2010 |
| ON | ORNE, OMNRF, ORNE resource and recreation, NRN, Statistics Canada, OSM |
| QC | NRN, AQReseau+, OSM, Statistics Canada |
| NB | NRN, NB Forest Roads (plus roads digitized by hand from imagery), OSM, Statistics Canada |
| NS | NRN, NSTDB, OSM |
| NL | NRN, OSM, NL Resource Access Roads, Statistics Canada |
| PE | NRN, PEI Forest Roads |
| YT | NRN, Yukon Forest Resource Roads, OSM, Statistics Canada |
| NT | NRN, OSM, Statistics Canada, BEAD 2015, BEAD 2010 |
| NU | NRN, OSM |

## Seismic lines and dates

The seismic layers keep their source attributes (from the compilation's
seismic metadata and the file schemas). Date-bearing fields by layer:

| Layer | Date fields |
| --- | --- |
| AB (ABMI Human Footprint) | `YEAR` |
| YK | `YEAR` |
| NT (NEB) | `Start_Year`, `End_Year`, `ActualStar`, `ActualEndD` |
| BC plans 1996 to 2004 | `APPL_RECD`, `COMP_DATE` |
| BC plans 2002 to 2006 | `APPL_RECD`, `COMP_DATE` |
| BC permits (2006 on) | `STAGE_EFF_`, `STATUS` |
| SK | none (no attributes) |

These are the only dated linear features in the compilation. Value coverage
and completeness of these fields have not been tallied yet.

## Licence and availability

The metadata calls the dataset "available via private share only", with a
public release by Wildlife Conservation Society Canada planned and a "how to
cite" URL still a placeholder. The stated use constraint is free of charge
with no warranty. No licence is named. Component licences are mixed (see
`02_data_sources.md`), and BC DRA is "Access Only". Do not redistribute any
part of it, or derived products, until this is resolved with the co-authors
and WCS Canada.

## Implications for the pipeline

1. The baseline is mostly non-OSM data, so issue #3 should validate an OSM-only
   pipeline against the OSM rows of Table 4 in the paper, not against this
   layer. Compare against this layer separately, as a measure of OSM
   completeness.
2. For issue #4, the largest non-OSM contributors are BC DRA, AQReseau+,
   OMNRF and AB HFP. The per-source cleaning rules in `02_data_sources.md` and
   the class mapping here are a starting point for harmonization.
3. The manual merge is the main obstacle to a scripted update. A scripted
   approach would use the same priority order and buffer-erase logic, without
   the visual scan, and would need a way to measure what the scan removed.
4. The OSM trails file with `osm_id`, and `ORIG_ID` on OSM rows, are possible
   keys for OSM-history work in issue #5.

## Open questions

- Which of the merged layer's OSM rows use the 2021 Geofabrik extract exactly?
- Year coverage and completeness of the seismic layers.
- Whether the roadless-area layers behind Table 4 still exist, and where.
- Release status and licence of the compilation.
