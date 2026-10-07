"""atomistic.py — layer 2: the atoms themselves, with a universal machine-learned interatomic potential.

The engine is MACE (MACE-MPA-0 by default: an equivariant graph network trained on ~3.5 million DFT calculations of
crystals across the periodic table, PBE level; ~0.02-0.03 eV/atom typical error on formation energies). Every number
below is a real relaxation or finite-difference calculation on a periodic cell of atoms — no fitted "alloy" rules:

  references(el)          FCC / BCC / HCP cells of the pure element relaxed → energy and volume per atom; the ground
                          state is the lowest (cached in cache/refs_<calc>.json)
  solid_solution(at, L)   a random substitutional cell (~100 atoms) of the composition on lattice L, fully relaxed
                          (cell + positions): energy/atom, volume/atom, density, mean lattice distortion
  formation / mixing      E_form = E_ss − Σ c_i E_i(ground);  E_mix(L) = E_ss(L) − Σ c_i E_i(L)
  lattice_preference      FCC vs BCC vs HCP cells of the same composition — which the atoms prefer
  competing_phases        the ordered compounds the pairs could form instead (B2, L1₂, L1₀, C15 + C14 Laves, A15, the σ
                          phase) and the triples (L2₁ Heusler) relaxed →
                          a convex-hull-lite at the alloy composition: decomposition energy ΔE_dec of the solid
                          solution and the temperature T* above which mixing entropy makes the solution win
  elastic(atoms)          6 strains ± δ with internal relaxation → C_ij → Hill bulk and shear moduli, E, ν, Pugh ratio
  v6 (2026-10-03): hexagonal cells relax a and c independently (HCP_MASK, no shear) and are built with the base element's
  own c/a from its reference (zinc 1.88, not the ideal 1.633 that left zinc with no stiffness in the validation);
  lattice_check compares angles with the starting cell, so an hcp cell is no longer "unstable" for being hexagonal.
  v7 (2026-10-05): ordered_cell() builds a B2-ORDERED bcc supercell (X on one sublattice, Y on the other) and
  solid_solution() accepts a prebuilt cell — for the β-brass / NiTi-type compositions whose random bcc cell is
  mechanically unstable at 0 K while the ordered B2 they really are is not (run 9 lost four cells that way).
                          B/G (ductile > 1.75), Cauchy pressure C12−C44, Born stability
A calculator of kind "emt" (ASE's built-in effective-medium theory, Al/Cu/Ni/Pd/Ag/Pt/Au only) exists for testing the
machinery without MACE; results with it are not physics for anything else.
"""
import fcntl
import json
import math
import os
import time
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.build import bulk
from ase.optimize import FIRE, LBFGS

try:
    from ase.filters import FrechetCellFilter as CellFilter
except Exception:  # noqa: BLE001
    from ase.constraints import ExpCellFilter as CellFilter

from .elements import info

EV_A3_TO_GPA = 160.21766208
CACHE = Path(__file__).resolve().parent.parent / "cache"
KB_EV = 8.617333262e-5


