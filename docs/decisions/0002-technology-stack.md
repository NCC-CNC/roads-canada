# Technology stack

## Status

Accepted

## Context

The roadless-area pipeline (issue #3) needs a language, storage format,
dependency manager, spatial engine and run environment. The goal is low
maintenance effort: a refresh should be a scripted run, not a research project.
Inputs are large (a national OSM extract plus provincial layers, see
`docs/design/02_data_sources.md`) and mostly vector.

## Decision

- **Language:** Python.
- **Storage:** GeoParquet files for intermediate and output data. No database
  server.
- **Environment:** uv with `pyproject.toml` and a lockfile.
- **Spatial engine:** GeoPandas and Shapely for geometry operations such as
  the 1 km road buffer and roadless patch extraction, DuckDB (spatial
  extension) for filtering and joins over GeoParquet.
- **Compute:** a local workstation first. Scheduled runs (GitHub Actions or
  NCC cloud) are deferred until the pipeline exists and its resource needs are
  known.

## Consequences

- Plain files and one language keep the pipeline easy to reproduce and share,
  and avoid running a server.
- GeoParquet is readable from R and QGIS, so analysts who prefer those tools
  are not locked out.
- Vector buffering of national-scale roads may be slow or memory-hungry. If the
  prototype shows this, a raster distance-to-road approach is the fallback, at
  the cost of exactness against the paper's method. Revisit in a new ADR after
  issue #3.
- GDAL-based dependencies can be awkward on Windows. If uv installs prove
  unreliable, a conda environment is the fallback.
- Running locally means no automated refresh yet; that is a known gap.
