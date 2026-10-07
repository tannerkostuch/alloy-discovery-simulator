#!/usr/bin/env python3
"""diag_cantor.py — why did the Cantor cell come out at +0.5 eV/atom? Same 108-atom cell on GPU and CPU, energies and
forces before/after relaxation, step by step, printed. This is the check that showed MACE's forces to be wrong on an
AMD RX 9070 XT under ROCm 7.0 (2026-09-29) and made the CPU the default device; needs a GPU that torch can see."""
import sys, time, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from alloysim import atomistic as A, compo

at = compo.parse("CoCrFeMnNi")
for dev, dtype in (("cuda", "float64"), ("cpu", "float64"), ("cuda", "float32")):
    try:
        eng = A.Engine(kind="mace", device=dev, dtype=dtype, log=print)
    except Exception as e:
        print(dev, dtype, "engine failed:", e); continue
    cell = A.random_cell(at, "fcc", target_atoms=108, seed=0, engine=eng)
    eng.attach(cell)
    t = time.time(); e0 = cell.get_potential_energy() / len(cell); f0 = np.abs(cell.get_forces()).max(); dt = time.time() - t
    d = cell.get_all_distances(mic=True); np.fill_diagonal(d, 99)
    print(f"[{dev} {dtype}] initial: a_cell={cell.cell.lengths()[0]:.3f} Å  E={e0:.4f} eV/atom  max|F|={f0:.3f} eV/Å  min d={d.min():.3f} Å  ({dt*1000:.0f} ms per call)")
    from ase.optimize import FIRE, LBFGS
    from ase.filters import FrechetCellFilter
    for name, Opt in (("FIRE+cell", FIRE), ("LBFGS+cell", LBFGS)):
        c = cell.copy(); eng.attach(c)
        opt = Opt(FrechetCellFilter(c), logfile=None)
        t = time.time()
        for i in range(1, 16):
            conv = opt.run(fmax=0.02, steps=20 * i)
            e = c.get_potential_energy() / len(c); f = np.abs(c.get_forces()).max(); s = np.abs(c.get_stress()).max() * 160.2
            print(f"   {name} step {opt.get_number_of_steps():4d}: E={e:.4f} eV/atom max|F|={f:.3f} max|σ|={s:.2f} GPa  a={c.cell.lengths()[0]:.3f} Å vol/atom={c.get_volume()/len(c):.3f}")
            if conv:
                print(f"   converged after {opt.get_number_of_steps()} steps in {time.time()-t:.0f} s"); break
        refs = sum(x * eng.ground(el)[1]["e"] for el, x in at.items())
        print(f"   E_form vs ground refs = {e - refs:+.4f} eV/atom")
    if dev == "cuda" and dtype == "float64":
        # same relaxed-ish geometry, single-point on CPU to compare numerics
        pass