# ------------------------------------------------------------------ the calculator
class Engine:
    """one calculator + its caches. kind: "auto" (MACE if it imports, else EMT), "mace", "emt"."""

    def __init__(self, kind="auto", model="medium-mpa-0", device=None, dtype="float64", log=print, threads=None):
        """threads: CPU threads for torch (default: all). spec = the kwargs a worker process needs to build a twin."""
        self.log = log
        self.kind = None
        self.calc = None
        self.name = None
        self.spec = {"kind": kind, "model": model, "device": device, "dtype": dtype, "threads": threads}
        self.device = device or "cpu"
        if kind in ("auto", "mace"):
            try:
                import torch
                from mace.calculators import mace_mp
                # CPU by default: on an AMD RX 9070 XT (ROCm 7.0, gfx1201) MACE's energies were right but its FORCES on a
                # 108-atom cell were garbage in float64 and NaN in float32 (diag_cantor.py shows it, 2026-09-29). Pass
                # device="cuda" explicitly to try the GPU again after a torch/mace update.
                dev = device or "cpu"
                if dev == "cpu":
                    torch.set_num_threads(max(1, int(threads or os.cpu_count() or 1)))
                self.calc = mace_mp(model=model, device=dev, default_dtype=dtype)
                self.kind, self.name = "mace", f"mace-{model}-{dev}"
                gpu = torch.cuda.get_device_name(0) if dev == "cuda" else f"cpu, {torch.get_num_threads()} threads"
                log(f"[engine] MACE {model} on {dev} ({gpu})")
            except Exception as e:  # noqa: BLE001
                if kind == "mace":
                    raise
                log(f"[engine] MACE not available ({e.__class__.__name__}: {e}) — falling back to EMT (test physics only)")
        if self.calc is None:
            from ase.calculators.emt import EMT
            self.calc = EMT()
            self.kind, self.name = "emt", "emt"
        CACHE.mkdir(parents=True, exist_ok=True)
        self._refs_path = CACHE / f"refs_{self.name}.json"
        self._pairs_path = CACHE / f"pairs_{self.name}_v3.json"     # v2: + C14, σ, L2₁; v3: C15 sites fixed (2026-09-29)
        self.refs, self.pairs = {}, {}
        self.refresh()

    def attach(self, atoms):
        atoms.calc = self.calc
        return atoms

    # the caches are shared between the worker processes of a parallel run: every read/write goes through one lock
    # file, a write merges what is on disk with what is in memory, and refresh() picks up what other workers found
    def _locked(self, fn):
        lock = CACHE / f".{self.name}.lock"
        with open(lock, "w") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            try:
                return fn()
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)

    def _merge(self, path, mem):
        try:
            cur = json.loads(path.read_text()) if path.exists() else {}
        except Exception:  # noqa: BLE001
            cur = {}
        mem.update({k: v for k, v in cur.items() if k not in mem})
        return cur

    def refresh(self):
        """merge the on-disk caches into memory (what other workers computed meanwhile)."""
        self._locked(lambda: (self._merge(self._refs_path, self.refs), self._merge(self._pairs_path, self.pairs)))

    def save(self):
        def _w():
            for path, mem in ((self._refs_path, self.refs), (self._pairs_path, self.pairs)):
                cur = self._merge(path, mem)
                cur.update(mem)
                tmp = path.with_suffix(".tmp%d" % os.getpid())
                tmp.write_text(json.dumps(cur, indent=1))
                os.replace(tmp, path)
        self._locked(_w)

    # -------------------------------------------------------------- relaxations
    def relax(self, atoms, fmax=0.02, steps=300, cell=True, hydrostatic=False, mask=None):
        """relax positions (+ cell) in place; -> (converged, n_steps). mask: which cell strains may move (Voigt, 6 flags) —
        HCP_MASK lets a hexagonal cell change a and c but not shear (v6: zinc's c/a is 1.856, not the ideal 1.633)."""
        self.attach(atoms)
        target = (CellFilter(atoms, hydrostatic_strain=hydrostatic, mask=mask) if mask is not None
                  else CellFilter(atoms, hydrostatic_strain=hydrostatic)) if cell else atoms
        # LBFGS first (converged the Cantor cell in 29 steps where FIRE took 52); FIRE as the fallback
        total = 0
        for Opt in (LBFGS, FIRE):
            opt = Opt(target, logfile=None)
            try:
                conv = opt.run(fmax=fmax, steps=steps)
            except Exception as e:  # noqa: BLE001
                self.log(f"[relax] {Opt.__name__} stopped: {e}")
                conv = False
            total += opt.get_number_of_steps()
            if conv:
                return True, total
        return False, total

    def energy(self, atoms):
        self.attach(atoms)
        return float(atoms.get_potential_energy())

    # -------------------------------------------------------------- elemental references
    def reference(self, el, lattice):
        """{'e': eV/atom, 'v': Å³/atom, 'a': lattice constant (Å)} for the element on the lattice (cached)."""
        key = f"{el}:{lattice}"
        if key not in self.refs:
            self.refresh()
        if key in self.refs and (lattice != "hcp" or "ca" in self.refs[key]):
            return self.refs[key]                              # hcp entries from before v6 carry no c/a: made again (seconds)
        a0 = guess_a(el, lattice)
        at = elemental_cell(el, lattice, a0)
        n = len(at)
        v_start = at.get_volume() / n
        kw = {"hydrostatic": False, "mask": HCP_MASK} if lattice == "hcp" else {"hydrostatic": True}
        if lattice == "hcp":
            # the ideal c/a is a flat saddle for zinc and cadmium (the slope only starts past c/a 1.7), where an optimizer
            # stops with the stress below fmax: scan c/a at the same volume, volume-relax each, start from the lowest
            best = None
            for ca in (1.57, 1.633, 1.70, 1.78, 1.86, 1.94):
                a_ = a0 * (1.633 / ca) ** (1 / 3)
                x = bulk(el, "hcp", a=a_, c=ca * a_)
                self.relax(x, fmax=0.01, steps=100, cell=True, hydrostatic=True)
                e_ = self.energy(x) / n
                if best is None or e_ < best[0]:
                    best = (e_, x)
            at = best[1]
            self.relax(at, fmax=0.002, steps=300, cell=True, **kw)
        else:
            self.relax(at, fmax=0.01, steps=200, cell=True, **kw)
        v = at.get_volume() / n
        if v < 0.6 * v_start or v < 5.0:                       # collapsed into a spurious high-pressure minimum: try once more, bigger
            self.log(f"[ref] {el} {lattice} collapsed to {v:.1f} Å³ from {v_start:.1f} — retrying from a larger cell")
            at = elemental_cell(el, lattice, a0 * 1.25)
            self.relax(at, fmax=0.01, steps=200, cell=True, **kw)
            v = at.get_volume() / n
            if v < 0.6 * v_start or v < 5.0:
                raise RuntimeError(f"{el} {lattice}: unphysical reference volume {v:.1f} Å³")
        e = self.energy(at) / n
        if lattice == "hcp":
            la, lc = (float(np.linalg.norm(x)) for x in (at.get_cell()[0], at.get_cell()[2]))
            self.refs[key] = {"e": e, "v": v, "a": la, "ca": lc / la}     # the model's own c/a (Zn 1.88, Mg 1.62, Ti 1.60)
        else:
            a = (4 * v) ** (1 / 3) if lattice == "fcc" else (2 * v) ** (1 / 3) if lattice == "bcc" else (8 * v) ** (1 / 3)
            self.refs[key] = {"e": e, "v": v, "a": a}
        self.save()
        return self.refs[key]

    def ground(self, el):
        """lowest of fcc/bcc/hcp for the element (the model's own ground state) — plus diamond for Si/Ge/C, so that an
        Al-Si alloy's hull knows silicon would rather be silicon (the eutectic), not a metal in solution (2026-09-30)."""
        best = None
        for L in ("fcc", "bcc", "hcp") + (("diamond",) if el in DIAMOND else ()):
            try:
                r = self.reference(el, L)
            except Exception as e:  # noqa: BLE001
                self.log(f"[ref] {el} {L} failed: {e}")
                continue
            if best is None or r["e"] < best[1]["e"]:
                best = (L, r)
        return best


