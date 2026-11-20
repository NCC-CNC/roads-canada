# Data search brief: what is still missing and where to look

Compiled 2026-11-19 for the project owner, who is searching for data outside
what the assistant can reach. Facts come from notes 03, 04, 11, 12, 13, 14 and
16. Lines marked "suggestion" are leads not yet checked.

## Already on disk (do not search for these)

The 2021 Poley compilation is in
`data/external/poley2022/canada_linear_features/` (layer `roads_merge` in
`roads.gdb`). Filter on `SOURCE_DS`:

| Wanted | `SOURCE_DS` | km |
| --- | --- | --- |
| Saskatchewan Human Footprint | `SK_HFP` | 74,578 |
| PEI forest roads | `PEI_FORESTROADS` | 921 |
| BEAD 2010 and 2015 (MB, NT) | `BEAD2010`, `BEAD2015` | 4,394 and 11,718 |
| Manitoba MLI 20K | `MLI_20K_TL` | 84,095 |
| NB Forest Roads and hand-digitized additions | `NB_FORESTROADS`, `NB_FORESTROADS_ADDED` | 64,359 and 13,490 |
| Alberta HFP (clipped, merged) | `AB_HFP` | 152,068 |

Caveats: each lower-priority source was erased inside a buffer around higher
ones, so these are the parts the NRN and others did not cover. The metadata
says "private share only" and names no licence (issue #32).

## Still worth finding

Priority order.

### 1. Alberta HFI 2018, unclipped (done 2026-11-20)

Resolved: the lead author supplied the ABMI link; see note 18. It reproduces
the paper (46.5% against 47.0%). Kept below for the record.

- Why: our 2023 edition gives 36.4% against the paper's 47.0%. Most of the gap
  is explained by new road classes; the rest is one block (paper 91,101 km2,
  ours 36,877 km2). Only the 2018 edition can confirm it (note 12).
- Need: the HFI roads or linear features for 2018, with `YEAR` and `SOURCE`.
- Where: ABMI Geospatial Centre (current editions are in `data/raw/ab_hfi`);
  ask ABMI for archived editions. Also the lead author, and the Wayback
  Machine for old download pages (suggestion).
- Check on receipt: edition year, licence (ABMI forbids resale), whether
  `YEAR` is populated.

### 2. Manitoba forestry or resource roads

- Why: our MB layer is the fixed 2009-vintage MLI 20K plus raw BEAD. MB is
  flagged lower confidence (ADR 0004).
- Need: any provincial forest or resource road layer, newer than 2009, with a
  status field if possible.
- Where: DataMB catalogue (check by hand), Manitoba Natural Resources and
  Northern Development forestry branch (no contact found yet), forest
  management licensee plans (suggestion).
- Already ruled out: the geoportal Manitoba Road Network (2016 to 2022) covers
  only department-maintained roads; Manitoba Road Network 2023 has 1,476 lines.

### 3. New Brunswick status or class field

- Why: the Forest Roads layer (Socrata `gnb.socrata.com`, id `udwq-sw5i`) has
  geometry only, so NB has no strict variant. NB is 3.4% roadless, the least
  certain large difference.
- Need: a status, class or year field for the same roads.
- Where: NB Department of Natural Resources (owner of the IRIU portal data).

### 4. Saskatchewan and PEI, newer public sources

- Why: the compilation gives the paper's edition, but it is old and private.
  A public current layer would be citable and refreshable.
- Saskatchewan: `egis@gov.sk.ca`. SURN is NRN-derived and adds no roads. GeoHub
  has forest boundary and cover layers but no road layer found.
- PEI: forestry or environment branch. The public centreline layer (16,910
  features) duplicates the NRN.
- Drafts: note 16.

### 5. Licence and sharing terms

- Poley compilation: terms from the authors (email sent 2026-11-19). Reply
  2026-11-20: WCS will tell the BC Government it intends to redistribute
  altered BC data and expects to share the full dataset; not yet confirmed.
  Follow up with the lead author in early 2027.
- Yukon road layers: licence unverified.
- BC DRA ("Access Only"), ABMI (no resale), NT winter road inference.
- Tracked in issue #32.

## Low priority

- **NT winter roads:** the portal items are opening dates and traffic counts,
  with no geometry. Ask NWT Department of Infrastructure if status matters.
- **BEAD cleaning:** the paper hand-cleaned BEAD; the compilation copy
  probably carries that. Verify before relying on it.
- **Nunavut:** nothing exists beyond the NRN and OSM; about 100% roadless.
- **Newer PEI NRN edition** (19,758 segments): changes NRN by under 1 point.

## What to record when you find something

Source name and URL, edition date, licence text, whether it has a road status
or class field, and file format. Put the file in `data/raw/` (ignored), add a
line here, and tell the assistant so a loader can be written.
