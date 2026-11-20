"""Fetch inputs for the OSM roadless prototype into data/raw/.

Usage:
  uv run python src/roadless/fetch_inputs.py osm <region-path> [YYMMDD|latest]
  uv run python src/roadless/fetch_inputs.py boundary <province name>
  uv run python src/roadless/fetch_inputs.py pbf <region-path> <YYMMDD>
  uv run python src/roadless/fetch_inputs.py nrn <two-letter code, e.g. ns>
  uv run python src/roadless/fetch_inputs.py bcdra
  uv run python src/roadless/fetch_inputs.py abhfi
  uv run python src/roadless/fetch_inputs.py rqtt
  uv run python src/roadless/fetch_inputs.py socrata <host> <resource-id> <name>
  uv run python src/roadless/fetch_inputs.py arcgis <layer-url> <name> [where]

Examples:
  fetch_inputs.py osm north-america/canada/nova-scotia 210101
  fetch_inputs.py boundary "Nova Scotia"

Geofabrik keeps public snapshots dated 1 January each year back to 2014.
Boundaries: the default is the Statistics Canada 2016 Cartographic Boundary
File (lpr_000b16a_e.zip), which reproduces the paper's land areas (ADR 0003).
Download it manually from Statistics Canada (Boundary Files, 2016 Census,
Provinces/territories, Cartographic Boundary File, ArcGIS, English) and place
the zip in data/raw/. If it is absent, the fallback is geoBoundaries CAN ADM1
(pinned commit; about 650 MB national file, only the province is kept), which
leaves coastal slivers and gives more patches than the paper.
"""
import os
import sys
import json
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

RAW = Path("data/raw")
GEOFABRIK = "https://download.geofabrik.de"
GEOBOUNDARIES = (
    "https://github.com/wmgeolab/geoBoundaries/raw/41af8f1/"
    "releaseData/gbOpen/CAN/ADM1/geoBoundaries-CAN-ADM1.geojson"
)


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        # Download under a temporary name and rename on success, so an
        # interrupted download never leaves a truncated file that looks complete.
        tmp = dest.with_name(dest.name + ".part")
        try:
            urllib.request.urlretrieve(url, tmp)
            tmp.replace(dest)
        finally:
            tmp.unlink(missing_ok=True)
    return dest


def fetch_osm(region: str, stamp: str = "latest") -> Path:
    name = region.rsplit("/", 1)[-1]
    url = f"{GEOFABRIK}/{region}-{stamp}-free.shp.zip"
    return download(url, RAW / f"{name}_{stamp}.shp.zip")


def fetch_pbf(region: str, stamp: str) -> Path:
    """Dated regional .osm.pbf (base extract for replication-diff geometry).

    Geofabrik's `-latest` name is a redirect page, so pass an explicit date.
    """
    name = region.rsplit("/", 1)[-1]
    return download(f"{GEOFABRIK}/{region}-{stamp}.osm.pbf", RAW / f"{name}_{stamp}.osm.pbf")


NRN_URL = "https://geo.statcan.gc.ca/nrn_rrn/{p}/nrn_rrn_{p}_GPKG.zip"


def fetch_nrn(code: str) -> Path:
    """National Road Network GeoPackage (English) for one province or territory.

    Downloads the Statistics Canada zip to data/raw/nrn/ and extracts the
    English .gpkg next to it; returns the .gpkg path. Current edition only:
    StatCan publishes no dated archive at this URL.
    """
    code = code.lower()
    zip_path = download(NRN_URL.format(p=code), RAW / "nrn" / f"nrn_rrn_{code}_GPKG.zip")
    found = sorted((RAW / "nrn" / code).rglob("*_en.gpkg"))
    if found:
        return found[-1]
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(RAW / "nrn" / code, [n for n in z.namelist() if n.endswith("_en.gpkg")])
    return sorted((RAW / "nrn" / code).rglob("*_en.gpkg"))[-1]


BCDRA_URL = "https://nrs.objectstore.gov.bc.ca/itqlyp/DRA_Public/dgtl_road_atlas.gdb.zip"


def fetch_bcdra() -> Path:
    """BC Digital Road Atlas (full province geodatabase, about 258 MB).

    The zip holds the geodatabase files flat, so they are extracted into a
    `dra.gdb` folder GDAL can open. Current edition only (monthly updates).
    """
    d = RAW / "bc_dra"
    zip_path = download(BCDRA_URL, d / "dgtl_road_atlas.gdb.zip")
    gdb = d / "dra.gdb"
    if not gdb.exists():
        tmp = d / "dra.gdb.part"
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(tmp)
        tmp.replace(gdb)
    return gdb


