# Poley et al. (2022)

Reference copies of the paper and its Supporting Information.

- Poley, L.G., Schuster, R., Smith, W. and Ray, J.C. (2022). Identifying
  differences in roadless areas in Canada based on global, national, and
  regional road datasets. Conservation Science and Practice 4(4): e12656.
  <https://doi.org/10.1111/csp2.12656>
- Licence: Creative Commons Attribution (open access article).
- Files: `Poley_et_al_2022_Roadless_Areas_Canada.pdf` (paper) and
  `csp212656-sup-0001-supinfo.pdf` (Supporting Information, dataset sources
  and cleaning rules).
- Retrieved 2026-11-17.

The authors' roadless-area outputs and code are not published with the paper.

Extracted tables (made by `src/roadless/paper_tables.py`, which reads the PDF
with `pdftotext`):

- `poley2022_table2_road_length.csv`: Table 2, road length by dataset for all
  13 jurisdictions.
- `poley2022_table4_roadless.csv`: Table 4, roadless area and patch metrics
  for BC, AB, ON, QC and NS. Three cells print with leading digits missing in
  the PDF (AB OSM, AB ABHFP, ON GRIP roadless area). They are restored from
  the printed percent cover and marked `reconstructed = yes`.
