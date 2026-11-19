"""Compare our roadless-area runs with Table 4 of Poley et al. (2022).

Usage: uv run python src/roadless/compare_to_paper.py
Prints a markdown table. Reads data/processed/*/stats.json and the CSV made by
paper_tables.py.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "data/external/poley2022/poley2022_table4_roadless.csv"
PROC = ROOT / "data/processed"
# province code -> (slug, paper provincial dataset, our provincial label)
PROVS = {
    "BC": ("british-columbia", "BCDRA", "bcdra"),
    "AB": ("alberta", "ABHFP", "abhfi"),
    "ON": ("ontario", "ORN", "on"),
    "QC": ("quebec", "AQR", "qc"),
    "NS": ("nova-scotia", "NSTDB", "ns"),
}


def stats(label, slug):
    p = PROC / label / slug / "stats.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    paper = {(r["province"], r["dataset"]): r for r in csv.DictReader(open(PAPER))}
    print("| Prov | Source | Paper km2 | Ours km2 | Diff % | Paper % | Ours % | Paper patches | Our patches | Paper mean km2 | Our mean km2 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for prov, (slug, pds, plabel) in PROVS.items():
        for name, pname, ours in [("OSM 2021", "OSM", stats("210101", slug)),
                                  ("NRN", "NRN", stats("nrn", slug)),
                                  (pds, pds, stats(plabel, slug))]:
            p = paper[(prov, pname)]
            if ours is None:
                continue
            pk, ok = float(p["roadless_km2"]), ours["roadless_km2"]
            print(f"| {prov} | {name} | {pk:,.0f} | {ok:,.0f} | {100*(ok-pk)/pk:+.1f} | "
                  f"{p['pct_roadless']} | {ours['pct_roadless']:.1f} | {int(p['n_patches']):,} | "
                  f"{ours['patches']:,} | {float(p['mean_patch_km2']):.1f} | {ours['mean_km2']:.1f} |")


if __name__ == "__main__":
    main()