# ------------------------------------------------------------------ cells
DIAMOND = {"Si", "Ge", "C"}                          # elements whose real ground state is the diamond lattice
# atomic volumes (Å³) of the elements that have no metallic radius in the tables — the radius fallback (Si 1.1 Å →
# 8 Å³) started their metallic cells so compressed that MACE relaxed them into a spurious minimum 6 eV too deep
# (Si "bcc" at 7 Å³, 2026-09-30). From these volumes (metallic lattices 0.75× the open diamond volume) the
# references come out physical: Si diamond −5.415 eV (Materials Project −5.42), fcc −4.91, bcc −4.92.
ATOMIC_VOLUME = {"Si": 20.0, "Ge": 22.6, "C": 5.7, "Sn": 27.0, "Sb": 30.4, "Bi": 35.4, "As": 21.5, "Se": 27.3, "Te": 34.0,
                 "Ga": 19.6, "In": 26.1, "P": 17.0, "S": 25.7, "B": 7.3}


def guess_a(el, lattice):
    """starting lattice constant (Å): from the tabulated atomic volume where there is one, else the metallic radius."""
    v = ATOMIC_VOLUME.get(el)
    if v is not None:
        if lattice == "diamond":
            return (8 * v) ** (1 / 3)
        vm = v * (0.75 if el in DIAMOND else 1.0)           # the metallic phases of Si/Ge/C are denser than diamond
        if lattice == "fcc":
            return (4 * vm) ** (1 / 3)
        if lattice == "bcc":
            return (2 * vm) ** (1 / 3)
        return (vm / (math.sqrt(3) / 4 * 1.633)) ** (1 / 3)
    r = info(el)["radius"] or 1.4
    if lattice == "fcc":
        return 2 * math.sqrt(2) * r
    if lattice == "bcc":
        return 4 * r / math.sqrt(3)
    if lattice == "diamond":
        return 8 * r / math.sqrt(3)
    return 2 * r                                   # hcp a (c = 1.633 a)


HCP_MASK = [1, 1, 1, 0, 0, 0]                            # Voigt flags: xx, yy, zz free; no shear — a hexagonal cell keeps its angles


def hcp_ca(at, engine=None):
    """c/a for an hcp alloy cell: the majority element's own, from the engine's reference (ideal 1.633 without an engine)."""
    ref_el = max(at, key=at.get)
    if engine is not None:
        try:
            return float(engine.reference(ref_el, "hcp").get("ca", 1.633))
        except Exception:  # noqa: BLE001
            pass
    return 1.633


def elemental_cell(el, lattice, a):
    if lattice == "hcp":
        return bulk(el, "hcp", a=a, c=1.633 * a)
    return bulk(el, lattice, a=a, cubic=True)      # fcc, bcc, diamond


