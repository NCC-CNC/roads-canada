# Roadless area by jurisdiction: all runs (issue #4)

Compiled 2026-11-19 by `summary_table.py` from `data/processed/*/stats.json` and
the paper's Table 4 (`poley2022_table4_roadless.csv`). Same method everywhere
(1 km buffer, StatCan 2016 land mask, EPSG:3347); OSM is the 2021-01-01
snapshot, the rest are the current editions on 2026-11-19. Sources and filters
are in notes 10, 11, 13 and 14.

| Jurisdiction | OSM 2021 % | NRN % | Best source | Best % | Strict % | Paper provincial % |
| --- | --- | --- | --- | --- | --- | --- |
| BC | 81.4 | 89.7 | BC DRA | 53.9 | 54.8 | 52.0 |
| AB | 56.7 | 59.4 | HFI 2023 | 36.4 | 44.2 | 47.0 |
| SK | 56.3 | 56.8 | none (NRN, OSM only) |  |  |  |
| MB | 83.4 | 85.2 | NRN + MLI 20k + BEAD | 77.2 | 80.5 |  |
| ON | 75.9 | 75.9 | ORN + MNR | 66.5 | 66.7 | 63.0 |
| QC | 86.4 | 91.4 | RQTT | 70.1 | 70.1 | 70.0 |
| NB | 43.0 | 46.6 | NBRN + Forest Roads | 3.4 |  |  |
| NS | 20.5 | 21.7 | NSTDB | 9.4 | 9.4 | 9.0 |
| PE | 5.8 | 6.0 | none (NRN, OSM only) |  |  |  |
| NL | 90.7 | 93.7 | NRN + Resource Access Roads | 88.2 | 88.4 |  |
| YT | 96.8 | 97.7 | Road Network + Forest Resource Roads | 97.5 | 97.6 |  |
| NT | 99.2 | 99.1 | NRN + BEAD | 98.5 |  |  |
| NU | 99.9 | 100.0 | none (NRN, OSM only) |  |  |  |

"Best source" is the most detailed dataset run for the jurisdiction, with the
paper's exclusions. "Strict" drops more roads (vegetated, winter, track and
similar), so it is an upper bound on roadless area. The last column is the
paper's provincial-dataset result, where it had one.

## Reading the table

- **Provincial and resource-road sources lower roadless area in every
  jurisdiction that has one**, by 2 points (YT) to 40 (NB). OSM and the NRN are
  ceilings.
- **Agreement with the paper** where it has a provincial dataset: BC, QC and
  NS within 2 points; ON 3.5 above; AB 10.6 below (default) or 2.8 below
  (strict). See note 12.
- **No source beyond OSM and the NRN:** SK, PE and NU. NU is empty of roads
  either way; SK and PE need a department request (note 14).
- **NB (3.4%) has no strict variant**, because the Forest Roads layer has
  geometry only. It is the least certain of the large differences.

## Choosing a headline figure

This choice is the project owner's. A rule that fits the evidence so far:

1. Headline is the best-source default for each jurisdiction, with the strict
   figure shown as the upper end of a range.
2. Where only OSM and the NRN exist (SK, PE, NU), report the OSM figure and
   label it a ceiling.
3. Flag NB and MB as lower confidence (no status field; 2009 edition).
