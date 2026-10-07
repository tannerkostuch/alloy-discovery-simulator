#!/usr/bin/env python3
"""run_search.py — the discovery run.
  python3 run_search.py --family 3d_hea --objective specific_strength --sample 3000 --keep 24
  (v2, 2026-10-05: --seed N for a second pass with other compositions; objective strong_ductile_cal = calibrated yield)
Results: results/<run>/DISCOVERIES.md (+ one JSON per candidate; a crashed run resumes from them).
"""
import argparse
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alloysim import atomistic as A, search as S  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="3d_hea", choices=sorted(S.FAMILIES))
    ap.add_argument("--objective", default="specific_strength", choices=sorted(S.OBJECTIVES))
    ap.add_argument("--sample", type=int, default=2000); ap.add_argument("--keep", type=int, default=24)
    ap.add_argument("--seeds", type=int, default=1, help="random cells per lattice (1 = fastest)")
    ap.add_argument("--atoms", type=int, default=108); ap.add_argument("--run-name", default=None)
    ap.add_argument("--engine", default="auto"); ap.add_argument("--model", default="medium-mpa-0"); ap.add_argument("--device", default=None)
    ap.add_argument("--no-elastic", action="store_true"); ap.add_argument("--no-hull", action="store_true")
    ap.add_argument("--include", nargs="*", default=[], help="formulas to evaluate first (the known alloys the run must re-find), e.g. CoCrNi")
    ap.add_argument("--workers", type=int, default=0, help="candidates evaluated at once (0 = auto: 4 on a 16-thread CPU, 1 on a GPU)")
    ap.add_argument("--seed", type=int, default=0, help="shortlist sampling seed (v2: a second pass of a family with --seed 1 tries other compositions)")
    ap.add_argument("--avoid-run", nargs="*", default=[], help="earlier run names whose shortlisted compositions this run stays clear of (v2)")
    a = ap.parse_args()
    eng = A.Engine(kind=a.engine, model=a.model, device=a.device, log=print)
    workers = a.workers or S.auto_workers(eng)
    out, res = S.run(eng, a.family, a.objective, n_sample=a.sample, keep=a.keep, seeds=tuple(range(a.seeds)), target_atoms=a.atoms,
                     run_name=a.run_name, log=print, do_elastic=not a.no_elastic, do_hull=not a.no_hull, include=a.include,
                     workers=workers, seed=a.seed, avoid_runs=a.avoid_run)
    print(f"\n-> {out / 'DISCOVERIES.md'}")


if __name__ == "__main__":
    main()
