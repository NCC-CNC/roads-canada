# 00 Project Brief

## What this is

roads-canada is an effort to keep Canadian road network data and the
roadless-area estimates derived from it current, at a fraction of the effort
of the original research paper.

It is a research and planning tool, not a new road map of Canada. The goal is
that a planner can get a current roadless-area layer and summary statistics
without a months-long manual data assembly.

## Who it is for

- Conservation planners and analysts (NCC and partners).
- Researchers using roadless or intactness metrics.

## Background

Poley et al. (2022) compared global (gROADS, GRIP, OSM), national (Statistics
Canada, National Road Network) and provincial road datasets. Key findings:

- Provincial datasets are the most complete, but existed for only 5 provinces
  (BC, AB, ON, QC, NS) in 2021.
- OSM averaged 78% of provincial road length, but about 48% in forest,
  grassland and shrubland areas, where low-use resource roads dominate.
- gROADS and GRIP averaged 11% to 14% and overstate roadless area.
- No dataset has reliable creation dates or decommissioning information.

## The core idea (one screen)

Automate the repeatable parts of the paper's method (download, filter to
vehicle roads, 1 km buffer, roadless patch metrics), and add cheap ways to
detect and ingest change, so a refresh is a scheduled run plus a short review,
not a research project.

## MVP scope

1. Inventory of road data sources by jurisdiction: coverage, licence, format,
   update frequency.
2. Scripted pipeline reproducing the paper's roadless-area calculation from
   OSM and one provincial dataset.
3. Documented refresh procedure and versioned outputs.

See `docs/design/01_update_strategies.md` for the longer list of options.

## Explicit non-goals (for now)

- Manually digitizing roads at national scale.
- Modelling road traffic or ecological effects beyond a fixed buffer.
- Replacing provincial datasets; the aim is to use and complement them.
