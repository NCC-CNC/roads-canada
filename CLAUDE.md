# CLAUDE.md

Working rules and durable context for this project. This file is loaded into
context automatically, so keep it to direction and rules, not a task list.

## Project name

roads-canada

## Project purpose

Keep Canada's road network data, and the roadless-area estimates derived from
it, up to date with much less effort than the 2022 paper that first produced
them (Poley et al., Conservation Science and Practice 4:e12656). For
conservation planners and researchers who need current, defensible
roadless-area numbers. See `docs/design/00_project_brief.md`.

## Project status

Design stage. No code yet. Next milestones: survey current open road data by
jurisdiction, then prototype a scripted roadless-area pipeline. Open GitHub
issues are the live task tracker.

## Scope

In scope: data sourcing, harmonization, roadless-area calculation, and change
detection for Canadian road networks. Not in scope: new national road
mapping by manual digitizing, or road-effect modelling beyond a simple buffer.
Do not expand scope without a design note in `docs/design/` or an ADR in
`docs/decisions/`.

## Stack

Python with uv and `pyproject.toml`; GeoPandas, Shapely, pyosmium (OSM diffs) and DuckDB (spatial)
over GeoParquet files; no database server; local workstation first. Reasoning
and fallbacks in `docs/decisions/0002-technology-stack.md`.

## Commands

- `uv sync`: install dependencies.
- `uv run pytest`: run the tests (synthetic roadless-area check).
- `uv run python src/roadless/osm_roadless.py <geofabrik.shp.zip> <boundary-file> <name>`:
  OSM roadless-area prototype (issue #3). Fetch inputs first with
  `uv run python src/roadless/fetch_inputs.py osm|boundary ...`. Downloads go in `data/raw/` (ignored).
- `uv run python src/roadless/osm_change.py <old.shp.zip> <new.shp.zip> <boundary-file> <name>`:
  roadless-area change between two OSM snapshots (issue #5).
- `uv run python src/roadless/run_regions.py <YYMMDD> <province>...|all [--force]`:
  resumable multi-province run; results in `data/processed/<YYMMDD>/<slug>/`, failures in `errors.log`.
  Use `nrn` in place of `<YYMMDD>` to run the National Road Network instead of OSM (issue #4).
- `uv run python src/roadless/bcdra_roadless.py [--strict]`: BC Digital Road Atlas (issue #4).
- `uv run python src/roadless/abhfi_roadless.py [--strict]`: Alberta Human Footprint Inventory (issue #4).
- `uv run python src/roadless/{on,qc,ns,yt}_roadless.py [--strict]`: Ontario, Quebec, Nova Scotia and Yukon provincial datasets (issue #4; note 11).
- `uv run python src/roadless/paper_tables.py` then `compare_to_paper.py`: extract the paper's
  Tables 2 and 4 to CSV, and compare our runs with Table 4 (note 12).
- `uv run python src/roadless/nb_roadless.py`: New Brunswick NBRN plus Forest Roads (issue #4; note 13).
- `uv run python src/roadless/{nl,mb}_roadless.py [--strict]` and `nt_roadless.py`: NL, MB and NT with the
  resource-road sources the paper's baseline used (issue #4; note 14).

- `uv run python src/roadless/abhfi_diagnostics.py [outdir]`: why Alberta HFI 2023 differs from the paper
  (class footprint, isolation, largest-block check; note 12; needs the `abhfi_strict` run).

Keep `CONTRIBUTING.md` Setup in step.

## Repo structure

{{Optional: a short map of top-level directories, only if it adds real
orientation beyond exploring the tree. State layering rules here too, such as "`core/` never imports from `ui/`".
Keep it brief and expect it to drift; when in doubt, explore the tree rather
than trusting this section.}}

## Working rules

- Branch from `main`; one short-lived branch per change. Open a pull request
  into `main`; CI must pass before merge.
- One pull request per working session unless the user says otherwise; put
  further work in the same branch. Ask before opening a second PR.
- Conventional Commits (for example `feat: ...`, `fix: ...`, `chore: ...`,
  `docs: ...`).
- No em dashes in code, comments, docs, commit messages, or user-facing text.
- Significant technical or design decisions get an ADR in `docs/decisions/`.
- Design notes live in `docs/design/`; session handoffs in `docs/handoffs/`.
- Keep changes small and focused; update docs when behaviour or design changes.
