# meam_check.py — is a MEAM parameter set good enough for the zinc family? (2026-10-05; the result is in docs/RESULTS.md)
# Needs LAMMPS with the MEAM package:  pip install lammps mpich  (the mpich wheel carries the libmpi the lammps wheel
# links; run with LD_LIBRARY_PATH=<venv>/lib) and a parameter set, which is NOT part of this repository — the one tested
# was Dickel, Baskes, Aslam & Barrett 2018 (Mg-Al-Zn) from the NIST Interatomic Potentials Repository.
# Pure elements: lattice constant, c/a and the elastic constants against experiment; then one alloy cell (a 96-atom random
# hcp solid solution, the chain's own recipe: a and c free, no shear; ±0.5 % strains with internal relaxation; Hill averages).
# env: MEAM_LIB, MEAM_PAR (the two files), MEAM_ELS (optional: the library names to load, in the parameter file's index order),
#      MEAM_CHECK ("Zn:hcp:2.66:1.856,Mg:hcp:3.21:1.624,Al:fcc:4.05"), MEAM_ALLOY ("Zn:0.907,Al:0.093").
import os
import re
import sys
import time

import numpy as np
from ase.build import bulk
from ase.calculators.lammpslib import LAMMPSlib
from ase.optimize import FIRE, LBFGS

try:
    from ase.filters import FrechetCellFilter as CellFilter
except Exception:  # noqa: BLE001
    from ase.constraints import ExpCellFilter as CellFilter

LIB, PAR = os.environ["MEAM_LIB"], os.environ["MEAM_PAR"]
EV_A3_TO_GPA = 160.21766208
found = []
for m in re.finditer(r"^\s*'([A-Za-z0-9]+)'", open(LIB).read(), re.M):
    if m.group(1) not in found:
        found.append(m.group(1))
names = os.environ["MEAM_ELS"].split() if os.environ.get("MEAM_ELS") else found       # the parameter file indexes them in this order
sym = {n: re.match(r"[A-Z][a-z]?", n).group(0) for n in names}
types = {sym[n]: i + 1 for i, n in enumerate(names)}
cmds = ["pair_style meam", f"pair_coeff * * {LIB} {' '.join(names)} {PAR} {' '.join(names)}"]
print("library entries:", found, "| loaded:", names, "| LAMMPS types:", types)
print("  ", cmds[1].replace(os.path.dirname(LIB) + "/", ""))


def calc():
    return LAMMPSlib(lmpcmds=cmds, atom_types=types, keep_alive=True, log_file=None)


def relax(at, fmax=0.001, steps=500, cell=True, mask=None):
    at.calc = calc()
    t = CellFilter(at, mask=mask) if cell else at
    for Opt in (LBFGS, FIRE):
        try:
            if Opt(t, logfile=None).run(fmax=fmax, steps=steps):
                return True
        except Exception as e:  # noqa: BLE001
            print("   relax stopped:", str(e)[:120])
    return False


