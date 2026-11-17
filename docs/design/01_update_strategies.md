# 01 Update Strategies

Options for keeping road and roadless-area data current with low effort,
roughly ordered from least to most effort. Evidence comes from Poley et al.
(2022); items marked "to verify" have not been checked.

## 1. Scripted, scheduled pipeline

Replace manual ArcMap steps with a reproducible script: download, filter to
vehicle roads, buffer 1 km, compute roadless patch metrics. Re-run when
sources update. This is the foundation for everything else.

## 2. Re-survey provincial and territorial open data

Only 5 provinces had provincial road datasets in 2021. Check what others
publish now (NB, MB, SK, NL, territories) and whether annual footprint layers
exist, such as ABMI Human Footprint or BC Cumulative Effects Framework
disturbance data. To verify.

## 3. OpenStreetMap change feed

OSM history carries timestamps, which addresses the missing-date problem.
Use Geofabrik or planet extracts and Overpass for monthly refreshes and for
tracking edits in remote areas. Overture Maps may be a convenient conflated
input (to verify coverage and licence). Targeted mapping of resource roads
with partners (mapathons, Indigenous Guardians) could close OSM's gap in
remote areas.

## 4. Satellite and machine-learning change detection

Use Landsat or Sentinel-2 time series, and forest-loss products, to flag new
linear disturbances (cutlines, logging roads). Existing AI-derived road
layers (Microsoft, Meta) may help fill gaps (to verify Canadian coverage and
licence). Treat as a flag for where to look, with sample-based validation.

## 5. Regulator and industry permit data

Forestry road permits, oil and gas regulators and mining claims record where
resource roads are authorized, with dates. Forest certification (FSC, SFI) is
another route to industry road data.

## 6. Data sharing with recreation and commercial mappers

Backroad Mapbooks and similar sources (snowmobile and ATV associations, Trans
Canada Trail, GPS-track platforms such as Gaia, Strava Metro, Wikiloc) are
strong in back-country and recreational roads, where OSM is weakest, and may
carry use information. Provenance and licensing of their data is unverified;
much may derive from provincial sources. Pitch idea: credited partnership,
aggregated roadless statistics in return, limited-use licence for derived
metrics rather than raw geometry.

## 7. Institutional route

NRCan and the federal-provincial-territorial geomatics community coordinate
the National Road Network. A short policy brief or ask through NRCan or ECCC
could push for consistent provincial datasets with national coordination,
which is the paper's own conclusion.

## Suggested sequence

1. Build the pipeline (1) with monthly OSM extracts (3) as the first input.
2. Re-survey provincial availability (2).
3. Pursue data-sharing outreach (6) in parallel, without depending on it.
4. Use change detection (4) as a flag only.
