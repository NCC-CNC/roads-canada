# roads-canada

Keeping Canada's road network and roadless-area estimates current with far
less effort than a one-off research paper.

## Background

Poley, Schuster, Smith and Ray (2022) compared global, national and provincial
road datasets across Canada and showed that the choice of dataset changes
roadless-area estimates dramatically. Provincial datasets are the most
complete but exist for only a few provinces, OSM is the best national
alternative but misses many low-use roads, and no dataset carries reliable
dates or decommissioning information. The paper took a large manual effort
(Poley et al. 2022, Conservation Science and Practice 4:e12656,
<https://doi.org/10.1111/csp2.12656>). This repo explores how to keep those
estimates up to date without repeating that effort.

## Goals

- A scripted, reproducible pipeline that rebuilds the roadless-area
  calculation whenever source data updates.
- A current inventory of which jurisdictions publish road data, under what
  licence, and how often it changes.
- Low-effort ways to detect change (OSM history, satellite change detection,
  permit data) and to bring in new data (partnerships and data sharing).

See `docs/design/00_project_brief.md` for the brief and
`docs/design/01_update_strategies.md` for the options under consideration.

## Status

Early design. No code yet. Open issues track the next steps.

## Solo-maintainer auto-merge (optional)

`.github/workflows-optional/` holds two workflows that make the owner's own
green PRs merge themselves. They are not active until you move them into
`.github/workflows/`.

- `auto-merge.yml` arms squash auto-merge on PRs opened by the repository
  owner (never on anyone else's, Dependabot included) and brings the PR level
  with `main`.
- `update-branches.yml` updates every armed PR after each push to `main`, so
  strict "up to date" branch protection does not leave them stuck BEHIND.

One-time setup: create a fine-grained personal access token for this repo only
(Contents, Pull requests and Workflows: read/write) and store it as the
`AUTO_MERGE_TOKEN` secret. `GITHUB_TOKEN` cannot be used because GitHub starts
no workflows for pushes or merges made with it, so the PR's checks would never
run on the updated branch. Rotate the PAT before it expires. `ci.yml` already
runs on PRs only: with strict protection every PR is tested against current
`main` before it merges.

## Cache warming (optional)

`.github/workflows-optional/warm-cache.yml` saves a cache from `main`, because
a PR can read caches saved on `main` but not caches saved by another PR. Use it
if a CI job downloads something slow on every run. Move it into
`.github/workflows/`, fill in the two placeholders, and use the same path and
key in the `actions/cache` step of your CI job.

## Repo scaffolding

- `CLAUDE.md`: working rules and durable context, loaded automatically by
  Claude Code.
- `.claude/settings.json`: default tool permissions for Claude Code sessions
  in this repo.
- `docs/design/`: design notes, starting with a project brief template.
- `docs/decisions/`: Architecture Decision Records (ADRs).
- `docs/handoffs/`: session handoff template for continuity between work
  sessions.
- `.github/`: issue forms, PR template, Dependabot config, a stack-neutral CI
  workflow (docs-only PRs skip stack jobs, one required `checks` status), and
  optional solo-maintainer auto-merge and cache-warming workflows.
- `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `LICENSE`.
- `scripts/bootstrap-repo-settings.sh`: one-time repo settings setup (branch
  protection, auto-merge, labels) that a template cannot carry over on its
  own.

## Data attribution

Roadless-area results use the Statistics Canada 2016 Cartographic Boundary
File as the land mask. Adapted from Statistics Canada, Boundary Files, 2016
Census, Catalogue no. 92-160-X. This does not constitute an endorsement by
Statistics Canada of this product.

## License

GNU General Public License v3.0 (inherited from the project template; to be confirmed).