ABHFI_URL = "https://ftp-public.abmi.ca///GISData/HumanFootprint/2023/HFI2023_v1_1.gdb.zip"


def fetch_abhfi() -> Path:
    """Alberta Human Footprint Inventory 2023 (ABMI), about 4.8 GB zip.

    Licence (metadata section 1.11): reproduction free for educational, data
    collection or non-profit purposes with acknowledgement; no resale.
    Downloads are not resumable here (a stale .part is overwritten); extracts to
    data/raw/ab_hfi/ and returns the geodatabase path.
    """
    d = RAW / "ab_hfi"
    zip_path = download(ABHFI_URL, d / "HFI2023_v1_1.gdb.zip")
    gdb = d / "HFI2023_v1_1" / "HFI2023_v1_1.gdb"
    if not gdb.exists():
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(d)
    return gdb


ABHFI_2018_URL = "https://ftp-public.abmi.ca/GISData/HumanFootprint/2018/HFI_2018_v1.gdb.zip"


def fetch_abhfi_2018() -> Path:
    """Alberta Human Footprint Inventory 2018 (ABMI), about 3.4 GB zip.

    The edition the paper used (note 12). The ABMI page names no licence; see
    its Terms and Conditions (issue #32). Extracts to data/raw/ab_hfi_2018/extracted/.
    """
    d = RAW / "ab_hfi_2018"
    zip_path = download(ABHFI_2018_URL, d / "HFI_2018_v1.gdb.zip")
    gdb = d / "extracted" / "HFI_2018_v1.gdb"
    if not gdb.exists():
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(d / "extracted")
    return gdb


def _arcgis_json(url: str, params: dict, tries: int = 5) -> dict:
    q = urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            with urllib.request.urlopen(f"{url}?{q}", timeout=120) as r:
                d = json.load(r)
            if "error" in d:
                raise RuntimeError(d["error"])
            return d
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def fetch_arcgis(layer_url: str, name: str, where: str = "1=1") -> Path:
    """Download an ArcGIS REST feature layer to data/raw/<name>.gpkg (layer `roads`).

    Pages by OBJECTID in the layer's maximum record count, keeps each page as a
    GeoJSON file under data/raw/<name>_pages/ so an interrupted run resumes, then
    merges them. Coordinates arrive as WGS84 (GeoJSON); the pipeline reprojects.
    Current edition only: services keep no history.
    """
    import geopandas as gpd
    import pandas as pd

    out = RAW / f"{name}.gpkg"
    if out.exists():
        return out
    pages = RAW / f"{name}_pages"
    pages.mkdir(parents=True, exist_ok=True)
    info = _arcgis_json(layer_url, {"f": "json"})
    step = min(int(info.get("maxRecordCount", 1000)), 2000)
    oid_field = next((f["name"] for f in info["fields"] if f["type"] == "esriFieldTypeOID"), "OBJECTID")
    ids = _arcgis_json(f"{layer_url}/query", {"where": where, "returnIdsOnly": "true", "f": "json"})
    oids = sorted(ids["objectIds"])
    print(f"{name}: {len(oids):,} features, {step} per page", file=sys.stderr, flush=True)
    chunks = [oids[i:i + step] for i in range(0, len(oids), step)]

    def get(n_chunk):
        n, chunk = n_chunk
        dest = pages / f"p{n:05d}.geojson"
        if dest.exists():
            return
        d = _arcgis_json(f"{layer_url}/query", {
            "where": f"{oid_field} >= {chunk[0]} AND {oid_field} <= {chunk[-1]} AND ({where})",
            "outFields": "*", "outSR": 4326, "f": "geojson"})
        tmp = dest.with_name(dest.name + ".part")
        tmp.write_text(json.dumps(d))
        tmp.replace(dest)

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(get, enumerate(chunks)))
    frames = [gpd.read_file(f) for f in sorted(pages.glob("p*.geojson"))]
    gdf = pd.concat(frames, ignore_index=True)
    if len(gdf) < len(oids):
        raise RuntimeError(f"{name}: got {len(gdf)} of {len(oids)} features")
    tmp = out.with_name(out.name + ".part")
    gpd.GeoDataFrame(gdf, crs="EPSG:4326").to_file(tmp, layer="roads", driver="GPKG")
    tmp.replace(out)
    return out