def vegard_a(at, lattice, engine=None):
    """lattice constant from the composition-weighted elemental volumes on that lattice (engine's refs if given)."""
    vbar = 0.0
    for el, c in at.items():
        if engine is not None:
            try:
                v = engine.reference(el, lattice)["v"]
            except Exception:  # noqa: BLE001
                v = None
        else:
            v = None
        if v is None:
            a0 = guess_a(el, lattice)
            v = a0 ** 3 / 4 if lattice == "fcc" else (a0 ** 3 / 2 if lattice == "bcc" else math.sqrt(3) / 2 * a0 ** 2 * 1.633 * a0 / 2)
        vbar += c * v
    if lattice == "fcc":
        return (4 * vbar) ** (1 / 3), vbar
    if lattice == "bcc":
        return (2 * vbar) ** (1 / 3), vbar
    return (vbar / (math.sqrt(3) / 4 * hcp_ca(at, engine))) ** (1 / 3), vbar


def counts_for(at, n):
    """exact atom counts for n sites from fractions (largest-remainder rounding)."""
    raw = {el: c * n for el, c in at.items()}
    counts = {el: int(math.floor(x)) for el, x in raw.items()}
    short = n - sum(counts.values())
    for el, _ in sorted(raw.items(), key=lambda kv: -(kv[1] - math.floor(kv[1])))[:short]:
        counts[el] += 1
    return counts


def random_cell(at, lattice, a=None, target_atoms=108, seed=0, engine=None):
    """a random substitutional supercell of the composition; -> Atoms (with .info['ideal'] fractional positions)."""
    if a is None:
        a, _ = vegard_a(at, lattice, engine)
    ref_el = max(at, key=at.get)
    if lattice == "hcp":
        base = bulk(ref_el, "hcp", a=a, c=hcp_ca(at, engine) * a)
        rep = (4, 4, 3)
    elif lattice == "bcc":
        base = bulk(ref_el, "bcc", a=a, cubic=True)
        k = max(2, round((target_atoms / 2) ** (1 / 3)))
        rep = (k, k, k)
    else:
        base = bulk(ref_el, "fcc", a=a, cubic=True)
        k = max(2, round((target_atoms / 4) ** (1 / 3)))
        rep = (k, k, k)
    cell = base.repeat(rep)
    n = len(cell)
    counts = counts_for(at, n)
    symbols = [el for el, k in counts.items() for _ in range(k)]
    rng = np.random.default_rng(seed)
    rng.shuffle(symbols)
    cell.set_chemical_symbols(symbols)
    cell.info["ideal"] = cell.get_scaled_positions().copy()
    cell.info["lattice"] = lattice
    return cell


def ordered_cell(at, X, Y, a=None, target_atoms=108, seed=0, engine=None, kind="b2"):
    """v7: a B2-ORDERED bcc supercell of the composition — X fills one sublattice (the cube corners), Y the other (the
    body centres), as far as the composition allows; everything else, and what does not fit, goes at random on the
    sites left. The cell a β-brass (CuZn), NiTi or NiAl-type alloy really is: a RANDOM bcc cell of Cu-Zn-Al at 0 K is
    mechanically unstable in the model, the ordered one is not. -> Atoms (info['ordered'] = 'B2-XY')."""
    if kind != "b2":
        raise ValueError(kind)
    if a is None:
        a, _ = vegard_a(at, "bcc", engine)
    ref_el = max(at, key=at.get)
    base = bulk(ref_el, "bcc", a=a, cubic=True)             # atom 0 at (0,0,0), atom 1 at (½,½,½)
    k = max(2, round((target_atoms / 2) ** (1 / 3)))
    cell = base.repeat((k, k, k))                            # ASE keeps the 2-atom order per copy: sublattice = index % 2
    n = len(cell)
    counts = counts_for(at, n)
    rng = np.random.default_rng(seed)
    sub_a = [i for i in range(n) if i % 2 == 0]
    sub_b = [i for i in range(n) if i % 2 == 1]
    rng.shuffle(sub_a); rng.shuffle(sub_b)
    symbols = [None] * n
    nx = min(counts.get(X, 0), len(sub_a))
    for i in sub_a[:nx]:
        symbols[i] = X
    ny = min(counts.get(Y, 0), len(sub_b))
    for i in sub_b[:ny]:
        symbols[i] = Y
    left = [el for el, c in counts.items() for _ in range(c - (nx if el == X else 0) - (ny if el == Y else 0))]
    rng.shuffle(left)
    free = [i for i in range(n) if symbols[i] is None]
    rng.shuffle(free)
    for i, el in zip(free, left):
        symbols[i] = el
    assert all(s is not None for s in symbols) and len(left) == len(free), (counts, nx, ny)
    cell.set_chemical_symbols(symbols)
    cell.info["ideal"] = cell.get_scaled_positions().copy()
    cell.info["lattice"] = "bcc"
    cell.info["ordered"] = f"B2-{X}{Y}"
    return cell


