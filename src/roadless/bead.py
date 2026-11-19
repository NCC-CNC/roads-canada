"""ECCC Boreal Ecosystem Anthropogenic Disturbance (BEAD) roads, 2010 and 2015 editions.

Environment and Climate Change Canada, Open Government Licence - Canada. The
paper added BEAD roads to its Manitoba and Northwest Territories networks
(note 13), where resource roads are otherwise missing. Both editions are
Landsat-interpreted (2008 to 2010 and 2015) and cover the boreal zone and
boreal caribou ranges, not all of Canada.

- 2010: zip of shapefiles (584k linear features, ALBERS), downloaded from
  https://www.ec.gc.ca/data_donnees/STB-DGST/003/Boreal-ecosystem-anthropogenic-disturbance-vector-data-2008-2010.zip
  and extracted to data/raw/bead2010/.
- 2015: ArcGIS service DisturbanceFootprintUpdatedFor2015 layer 0, fetched with
  `fetch_inputs.py arcgis <layer> bead2015_roads "Class='Road'"` (82,261 roads).

Only features of Class 'Road' are used. The paper cleaned them by hand
(dropping segments that did not follow a visible road and small unconnected
segments); that is not reproduced here, so these are raw BEAD roads.
"""
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

from fetch_inputs import RAW, download, fetch_arcgis, fetch_boundary
from osm_roadless import CRS, load_boundary

URL_2010 = "https://www.ec.gc.ca/data_donnees/STB-DGST/003/Boreal-ecosystem-anthropogenic-disturbance-vector-data-2008-2010.zip"
SVC_2015 = "https://maps-cartes.ec.gc.ca/arcgis/rest/services/STB_DGST/DisturbanceFootprintUpdatedFor2015/MapServer/0"
SHP_2010 = RAW / "bead2010" / "EC_borealdisturbance_linear_2008_2010_FINAL_ALBERS.shp"


def fetch_bead2010() -> Path:
    if not SHP_2010.exists():
        z = download(URL_2010, RAW / "bead2010" / "bead2010.zip")
        with zipfile.ZipFile(z) as f:
            f.extractall(RAW / "bead2010")
    return SHP_2010


def fetch_bead2015() -> Path:
    return fetch_arcgis(SVC_2015, "bead2015_roads", "Class='Road'")


def load_bead(province: str) -> gpd.GeoDataFrame:
    """BEAD roads (both editions) within 2 km of the province, EPSG:3347.

    The 2 km margin keeps roads just across the border, whose 1 km buffer
    reaches into the province, and drops roads in neighbouring provinces.
    """
    land = load_boundary(fetch_boundary(province)).to_crs(CRS).geometry.union_all()
    bbox = tuple(land.bounds)
    near = land.buffer(2000)
    parts = []
    for path, layer in ((fetch_bead2010(), None), (fetch_bead2015(), "roads")):
        g = gpd.read_file(path, layer=layer, engine="pyogrio", columns=["Class"],
                          where="Class = 'Road'", bbox=_bbox_in(path, layer, bbox))
        g = g.to_crs(CRS)
        parts.append(g[g.intersects(near)][["geometry"]])
    return gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=CRS)


def _bbox_in(path: Path, layer, bbox_3347: tuple) -> tuple:
    """Reproject a 3347 bounding box into the file's CRS for the read filter."""
    import pyogrio
    from shapely.geometry import box
    crs = pyogrio.read_info(path, layer=layer)["crs"]
    return tuple(gpd.GeoSeries([box(*bbox_3347)], crs=CRS).to_crs(crs).total_bounds)
