"""Extract Tables 2 and 4 of Poley et al. (2022) from the paper PDF into CSV.

Usage: uv run python src/roadless/paper_tables.py [pdf] [out_dir]

Needs `pdftotext` (poppler). Three Table 4 cells are printed with leading
digits missing in the PDF itself (AB OSM, AB ABHFP, ON GRIP roadless area);
they are restored from the printed percent cover and flagged `reconstructed`.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

DATASETS = {"gROADS", "GRIP", "OSM", "NRN", "SC", "BCDRA", "ABHFP",
            "ORN", "AQR", "NSTDB"}
PROV = {"BC", "AB", "SK", "MB", "ON", "QC", "NB", "NS", "PE", "NL", "NU", "YK", "NT"}
NUM = r"-?[\d,]+(?:\.\d+)?"

# (province, dataset) -> (printed value, reconstructed value). Printed digits
# are cut off in the PDF; the reconstruction keeps the printed % cover true.
FIXES = {("AB", "OSM"): (63598, 363598), ("AB", "ABHFP"): (99382, 299382),
         ("ON", "GRIP"): (2546, 902546)}


def num(s):
    return float(s.replace(",", ""))


def parse(text):
    t2, t4 = [], []
    t2_prov = t4_prov = None
    t4_area = None
    in2 = in4 = False
    for line in text.splitlines():
        if "TABLE 2" in line.replace("T A B L E 2", "TABLE 2") or "T A B L E 2" in line:
            in2, in4 = True, False
        if "TABLE 4" in line or "T A B L E 4" in line:
            in2, in4 = False, True
        if line.strip().startswith("Abbreviations"):
            in2 = in4 = False
        toks = line.split()
        if not toks:
            continue
        if in2:
            m = re.match(rf"\s*(?:({'|'.join(PROV)})\s+({NUM})\s+)?(Global|National|Provincial)\s+(\S+)\s+({NUM})\s+({NUM})\s+(\d+)%", line)
            if m:
                if m.group(1):
                    t2_prov, area = m.group(1), num(m.group(2))
                    t2_area = area
                t2.append([t2_prov, t2_area, m.group(3), m.group(4),
                           num(m.group(5)), num(m.group(6)), int(m.group(7))])
        if in4:
            m = re.match(rf"\s*(?:({'|'.join(PROV)})\s+({NUM})\s+)?(?:Prov\.\s+)?({'|'.join(DATASETS)})\s+({NUM})\s+(\d+)%\s+((?:{NUM}\s+){{9}}{NUM})\s*$", line)
            if m:
                if m.group(1):
                    t4_prov, t4_area = m.group(1), num(m.group(2))
                vals = [num(x) for x in m.group(6).split()]
                vals = vals[:3] + [int(v) for v in vals[3:]]
                t4.append([t4_prov, t4_area, m.group(3), num(m.group(4)),
                           int(m.group(5))] + vals)
    return t2, t4


def main():
    here = Path(__file__).resolve().parents[2]
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "data/external/poley2022/Poley_et_al_2022_Roadless_Areas_Canada.pdf"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else pdf.parent
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True,
                          capture_output=True, text=True).stdout
    t2, t4 = parse(text)
    for r in t4:
        fix = FIXES.get((r[0], r[2]))
        r.insert(5, "no")
        if fix and r[3] == fix[0]:
            r[3], r[5] = fix[1], "yes"
        r[3] = int(r[3])
        r[1] = int(r[1])
    with open(out / "poley2022_table2_road_length.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["province", "area_km2", "scale", "dataset", "road_length_km",
                    "road_density_km_per_km2", "pct_of_comprehensive"])
        w.writerows(t2)
    with open(out / "poley2022_table4_roadless.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["province", "area_km2", "dataset", "roadless_km2", "pct_roadless",
                    "reconstructed", "mean_patch_km2", "max_patch_km2",
                    "median_patch_km2", "n_patches", "n_gt1", "n_gt5", "n_gt10",
                    "n_gt50", "n_gt100", "n_gt1000"])
        w.writerows(t4)
    print(f"Table 2: {len(t2)} rows; Table 4: {len(t4)} rows -> {out}")


if __name__ == "__main__":
    main()
