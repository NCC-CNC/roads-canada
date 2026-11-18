"""Fetch inputs for the OSM roadless prototype into data/raw/.

Usage:
  uv run python src/roadless/fetch_inputs.py osm <region-path> [YYMMDD|latest]
  uv run python src/roadless/fetch_inputs.py boundary <province name>
  uv run python src/roadless/fetch_inputs.py pbf <region-path> <YYMMDD>
  uv run python src/roadless/fetch_inputs.py nrn <two-letter code, e.g. ns>
  uv run python src/roadless/fetch_inputs.py bcdra

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
    print({"osm": fetch_osm, "boundary": fetch_boundary, "pbf": fetch_pbf, "nrn": fetch_nrn, "bcdra": fetch_bcdra}[kind](*rest))