# ------------------------------------------------------------------ the solid solution
def solid_solution(engine, at, lattice, seed=0, target_atoms=108, fmax=0.02, steps=300, cell=None):
    """relax a random cell — atoms free, the cell scaled hydrostatically (volume only) so the lattice stays what it is
    labelled: with all six strains free a cubic cell walks the Bain path and an "fcc" NbMoTaW cell turns bcc (or the
    other way round), which is how the first smoke test got both famous alloys on the wrong lattice (2026-09-29).
    lattice_check() afterwards says whether the winning cell WOULD transform. -> dict with energies, volume, density,
    distortion, cell and convergence. cell: a prebuilt cell (v7: ordered_cell) instead of a random one."""
    t0 = time.time()
    if cell is None:
        cell = random_cell(at, lattice, target_atoms=target_atoms, seed=seed, engine=engine)
    if lattice == "hcp":                                   # v6: a and c free, no shear (zinc: c/a 1.856; the ideal-c/a cell had no stiffness)
        conv, nsteps = engine.relax(cell, fmax=fmax, steps=steps, cell=True, hydrostatic=False, mask=HCP_MASK)
    else:
        conv, nsteps = engine.relax(cell, fmax=fmax, steps=steps, cell=True, hydrostatic=True)
    n = len(cell)
    e = engine.energy(cell) / n
    v = cell.get_volume() / n
    mass = sum(info(s)["mass"] for s in cell.get_chemical_symbols()) / n
    rho = mass * 1.66053906660 / v                       # g/cm³  (amu/Å³ → g/cm³)
    # lattice distortion: displacement from the ideal sites carried through the relaxed cell
    ideal = cell.info["ideal"] @ cell.get_cell()[:]
    d = cell.get_positions() - ideal
    d -= np.round(d @ np.linalg.inv(cell.get_cell()[:])) @ cell.get_cell()[:]
    disp = np.linalg.norm(d, axis=1)
    if lattice == "hcp":
        cv = cell.get_cell()[:]
        ca_cell = (np.linalg.norm(cv[2]) / 3) / (np.linalg.norm(cv[0]) / 4)        # the (4, 4, 3) repeat of the 2-atom base
        nn = (v / (math.sqrt(3) / 4 * ca_cell)) ** (1 / 3)                         # the in-plane spacing a
    else:
        nn = (v * 4) ** (1 / 3) / math.sqrt(2) if lattice == "fcc" else (v * 2) ** (1 / 3) * math.sqrt(3) / 2
    return {
        "lattice": lattice, "n_atoms": n, "seed": seed, "converged": conv, "steps": nsteps,
        "e_per_atom": e, "v_per_atom": v, "density_gcc": rho,
        "distortion_A": float(disp.mean()), "distortion_rel": float(disp.mean() / nn), "nn_distance_A": nn,
        "cell": cell.get_cell()[:].tolist(), "seconds": round(time.time() - t0, 1), "atoms": cell,
    }


def lattice_check(engine, atoms, e_per_atom, steps=150, fmax=0.02):
    """let the cell go fully free for a while: how much energy it gains and how far the cell shape moves. A drop of more
    than ~10 meV/atom or a cell that stops being (near) cubic means the lattice is not mechanically stable in the model
    (it would transform, e.g. along the Bain path) — reported, not hidden."""
    a = atoms.copy()
    c0 = a.get_cell()[:].copy()
    l0 = np.linalg.norm(c0, axis=1)
    engine.relax(a, fmax=fmax, steps=steps, cell=True, hydrostatic=False)
    e1 = engine.energy(a) / len(a)
    c1 = a.get_cell()[:]
    l1 = np.linalg.norm(c1, axis=1)
    ratio = (l1 / l0) / np.mean(l1 / l0)                      # anisotropic length change (1,1,1 = still the same shape)
    cos0 = [abs(np.dot(c0[i], c0[j]) / (l0[i] * l0[j])) for i, j in ((0, 1), (0, 2), (1, 2))]
    cos1 = [abs(np.dot(c1[i], c1[j]) / (l1[i] * l1[j])) for i, j in ((0, 1), (0, 2), (1, 2))]
    drop = float(e_per_atom - e1)
    shape = float(max(abs(ratio - 1).max(), max(abs(x1 - x0) for x0, x1 in zip(cos0, cos1))))   # v6: vs the start (hcp is 120°)
    return {"e_drop_eV": drop, "shape_change": shape, "stable": bool(drop < 0.010 and shape < 0.05)}


def formation_energy(engine, at, e_ss):
    """E_form vs the elements' ground states, plus which state each element took (eV/atom)."""
    ref = 0.0
    states = {}
    for el, c in at.items():
        g = engine.ground(el)
        if g is None:
            return None, states
        states[el] = g[0]
        ref += c * g[1]["e"]
    return e_ss - ref, states


def mixing_energy(engine, at, e_ss, lattice):
    ref = 0.0
    for el, c in at.items():
        ref += c * engine.reference(el, lattice)["e"]
    return e_ss - ref


