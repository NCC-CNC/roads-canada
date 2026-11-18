# OSM change detection: design note and Nova Scotia feasibility test (issue #5)

## Question

Can OSM timestamps or snapshots identify roads added since a baseline, so
roadless-area refreshes are incremental and focus on remote land?

## Options

| Option | Timestamps | Access | Fit |
| --- | --- | --- | --- |
| Dated Geofabrik snapshots (1 January, 2014 onward) | No, but `osm_id` allows set differences | Public | Works now; yearly resolution |
| Geofabrik internal history extracts (`.osh.pbf`) | Yes, per object version | Needs an OSM login | Best for exact "added since date D"; not tested |
| Planet replication (minutely, hourly, daily diffs) | Yes | Public | Suited to a rolling refresh; needs a tool such as osmium to apply and filter. Not tested |

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
difference of +6 km2 (0.05%). The gap is most plausibly the 404 removed ways,
which the shortcut ignores; this was not checked directly.

## Findings

- Change is small and mostly in already-roaded land: about 95% of added road
  length is within 1 km of existing roads. Remote-area loss is a handful of
  ways, so a refresh should report lost roadless polygons, not just totals.
- The incremental shortcut reproduces the full rebuild closely, so a refresh
  only needs to process new `osm_id`s (and removals, to recover area).
- Net change is sensitive to deletions and to OSM mapping effort, not only to
  real road building. Added roads in OSM can be mapping catch-up, not new roads.

## Recommendation

1. Use dated snapshots for the first change layer; they need no new tooling.
2. For a rolling refresh, test planet replication diffs filtered to Canada and
   to the paper's road classes, and compare with a history extract.
3. Validate flagged remote additions against imagery or the NRN before
   reporting them as new roads.

## Not done

Only one region and one year pair. History extracts and replication diffs were
assessed from documentation, not run. Removed-road effect on the +6 km2 gap not
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