RQTT_URL = ("https://diffusion.mern.gouv.qc.ca/diffusion/RGQ/Vectoriel/Theme/Local/RQTT/"
            "OGC(GPKG)/RQTT_GPKG.zip")


def fetch_rqtt() -> Path:
    """Quebec Referentiel quebecois du transport terrestre (GeoPackage, about 409 MB zip)."""
    d = RAW / "qc_rqtt"
    zip_path = download(RQTT_URL, d / "RQTT_GPKG.zip")
    found = sorted(d.rglob("RQTT.gpkg"))
    if not found:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(d)
        found = sorted(d.rglob("RQTT.gpkg"))
    return found[0]


def fetch_socrata(host: str, resource_id: str, name: str, page: int = 50_000) -> Path:
    """Download a Socrata geospatial dataset to data/raw/<name>.gpkg (layer `roads`).

    Pages the GeoJSON resource endpoint ordered by row id, one file per page, so
    an interrupted run resumes; checks the row count before writing.
    """
    import geopandas as gpd
    import pandas as pd

    out = RAW / f"{name}.gpkg"
    if out.exists():
        return out
    pages = RAW / f"{name}_pages"
    pages.mkdir(parents=True, exist_ok=True)
    base = f"https://{host}/resource/{resource_id}"
    with urllib.request.urlopen(f"{base}.json?" + urllib.parse.urlencode({"$select": "count(*)"}),
                                timeout=120) as r:
        total = int(json.load(r)[0]["count"])
    for n, off in enumerate(range(0, total, page)):
        dest = pages / f"p{n:05d}.geojson"
        if dest.exists():
            continue
        q = urllib.parse.urlencode({"$limit": page, "$offset": off, "$order": ":id"})
        for i in range(5):
            try:
                with urllib.request.urlopen(f"{base}.geojson?{q}", timeout=600) as r:
                    data = r.read()
                break
            except Exception:
                if i == 4:
                    raise
                time.sleep(2 ** i)
        tmp = dest.with_name(dest.name + ".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
    gdf = pd.concat([gpd.read_file(f) for f in sorted(pages.glob("p*.geojson"))], ignore_index=True)
    if len(gdf) != total:
        raise RuntimeError(f"{name}: got {len(gdf)} of {total} rows")
    tmp = out.with_name(out.name + ".part")
    gpd.GeoDataFrame(gdf, crs="EPSG:4326").to_file(tmp, layer="roads", driver="GPKG")
    tmp.replace(out)
    return out


STATCAN_ZIP = RAW / "lpr_000b16a_e.zip"


def fetch_boundary(province: str) -> Path:
    import geopandas as gpd

    out = RAW / f"boundary_{province.lower().replace(' ', '_')}.gpkg"
    if out.exists():
        return out
    if STATCAN_ZIP.exists():
        gdf = gpd.read_file(f"zip://{STATCAN_ZIP}!lpr_000b16a_e.shp", engine="pyogrio")
        sel = gdf[gdf["PRENAME"] == province]
        if sel.empty:
            raise SystemExit(f"No province {province!r}; have {gdf['PRENAME'].tolist()}")
        sel.to_file(out, driver="GPKG")
        return out
    print(f"{STATCAN_ZIP} not found; falling back to geoBoundaries (not paper-equivalent)",
          file=sys.stderr)
    os.environ.setdefault("OGR_GEOJSON_MAX_OBJ_SIZE", "0")
    national = download(GEOBOUNDARIES, RAW / "gb_can_adm1.geojson")
    gdf = gpd.read_file(national)
    sel = gdf[gdf["shapeName"] == province]
    if sel.empty:
        raise SystemExit(f"No province {province!r}; have {gdf['shapeName'].tolist()}")
    sel.to_file(out, driver="GPKG")
    national.unlink()  # keep only the small per-province file
    return out


if __name__ == "__main__":
    kind, *rest = sys.argv[1:]
    print({"osm": fetch_osm, "boundary": fetch_boundary, "pbf": fetch_pbf, "nrn": fetch_nrn, "bcdra": fetch_bcdra, "abhfi": fetch_abhfi, "arcgis": fetch_arcgis, "rqtt": fetch_rqtt, "socrata": fetch_socrata}[kind](*rest))
