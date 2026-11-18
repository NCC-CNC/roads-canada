"""Probe: what do Geofabrik daily replication diffs give for roadless change? (issue #5)

Downloads a run of daily .osc.gz diffs for one region, keeps highway ways with
the same class exclusions as the roadless method, and reports created, modified
and deleted ways. Geometry comes only from nodes present in the diffs, so the
report also says how many road ways can be drawn from the diffs alone.
Usage: uv run python src/roadless/osm_diff_probe.py <geofabrik-region> <first-seq> <last-seq> <patches.parquet>
Example: osm_diff_probe.py north-america/canada/new-brunswick 4946 4975 data/processed/210101/new-brunswick/patches.parquet
"""
import gzip
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString

from osm_roadless import CRS, EXCLUDED_FCLASS

RAW = Path("data/raw/diffs")
BASE = "https://download.geofabrik.de"


def diff_path(seq: int) -> str:
    return f"{seq // 1_000_000:03d}/{(seq // 1000) % 1000:03d}/{seq % 1000:03d}"


def fetch(region: str, seq: int) -> Path:
    dest = RAW / region.rsplit("/", 1)[-1] / f"{seq}.osc.gz"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        try:
            urllib.request.urlretrieve(f"{BASE}/{region}-updates/{diff_path(seq)}.osc.gz", tmp)
            tmp.replace(dest)
        finally:
            tmp.unlink(missing_ok=True)
    return dest


def parse(path: Path):
    """Yield (action, kind, element-dict) for nodes and ways in one diff."""
    with gzip.open(path, "rb") as f:
        for _, action in ET.iterparse(f):
            if action.tag not in ("create", "modify", "delete"):
                continue
            for el in action:
                if el.tag == "node" and action.tag != "delete":
                    yield action.tag, "node", {"id": el.get("id"), "lon": float(el.get("lon")), "lat": float(el.get("lat"))}
                elif el.tag == "way":
                    tags = {t.get("k"): t.get("v") for t in el.findall("tag")}
                    yield action.tag, "way", {
                        "id": el.get("id"), "version": int(el.get("version")), "ts": el.get("timestamp"),
                        "tags": tags, "refs": [n.get("ref") for n in el.findall("nd")],
                    }
            action.clear()


def is_road(tags: dict) -> bool:
    h = tags.get("highway")
    return h is not None and h not in EXCLUDED_FCLASS


def main(region: str, first: str, last: str, patches_path: str) -> None:
    nodes, ways, counts = {}, {}, Counter()
    for seq in range(int(first), int(last) + 1):
        for action, kind, el in parse(fetch(region, seq)):
            if kind == "node":
                nodes[el["id"]] = (el["lon"], el["lat"])
            elif action == "delete":
                counts["deleted_ways"] += 1
            elif is_road(el["tags"]):
                ways[el["id"]] = (action, el)  # last state in window wins
    created = {i: e for i, (a, e) in ways.items() if a == "create"}
    modified = {i: e for i, (a, e) in ways.items() if a == "modify"}
    print(f"diffs {first}-{last}: road ways created {len(created):,}, modified {len(modified):,}, "
          f"deleted ways (any type) {counts['deleted_ways']:,}")

    def drawable(e):
        return all(r in nodes for r in e["refs"])

    for label, group in (("created", created), ("modified", modified)):
        full = {i: e for i, e in group.items() if drawable(e)}
        part = sum(1 for e in group.values() if any(r in nodes for r in e["refs"]))
        print(f"{label}: fully drawable from diffs {len(full):,} of {len(group):,}; "
              f"at least one node present {part:,}")

    full_new = {i: e for i, e in created.items() if drawable(e) and len(e["refs"]) >= 2}
    if not full_new:
        return
    geoms = [LineString([nodes[r] for r in e["refs"]]) for e in full_new.values()]
    new = gpd.GeoDataFrame({"way_id": list(full_new)}, geometry=geoms, crs="EPSG:4326").to_crs(CRS)
    patches = gpd.read_parquet(patches_path)
    union = patches.geometry.union_all()
    new_len = new.geometry.length.sum() / 1e3
    inside = new.geometry.intersection(union).length.sum() / 1e3
    print(f"drawable new roads: {new_len:,.0f} km; inside 2021 roadless land: {inside:,.0f} km "
          f"({100 * inside / new_len:.1f}%)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
