"""Consolidated roadless-area table, one row per jurisdiction.

Usage: uv run python src/roadless/summary_table.py [out.csv]
Reads data/processed/*/<slug>/stats.json and the paper's Table 4 CSV. Prints a
markdown table; the best-source column is the most detailed dataset run for the
jurisdiction (a provincial or resource-road source), else the NRN.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data/processed"
PAPER = ROOT / "data/external/poley2022/poley2022_table4_roadless.csv"

# code, name, slug, best-source label (dir), description, paper provincial dataset
ROWS = [
    ("BC", "British Columbia", "british-columbia", "bcdra", "BC DRA", "BCDRA"),
    ("AB", "Alberta", "alberta", "abhfi", "HFI 2023", "ABHFP"),
    ("SK", "Saskatchewan", "saskatchewan", None, "none (NRN, OSM only)", None),
    ("MB", "Manitoba", "manitoba", "mb", "NRN + MLI 20k + BEAD", None),
    ("ON", "Ontario", "ontario", "on", "ORN + MNR", "ORN"),
    ("QC", "Quebec", "quebec", "qc", "RQTT", "AQR"),
    ("NB", "New Brunswick", "new-brunswick", "nb", "NBRN + Forest Roads", None),
    ("NS", "Nova Scotia", "nova-scotia", "ns", "NSTDB", "NSTDB"),
    ("PE", "Prince Edward Island", "prince-edward-island", None, "none (NRN, OSM only)", None),
    ("NL", "Newfoundland and Labrador", "newfoundland-and-labrador", "nl", "NRN + Resource Access Roads", None),
    ("YT", "Yukon", "yukon", "yt", "Road Network + Forest Resource Roads", None),
    ("NT", "Northwest Territories", "northwest-territories", "nt", "NRN + BEAD", None),
    ("NU", "Nunavut", "nunavut", None, "none (NRN, OSM only)", None),
]


def pct(label, slug):
    p = PROC / label / slug / "stats.json"
    return json.loads(p.read_text())["pct_roadless"] if p.exists() else None


def fmt(x):
    return "n/a" if x is None else f"{x:.1f}"


def main():
    paper = {(r["province"], r["dataset"]): float(r["pct_roadless"]) for r in csv.DictReader(open(PAPER))}
    out = []
    for code, name, slug, label, desc, pds in ROWS:
        out.append([code, fmt(pct("210101", slug)), fmt(pct("nrn", slug)), desc,
                    fmt(pct(label, slug) if label else None),
                    fmt(pct(f"{label}_strict", slug) if label else None),
                    str(paper[(code, pds)]) if pds else "n/a"])
    head = ["Jurisdiction", "OSM 2021 %", "NRN %", "Best source", "Best %", "Strict %", "Paper provincial %"]
    print("| " + " | ".join(head) + " |\n| " + " | ".join("---" for _ in head) + " |")
    for r in out:
        print("| " + " | ".join(r) + " |")
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", newline="") as f:
            csv.writer(f).writerows([head] + out)


if __name__ == "__main__":
    main()
