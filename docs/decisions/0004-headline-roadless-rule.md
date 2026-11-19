# Headline roadless-area rule

## Status

Accepted (2026-11-19). Closes issue #30.

## Context

Every jurisdiction has several roadless-area figures (OSM, NRN, a provincial or
resource-road source, and sometimes a strict variant that drops vegetated,
winter, track and similar roads). They differ by up to 40 points, so a published
number needs one stated rule. Evidence is in
`docs/design/15_results_by_jurisdiction.md`.

## Decision

1. The headline is the best-source default figure for each jurisdiction, with
   the strict figure shown as the upper end of a range.
2. Where only OSM and the NRN exist (SK, PE, NU), report the OSM figure and
   label it a ceiling (an upper bound on roadless area).
3. Flag NB and MB as lower confidence (NB has no status field and so no strict
   variant; the MB layer is a 2009 edition).

## Consequences

- Alberta is published as 36.4% (range to 44.2%), which is below the paper's
  47.0%. The gap is explained in note 12 and stays visible rather than hidden.
- Jurisdictions with no strict variant (NB, NT) show a single figure.
- The rule is applied by `summary_table.py`; any published number must come from
  its output.
- Licence review (#32) still gates what can be made public.
