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

Not yet chosen. Candidates are Python (GDAL/GeoPandas) or R, with PostGIS or
GeoParquet for storage. Record the choice as an ADR.

## Commands

{{The everyday commands: run, test, lint/typecheck, build. One line each, and
mark which ones are gates (non-zero exit blocks a merge). Say how long the
slow ones take and which ones CI skips, so nobody runs a 20 minute suite by
accident. Fill in once the stack is chosen; `CONTRIBUTING.md` Setup should
match.}}

## Repo structure

{{Optional: a short map of top-level directories, only if it adds real
orientation beyond exploring the tree. State layering rules here too, such as "`core/` never imports from `ui/`".
Keep it brief and expect it to drift; when in doubt, explore the tree rather
than trusting this section.}}

## Working rules

- Branch from `main`; one short-lived branch per change. Open a pull request
  into `main`; CI must pass before merge.
- Conventional Commits (for example `feat: ...`, `fix: ...`, `chore: ...`,
  `docs: ...`).
- No em dashes in code, comments, docs, commit messages, or user-facing text.
- Significant technical or design decisions get an ADR in `docs/decisions/`.
- Design notes live in `docs/design/`; session handoffs in `docs/handoffs/`.
- Keep changes small and focused; update docs when behaviour or design changes.
