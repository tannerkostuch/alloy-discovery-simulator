"""sfe.py — the intrinsic stacking-fault energy of an FCC alloy (the number behind "why is CoCrNi so tough").

A low stacking-fault energy (< ~30 mJ/m²) means dislocations split wide, twins form easily and the alloy work-hardens
(TWIP/TRIP); a high one (Al ~ 160 mJ/m²) means easy cross-slip and a soft, ductile metal. Neither the elastic
constants nor the solute-strengthening model see this, so for the FCC families it is the missing ductility descriptor.

Method (the tilted-cell method, standard for generalized stacking faults): an FCC cell with the (111) planes stacked
along z; the top cell vector is tilted by the Shockley partial b_p = a/√6 along [112̄], which puts ONE intrinsic
stacking fault per periodic image into the crystal; the atoms relax along z only (FixedLine constraint); the energy
difference over the cross-section area is the fault energy.  For a random alloy the number depends on which atoms
sit at the fault plane, so every one of the n_layers fault positions is sampled (a cyclic shift of the layers) and
the mean ± spread is reported.  The same occupation is used for the perfect and the faulted cells.
Units: eV/Å² × 16021.77 = mJ/m².  Validation: Cu ~45, Ni ~125, Al ~166 mJ/m² (experiment; DFT-PBE gives Cu ~40,
Ni ~130, Al ~140).
"""
import numpy as np
from ase.build import fcc111
from ase.constraints import FixedLine

from . import atomistic as A

EV_A2_TO_MJ_M2 = 16021.77


def oriented_cell(at, a, size=(3, 4, 9), seed=0):
    """periodic FCC cell with (111) layers along z, orthogonal in-plane (nx × ny/2 rectangles of 2 atoms per layer, so
    (3, 4, 9) = 12 atoms × 9 layers = 108), random occupation of the composition."""
    atoms = fcc111("X", size=size, a=a, orthogonal=True, periodic=True)
    atoms.center(axis=2)
    atoms.set_pbc(True)
    n = len(atoms)
    counts = A.counts_for(at, n)
    syms = [el for el, c in counts.items() for _ in range(c)]
    rng = np.random.default_rng(seed)
    rng.shuffle(syms)
    atoms.set_chemical_symbols(syms)
    return atoms


def _relax_z(engine, atoms, fmax=0.02, steps=200):
    atoms.set_constraint(FixedLine(indices=list(range(len(atoms))), direction=[0, 0, 1]))
    engine.relax(atoms, fmax=fmax, steps=steps, cell=False)
    return engine.energy(atoms)


def stacking_fault_energy(engine, at, a=None, size=(3, 4, 9), seed=0, planes=None, log=print):
    """-> dict: sfe_mJm2 (mean), spread (max-min), per-plane list, area. a: FCC lattice constant (Vegard if None)."""
    a = a or A.vegard_a(at, "fcc", engine)[0]
    base = oriented_cell(at, a, size=size, seed=seed)
    e0 = _relax_z(engine, base.copy())
    area = float(np.linalg.norm(np.cross(base.cell[0], base.cell[1])))
    nz = size[2]
    dz = base.cell[2, 2] / nz                                   # one (111) layer
    # ase's orthogonal (111) cell: y (= [112̄]) is a·√6/2 = 3 b_p per TWO rows (size[1] must be even) → b_p = y / (ny/2) / 3
    bp = base.cell[1, 1] / (size[1] / 2) / 3.0
    planes = list(range(nz)) if planes is None else list(planes)

    def faulted(k, sign):
        sh = base.copy()
        pos = sh.get_positions()
        pos[:, 2] = (pos[:, 2] + k * dz) % base.cell[2, 2]      # cyclic shift: the fault (at the cell boundary) moves k layers
        sh.set_positions(pos)
        sh.wrap()
        cell = sh.cell[:].copy()
        cell[2, 1] += sign * bp                                 # tilt the top vector by ± the partial
        sh.set_cell(cell, scale_atoms=False)
        return (_relax_z(engine, sh) - e0) / area * EV_A2_TO_MJ_M2

    # one sign of the tilt is the intrinsic fault (…ABC|BCA…), the other stacks a layer on top of its twin (run-on,
    # several hundred mJ/m²): decide the sign on the first plane, keep it for the rest
    g_plus, g_minus = faulted(planes[0], +1), faulted(planes[0], -1)
    sign = +1 if g_plus <= g_minus else -1
    vals = [float(min(g_plus, g_minus))]
    log(f"[sfe] plane {planes[0]}: {vals[0]:.0f} mJ/m² (the other tilt: {max(g_plus, g_minus):.0f})")
    for k in planes[1:]:
        g = float(faulted(k, sign))
        vals.append(g)
        log(f"[sfe] plane {k}: {g:.0f} mJ/m²")
    return {"sfe_mJm2": float(np.mean(vals)), "sfe_spread_mJm2": float(np.max(vals) - np.min(vals)) if len(vals) > 1 else 0.0,
            "per_plane_mJm2": vals, "area_A2": area, "a_A": a, "n_atoms": len(base), "planes": planes}
