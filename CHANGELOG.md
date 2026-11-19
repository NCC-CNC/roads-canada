# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Roadless-area pipeline (issues #3, #4, #5): OSM, NRN and provincial dataset
  loaders, OSM change detection, a resumable multi-province runner, paper
  Tables 2 and 4 as CSV with a comparison, a consolidated results table, and
  design notes 05 to 16.
- CI: `changes` job so docs-only PRs skip stack jobs, a single required
  `checks` job, a commented cache example, and an opt-in `warm-cache.yml`.
- Hints in `CLAUDE.md`, `CONTRIBUTING.md`, `.gitignore` and the handoff
  template.
- Initial project harness: issue and PR templates, contribution and security
  policies, docs structure (design, decisions, handoffs), and Claude Code
  working rules.

### Changed

- `ci.yml` runs on pull requests only; `bootstrap-repo-settings.sh` gates on
  `checks` by default.
