"""Why the Alberta HFI 2023 roadless area is below the paper's (note 12).

Two diagnostics on the road centerline layer, default filter (paper exclusion):
1. Unique footprint per road class: roadless land that exists only because that
   class is absent (leave-one-class-out), per km of road, and how far sampled
   segments lie from the nearest road of any other class.
2. The largest strict-variant patch, and how much of it each strict-only class
   (vegetated, vegetated-OSE, winter) removes when added back on its own.
Needs data/processed/abhfi_strict/alberta/patches.parquet for part 2.
Usage: uv run python src/roadless/abhfi_diagnostics.py [outdir]   (about 15 minutes)
Output: abhfi_class_footprint.csv, abhfi_class_distance.csv, printed block check.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely import union_all

from fetch_inputs import fetch_abhfi, fetch_boundary
from osm_roadless import BUFFER_M, CRS, load_boundary
import abhfi_roadless as a

GROUP = {"ROAD-GRAVEL-1L": "gravel", "ROAD-GRAVEL-2L": "gravel", "ROAD-UNIMPROVED": "unimproved",
         "TRUCK-TRAIL": "truck_trail", "ROAD-VEGETATED": "vegetated", "ROAD-VEGETATED-OSE": "vegetated_OSE",
         "ROAD-WINTER": "winter", "ROAD-UNCLASSIFIED": "unclassified"}  # the rest: paved_other


def class_footprint(roads: gpd.GeoDataFrame, land) -> pd.DataFrame:
    names = sorted(roads.grp.unique())
    km = {g: roads[roads.grp == g].length.sum() / 1000 for g in names}
    buf = {g: union_all(roads[roads.grp == g].geometry.buffer(BUFFER_M).values) for g in names}
    pre, suf, acc = [], [None] * len(names), None
    for g in names:
        acc = buf[g] if acc is None else acc.union(buf[g])
        pre.append(acc)
    acc = None
    for i in range(len(names) - 1, -1, -1):
        acc = buf[names[i]] if acc is None else acc.union(buf[names[i]])
        suf[i] = acc
    total = land.difference(pre[-1]).area / 1e6
    rows = []
    for i, g in enumerate(names):
        parts = [x for x in (pre[i - 1] if i else None, suf[i + 1] if i < len(names) - 1 else None) if x is not None]
        others = parts[0] if len(parts) == 1 else parts[0].union(parts[1])
        gain = land.difference(others).area / 1e6 - total
        foot = land.intersection(buf[g]).area / 1e6
        rows.append(dict(group=g, km=km[g], footprint_km2=foot, unique_km2=gain,
                         pct_footprint_unique=100 * gain / foot, unique_km2_per_km=gain / km[g]))
    return pd.DataFrame(rows).sort_values("unique_km2", ascending=False)


def class_distance(roads: gpd.GeoDataFrame, n: int = 20000) -> pd.DataFrame:
    out = []
    for g in sorted(roads.grp.unique()):
        s = roads[roads.grp == g].sample(min(n, (roads.grp == g).sum()), random_state=1)
        pts = gpd.GeoDataFrame(geometry=s.geometry.interpolate(0.5, normalized=True), crs=CRS)
        j = gpd.sjoin_nearest(pts, roads[roads.grp != g][["geometry"]], distance_col="d", how="left")
        d = j.groupby(level=0).d.min()
        out.append(dict(group=g, n=len(d), median_m=d.median(), p25_m=d.quantile(.25), p75_m=d.quantile(.75),
                        pct_within_2km=100 * (d <= 2000).mean(), pct_over_5km=100 * (d > 5000).mean()))
    return pd.DataFrame(out)


def block_check(raw: gpd.GeoDataFrame) -> None:
    strict = gpd.read_parquet("data/processed/abhfi_strict/alberta/patches.parquet")
    big = strict.loc[strict.area_km2.idxmax()].geometry
    ex = raw[raw.FEATURE_TY.isin(a.STRICT_EXTRA_TYPE)]
    ex = ex[ex.intersects(big)].copy()
    ex["km"] = ex.length / 1000
    print(f"strict largest patch {big.area / 1e6:,.0f} km2")
    print(ex.groupby(["FEATURE_TY", "SOURCE"]).km.agg(["count", "sum"]).round(0))

    def largest(sub):
        rem = big.difference(sub.geometry.buffer(BUFFER_M).union_all())
        return gpd.GeoSeries([rem], crs=CRS).explode(index_parts=False).area.max() / 1e6

    for t in a.STRICT_EXTRA_TYPE:
        print(f"largest block with only {t} added back: {largest(ex[ex.FEATURE_TY == t]):,.0f} km2")
    print(f"largest block with all three added back: {largest(ex):,.0f} km2")


def main(outdir: str = ".") -> None:
    raw = gpd.read_file(fetch_abhfi(), layer=a.LAYER, engine="pyogrio",
                        columns=["FEATURE_TY", "SOURCE", "YEAR"]).to_crs(CRS)
    roads = raw[~raw.FEATURE_TY.isin(a.EXCLUDED_TYPE)].copy()
    roads["grp"] = roads.FEATURE_TY.map(GROUP).fillna("paved_other")
    land = load_boundary(fetch_boundary("Alberta")).geometry.union_all()
    fp = class_footprint(roads, land)
    fp.to_csv(Path(outdir) / "abhfi_class_footprint.csv", index=False)
    print(fp.round(2).to_string(index=False))
    dist = class_distance(roads)
    dist.to_csv(Path(outdir) / "abhfi_class_distance.csv", index=False)
    print(dist.round(1).to_string(index=False))
    block_check(raw)


if __name__ == "__main__":
    main(*sys.argv[1:2])
