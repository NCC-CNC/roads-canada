# 02 Road Data Sources by Jurisdiction

Survey of publicly available road and linear-disturbance datasets, for
issue #1. Compiled 2026-11-17 from web research. "Unverified" means it could
not be confirmed from an official page; several portals are JavaScript-rendered
or blocked automated fetching, so some details come from catalogue APIs,
mirrors on open.canada.ca, or search snippets. Check licence terms at the
source before redistributing anything. Landing-page URLs were reachable for 9
of 10 spot-checked links (open.yukon.ca returns 403 to automated requests).

## Summary

- Provincial or territorial road data now exist for most jurisdictions, but
  completeness of resource, forestry and low-use roads is unconfirmed for
  many. The datasets with documented resource or forest roads are BC (DRA and
  tenure roads), AB (ABMI Human Footprint), ON (MNR Road Segments), NB
  (NBRN and Forest Roads), YT (Forestry Resource Roads) and NL (Resource
  Access Roads, download unverified).
- SK, MB, NS, PE and NU appear to rely on public-road or NRN-derived layers.
- No source has a verified construction or decommissioning date. The nearest
  are BC `DATA_CAPTURE_DATE`, AB origin-year and imagery-year attributes, MB
  `FromDate`/`ToDate` (usefulness unverified), and NL's access-status field.
- Licensing needs follow-up: BC DRA is "Access Only" rather than an open
  licence, ABMI states none on the 2023 page, ON MNR Road Segments conflicts
  between sources, and PE and NL name none.

## Provinces and territories