# ------------------------------------------------------------------ competing ordered compounds
def prototype(kind, A, B, a):
    """ordered binary prototypes as ASE Atoms. kind: b2 (AB), l12 (A3B), l10 (AB), c15 (AB2, Laves), a15 (A3B)."""
    if kind == "b2":
        return Atoms(f"{A}{B}", scaled_positions=[[0, 0, 0], [0.5, 0.5, 0.5]], cell=[a, a, a], pbc=True)
    if kind == "l12":
        return Atoms(f"{A}3{B}", scaled_positions=[[0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5], [0, 0, 0]], cell=[a, a, a], pbc=True)
    if kind == "l10":
        return Atoms(f"{A}2{B}2", scaled_positions=[[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]], cell=[a, a, a], pbc=True)
    if kind == "a15":
        return Atoms(f"{A}6{B}2", scaled_positions=[[0.25, 0, 0.5], [0.75, 0, 0.5], [0.5, 0.25, 0], [0.5, 0.75, 0],
                                                     [0, 0.5, 0.25], [0, 0.5, 0.75], [0, 0, 0], [0.5, 0.5, 0.5]],
                     cell=[a, a, a], pbc=True)
    from pymatgen.core import Lattice, Structure
    from pymatgen.io.ase import AseAtomsAdaptor
    if kind == "c15":                                  # Laves MgCu2 type: A on the 8-fold site, B on the 16-fold (AB2)
        # pymatgen's Fd-3m setting puts (1/2,1/2,1/2) on the 8-fold and (1/8,1/8,1/8) on the 16-fold site — the first
        # version had them the other way round and every "C15-AB" was really A2B (smoke test, 2026-09-29; cache v3)
        s = Structure.from_spacegroup("Fd-3m", Lattice.cubic(a), [A, B], [[0.5, 0.5, 0.5], [0.125, 0.125, 0.125]])
        s = s.get_primitive_structure()
        at = AseAtomsAdaptor.get_atoms(s)
        syms = at.get_chemical_symbols()
        assert syms.count(A) * 2 == syms.count(B), f"C15 {A}{B}: {syms}"
        return at
    if kind == "c14":                                  # Laves MgZn2 type: A 4f, B 2a + 6h (AB2), 12 atoms; a passed = volume/atom
        s = Structure.from_spacegroup("P6_3/mmc", Lattice.hexagonal(5.22, 8.57), [A, B, B],
                                      [[1 / 3, 2 / 3, 0.0630], [0, 0, 0], [0.8306, 0.6612, 0.25]])
        s.scale_lattice(a * len(s))
        return AseAtomsAdaptor.get_atoms(s)
    if kind == "sigma":                                # σ phase, Fe-Cr type (P4_2/mnm, Yakel 1983): 30 atoms, A on the CN12
        s = Structure.from_spacegroup("P4_2/mnm", Lattice.tetragonal(8.7995, 4.5442), [A, B, B, A, B],   # sites, B on CN14/15
                                      [[0, 0, 0], [0.3981, 0.3981, 0], [0.4632, 0.1316, 0], [0.7376, 0.0653, 0], [0.1823, 0.1823, 0.2524]])
        s.scale_lattice(a * len(s))                    # a passed = volume/atom
        return AseAtomsAdaptor.get_atoms(s)
    # 2026-09-30, the backyard families: the precipitates of aluminium, copper and magnesium alloys were not in the list —
    # θ-Al2Cu (C16), Mg2Si (C1), Al3Ti/Al3V/Al3Zr (D0_22), Ti3Al/Ni3Sn-type (D0_19, the closest stand-in for Cu3Sn).
    # All scaled to the volume per atom passed as `a` (like c14/sigma). A = the FIRST species named in PROTOTYPES' fraction.
    if kind == "c16":                                  # Al2Cu type, I4/mcm: A (the 1/3 species) on 4a, B on 8h — 12 atoms
        s = Structure.from_spacegroup("I4/mcm", Lattice.tetragonal(6.067, 4.877), [A, B], [[0, 0, 0.25], [0.1581, 0.6581, 0]])
        s.scale_lattice(a * len(s))
        at = AseAtomsAdaptor.get_atoms(s); syms = at.get_chemical_symbols()
        assert syms.count(A) * 2 == syms.count(B), f"C16 {A}{B}: {syms}"
        return at
    if kind == "c1":                                   # CaF2 / Mg2Si type, Fm-3m: A (1/3) on 4a, B on 8c — primitive 3 atoms
        s = Structure.from_spacegroup("Fm-3m", Lattice.cubic(6.35), [A, B], [[0, 0, 0], [0.25, 0.25, 0.25]]).get_primitive_structure()
        s.scale_lattice(a * len(s))
        at = AseAtomsAdaptor.get_atoms(s); syms = at.get_chemical_symbols()
        assert syms.count(A) * 2 == syms.count(B), f"C1 {A}{B}: {syms}"
        return at
    if kind == "d022":                                 # Al3Ti type, I4/mmm: A (3/4) on 2b + 4d, B on 2a — 8 atoms
        s = Structure.from_spacegroup("I4/mmm", Lattice.tetragonal(3.85, 8.58), [B, A, A], [[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0.25]])
        s.scale_lattice(a * len(s))
        at = AseAtomsAdaptor.get_atoms(s); syms = at.get_chemical_symbols()
        assert syms.count(A) == 3 * syms.count(B), f"D022 {A}{B}: {syms}"
        return at
    if kind == "d019":                                 # Ni3Sn / Ti3Al type, P6_3/mmc: A (3/4) on 6h, B on 2c — 8 atoms
        s = Structure.from_spacegroup("P6_3/mmc", Lattice.hexagonal(5.77, 4.64), [A, B], [[5 / 6, 2 / 3, 0.25], [1 / 3, 2 / 3, 0.25]])
        s.scale_lattice(a * len(s))
        at = AseAtomsAdaptor.get_atoms(s); syms = at.get_chemical_symbols()
        assert syms.count(A) == 3 * syms.count(B), f"D019 {A}{B}: {syms}"
        return at
    raise ValueError(kind)


