"""Fetch inputs for the OSM roadless prototype into data/raw/.

Usage:
  uv run python src/roadless/fetch_inputs.py osm <region-path> [YYMMDD|latest]
  uv run python src/roadless/fetch_inputs.py boundary <province name>

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
        urllib.request.urlretrieve(url, dest)
    return dest


def fetch_osm(region: str, stamp: str = "latest") -> Path:
    name = region.rsplit("/", 1)[-1]
    url = f"{GEOFABRIK}/{region}-{stamp}-free.shp.zip"
    return download(url, RAW / f"{name}_{stamp}.shp.zip")


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
    print({"osm": fetch_osm, "boundary": fetch_boundary}[kind](*rest))
