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
uv run python src/roadless/fetch_inputs.py boundary "Nova Scotia"
uv run python src/roadless/osm_roadless.py data/raw/nova-scotia_210101.shp.zip data/raw/boundary_nova_scotia.gpkg NS_210101
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