def moduli(C):
    S = np.linalg.inv(C)
    B_V = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    G_V = (C[0, 0] + C[1, 1] + C[2, 2] - C[0, 1] - C[0, 2] - C[1, 2] + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    B_R = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    G_R = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    B, G = (B_V + B_R) / 2, (G_V + G_R) / 2
    return B, G, 9 * B * G / (3 * B + G)


def elastic(at, delta=0.005, fmax=0.002):
    cell0 = at.get_cell()[:].copy()
    C = np.zeros((6, 6))
    for j in range(6):
        ss = []
        for sign in (+1, -1):
            eps = np.zeros((3, 3))
            if j < 3:
                eps[j, j] = sign * delta
            else:
                p, q = {3: (1, 2), 4: (0, 2), 5: (0, 1)}[j]
                eps[p, q] = eps[q, p] = sign * delta / 2
            a = at.copy()
            a.set_cell(cell0 @ (np.eye(3) + eps), scale_atoms=True)
            relax(a, fmax=fmax, steps=300, cell=False)
            ss.append(a.get_stress(voigt=True) * EV_A3_TO_GPA)
        C[:, j] = (ss[0] - ss[1]) / (2 * delta)
    return 0.5 * (C + C.T)


EXP = {  # room-temperature single-crystal constants (GPa), polycrystal B and G
    "Zn": dict(a=2.665, ca=1.856, C11=165, C12=31, C13=50, C33=62, C44=40, B=70, G=43),
    "Mg": dict(a=3.209, ca=1.624, C11=59.4, C12=25.6, C13=21.4, C33=61.6, C44=16.4, B=35, G=17),
    "Al": dict(a=4.050, C11=107, C12=61, C44=28, B=76, G=26),
    "Cd": dict(a=2.979, ca=1.886, C11=115, C12=40, C13=41, C33=51, C44=20, B=47, G=24),
}
refs = {}
for spec in os.environ.get("MEAM_CHECK", "Zn:hcp:2.66:1.856,Mg:hcp:3.21:1.624,Al:fcc:4.05").split(","):
    p = spec.split(":")
    el, lat, a0 = p[0], p[1], float(p[2])
    if el not in types:
        print(f"{el}: not in this parameter set"); continue
    t0 = time.time()
    x = EXP.get(el, {})
    try:
        if lat == "hcp":
            ca0 = float(p[3])
            best, scan = None, []
            for ca in (1.57, 1.633, 1.70, 1.78, 1.86, 1.94):       # the ideal c/a was a flat saddle for zinc in MACE: scan first
                a_ = a0 * (ca0 / ca) ** (1 / 3)
                at = bulk(el, "hcp", a=a_, c=ca * a_)
                relax(at, fmax=0.01, steps=200, cell=True, mask=[1, 1, 1, 0, 0, 0])
                e = at.get_potential_energy() / len(at)
                cv = at.get_cell()[:]
                scan.append((ca, np.linalg.norm(cv[2]) / np.linalg.norm(cv[0]), e))
                if best is None or e < best[0]:
                    best = (e, at.copy())
            at = best[1]
            relax(at, fmax=0.0005, steps=500, cell=True, mask=[1, 1, 1, 0, 0, 0])
            cv = at.get_cell()[:]
            la, lc = np.linalg.norm(cv[0]), np.linalg.norm(cv[2])
            C = elastic(at)
            B, G, E = moduli(C)
            refs[el] = (la, lc / la)
            print(f"{el} hcp: a {la:.3f} (expt {x.get('a')}), c/a {lc/la:.3f} (expt {x.get('ca')}), V {at.get_volume()/len(at):.2f} A3/atom, E {at.get_potential_energy()/len(at):.4f} eV/atom  [{time.time()-t0:.0f} s]")
            print("    c/a scan (start → relaxed c/a, meV/atom above the lowest): " + ", ".join(f"{c0:.2f}→{c1:.3f} {1000*(e-best[0]):+.1f}" for c0, c1, e in scan))
            print(f"    C11 {C[0,0]:.0f} ({x.get('C11')})  C12 {C[0,1]:.0f} ({x.get('C12')})  C13 {C[0,2]:.0f} ({x.get('C13')})  C33 {C[2,2]:.0f} ({x.get('C33')})  C44 {C[3,3]:.0f} ({x.get('C44')})  C66 {C[5,5]:.0f}")
        else:
            at = bulk(el, lat, a=a0, cubic=True)
            relax(at, fmax=0.0005, steps=500, cell=True, mask=[1, 1, 1, 0, 0, 0])
            la = np.linalg.norm(at.get_cell()[0])
            C = elastic(at)
            B, G, E = moduli(C)
            print(f"{el} {lat}: a {la:.3f} (expt {x.get('a')}), V {at.get_volume()/len(at):.2f} A3/atom, E {at.get_potential_energy()/len(at):.4f} eV/atom  [{time.time()-t0:.0f} s]")
            print(f"    C11 {C[0,0]:.0f} ({x.get('C11')})  C12 {C[0,1]:.0f} ({x.get('C12')})  C44 {C[3,3]:.0f} ({x.get('C44')})")
        gx, bx = x.get("G"), x.get("B")
        print(f"    B {B:.0f} ({bx})  G {G:.0f} ({gx})  E {E:.0f}" + (f"  |  G error {100*(G/gx-1):+.0f} %, B error {100*(B/bx-1):+.0f} %" if gx and bx else "")
              + f"  |  Born stable: {bool(np.linalg.eigvalsh(C).min() > 0)}")
    except Exception as e:  # noqa: BLE001
        print(f"{el} {lat}: FAILED — {e.__class__.__name__}: {str(e)[:200]}")
    sys.stdout.flush()

# ---- one alloy cell, the chain's recipe -------------------------------------------------------------------------
alloy = os.environ.get("MEAM_ALLOY", "Zn:0.907,Al:0.093")
frac = {k: float(v) for k, v in (s.split(":") for s in alloy.split(","))}
host = max(frac, key=frac.get)
if all(el in types for el in frac) and host in refs:
    t0 = time.time()
    a_h, ca_h = refs[host]
    cell = bulk(host, "hcp", a=a_h, c=ca_h * a_h).repeat((4, 4, 3))
    n = len(cell)
    counts = {el: int(round(c * n)) for el, c in frac.items() if el != host}
    syms = [host] * n
    rng = np.random.default_rng(0)
    idx = rng.permutation(n)
    k = 0
    for el, c in counts.items():
        for i in idx[k:k + c]:
            syms[i] = el
        k += c
    cell.set_chemical_symbols(syms)
    try:
        ok = relax(cell, fmax=0.005, steps=400, cell=True, mask=[1, 1, 1, 0, 0, 0])
        cv = cell.get_cell()[:]
        ca = (np.linalg.norm(cv[2]) / 3) / (np.linalg.norm(cv[0]) / 4)
        masses = cell.get_masses().sum()
        rho = masses * 1.66053906660 / cell.get_volume()
        C = elastic(cell, fmax=0.005)
        B, G, E = moduli(C)
        comp = "".join(f"{el}{syms.count(el)}" for el in sorted(set(syms), key=lambda s: -syms.count(s)))
        print(f"alloy {comp} ({n} atoms, random hcp, seed 0): converged {ok}, c/a {ca:.3f}, rho {rho:.2f} g/cm3  [{time.time()-t0:.0f} s]")
        print(f"    C11 {(C[0,0]+C[1,1])/2:.0f}  C33 {C[2,2]:.0f}  C12 {C[0,1]:.0f}  C13 {(C[0,2]+C[1,2])/2:.0f}  C44 {(C[3,3]+C[4,4])/2:.0f}  C66 {C[5,5]:.0f}")
        print(f"    B {B:.0f}  G {G:.0f}  E {E:.0f} GPa  |  Born stable: {bool(np.linalg.eigvalsh(C).min() > 0)}")
    except Exception as e:  # noqa: BLE001
        print(f"alloy cell FAILED — {e.__class__.__name__}: {str(e)[:200]}")
else:
    print(f"alloy {alloy}: skipped (elements not all in the set, or no hcp reference for {host})")
