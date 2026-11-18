# OSM change detection: design note and Nova Scotia feasibility test (issue #5)

## Question

Can OSM timestamps or snapshots identify roads added since a baseline, so
roadless-area refreshes are incremental and focus on remote land?

## Options

| Option | Timestamps | Access | Fit |
| --- | --- | --- | --- |
| Dated Geofabrik snapshots (1 January, 2014 onward) | No, but `osm_id` allows set differences | Public | Works now; yearly resolution |
| Geofabrik internal history extracts (`.osh.pbf`) | Yes, per object version | Needs an OSM login | Best for exact "added since date D"; not tested |
| Replication diffs (Geofabrik per-region daily; planet minutely, hourly, daily) | Yes | Public | Suited to a rolling refresh. Geofabrik daily diffs tested for New Brunswick, see below |

The free Geofabrik shapefile has no timestamp field, so the snapshot route
detects change only by comparing `osm_id` sets between two files. A way that
was edited but kept its id is not flagged as new (geometry extensions to an
existing way are missed), and a way deleted is flagged as removed.

## Feasibility test: Nova Scotia, 2021-01-01 vs 2022-01-01

`src/roadless/osm_change.py` runs the paper's method (1 km buffer, StatCan 2016
land mask, same class exclusions) on both snapshots and diffs them. Runtime is
about 80 seconds.

| Measure | Result |
| --- | --- |
| Roads kept, old / new | 108,638 / 111,894 |
| `osm_id` added / removed | 3,660 (794 km) / 404 |
| Added road length inside old roadless land | 41 km (5.2%) |
| Added ways touching an old patch of 100 km2 or more | 15 |
| Roadless area, old / new | 11,800 / 11,696 km2 (-104) |
| Patches, old / new | 2,575 / 2,577 |
| Roadless land lost (polygons) | 454 polygons, 110 km2 |

Incremental route: buffer only the added roads and subtract them from the old
patches. Result 11,702 km2 against 11,696 km2 from the full rebuild, a
difference of +6 km2 (0.05%). See "Three regions" below for what drives the gap.

## Findings

- Change is small, and where it falls varies by region (see below). In Nova
  Scotia about 95% of added road length is within 1 km of existing roads; in
  NB and NL a much larger share is in remote land. A refresh should report lost
  roadless polygons, not just totals.
- The incremental shortcut reproduces the full rebuild closely, so a refresh
  only needs to process new `osm_id`s (and removals, to recover area).
- Net change is sensitive to deletions and to OSM mapping effort, not only to
  real road building. Added roads in OSM can be mapping catch-up, not new roads.

## Recommendation

1. Use dated snapshots for the first change layer; they need no new tooling.
2. For a rolling refresh, use Geofabrik's per-region daily diffs plus a
   current regional extract for geometry (tested, see below). Only new ways
   need buffering; edits can be skipped. Deleted roads need an older extract.
   A history extract is only needed for exact edit dates.
3. Validate flagged remote additions against imagery or the NRN before
   reporting them as new roads.

## Not done

Only one region and one year pair. History extracts were assessed from
documentation, not run. Removed-road effect on the +6 km2 gap not
isolated.

## Scaling to other provinces

`src/roadless/run_regions.py` runs the baseline for many provinces without one
failure costing the rest: it verifies each zip before computing, writes a
`stats.json` done marker last, skips finished provinces on rerun, and logs
failures to `errors.log` while continuing. Checked on Nova Scotia (29 s, 20.5%
roadless, matching the earlier run), Nunavut (13 s) and Yukon (3 s); a missing
snapshot (404) logged an error for both provinces and exited 1.

Tested and rejected: a coarser buffer (`quad_segs` 4 or 2) was not faster on
Nova Scotia and overstated roadless area by 0.7% and 2.4%. Not yet built:
tiling, which is the next step if BC, ON or QC prove too slow or memory-heavy.
Their runtimes are untested through this runner.

## Three regions, 2021-01-01 vs 2022-01-01

