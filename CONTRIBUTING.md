# Contributing

Feedback, bug reports, and ideas are welcome through GitHub issues.

The workflow is:

1. Branch from `main` (one short-lived branch per change).
2. Keep changes small and focused.
3. Run the project checks locally before pushing (format, lint, tests, build).
   See the Setup section below for the exact commands once they are defined.
4. Open a pull request into `main`. CI must pass before merge.

## Setup

Prerequisites: [uv](https://docs.astral.sh/uv/) and Python 3.11 or newer.

```bash
uv sync
uv run python src/roadless/fetch_inputs.py osm north-america/canada/nova-scotia 210101
# Needs lpr_000b16a_e.zip in data/raw/ (StatCan 2016 cartographic boundary, manual download; see ADR 0003)
uv run python src/roadless/fetch_inputs.py boundary "Nova Scotia"
uv run python src/roadless/osm_roadless.py data/raw/nova-scotia_210101.shp.zip data/raw/boundary_nova_scotia.gpkg NS_210101
# Change between two snapshots (fetch the 220101 file the same way)
uv run python src/roadless/osm_change.py data/raw/ns_210101.shp.zip data/raw/ns_220101.shp.zip data/raw/boundary_nova_scotia.gpkg NS_2021_2022
# Probe Geofabrik daily replication diffs (needs the 2021 patches from run_regions)
uv run python src/roadless/osm_diff_probe.py north-america/canada/new-brunswick 4946 4975 data/processed/210101/new-brunswick/patches.parquet
# Same, with geometry for edited ways from a base extract (fetch it first)
uv run python src/roadless/fetch_inputs.py pbf north-america/canada/new-brunswick 261117
uv run python src/roadless/osm_diff_probe.py north-america/canada/new-brunswick 4946 4975 data/processed/210101/new-brunswick/patches.parquet data/raw/new-brunswick_261117.osm.pbf
# Several provinces, resumable (skips finished ones; --force to redo)
uv run python src/roadless/run_regions.py 210101 "Nova Scotia" Yukon
# Same, from the National Road Network (downloads the current edition; results in data/processed/nrn/)
uv run python src/roadless/run_regions.py nrn "Nova Scotia" Yukon
# BC Digital Road Atlas (about 15 minutes; --strict also drops trails and decommissioned roads)
uv run python src/roadless/bcdra_roadless.py [--strict]
# Alberta Human Footprint Inventory (4.8 GB download, about 5 minutes per variant)
uv run python src/roadless/abhfi_roadless.py [--strict]
# Ontario, Quebec, Nova Scotia, Yukon provincial datasets (downloads on first run; 1 to 10 minutes each)
for p in on qc ns yt; do uv run python src/roadless/${p}_roadless.py [--strict]; done
# New Brunswick (NBRN plus Forest Roads), then NL, MB and NT with resource-road sources
uv run python src/roadless/nb_roadless.py
for p in nl mb; do uv run python src/roadless/${p}_roadless.py [--strict]; done
uv run python src/roadless/nt_roadless.py
# Paper Tables 2 and 4 to CSV, comparison with our runs, consolidated table
uv run python src/roadless/paper_tables.py
uv run python src/roadless/compare_to_paper.py
uv run python src/roadless/summary_table.py
# Why Alberta HFI 2023 differs from the paper (needs the abhfi_strict run)
uv run python src/roadless/abhfi_diagnostics.py
```

Run the tests with `uv run pytest`. There is no lint step yet; CI runs whatever
`.github/workflows/ci.yml` defines. See `CLAUDE.md` for commands and `docs/design/05_osm_prototype_nova_scotia.md`
for what to expect from the output.

## Conventions

- Conventional Commits (for example `feat: ...`, `fix: ...`, `chore: ...`,
  `docs: ...`).
- No em dashes in code, comments, docs, commit messages, or user-facing text.
- See `CLAUDE.md` for the full working rules and `docs/` for design notes and
  decision records.
