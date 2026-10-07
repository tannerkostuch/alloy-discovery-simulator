#!/usr/bin/env python3
"""run_sfe.py — stacking-fault energies of FCC alloys (the ductility/twinning descriptor; see alloysim/sfe.py).
  python3 run_sfe.py --validate                      # Cu, Ni, Al, CoCrNi, CoCrFeMnNi vs experiment → data/SFE_VALIDATION.md
  python3 run_sfe.py CoCrNi Ni40Fe29Cr17V14          # any FCC compositions → printed
  python3 run_sfe.py --from-run run1-medium_entropy_fcc --top 6
                                                    # the top FCC candidates of a run: adds "sfe" to their JSONs + SFE.md there
On the CPU an alloy is ~10 min (108-atom cell, one perfect + ten faulted relaxations along z).
"""
import argparse
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alloysim import atomistic as A, compo, sfe, search as S  # noqa: E402

EXPT = {"Cu": 45, "Ni": 125, "Al": 166, "CoCrNi": 22, "CoCrFeMnNi": 30}     # mJ/m², experiment (±10 typical)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("formulas", nargs="*")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--from-run", default=None); ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--engine", default="auto"); ap.add_argument("--model", default="medium-mpa-0"); ap.add_argument("--device", default=None)
    ap.add_argument("--seeds", type=int, default=1)
    a = ap.parse_args()
    eng = A.Engine(kind=a.engine, model=a.model, device=a.device, log=print)
    sim = Path(__file__).resolve().parent

    def one(f, at, seeds):
        t = time.time()
        rs = [sfe.stacking_fault_energy(eng, at, seed=s, log=print) for s in range(seeds)]
        vals = [v for r in rs for v in r["per_plane_mJm2"]]
        out = {"sfe_mJm2": sum(vals) / len(vals), "sfe_spread_mJm2": max(vals) - min(vals), "per_plane_mJm2": vals,
               "n_atoms": rs[0]["n_atoms"], "a_A": rs[0]["a_A"], "seeds": seeds, "seconds": round(time.time() - t)}
        print(f"{f}: SFE {out['sfe_mJm2']:.0f} mJ/m² (plane to plane {out['sfe_spread_mJm2']:.0f}) — {out['seconds']} s")
        return out

    if a.validate:
        lines = ["# stacking-fault energy — validation", "", f"engine: {eng.name}", "", "| alloy | model (mJ/m²) | spread | experiment |", "|---|---|---|---|"]
        for f, ref in EXPT.items():
            try:
                r = one(f, compo.parse(f), a.seeds)
                lines.append(f"| {f} | {r['sfe_mJm2']:.0f} | {r['sfe_spread_mJm2']:.0f} | {ref} |")
            except Exception as e:  # noqa: BLE001
                lines.append(f"| {f} | failed: {e} | | {ref} |")
        (sim / "data").mkdir(exist_ok=True)
        (sim / "data" / "SFE_VALIDATION.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines))
    if a.from_run:
        out = S.RESULTS / a.from_run
        cands = []
        for p in sorted(out.glob("*.json")):
            if p.name == "shortlist.json":
                continue
            r = json.loads(p.read_text())
            if r.get("lattice") == "fcc" and not r.get("error"):
                cands.append((p, r))
        # the run's ranking: DISCOVERIES.md order = score; recompute it here
        obj = None
        for line in (out / "DISCOVERIES.md").read_text().splitlines():
            if line.startswith("# ") and "ranked by" in line:
                obj = line.split("ranked by")[-1].strip()
        cands.sort(key=lambda t: -(S.score(t[1], obj) or 0.0) if obj else 0)
        rows = ["# stacking-fault energies of the top FCC candidates", "", f"run: {a.from_run} · engine: {eng.name}", "",
                "| alloy | SFE (mJ/m²) | plane to plane | reading |", "|---|---|---|---|"]
        for p, r in cands[: a.top]:
            if "sfe" in r and r["sfe"].get("engine") == eng.name:
                s = r["sfe"]
            else:
                s = one(r["formula"], r["at"], a.seeds); s["engine"] = eng.name
                r["sfe"] = s
                p.write_text(json.dumps(r, indent=1, default=float))
            v = s["sfe_mJm2"]
            reading = "very low: twinning/TRIP territory (tough, strong work-hardening)" if v < 20 else ("low: twinning likely (CoCrNi-like)" if v < 40 else ("medium: planar slip" if v < 80 else "high: easy cross-slip (Al/Ni-like)"))
            rows.append(f"| {r['formula']} | {v:.0f} | {s['sfe_spread_mJm2']:.0f} | {reading} |")
        (out / "SFE.md").write_text("\n".join(rows) + "\n")
        print("\n".join(rows))
    for f in a.formulas:
        one(f, compo.parse(f), a.seeds)


if __name__ == "__main__":
    main()