| | Nova Scotia | New Brunswick | Newfoundland and Labrador |
| --- | --- | --- | --- |
| Ways added / removed | 3,660 / 404 | 5,592 / 467 | 3,016 / 192 |
| Added length (km) | 794 | 1,226 | 529 |
| Added length inside old roadless land | 41 km (5.2%) | 270 km (22.0%) | 188 km (35.5%) |
| Added ways touching a patch of 100 km2 or more | 15 | 91 | 80 |
| Roadless change (km2) | -104 | -533 | -284 |
| Roadless land lost, polygons / km2 | 454 / 110 | 662 / 534 | 435 / 305 |
| Incremental minus full rebuild (km2) | +6 | +35 | -10 |

The incremental gap has both signs, so one cause does not explain it. Removed
ways, which the shortcut ignores, push the incremental result below the full
rebuild (NL, -10). Ways that kept their `osm_id` but were extended or
re-routed are not flagged as added, which pushes it above (NS, NB). The earlier
statement that removals explain the Nova Scotia gap was wrong in sign and is
withdrawn. Both effects are small (at most 0.1% of roadless area here). A
refresh should also flag changed ways, which needs object versions or
timestamps (history extract or replication diffs), not the shapefile alone.
Neither cause was isolated by direct test.

## Replication diff test: New Brunswick, last 30 daily diffs

Geofabrik publishes a daily `.osc.gz` per region at
`download.geofabrik.de/<region>-updates/` (state file gives the latest
sequence number). Retention is about four months: sequence 4850 (2026-07-15)
existed, 4800 did not. `src/roadless/osm_diff_probe.py` fetched sequences
4946 to 4975 (2026-10-19 to 2026-11-17), stdlib XML parsing only. Cost: 1.9 MB
downloaded and 47 s, mostly network.

| Measure | Result |
| --- | --- |
| Road ways created / modified | 553 / 903 |
| Ways deleted (any type; deletes carry no tags) | 379 |
| Created ways fully drawable from the diffs alone | 374 of 553 (68%) |
| Modified ways fully drawable from the diffs alone | 76 of 903 (8%) |
| Drawable new roads | 95 km, of which 12 km (12.4%) inside 2021 roadless land |

Findings:

- Diffs are tiny and give per-object timestamps and versions, so they separate
  new ways from edited ways, which the snapshot method cannot. A monthly or
  daily refresh is cheap to fetch.
- A diff holds only changed nodes. Most new ways can be drawn from it, but
  edited ways mostly cannot (8%), because their unchanged nodes are not in the
  file. Geometry needs a base node store, such as the current regional extract
  read with a location index (pyosmium or osmium), which this probe did not
  add as a dependency.
- Deletes lack tags, so removed roads cannot be told from other deletions
  without the base data. Same fix.
- The 12.4% "inside 2021 roadless land" figure uses the 2021 patches, so it
  includes roads built between 2021 and October 2026. It is a plumbing check,
  not a change estimate.
- Retention is limited, so a rolling refresh must run at least every few
  months, or start from a fresh extract each time.
- Not tested: planet minutely or hourly diffs, other regions.

### With a base extract (pyosmium)

The probe takes an optional base `.osm.pbf` (here the 2026-11-17 New Brunswick
extract, 66 MB, fetched with `fetch_inputs.py pbf`). The diffs say which ways
changed and when; the extract supplies geometry through a node location index.
`osmium` (pyosmium 4.3) is now a project dependency. Run time 30 s.

| Measure | Result |
| --- | --- |
| Changed road ways resolved | 1,455 of 1,456 |
| Created: ways / length / inside 2021 roadless land | 552 / 182 km / 22 km (12.2%) |
| Modified: ways / length / inside 2021 roadless land | 903 / 768 km / 18 km (2.3%) |

- Resolution rises from 68% to about 100% for created ways and from 8% to 100%
  for modified ways, so a base extract is enough; no full history is needed.
- Edits touch four times the road length of new ways (768 vs 182 km) but almost
  none of it is remote (2.3%), so edits can be ignored for roadless change. New
  ways are where remote change shows up.
- The extract is current (2026-11-17), so a way created and then deleted inside
  the window is absent from it, and a way's geometry is its latest, not its
  state on the day it changed.
- Still unresolved: deleted roads. Delete records carry no tags or geometry,
  so removed road length needs an older extract to look the ids up in.
- Geofabrik's `-latest` file name is a 307 redirect page. A plain `curl -sf`
  saved the 289-byte redirect body as the file; use `-L` or a dated name.
