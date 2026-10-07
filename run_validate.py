#!/usr/bin/env python3
"""run_validate.py — the simulation against a reference database of known alloys, tier by tier (alloysim/validate.py).
The database is $ALLOYS_DB or data/alloys.json (format: docs/DATABASE.md; a ten-alloy example: data/alloys.example.json).

  python run_validate.py --tier 1                      # every usable record: lattice + density (~6 h on 16 threads)
  python run_validate.py --tier 2                      # annealed solid solutions + measured moduli: E, G, ν, σy
  python run_validate.py --tier 3                      # the phase subset: hull-lite (brass, stainless, NiTi, γ', …)
  python run_validate.py --list [--tier N]             # only print what would run and what is skipped, and why
  python run_validate.py --families copper nickel      # a subset;  --limit 20 to try it;  --ids fe-stainless-304 …
Results: results/validation/tier<N>/<id>.json, the scorecard results/validation/VALIDATION.md + validation.csv
(rebuilt after every result), results/validation/skipped.json. Resumable: stop it with Ctrl-C and run it again.
"""
import argparse
import json
import sys
import warnings
from collections import Counter
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alloysim import atomistic as A  # noqa: E402
from alloysim import compo  # noqa: E402
from alloysim import validate as V  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", type=int, default=1, choices=(1, 2, 3))
    ap.add_argument("--families", nargs="*", default=None)
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--atoms", type=int, default=108)
    ap.add_argument("--workers", type=int, default=0, help="0 = auto (4 on a 16-thread CPU)")
    ap.add_argument("--engine", default="auto"); ap.add_argument("--model", default="medium-mpa-0"); ap.add_argument("--device", default=None)
    ap.add_argument("--list", action="store_true", help="print the selection and exit")
    ap.add_argument("--scorecard", action="store_true", help="only rebuild VALIDATION.md from what is on disk")
    a = ap.parse_args()
    if a.scorecard:
        V.write_scorecard(); return
    if not compo.have_db():
        sys.exit(f"no reference database at {compo.DB_FINAL}\n"
                 "The validation compares the chain with measured values of known alloys, so it needs a database of them:\n"
                 "set ALLOYS_DB=/path/to/alloys.json or put one at data/alloys.json (format: docs/DATABASE.md).\n"
                 "To try it on ten well-known alloys:  ALLOYS_DB=data/alloys.example.json python run_validate.py --list")
    records, skipped = V.select(families=a.families, ids=a.ids)
    V.RESULTS.mkdir(parents=True, exist_ok=True)
    (V.RESULTS / "skipped.json").write_text(json.dumps(skipped, indent=1))
    sub = V.tier_subset(records, a.tier)
    fams = Counter(r["family"] for r in sub)
    print(f"database: {len(records) + len(skipped)} records → {len(records)} usable, {len(skipped)} skipped; tier {a.tier}: {len(sub)} to run")
    print("  per family: " + ", ".join(f"{k} {v}" for k, v in sorted(fams.items(), key=lambda kv: -kv[1])))
    print("  skipped because: " + ", ".join(f"{k} ({v})" for k, v in Counter(s[1].split(":")[0].split(" [")[0][:34] for s in skipped).most_common(8)))
    if a.list:
        for r in sub[: a.limit or None]:
            m = r["measured"]
            print(f"  {r['id']:40s} {r['formula']:40s} expected {'/'.join(r['expected'])}{' vs ' + r['rival'] if r['rival'] else ''}"
                  f"  ρ {m['density_gcc']}  E {m['E_GPa']}  σy {m['yield_MPa']} ({m['yield_condition']}){' [solid solution]' if m['yield_is_solid_solution'] else ''}")
        return
    eng = A.Engine(kind=a.engine, model=a.model, device=a.device)
    V.run_tier(eng, a.tier, sub, target_atoms=a.atoms, workers=a.workers, limit=a.limit)


if __name__ == "__main__":
    main()
