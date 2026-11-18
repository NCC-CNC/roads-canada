"""Probe: what do Geofabrik daily replication diffs give for roadless change? (issue #5)

Downloads a run of daily .osc.gz diffs for one region, keeps highway ways with
the same class exclusions as the roadless method, and reports created, modified
and deleted ways. Geometry comes only from nodes present in the diffs, so the
report also says how many road ways can be drawn from the diffs alone.
With a base extract (.osm.pbf dated at or after the last diff), geometry for
every created or modified way is read from the extract instead, so edited ways
can be drawn too. The diffs then supply which ways changed and when.
Usage: uv run python src/roadless/osm_diff_probe.py <geofabrik-region> <first-seq> <last-seq> <patches.parquet> [base.osm.pbf]
Example: osm_diff_probe.py north-america/canada/new-brunswick 4946 4975 data/processed/210101/new-brunswick/patches.parquet data/raw/new-brunswick_261117.osm.pbf
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


def base_geometries(pbf: str, way_ids: set[int]) -> dict[str, list]:
    """Coordinates of the wanted ways, read from a base extract with node locations."""
    import osmium

    out = {}
    fp = osmium.FileProcessor(pbf, osmium.osm.NODE | osmium.osm.WAY).with_locations()
    for o in fp:
        if o.is_way() and o.id in way_ids:
            try:
                out[str(o.id)] = [(n.lon, n.lat) for n in o.nodes]
            except osmium.InvalidLocationError:
                pass
    return out


def main(region: str, first: str, last: str, patches_path: str, base_pbf: str | None = None) -> None:
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

    patches = gpd.read_parquet(patches_path)
    union = patches.geometry.union_all()

    def report(label: str, coords: dict) -> None:
        lines = {i: c for i, c in coords.items() if len(c) >= 2}
        if not lines:
            return
        g = gpd.GeoDataFrame({"way_id": list(lines)}, geometry=[LineString(c) for c in lines.values()],
                             crs="EPSG:4326").to_crs(CRS)
        total = g.geometry.length.sum() / 1e3
        inside = g.geometry.intersection(union).length.sum() / 1e3
        print(f"{label}: {len(lines):,} ways, {total:,.0f} km; inside 2021 roadless land: "
              f"{inside:,.0f} km ({100 * inside / total:.1f}%)")

    if base_pbf is None:
        report("created, from diff nodes only",
               {i: [nodes[r] for r in e["refs"]] for i, e in created.items() if drawable(e)})
        return
    wanted = {int(i) for i in ways}
    geoms = base_geometries(base_pbf, wanted)
    print(f"resolved from base extract: {len(geoms):,} of {len(wanted):,} changed road ways "
          f"(rest deleted or no longer a way after the diff window)")
    report("created, from base extract", {i: g for i, g in geoms.items() if i in created})
    report("modified, from base extract", {i: g for i, g in geoms.items() if i in modified})


if __name__ == "__main__":
    main(*sys.argv[1:6])
