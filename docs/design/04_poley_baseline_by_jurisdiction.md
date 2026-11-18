# 04 The Poley 2021 Baseline, Province by Province

Per-jurisdiction breakdown of the merged roads layer described in
`03_poley_baseline_dataset.md`. Compiled 2026-11-17 from `ogrinfo` queries over
the 13 per-province shapefiles (`SOURCE_DS` and lower-cased `GEN_CLASS`,
lengths from `ST_Length` in EPSG:3347, rounded to km). The 13 totals sum to
3,180,891 km, matching the national tally. Paper figures are from Table 2 and
Table 4 of Poley et al. (2022). Nothing here has been checked against imagery.

## Merged layer against the paper's Table 2

"Paper best" is the dataset with the longest total in the paper's Table 2 for
that jurisdiction (a provincial dataset where one existed, otherwise OSM, or
NRN for NT).

| Jurisdiction | Merged km | Paper best (dataset) km | Ratio | OSM km in merged | OSM share of merged |
| --- | --- | --- | --- | --- | --- |
| BC | 735,796 | 788,946 (BCDRA) | 0.93 | 383 | 0.1% |
| AB | 394,895 | 391,825 (ABHFP) | 1.01 | 7,608 | 1.9% |
| SK | 347,573 | 258,391 (OSM) | 1.35 | 6,944 | 2.0% |
| MB | 191,408 | 110,289 (OSM) | 1.74 | 6,600 | 3.4% |
| ON | 528,466 | 552,538 (ORN + MNRF) | 0.96 | 32,686 | 6.2% |
| QC | 661,696 | 644,738 (AQR) | 1.03 | 17,742 | 2.7% |
| NB | 117,805 | 55,662 (OSM) | 2.12 | 3,580 | 3.0% |
| NS | 118,038 | 107,867 (NSTDB) | 1.09 | 226 | 0.2% |
| PE | 7,888 | 8,796 (OSM) | 0.90 | 0 | 0% |
| NL | 49,232 | 39,006 (OSM) | 1.26 | 14,464 | 29.4% |
| YT | 12,757 | 13,489 (OSM) | 0.95 | 3,107 | 24.4% |
| NT | 13,125 | 7,401 (NRN) | 1.77 | 1,401 | 10.7% |
| NU | 2,212 | 2,268 (OSM) | 0.98 | 951 | 43.0% |

## Sources by jurisdiction (km)

| Jurisdiction | Sources, largest first |
| --- | --- |
| BC | BC_DRA 735,413; OSM 383 |
| AB | NRN 234,609; AB_HFP 152,068; OSM 7,608; STATSCAN 610 |
| SK | NRN 249,479; SK_HFP 74,578; STATSCAN 16,572; OSM 6,944 |
| MB | NRN 85,944; MLI_20K_TL 84,095; BEAD2015 8,022; OSM 6,600; STATSCAN 3,702; BEAD2010 3,045 |
| ON | OMNRF 270,366; ORNE 210,233; OSM 32,686; STATSCAN 7,859; ORNE_RESREC 5,113; NRN 2,209 |
| QC | AQRESEAU 483,025; NRN 160,149; OSM 17,742; STATSCAN 780 |
| NB | NB_FORESTROADS 64,359; NRN 35,665; NB_FORESTROADS_ADDED 13,490; OSM 3,580; STATSCAN 711 |
| NS | NSTDB 66,927; NRN 50,885; OSM 226 |
| PE | NRN 6,967; PEI_FORESTROADS 921 |
| NL | NRN 20,102; OSM 14,464; NL_RESROADS 12,277; STATSCAN 2,389 |
| YT | NRN 6,363; OSM 3,107; STATSCAN 2,840; FORESTRESOURCEROADS 447 |
| NT | NRN 5,317; BEAD2015 3,696; OSM 1,401; STATSCAN 1,362; BEAD2010 1,349 |
| NU | NRN 1,261; OSM 951 |

## Findings

1. **NRN is the base layer wherever it was highest priority.** Its length in
   the merged layer matches the paper's NRN total to within 0.2% in AB, SK, NB,
   NS, NL and QC. It does not match in NT (5,317 km against 7,401 km in the
   paper) or NU (1,261 km against 912 km). Cause unknown: a different NRN
   download, or cleanup. Needs a closer look before NRN is used as a
   reference there.
2. **The merged layer holds provincial data the paper never compared.** The
   paper names provincial datasets only for BC, AB, ON, QC and NS. The merge
   also includes MLI 20K (MB), SK Human Footprint, NB Forest Roads, PEI Forest
   Roads, NL Resource Access Roads and Yukon Forest Resource Roads. Where these
   matter, the merged layer is much longer than the paper's best dataset: NB
   2.12 times, MB 1.74, SK 1.35, NL 1.26. These are candidate sources for
   issue #4, and none appear in the paper's Table 2 or Table 4.
3. **OSM fills a small share of the merged length almost everywhere.** It is
   under 7% in the ten jurisdictions with large networks. It is large only
   where the network is small or the other sources are thin: NL 29%, YT 24%,
   NU 43%, NT 11%. PE has none.
4. **The merged layer is shorter than the paper's best dataset in BC (7%),
   ON (4%), PE (10%), YT (5%) and NU (2%).** The merge erased duplicates, and
   in PE and YT the paper's best dataset was OSM, which the merge largely
   dropped. It is not known whether the shortfall in BC and ON is duplicate
   removal or a different download.
5. **Class quality varies by jurisdiction.** All 368,735 km of the
   `unclassifed` typo is BC DRA, so half of BC has no usable `GEN_CLASS`; use
   the DRA's own `ORIG_CLASS` there. `track` dominates the provincial and
   resource-road layers: AQRESEAU 91%, OMNRF 99%, SK_HFP 100%, NB forest roads
   100%, NL_RESROADS 100%.
6. **BEAD layers are weak data.** BEAD (Boreal Ecosystem Anthropogenic
   Disturbance, Environment and Climate Change Canada) was digitized by hand
   from Landsat imagery (2008 to 2010 and 2015, 30 m). The authors added only
   its `road` features to MB and NT where resource roads were missing, after
   visual checks, and labelled them all resource/recreation. That is about
   16,000 km of lower-precision, single-date data (MB 11,067; NT 5,045).
7. **The authors' manual additions can be isolated.** `NB_FORESTROADS_ADDED`
   (13,490 km, 16,013 features) holds the roads digitized from imagery, about
   11% of NB's length. It is the only place the manual step is tagged.

## Implications for the pipeline

- **Validation scope.** Table 4 covers only BC, AB, ON, QC and NS, and the
  authors' roadless layers are not published, so each jurisdiction needs its
  own check. For the other eight, compare against the merged layer's length
  and source mix, not against Table 4.
- **Update effort differs by jurisdiction.** BC and NS are one dominant
  source. AB, SK, MB, ON and QC need two to six. A scripted update should be
  built per jurisdiction around a source list, as the metadata's priority
  table already is.
- **Candidate OSM test region.** NL has a large OSM share (29%), a small
  network (49,232 km) and an exact NRN match, so it is a cheap place to test
  an OSM plus NRN pipeline end to end. It is not in Table 4.

## Open questions

- Why NRN in NT and NU does not match the paper's NRN totals.
- Whether the BC and ON shortfalls against the paper come from the merge or
  from a different download of the source.
- Three Table 4 cells (AB OSM and ABHFP roadless area, ON GRIP roadless area)
  are missing leading digits in the PDF itself. Reconstructed values are in
  `07_osm_prototype_four_provinces.md`.
- Class breakdown by jurisdiction for all sources was collected only for the
  top 25 source and class pairs per province.