def prototype3(kind, X, Y, Z, v_atom):
    """ternary prototypes: l21 = Heusler X2YZ (Fm-3m: X 8c, Y 4a, Z 4b), 16 atoms, scaled to v_atom per atom."""
    from pymatgen.core import Lattice, Structure
    from pymatgen.io.ase import AseAtomsAdaptor
    if kind == "l21":
        s = Structure.from_spacegroup("Fm-3m", Lattice.cubic(5.95), [X, Y, Z], [[0.25, 0.25, 0.25], [0, 0, 0], [0.5, 0.5, 0.5]])
        s.scale_lattice(v_atom * len(s))
        return AseAtomsAdaptor.get_atoms(s)
    raise ValueError(kind)


# (kind, fraction of A); c14 and sigma take the volume per atom instead of a lattice constant (they scale themselves)
PROTOTYPES = [("b2", 0.5), ("l12", 0.75), ("l10", 0.5), ("c15", 1 / 3), ("c14", 1 / 3), ("a15", 0.75), ("sigma", 1 / 3),
              ("c16", 1 / 3), ("c1", 1 / 3), ("d022", 0.75), ("d019", 0.75)]      # the last four added 2026-09-30
VOLUME_KINDS = {"c14", "sigma", "c16", "c1", "d022", "d019"}


def pair_compounds(engine, A, B):
    """relaxed energies of the ordered prototypes of the pair (both orders where it matters); cached. -> list of
    {name, comp {A: xA, B: xB}, e (eV/atom)}."""
    key = "|".join(sorted([A, B]))
    if key not in engine.pairs:
        engine.refresh()
    out = list(engine.pairs.get(key, []))
    have = {p["name"].split("-", 1)[0].lower() for p in out}
    todo = [(kind, xA) for kind, xA in PROTOTYPES if kind not in have]     # a cached pair gets the kinds added later
    if not todo:
        return out
    vA, vB = engine.ground(A)[1]["v"], engine.ground(B)[1]["v"]
    for kind, xA in todo:
        for (X, Y, x) in ((A, B, xA), (B, A, xA)):
            if kind in ("b2", "l10") and X == B:
                continue                                    # symmetric prototypes: one order is enough
            vbar = x * (vA if X == A else vB) + (1 - x) * (vB if X == A else vA)
            n_cell = {"b2": 2, "l12": 4, "l10": 4, "a15": 8, "c15": 24}.get(kind, 1)
            a = vbar if kind in VOLUME_KINDS else (n_cell * vbar) ** (1 / 3)
            try:
                at = prototype(kind, X, Y, a)
                engine.relax(at, fmax=0.02, steps=200, cell=True)
                e = engine.energy(at) / len(at)
                comp = {X: x, Y: 1 - x}
                out.append({"name": f"{kind.upper()}-{X}{Y}", "comp": comp, "e": e})
            except Exception as ex:  # noqa: BLE001
                engine.log(f"[proto] {kind} {X}{Y} failed: {ex}")
    engine.pairs[key] = out
    engine.save()
    return out


def triple_compounds(engine, A, B, C):
    """the Heusler L2₁ X2YZ variants of a triple (3 choices of X); cached under the sorted triple."""
    key = "|".join(sorted([A, B, C]))
    if key not in engine.pairs:
        engine.refresh()
    if key in engine.pairs:
        return engine.pairs[key]
    out = []
    vol = {e: engine.ground(e)[1]["v"] for e in (A, B, C)}
    for X, Y, Z in ((A, B, C), (B, A, C), (C, A, B)):
        v_atom = 0.5 * vol[X] + 0.25 * vol[Y] + 0.25 * vol[Z]
        try:
            at = prototype3("l21", X, Y, Z, v_atom)
            engine.relax(at, fmax=0.02, steps=200, cell=True)
            out.append({"name": f"L21-{X}2{Y}{Z}", "comp": {X: 0.5, Y: 0.25, Z: 0.25}, "e": engine.energy(at) / len(at)})
        except Exception as ex:  # noqa: BLE001
            engine.log(f"[proto] l21 {X}2{Y}{Z} failed: {ex}")
    engine.pairs[key] = out
    engine.save()
    return out


