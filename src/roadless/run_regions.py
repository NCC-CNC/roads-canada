"""Resumable multi-province roadless-area runner.

Usage: uv run python src/roadless/run_regions.py <YYMMDD> <province>... [--force]
       uv run python src/roadless/run_regions.py <YYMMDD> all

Stages per province: fetch inputs, verify the zip, compute, write results to
data/processed/<YYMMDD>/<slug>/ (stats.json and patches.parquet). A finished
province (stats.json present) is skipped on rerun unless --force. A failure is
logged to data/processed/<YYMMDD>/errors.log and the loop moves on, so one bad
province does not cost the others. Exit code is 1 if any province failed.
"""
import json
import sys
import time
import traceback
import zipfile
from pathlib import Path

from fetch_inputs import fetch_boundary, fetch_osm
from osm_roadless import load_boundary, load_roads, roadless_patches, summarize

# StatCan PRENAME -> Geofabrik slug under north-america/canada/
PROVINCES = {
    "British Columbia": "british-columbia", "Alberta": "alberta",
    "Saskatchewan": "saskatchewan", "Manitoba": "manitoba", "Ontario": "ontario",
    "Quebec": "quebec", "New Brunswick": "new-brunswick", "Nova Scotia": "nova-scotia",
    "Prince Edward Island": "prince-edward-island",
    "Newfoundland and Labrador": "newfoundland-and-labrador",
    "Yukon": "yukon", "Northwest Territories": "northwest-territories",
    "Nunavut": "nunavut",
}


def verify_zip(path: Path) -> None:
    """Fail fast on a truncated or corrupt download, before any compute."""
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
    if bad:
        raise RuntimeError(f"{path} is corrupt (first bad member: {bad})")


def run_one(province: str, stamp: str, out_root: Path, force: bool) -> str:
    slug = PROVINCES[province]
    out = out_root / slug
    if (out / "stats.json").exists() and not force:
        return "skipped (done)"
    out.mkdir(parents=True, exist_ok=True)
    osm_zip = fetch_osm(f"north-america/canada/{slug}", stamp)
    verify_zip(osm_zip)
    boundary = load_boundary(fetch_boundary(province))
    t = time.time()
    roads = load_roads(osm_zip)
    patches = roadless_patches(roads, boundary)
    stats = summarize(patches, boundary.geometry.area.sum() / 1e6)
    stats.update(province=province, snapshot=stamp, roads_kept=len(roads),
                 seconds=round(time.time() - t))
    patches.to_parquet(out / "patches.parquet")
    (out / "stats.json").write_text(json.dumps(stats, indent=2))  # written last = done marker
    return f"done in {stats['seconds']} s, {stats['pct_roadless']:.1f}% roadless"


def main(argv: list[str]) -> int:
    force = "--force" in argv
    args = [a for a in argv if a != "--force"]
    stamp, names = args[0], args[1:]
    if names == ["all"]:
        names = list(PROVINCES)
    unknown = [n for n in names if n not in PROVINCES]
    if unknown:
        raise SystemExit(f"Unknown province(s) {unknown}; choose from {list(PROVINCES)}")
    out_root = Path("data/processed") / stamp
    out_root.mkdir(parents=True, exist_ok=True)
    failed = []
    for name in names:
        try:
            print(f"{name}: {run_one(name, stamp, out_root, force)}", flush=True)
        except Exception:
            failed.append(name)
            with open(out_root / "errors.log", "a") as f:
                f.write(f"--- {name} ---\n{traceback.format_exc()}\n")
            print(f"{name}: FAILED (see {out_root / 'errors.log'})", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