| Jurisdiction | Dataset (steward) | Resource and low-use roads | Licence | Access | Update | Dates or status |
| --- | --- | --- | --- | --- | --- | --- |
| BC | [DRA Master Partially-Attributed Roads](https://catalogue.data.gov.bc.ca/dataset/digital-road-atlas-dra-master-partially-attributed-roads) (GeoBC) | Yes: urban, rural and resource roads; ROAD_CLASS includes resource, recreation, skid, trail | "Access Only", free of charge; not an OGL-BC label | FGDB (258 MB), WMS, KML, BCGW download | Monthly | `DATA_CAPTURE_DATE`; no construction or decommissioning date |
| BC | [CEF Integrated Roads](https://catalogue.data.gov.bc.ca/dataset/a489bc6a-f676-4503-8cd7-dcf0bdf2ae99) (current; [archive](https://catalogue.data.gov.bc.ca/dataset/9568a219-819d-417a-be68-8431b6fb5de0) 2021, 2024, 2025) | Merges built roads with road tenures; coarse provincial use | Access Only | FGDB, ArcGIS REST (archive) | Modified 2026-07-20 | Tenure award date is not construction date |
| BC | [Human Disturbance 2025](https://catalogue.data.gov.bc.ca/dataset/7d61ff12-b85f-4aeb-ac8b-7b10e84b046c) | Excludes roads | Unverified | Catalogue | Annual-ish (2021, 2023, 2025) | Ranked by permanence |
| AB | [ABMI Human Footprint Inventory](https://abmi.ca/data-portal/86.html), latest 2023 (ABMI) | Yes: gravel, minor dirt access, well-pad access roads | None stated on 2023 page; older metadata allows non-profit reuse with attribution | 4.5 GB FGDB via anonymous FTP; earlier years back to 1950s | About annual; 2023 page modified 2026-10-15 | Origin-year and imagery-year attributes; classes under province-wide review |
| SK | [Saskatchewan Updated Road Network](https://geohub.saskatchewan.ca/maps/saskatchewan::saskatchewan-updated-road-network) (Government of SK) | NRN-derived rural and urban roads; forestry or industrial unverified | Standard Unrestricted Use Data Licence v2.0 | KML, SHP, FGDB (rural roads) | Modified 2025-02-05 | Unverified |
| MB | [Manitoba Road Network](https://geoportal.gov.mb.ca/datasets/manitoba::manitoba-road-network-2022) (annual to 2023) | Highways, provincial roads, access and winter roads; municipal and forestry unverified | OpenMB licence | Many formats, ArcGIS REST | 2023 edition (late 2024); none newer found | `FromDate`, `ToDate`, `CreatedDate`; reliability unverified |
| ON | [ORN Road Net Element](https://data.ontario.ca/en/dataset/ontario-road-network-road-net-element) (MTO) and [MNR Road Segments](https://data.ontario.ca/en/dataset/ministry-of-natural-resources-road-segments) (MNR) | ORN includes "resource and recreational roads"; MNR covers forest, parks and resource access; completeness unverified | OGL-Ontario; a mirror shows "Agreement Required" for MNR (unresolved) | GeoHub, ArcGIS REST | ORN weekly; MNR 2025-10-15 | No date or status fields seen (unverified) |
| QC | [Référentiel québécois du transport terrestre](https://www.donneesquebec.ca/recherche/dataset/referentiel-quebecois-du-transport-terrestre) (MRNF), successor to AQréseau+ | Tagged "Chemin forestier"; completeness unverified | CC-BY 4.0 | FGDB, GPKG, SHP; web service pending | Quarterly | Unverified |
| NB | NBRN ([GeoNB](https://geonb.snb.ca/arcgis/rest/services/GeoNB_Basemap_Topo/MapServer/6)) and [Forest Roads](https://dev.donnees.iriu.ca/en/dataset/68cee0f3-39fe-10ef-20b0-b8cc51b2a5e8) | Yes: primary and secondary forest roads; forest access on Crown and private land | OGL-NB | FGDB, SHP, REST; Forest Roads also GeoJSON and CSV | Forest Roads published 2026-01-23 | Unverified |
| NS | [NSTDB Roads, Trails and Rails](https://data.novascotia.ca/datasets/62ap-bhwk) (GeoNova) | Unclear; no dedicated forest roads layer found | OGL-Nova Scotia | SHP, GeoJSON, KML, CSV | Annual; modified 2026-11-11 | Feature codes only |
| PE | [PEI NRN](https://gis.princeedwardisland.ca/server/rest/services/Hosted/PEI_NRN/FeatureServer) | All roads centreline; private and woods roads unverified | None named (disclaimer only); price list exists | ArcGIS FeatureServer | Semi-annual (March 2026) | Unverified |
| NL | [Resource Access Roads](https://geoatlas.gov.nl.ca/custom/help/ResourceRoadsHelp.html) (Fisheries, Forestry and Agriculture); general roads only via federal NRN | Yes, resource access; Labrador coverage unverified | Unverified | Viewer in Geoscience Atlas; download unverified | Help file Feb 2024 | Access status: Open, Limited, ATV, Not Passable, Unknown |
| YT | [Yukon Road Network](https://open.yukon.ca/data/yukon-road-network) (Geomatics Yukon), [Forestry Resource Roads 50k](https://open.yukon.ca/data/forestry-resource-roads-50k), [Surface Disturbance Linear Features](https://open.yukon.ca/data/surface-disturbance-linear-features) | Forestry layer covers resource roads but is incomplete alone | Unverified (other Yukon data use OGL-Yukon) | Shapefile, ArcGIS, CKAN API | Road network metadata 2025-01-09; disturbance July 2025 | Unverified |
| NT | [Transportation_LCC](https://www.apps.geomatics.gov.nt.ca/arcgis/rest/services/GNWT/Transportation_LCC/MapServer/layers) (NWT Centre for Geomatics) | Community-focused; territory-wide resource roads unverified | Unverified | ArcGIS REST | Unverified | "Not for exact location" |
| NU | No territorial dataset found | None | n/a | Federal NRN, RNF, OSM only | n/a | n/a |

## National and global sources

| Source | Notes | Licence | Access | Update |
| --- | --- | --- | --- | --- |
| [Road Network File 2025](https://www150.statcan.gc.ca/n1/en/catalogue/92-500-X2025001) (Statistics Canada) | National; resource-road completeness unverified | OGL-Canada (per snippet) | GeoPackage, REST | Annual (June 2025) |
| [National Road Network](https://open.canada.ca/data/en/dataset/3d282116-e556-400c-9306-ca1a3cada77f) (Statistics Canada, 13 provincial and territorial datasets) | Built from provincial and territorial contributions; vintage varies | OGL-Canada | GPKG, SHP, WMS, REST | Annual |
| [OSM extracts](https://download.geofabrik.de/north-america/canada.html) (Geofabrik) | Canada and every province and territory, plus tracks as mapped; per-feature timestamps stripped from public extracts | ODbL | PBF | Daily |
| [Overture Maps transportation](https://docs.overturemaps.org/guides/transportation) | OSM plus TomTom; Canada coverage not broken out | ODbL, attribution required | GeoParquet | Monthly (2026-08-19 seen) |
| Microsoft ML Road Detections | Canada included; low-use road coverage unverified | ODbL (per GitHub and mirror) | Per-country files | Unverified |
| Meta AI roads | Nothing found for Canada | n/a | n/a | n/a |
| [BEAD](https://open.canada.ca/data/en/dataset/afd0ce47-17c3-445c-b823-2f86409da2e0) (NRCan) | Boreal only; 2008 to 2010 imagery epoch; mostly roads and seismic lines | Unverified | Unverified | Static |
| [CanLaD](https://donnees.iriu.ca/dataset/902801fd-4d9d-4df4-9e95-319e429545cc) (NRCan) | 30 m raster of fire, harvest, pest; not a roads layer | Unverified | Raster | To 2025 |
| Canada human footprint 2022 ([FACETS](https://facetsjournal.com/doi/10.1139/facets-2021-0063)) | 300 m research product with roads pressure | Unverified | Unverified | One-off |

No current national disturbance product with roads, and no Global Forest Watch
Canada road layer, was found.

## Regulator and permit data

Verified: BC Forest Tenure Road Segment Lines (updated 2025-04-30; "retired"
does not mean the road is gone) and AER monthly well and pipeline shapefiles
(not road layers). Unverified or not found: forestry, oil and gas and mining
road permits in AB, SK, MB, and oil, gas and mining roads in BC. Feeds issue #8.

## Implications for the pipeline

1. OSM (daily Geofabrik extracts) plus Overture is the only nationally
   consistent, openly licensed, frequently updated base.
2. Best candidates for a first provincial dataset (issue #4): BC DRA (resource
   classes, monthly, licence to check), ABMI HFI (repeat years, imagery dates),
   or NB (open licence, documented forest roads).
3. Date attributes are the missing piece everywhere; OSM history (issue #5)
   and ABMI origin years are the most promising routes.

## Follow-ups

- Resolve licences: BC "Access Only", ABMI 2023, ON MNR, PE, NL, Yukon, NWT.
- Read attribute documentation for QC, SK, NS, PE, ON and NRN for date and
  status fields.
- Confirm Labrador coverage and a download route for NL Resource Access Roads.
- Re-run Yukon and NWT checks with a browser, since fetches were blocked.