def hull_lite(engine, at, e_ss):
    """convex-hull-lite at the composition: the lowest-energy mixture of elements (ground states) and pair compounds
    with the same overall composition (linear programme). -> {e_hull, de_dec (eV/atom), mixture [(name, fraction)]}"""
    from scipy.optimize import linprog
    els = list(at)
    phases = []
    for el in els:
        g = engine.ground(el)
        phases.append((f"{el}({g[0]})", {el: 1.0}, g[1]["e"]))
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            for p in pair_compounds(engine, els[i], els[j]):
                phases.append((p["name"], p["comp"], p["e"]))
            for k in range(j + 1, len(els)):
                for p in triple_compounds(engine, els[i], els[j], els[k]):
                    phases.append((p["name"], p["comp"], p["e"]))
    E = np.array([p[2] for p in phases])
    A_eq = np.array([[p[1].get(el, 0.0) for p in phases] for el in els])
    b_eq = np.array([at[el] for el in els])
    res = linprog(E, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    if not res.success:
        return {"e_hull": None, "de_dec": None, "mixture": []}
    e_hull = float(res.fun)
    mix = [(phases[k][0], float(x)) for k, x in enumerate(res.x) if x > 1e-4]
    mix.sort(key=lambda kv: -kv[1])
    return {"e_hull": e_hull, "de_dec": e_ss - e_hull, "mixture": mix}


def entropy_temperature(de_dec_ev, at):
    """T* (K) above which ideal mixing entropy pays for the decomposition energy (compounds assumed entropy-free)."""
    s = -KB_EV * sum(c * math.log(c) for c in at.values() if c > 0)   # eV/K per atom
    if de_dec_ev is None or de_dec_ev <= 0 or s <= 0:
        return 0.0
    return de_dec_ev / s


# ------------------------------------------------------------------ elastic constants
def elastic(engine, atoms, delta=0.005, fmax=0.01, steps=200):
    """C_ij (GPa, Voigt 6x6) by ± strain with internal relaxation, then Hill averages."""
    base = atoms.copy()
    cell0 = base.get_cell()[:].copy()
    C = np.zeros((6, 6))
    for j in range(6):
        stresses = []
        for sign in (+1, -1):
            eps = np.zeros((3, 3))
            if j < 3:
                eps[j, j] = sign * delta
            else:
                p, q = {3: (1, 2), 4: (0, 2), 5: (0, 1)}[j]
                eps[p, q] = eps[q, p] = sign * delta / 2          # engineering shear γ = 2ε
            a = base.copy()
            a.set_cell(cell0 @ (np.eye(3) + eps), scale_atoms=True)
            engine.relax(a, fmax=fmax, steps=steps, cell=False)
            s = a.get_stress(voigt=True) * EV_A3_TO_GPA               # ASE: [xx, yy, zz, yz, xz, xy], + = tensile
            stresses.append(s)
        C[:, j] = (stresses[0] - stresses[1]) / (2 * delta)
    C = 0.5 * (C + C.T)
    return C, moduli(C)


def moduli(C):
    C = np.asarray(C)
    try:
        S = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        return {"error": "singular C"}
    B_V = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    G_V = (C[0, 0] + C[1, 1] + C[2, 2] - C[0, 1] - C[0, 2] - C[1, 2] + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    B_R = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    G_R = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    B, G = 0.5 * (B_V + B_R), 0.5 * (G_V + G_R)
    E = 9 * B * G / (3 * B + G) if (3 * B + G) else float("nan")
    nu = (3 * B - 2 * G) / (2 * (3 * B + G)) if (3 * B + G) else float("nan")
    c11 = (C[0, 0] + C[1, 1] + C[2, 2]) / 3
    c12 = (C[0, 1] + C[0, 2] + C[1, 2]) / 3
    c44 = (C[3, 3] + C[4, 4] + C[5, 5]) / 3
    eig = np.linalg.eigvalsh(C)
    return {
        "C11": c11, "C12": c12, "C44": c44, "B_GPa": B, "G_GPa": G, "E_GPa": E, "nu": nu,
        "pugh_B_over_G": B / G if G else float("nan"), "cauchy_C12_minus_C44": c12 - c44,
        "zener_A": 2 * c44 / (c11 - c12) if (c11 - c12) else float("nan"),
        "born_stable": bool(eig.min() > 0), "min_eig": float(eig.min()),
    }
