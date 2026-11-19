"""Shared driver for single-province dataset runs (BC DRA, Alberta HFI, ...).

A dataset module supplies a loader returning vehicle roads in EPSG:3347; this
writes stats.json (the done marker, last) and patches.parquet to
data/processed/<label>/<slug>/, in the same layout as run_regions.py.
"""
import json
import time
from pathlib import Path

from fetch_inputs import fetch_boundary
from osm_roadless import load_boundary, roadless_patches, summarize


def run(label: str, province: str, slug: str, load_roads, **extra) -> dict:
    out = Path("data/processed") / label / slug
    out.mkdir(parents=True, exist_ok=True)
    boundary = load_boundary(fetch_boundary(province))
    t = time.time()
    roads = load_roads()
    patches = roadless_patches(roads, boundary)
    stats = summarize(patches, boundary.geometry.area.sum() / 1e6)
    stats.update(province=province, roads_kept=len(roads),
                 road_km=round(roads.length.sum() / 1000), seconds=round(time.time() - t), **extra)
    patches.to_parquet(out / "patches.parquet")
    (out / "stats.json").write_text(json.dumps(stats, indent=2))
    print(f"{label}: {stats['road_km']:,} km, {stats['pct_roadless']:.1f}% roadless, "
          f"{stats['patches']} patches", flush=True)
    return stats
