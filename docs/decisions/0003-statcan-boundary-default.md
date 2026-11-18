# StatCan 2016 cartographic boundary as the default land mask

## Status

Accepted

## Context

The roadless-area result depends on the land mask. With the geoBoundaries
CAN ADM1 file, Nova Scotia gives about 3,800 patches against the paper's 2,459,
because the mask includes coastal slivers. The Statistics Canada 2016
Cartographic Boundary File reproduces the paper's land areas exactly in all
five Table 4 provinces, and roadless area is then within 0.5% of the paper and
patch counts within about 5% (design notes 06 and 07).

## Decision

- The default boundary is the Statistics Canada 2016 Cartographic Boundary
  File (`lpr_000b16a_e`), not the Digital file (`lpr_000a16a_e`), which extends
  into water.
- It is a manual download into `data/raw/` (StatCan returns 403 to automated
  clients). `fetch_inputs.py boundary <province>` extracts the province by
  name (`PRENAME`) into a GeoPackage.
- geoBoundaries stays as a fallback when the zip is absent, with a warning.
- The file is not committed to the repo until the Statistics Canada Open
  Licence terms are confirmed (open item in design note 06).

## Consequences

- Results are paper-comparable by default, at the cost of one manual step.
- Cite as Statistics Canada, Boundary Files, 2016 Census, Catalogue no.
  92-160-X.
- Change detection (issue #5) must use the same mask for both snapshot dates.
