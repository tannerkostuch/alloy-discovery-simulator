"""search.py — the discovery funnel: thousands of compositions → the screening rules → the atomistic physics on the
survivors → strength → a ranked list, each candidate compared with a reference database of known alloys when one is
supplied (docs/DATABASE.md).

A run:  sample(family, n)  →  screen  →  pick the top K by the cheap score  →  evaluate(engine, at)  →  rank(objective)
evaluate() is the whole physics chain for one composition:
  1. relax random cells on FCC and BCC (HCP too when the family says so) → which lattice wins, E_form, E_mix, density,
     lattice distortion
  2. the competing ordered compounds (cached per element pair) → ΔE_dec and T*
  3. elastic constants on the winning lattice → B, G, E, ν, Pugh, Cauchy pressure
  4. solute-strengthening yield stress at 77 / 300 / 600 / 900 / 1200 K
Everything is written as JSON per candidate (results/<run>/<formula>.json) so a crashed run resumes, then
DISCOVERIES.md ranks them.
v2 (2026-10-05, after the validation): every row also carries the CALIBRATED yield (calibrate.py: the host/solute factors
and floors the validation measured), the zinc/cadmium moduli factor, and notes — a soft or unstable cell, a β/γ-brass
zinc equivalent, a zinc/magnesium-rich alloy on a cubic lattice, uncalibrated solutes; the objective strong_ductile_cal
ranks by the calibrated yield (tin is no longer worth ×5.6); a bcc cell that comes out unstable while the hull says the
alloy would rather be a B2 compound is built again B2-ORDERED (atomistic.ordered_cell) and, when that cell is stable,
the row shows the ordered cell's numbers (the random cell's stay in the JSON); shortlists take a seed, so a second pass
of a family samples different compositions. Nothing that runs 1–9 were ranked on has changed.
"""
import json
import math
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

import numpy as np

from . import atomistic as A
from . import calibrate as CAL
from . import compo, screen
from .elements import allowed, info
from .strength import solute_strength

RESULTS = Path(__file__).resolve().parent.parent / "results"

# element pools and composition bounds (atomic fraction) per family; "lattices" = which cells to try
# "must" = minimum atomic fraction of an element that is always present; "max" = per-element caps (the solubility
# limits that keep a family what it says it is — without them the cheap score drifts to 45 % Al, which is a B2
# compound, not an FCC alloy: seen 2026-09-29 before the first run); the shortlist also insists the VEC lattice
# guess agrees with the family's first lattice.
FAMILIES = {
    "3d_hea": {
        "pool": ["Co", "Cr", "Fe", "Mn", "Ni", "Al", "Cu", "V", "Ti"], "n_elements": (4, 6), "bounds": (0.05, 0.35),
        "lattices": ["fcc", "bcc"], "note": "Cantor-family multi-principal alloys (3d metals + a little Al/Ti/V)",
        "max": {"Al": 0.15, "Cu": 0.20, "Ti": 0.12, "V": 0.20},
    },
    "refractory": {
        "pool": ["Nb", "Mo", "Ta", "W", "V", "Ti", "Zr", "Hf", "Cr"], "n_elements": (3, 5), "bounds": (0.10, 0.40),
        "lattices": ["bcc", "fcc"], "note": "refractory BCC multi-principal alloys", "max": {"Cr": 0.20},
    },
    "medium_entropy_fcc": {
        "pool": ["Ni", "Co", "Cr", "Fe", "Cu", "Mn", "Al", "V"], "n_elements": (3, 4), "bounds": (0.10, 0.50),
        "lattices": ["fcc", "bcc"], "note": "medium-entropy FCC alloys around Ni-Co-Cr (Al/V as minor additions)",
        "max": {"Al": 0.12, "V": 0.15, "Cu": 0.30, "Mn": 0.35},
    },
    "ti_light_bcc": {
        "pool": ["Ti", "Zr", "Nb", "V", "Ta", "Hf", "Mo", "Al", "Cr"], "n_elements": (3, 5), "bounds": (0.03, 0.75),
        "lattices": ["bcc", "hcp"], "note": "Ti-rich β (BCC) alloys, from multi-principal to TNZT-like (≥ 35 at% Ti)",
        "must": {"Ti": 0.35},   # 2026-09-29: was bounds 0.05-0.45 with no minimum — that could not even hold Ti-35Nb-7Zr-5Ta (70 at% Ti)
        "max": {"Al": 0.15, "Cr": 0.15},
    },
    "cu_alloys": {
        "pool": ["Cu", "Ni", "Zn", "Al", "Mn", "Fe", "Co", "Cr"], "n_elements": (2, 4), "bounds": (0.03, 0.60),
        "lattices": ["fcc", "bcc"], "note": "copper-based solid solutions (α-brass / bronze / cupronickel territory)", "must": {"Cu": 0.50},
        # 2026-09-30: "bcc" added after run 5 — its #1 (Cu58Zn32Al10) has a Guillet zinc equivalent of ~62 %, deep in the
        # β/γ-brass field, and an FCC-only family plus a hull without γ-brass (Cu5Zn8, not a prototype here) cannot see that;
        # with bcc in the list the disordered β at least competes, and B2-CuZn is in the hull
        "max": {"Al": 0.18, "Zn": 0.35, "Fe": 0.06, "Cr": 0.03, "Co": 0.06, "Mn": 0.20, "Ni": 0.50},
    },
    # ---- the BACKYARD families (2026-09-30: novel ways to mix the commonly available metals, something a hobbyist
    # could pour in a back yard): everything melts or dissolves below ~1150 °C — a propane or charcoal furnace and a
    # clay-graphite crucible. Zn, Mg and Sn are "volatile" by the castability rule; here that is the normal business of
    # brass and bronze founding (flux, a lid, Zn added last), so volatile_ok switches the penalty off. Sn and Si are on
    # the default exclusion list (non-cubic elements) but are fine as SOLUTES — a pool may name them. The compounds these
    # alloys would rather be (θ-Al2Cu, Mg2Si, MgZn2, CuZn, Cu-Sn, ZrAl3…) are exactly their age-hardening precipitates,
    # so "would rather be" is read as "what strengthens it on ageing", not only as a warning.
    "backyard_al": {
        "pool": ["Al", "Cu", "Mg", "Si", "Zn", "Mn", "Ag"], "n_elements": (2, 5), "bounds": (0.01, 0.99),
        "lattices": ["fcc"], "must": {"Al": 0.88}, "volatile_ok": True, "lattice_rule": "base", "spread": 0.025,
        "max": {"Cu": 0.05, "Mg": 0.10, "Si": 0.10, "Zn": 0.10, "Mn": 0.02, "Ag": 0.01},
        "note": "aluminium you can pour at 700 °C: 2xxx/5xxx/6xxx/7xxx territory and the crossover alloys between them",
    },
    "backyard_cu": {
        "pool": ["Cu", "Zn", "Sn", "Al", "Si", "Mn", "Ni", "Ag", "Mg"], "n_elements": (2, 4), "bounds": (0.01, 0.99),
        "lattices": ["fcc", "bcc"], "must": {"Cu": 0.58}, "volatile_ok": True, "lattice_rule": "base",
        "max": {"Zn": 0.38, "Sn": 0.10, "Al": 0.14, "Si": 0.07, "Mn": 0.20, "Ni": 0.10, "Ag": 0.05, "Mg": 0.04},
        "note": "brass, bronze, aluminium/silicon/manganese bronze and their mixes — copper poured at 1000–1150 °C",
    },
    "backyard_zn": {
        "pool": ["Zn", "Al", "Cu", "Mg", "Ag"], "n_elements": (2, 4), "bounds": (0.01, 0.99),
        "lattices": ["hcp", "fcc"], "must": {"Zn": 0.70}, "volatile_ok": True, "lattice_rule": "base", "spread": 0.04,
        "max": {"Al": 0.30, "Cu": 0.06, "Mg": 0.03, "Ag": 0.02},
        "note": "zinc die-cast territory (Zamak, ZA-8/12/27) — pours at 450 °C, the easiest backyard metal there is",
    },
    "backyard_hea": {
        "pool": ["Cu", "Zn", "Al", "Mn", "Sn", "Ni", "Ag", "Mg", "Si"], "n_elements": (4, 6), "bounds": (0.04, 0.60),
        "lattices": ["fcc", "bcc"], "must": {"Cu": 0.30}, "volatile_ok": True, "lattice_rule": "base",
        "max": {"Sn": 0.10, "Ni": 0.12, "Si": 0.08, "Mg": 0.10, "Ag": 0.08, "Al": 0.25, "Zn": 0.40, "Mn": 0.25},
        "note": "a 'high-entropy brass': four to six pour-able metals on a copper base — the corner nobody casts in a backyard yet",
    },
    # 2026-10-05: magnesium is the one backyard metal left now that hexagonal cells work (v6).
    # hcp only: magnesium is hcp at every casting composition (the fcc/bcc cells of a zinc-rich alloy in run 8 were
    # fictions that read as "two-phase casting"); the objective is stiff_stable (no yield model for hcp). Ca and Sn are
    # on the default exclusion list but are real magnesium alloying elements (Mg-Ca, Mg-Sn casting alloys). Molten
    # magnesium burns: the chain only ranks, it knows nothing about melting anything safely.
    "backyard_mg": {
        "pool": ["Mg", "Al", "Zn", "Mn", "Ca", "Si", "Sn", "Cu"], "n_elements": (2, 5), "bounds": (0.01, 0.99),
        "lattices": ["hcp"], "must": {"Mg": 0.85}, "volatile_ok": True, "lattice_rule": "base", "spread": 0.03,
        "max": {"Al": 0.12, "Zn": 0.05, "Mn": 0.02, "Ca": 0.04, "Si": 0.03, "Sn": 0.04, "Cu": 0.03},
        "note": "magnesium casting territory (AZ91/AM60/AS41, Mg-Zn, Mg-Sn, Mg-Ca) — pours at 700 °C under a flux or cover gas",
    },
}

OBJECTIVES = {
    # name: (description, function(result) -> score; higher is better; None = not scorable)
    "specific_strength": ("yield stress at 300 K per density (MPa per g/cm³), single-phase and ductile favoured",
                          lambda r: _sy(r, 300) / r["density_gcc"] * _phase_factor(r, 300) * _ductile_factor(r)),
    "high_temp": ("yield stress at 900 K, with a high melting point and a stable single phase at 900 K",
                  lambda r: _sy(r, 900) * _phase_factor(r, 900) * _ductile_factor(r) * (1.0 if r["screen"]["tm_mix_K"] >= 1800 else 0.5)),
    "strong_ductile": ("yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured",
                       lambda r: _sy(r, 300) * _phase_factor(r, 300) * _ductile_factor(r)),
    "stability": ("most negative formation energy with the solid solution on the hull",
                  lambda r: -r["e_form_eV"] * _phase_factor(r, 300)),
    "stiff_stable": ("shear modulus times the phase and ductility factors — for lattices the strengthening model does not cover (HCP zinc, magnesium)",
                     lambda r: float((r.get("elastic") or {}).get("G_GPa") or 0.0) * _phase_factor(r, 300) * _ductile_factor(r)),
    # v2: the calibrated yield (calibrate.py) in place of the raw one, and a soft cell (G < 10 GPa, B/G > 8) counts as unstable
    "strong_ductile_cal": ("CALIBRATED yield at 300 K (the validation's host/solute factors + floor) times the ductility factor, single phase at 300 K favoured; soft cells count as unstable",
                           lambda r: _sy_cal(r, 300) * _phase_factor(r, 300) * _ductile_factor(r, soft=True)),
}


def _sy(r, T):
    s = r.get("strength") or {}
    return float((s.get("sigma_y_MPa") or {}).get(str(T)) or (s.get("sigma_y_MPa") or {}).get(T) or 0.0)


def _sy_cal(r, T):
    """the calibrated yield at T (calibrate.calibrated_yield); the raw one when there is nothing to calibrate."""
    c = r.get("calibrated") or CAL.calibrated_yield(r) or {}
    v = (c.get("sigma_y_cal_MPa") or {}).get(str(T))
    return float(v) if v is not None else _sy(r, T)


def dg_service(r, T):
    """ΔG of the solid solution vs its decomposition products at T (eV/atom): ΔE_dec − T·S_ideal. > 0 = metastable,
    and the size says how hard it wants to decompose. None when there is no hull."""
    h = r.get("hull") or {}
    if h.get("de_dec") is None:
        return None
    s_ideal = -A.KB_EV * sum(c * math.log(c) for c in r["at"].values() if c > 0)
    return float(h["de_dec"] - T * s_ideal)


def _phase_factor(r, T=300):
    """exp(−ΔG(T)/0.04 eV): 1 when the solid solution is the stable state at the service temperature T, e^-1 when it
    sits 40 meV/atom above its decomposition products (about the model's own error bar), ~0.02 at 150 meV — the
    Alnico-like Fe-Co-Cu-Al cells of run 1 (2026-09-29) were 110 meV above a Heusler + Fe + Cu mixture and still
    topped the list with the old 300/T* factor; they are magnets that decompose on purpose, not FCC alloys. Halved
    when the winning lattice would transform with a free cell (lattice_check)."""
    dg = dg_service(r, T)
    f = 0.5 if dg is None else math.exp(-max(0.0, dg) / 0.04)
    if not (r.get("lattice_check") or {}).get("stable", True):
        f *= 0.5
    return f


def _ductile_factor(r, soft=False):
    """soft=True (v2 objectives): a cell with G under 10 GPa or B/G over 8 is treated like a Born-unstable one — the
    zinc-rich fcc cells of run 8 (G 3–5, B/G 14–24) passed the Born check and still had no stiffness worth the name."""
    m = r.get("elastic") or {}
    pugh, cauchy = m.get("pugh_B_over_G"), m.get("cauchy_C12_minus_C44")
    if pugh is None or (isinstance(pugh, float) and math.isnan(pugh)):
        return 0.7
    f = 1.0 if pugh >= 1.75 else max(0.2, pugh / 1.75)
    if cauchy is not None and cauchy < 0:
        f *= 0.7
    if not m.get("born_stable", True) or (soft and CAL.soft_cell(r)):
        f *= 0.1
    return f


# ------------------------------------------------------------------ candidates
def sample(family, n=2000, seed=0):
    """random compositions inside the family's rules; [(formula, at)] unique."""
    fam = FAMILIES[family]
    pool = list(fam["pool"])                            # a pool names its elements explicitly (Sn, Si… are fine as solutes)
    lo, hi = fam["bounds"]
    rng = np.random.default_rng(seed)
    seen, out = set(), []
    tries = 0
    while len(out) < n and tries < 50 * n:
        tries += 1
        k = int(rng.integers(fam["n_elements"][0], fam["n_elements"][1] + 1))
        els = list(rng.choice(pool, size=k, replace=False))
        for m in fam.get("must", {}):
            if m not in els:
                els[0] = m
        x = rng.dirichlet(np.ones(k) * 2.0)
        for m, mn in fam.get("must", {}).items():
            i = els.index(m)
            if x[i] < mn:                                  # lift the must-element to [mn, mn + 30 % of the rest], scale the others
                want = mn + rng.random() * (1 - mn) * 0.3
                others = 1.0 - x[i]
                x = x * ((1.0 - want) / others) if others > 0 else x
                x[i] = want
        if x.min() < lo or x.max() > hi:
            continue
        if any(x[els.index(m)] > mx for m, mx in fam.get("max", {}).items() if m in els):
            continue
        x = np.round(x / 0.01) * 0.01
        x[int(np.argmax(x))] += 1.0 - x.sum()                 # whole atomic per cents that add up to 100
        at = {str(e): round(float(v), 4) for e, v in zip(els, x) if v > 0}
        key = compo.formula(at, 0)
        if key in seen:
            continue
        seen.add(key)
        out.append((key, at))
    return out


def cheap_score(f, volatile_ok=False):
    """order the screening survivors: bigger misfit (strengthening) and a clear lattice, cheaper elements first."""
    d = f["delta_pct"] or 0.0
    s = min(d, 3.0) / 3.0                              # misfit strengthens; past ~3 % it is not a better bet, only a riskier one
    if f["lattice_guess"] == "fcc+bcc":
        s *= 0.8
    s *= 1.0 / (1.0 + 0.25 * f["price_class"])
    if f.get("volatile_elements") and not volatile_ok:
        s *= 0.6                                       # boils off in the furnace — harder to make (Gemini's review)
    if not screen.strict(f):
        s *= 0.7                                       # in the wide window only (dH < -15 or > 5): compounds more likely (Grok's note)
    return s


def shortlist(family, n_sample=2000, keep=24, seed=0, log=print, spread=0.10, avoid=()):
    """sample → screening rules → the top `keep` by cheap score, no two closer than `spread` (half-L1 distance in
    atomic fraction) so a run does not spend its hours on eight versions of one alloy. -> [(formula, at, features)]
    avoid (v2): compositions a second pass must stay `spread` away from — the first pass's shortlist."""
    cands = sample(family, n_sample, seed)
    fam = FAMILIES[family]
    want = fam["lattices"][0]
    spread = fam.get("spread", spread)                 # dilute families (backyard Al/Zn) live within a few at% of each other
    by_base = fam.get("lattice_rule") == "base"        # the VEC lattice rule is an HEA rule; an Al/Cu/Zn-based alloy takes its base's lattice
    rows = []
    n_avoided = 0
    for key, at in cands:
        if avoid and any(compo.distance(at, q) <= spread for q in avoid):
            n_avoided += 1
            continue
        f = screen.features(at)
        if screen.passes(f) and (by_base or want in f["lattice_guess"]):      # "fcc", "bcc" or the duplex "fcc+bcc"
            rows.append((cheap_score(f, fam.get("volatile_ok", False)), key, at, f))
    if avoid:
        log(f"[shortlist] {n_avoided} of {len(cands)} sampled compositions set aside: within {spread} of an earlier pass ({len(avoid)} alloys)")
    rows.sort(key=lambda r: -r[0])
    # breadth first: the best composition of every distinct element SET, round-robin over the sets (so a run tries
    # twelve different alloy systems, not twelve versions of one), then the spread rule on top
    by_set = {}
    for sc, key, at, f in rows:
        by_set.setdefault(tuple(sorted(at)), []).append((key, at, f))
    picked = []
    must = set(FAMILIES[family].get("must", {}))

    def crowded(at, share):   # a (non-must) element already in `share` of the picks (once there are four): enough of it
        if len(picked) < 4:
            return False
        return any(sum(el in q for _, q, _ in picked) >= share * len(picked) for el in at if el not in must)

    share = 0.6
    while len(picked) < keep and share <= 1.0:
        rank, stalled = 0, False
        while len(picked) < keep and not stalled:
            stalled = True
            for group in by_set.values():
                if rank < len(group):
                    key, at, f = group[rank]
                    if any(k == key for k, _, _ in picked):
                        continue
                    stalled = False
                    if all(compo.distance(at, q) > spread for _, q, _ in picked) and not crowded(at, share):
                        picked.append((key, at, f))
                        if len(picked) >= keep:
                            break
            rank += 1
        share += 0.1                                   # could not fill the list under this cap: relax it a little
    log(f"[shortlist] {family}: {len(cands)} sampled, {len(rows)} pass the rules + lattice, {len(by_set)} element sets, keeping {len(picked)} (spread ≥ {spread})")
    return picked


# ------------------------------------------------------------------ novelty
_DB = None


def known_alloys():
    """the reference database of known alloys (compo.DB_FINAL: $ALLOYS_DB or data/alloys.json); [] when there is none."""
    global _DB
    if _DB is None:
        try:
            _DB = compo.load_db()
        except Exception:  # noqa: BLE001
            _DB = []
    return _DB


def novelty(at, tol=0.06):
    """nearest known alloys by composition distance; new when none is within tol. Without a reference database
    nothing can be called new: is_new is None and the tables say "n/a"."""
    known = known_alloys()
    if not known:
        return {"is_new": None, "nearest": [], "checked": False}
    near = []
    for rid, name, fam, dat in known:
        d = compo.distance(at, dat)
        if d <= 0.25:
            near.append((d, rid, name, fam))
    near.sort()
    return {"is_new": not any(d <= tol for d, *_ in near), "nearest": [(round(d, 3), rid, name, fam) for d, rid, name, fam in near[:5]]}


def new_text(r, short=False):
    """the "new?" cell of a row: NEW, "near <alloy>" (short: "known"), or n/a when no reference database was there."""
    nv = r.get("novelty") or {}
    if nv.get("is_new") is None:
        return "n/a"
    if nv["is_new"]:
        return "NEW"
    if short:
        return "known"
    return "near " + str(nv["nearest"][0][2] if nv.get("nearest") else "?")


# ------------------------------------------------------------------ the physics chain for one composition
def evaluate(engine, at, lattices=("fcc", "bcc"), target_atoms=108, seeds=(0,), do_elastic=True, do_hull=True, log=print, do_check=True):
    """do_check=False skips the free-cell lattice check (the validation's cheap tier, 2026-09-30)."""
    t0 = time.time()
    r = {"formula": compo.formula(at), "at": at, "wt_pct": {k: round(v, 2) for k, v in compo.at_to_wt(at).items()},
         "engine": engine.name, "screen": screen.features(at), "cells": {}}
    r["screen"]["in_wide_window"] = screen.passes(r["screen"])        # Guo & Liu 2011: -22..7 kJ/mol, δ ≤ 6.6, Ω ≥ 1.1
    r["screen"]["in_zhang2008_window"] = screen.strict(r["screen"])   # Zhang 2008: -15..5 (Grok's note, 2026-09-29)
    best = None
    for L in lattices:
        es = []
        keep = None
        for s in seeds:
            try:
                ss = A.solid_solution(engine, at, L, seed=s, target_atoms=target_atoms)
            except Exception as e:  # noqa: BLE001
                log(f"[eval] {r['formula']} {L} seed {s} failed: {e}")
                continue
            es.append(ss["e_per_atom"])
            if keep is None or ss["e_per_atom"] < keep["e_per_atom"]:
                keep = ss
        if keep is None:
            continue
        r["cells"][L] = {k: v for k, v in keep.items() if k not in ("atoms", "cell")}
        r["cells"][L]["e_spread"] = float(max(es) - min(es)) if len(es) > 1 else 0.0
        if best is None or keep["e_per_atom"] < best[1]["e_per_atom"]:
            best = (L, keep)
    if best is None:
        r["error"] = "no cell relaxed"
        return r
    L, ss = best
    r["lattice"] = L
    if do_check:
        try:                                                      # would the winning cell transform if the cell were free?
            r["lattice_check"] = A.lattice_check(engine, ss["atoms"], ss["e_per_atom"])
        except Exception as e:  # noqa: BLE001
            r["lattice_check"] = {"error": str(e)}
    r["density_gcc"] = float(ss["density_gcc"])
    r["v_per_atom_A3"] = float(ss["v_per_atom"])
    r["distortion_rel"] = float(ss["distortion_rel"])
    ef, states = A.formation_energy(engine, at, ss["e_per_atom"])
    r["e_form_eV"] = None if ef is None else float(ef)
    r["element_ground_states"] = states
    r["e_mix_eV"] = float(A.mixing_energy(engine, at, ss["e_per_atom"], L))
    others = {k: float(v["e_per_atom"] - ss["e_per_atom"]) for k, v in r["cells"].items() if k != L}
    r["lattice_margin_eV"] = others
    if do_hull:
        try:
            h = A.hull_lite(engine, at, ss["e_per_atom"])
            h["T_star_K"] = float(A.entropy_temperature(h["de_dec"], at)) if h["de_dec"] is not None else None
            # ΔG(T) = ΔE_dec − T·S_ideal: is the solution the stable state at room, service and anneal temperature?
            s_ideal = -A.KB_EV * sum(c * math.log(c) for c in at.values() if c > 0)
            h["stable_at_K"] = {str(T): bool(h["de_dec"] is not None and h["de_dec"] - T * s_ideal <= 0) for T in (300, 900, 1200)}
            r["hull"] = h
        except Exception as e:  # noqa: BLE001
            r["hull"] = {"error": str(e)}
    if do_elastic:
        try:
            C, m = A.elastic(engine, ss["atoms"])
            r["elastic"] = {k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in m.items()}
            r["C_GPa"] = np.round(C, 1).tolist()
        except Exception as e:  # noqa: BLE001
            r["elastic"] = {"error": str(e)}
    m = r.get("elastic") or {}
    if L in ("fcc", "bcc") and not m.get("error") and (m.get("G_GPa") or 0) > 0 and m.get("born_stable", True):
        v_el = {el: engine.reference(el, L)["v"] for el in at}
        st = solute_strength(L, at, r["v_per_atom_A3"], v_el, m["G_GPa"], m["nu"])
        if st:
            st["sigma_y_MPa"] = {str(k): float(v) for k, v in st["sigma_y_MPa"].items()}
            r["strength"] = st
    if L == "bcc" and do_elastic and do_hull and _wants_b2(r):      # v2: the ordered B2 cell the alloy really is
        r["ordered"] = _ordered_retry(engine, at, r, target_atoms, seeds[0] if seeds else 0, log)
    v = view(r)
    r["calibrated"] = CAL.calibrated_yield(v)
    r["calibrated_moduli"] = CAL.calibrated_moduli(v)
    r["notes"] = CAL.notes(v)
    r["novelty"] = novelty(at)
    r["seconds"] = round(time.time() - t0, 1)
    return r


def _b2_product(r):
    """the B2 compound in the hull's mixture (fraction ≥ 0.2) -> (X, Y) or None."""
    for name, x in (r.get("hull") or {}).get("mixture") or []:
        if str(name).startswith("B2-") and x >= 0.2:
            els = re.findall(r"[A-Z][a-z]?", str(name)[3:])
            if len(els) == 2:
                return els[0], els[1]
    return None


def _wants_b2(r):
    """a bcc cell that is unstable (soft, Born-unstable or would transform) while the hull says the alloy would rather
    be a B2 compound: that is a β-brass / NiTi / NiAl-type alloy, and the random bcc cell is the wrong contender."""
    if r.get("lattice") != "bcc" or (r.get("elastic") or {}).get("error"):
        return False
    unstable = CAL.soft_cell(r) or not (r.get("lattice_check") or {}).get("stable", True)
    return bool(unstable and _b2_product(r) is not None)


def _ordered_retry(engine, at, r, target_atoms, seed, log=print):
    """build the B2-ordered cell, relax it the same way, check it, measure it: -> the 'ordered' block of the result."""
    X, Y = _b2_product(r)
    t0 = time.time()
    o = {"kind": f"B2-{X}{Y}", "stable": False}
    try:
        cell = A.ordered_cell(at, X, Y, target_atoms=target_atoms, seed=seed, engine=engine)
        ss = A.solid_solution(engine, at, "bcc", seed=seed, target_atoms=target_atoms, cell=cell)
        o.update({k: v for k, v in ss.items() if k not in ("atoms", "cell")})
        o["lattice_check"] = A.lattice_check(engine, ss["atoms"], ss["e_per_atom"])
        ef, _ = A.formation_energy(engine, at, ss["e_per_atom"])
        o["e_form_eV"] = None if ef is None else float(ef)
        h = r.get("hull") or {}
        if h.get("e_hull") is not None:
            o["de_dec_eV"] = float(ss["e_per_atom"] - h["e_hull"])
            o["T_star_K"] = float(A.entropy_temperature(o["de_dec_eV"], at))
        o["e_drop_vs_random_eV"] = float(r["cells"]["bcc"]["e_per_atom"] - ss["e_per_atom"])
        C, m = A.elastic(engine, ss["atoms"])
        o["elastic"] = {k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in m.items()}
        o["C_GPa"] = np.round(C, 1).tolist()
        probe = {"elastic": o["elastic"], "lattice_check": o["lattice_check"]}
        o["stable"] = bool(o["elastic"].get("born_stable", False) and not CAL.soft_cell(probe) and o["lattice_check"].get("stable", False))
        if o["stable"] and (o["elastic"].get("G_GPa") or 0) > 0:
            v_el = {el: engine.reference(el, "bcc")["v"] for el in at}
            st = solute_strength("bcc", at, ss["v_per_atom"], v_el, o["elastic"]["G_GPa"], o["elastic"]["nu"])
            if st:
                st["sigma_y_MPa"] = {str(k): float(v) for k, v in st["sigma_y_MPa"].items()}
                o["strength"] = st
        log(f"[b2] {r['formula']}: {o['kind']} ordered cell {o['e_drop_vs_random_eV']*1000:+.0f} meV below the random one, "
            f"G {o['elastic'].get('G_GPa', float('nan')):.0f} GPa, {'stable' if o['stable'] else 'still unstable'}")
    except Exception as e:  # noqa: BLE001
        o["error"] = f"{e.__class__.__name__}: {e}"
        log(f"[b2] {r.get('formula')}: ordered cell failed: {o['error']}")
    o["seconds"] = round(time.time() - t0, 1)
    return o


def view(r):
    """the numbers a row shows: the random cell's — or, when a B2-ordered cell was built and came out stable (v2), that
    cell's energies, density, moduli and strength (the random cell's stay in the JSON under 'cells' and 'elastic')."""
    o = r.get("ordered")
    if not o or not o.get("stable"):
        return r
    v = dict(r)
    v["lattice_view"] = "bcc (B2)"
    for k in ("e_form_eV", "density_gcc", "v_per_atom_A3", "elastic", "C_GPa", "strength", "lattice_check"):
        if k in o:
            v[k] = o[k]
    if "de_dec_eV" in o:
        h = dict(r.get("hull") or {})
        h["de_dec"], h["T_star_K"] = o["de_dec_eV"], o.get("T_star_K")
        v["hull"] = h
    return v


# ------------------------------------------------------------------ runs
# ------------------------------------------------------------------ result files: written whole or not at all
def _dump_json(path, obj):
    """temp file + rename: a power cut in the middle of a write leaves the old file or none, never half a file."""
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=float))
    os.replace(tmp, path)


def _load_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


# ------------------------------------------------------------------ worker processes (CPU runs: several candidates at once)
# One MACE force call on a 108-atom cell uses all 16 threads badly (small graph); four workers with four threads each
# get through a shortlist about twice as fast (2026-09-29). Each worker builds its own Engine from engine.spec; the
# caches on disk are shared through the Engine's lock file. "spawn" so torch's threads are never forked.
_W = {"engine": None}


def _worker_init(spec, threads):
    import warnings
    warnings.filterwarnings("ignore")
    spec = dict(spec); spec["threads"] = threads
    _W["engine"] = A.Engine(log=lambda *a, **k: None, **spec)


def _worker_eval(key, at, lattices, target_atoms, seeds, do_elastic, do_hull):
    t0 = time.time()
    r = evaluate(_W["engine"], at, lattices=lattices, target_atoms=target_atoms, seeds=seeds,
                 do_elastic=do_elastic, do_hull=do_hull, log=lambda *a, **k: None)
    return key, r, round(time.time() - t0)


def auto_workers(engine):
    """how many candidates to evaluate at once: 1 on a GPU, else cpu/4 capped at 4."""
    if getattr(engine, "device", "cpu") != "cpu" or engine.kind != "mace":
        return 1
    return max(1, min(4, (os.cpu_count() or 4) // 4))


def run(engine, family, objective="specific_strength", n_sample=2000, keep=24, seeds=(0,), target_atoms=108,
        run_name=None, log=print, do_elastic=True, do_hull=True, include=(), workers=1, seed=0, avoid_runs=()):
    """include: formulas evaluated first, before the shortlist (the known alloys a run must re-find).
    workers > 1: that many candidates at once in separate processes (CPU engines; see _worker_init).
    seed (v2): the shortlist's sampling seed — a second pass of a family with seed 1 tries other compositions;
    avoid_runs (v2): earlier run names whose shortlists the new one stays clear of (results/<run>/shortlist.json)."""
    fam = FAMILIES[family]
    run_name = run_name or f"{family}-{objective}-{time.strftime('%Y%m%d-%H%M')}"
    out = RESULTS / run_name
    out.mkdir(parents=True, exist_ok=True)
    avoid = []
    for prev in avoid_runs:
        try:
            avoid += [x["at"] for x in json.loads((RESULTS / prev / "shortlist.json").read_text())]
        except Exception as e:  # noqa: BLE001
            log(f"[run] could not read the shortlist of {prev} ({e}) — not avoided")
    short = [(compo.formula(compo.parse(f), 0), compo.parse(f), screen.features(compo.parse(f))) for f in include]
    short += shortlist(family, n_sample, keep, seed=seed, log=log, avoid=avoid)
    (out / "shortlist.json").write_text(json.dumps([{"formula": k, "at": at, "screen": f} for k, at, f in short], indent=1))
    results, todo = [], []
    for i, (key, at, f) in enumerate(short, 1):
        p = out / f"{key}.json"
        cached = _load_json(p)
        if cached is not None:
            results.append(cached)
            log(f"[{i}/{len(short)}] {key} (cached)")
        else:
            if p.exists():
                log(f"[{i}/{len(short)}] {key}: unreadable result file (cut-off write?) — recomputing")
                p.unlink(missing_ok=True)
            todo.append((i, key, at))
    if results:
        write_report(out, results, family, objective)
    if workers <= 1 or len(todo) <= 1:
        for i, key, at in todo:
            log(f"[{i}/{len(short)}] {key} …")
            r = evaluate(engine, at, lattices=fam["lattices"], target_atoms=target_atoms, seeds=seeds,
                         do_elastic=do_elastic, do_hull=do_hull, log=log)
            _dump_json(out / f"{key}.json", r)
            log(f"    {summary_line(r)}")
            results.append(r)
            write_report(out, results, family, objective)
        return out, results
    # parallel: the elemental references first, in this process, so the workers do not all compute them at once
    pool_els = sorted({el for _, _, at in todo for el in at})
    for el in pool_els:
        engine.ground(el)
    threads = max(1, (os.cpu_count() or 4) // workers)
    log(f"[run] {len(todo)} candidates on {workers} workers × {threads} threads")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn"), initializer=_worker_init,
                             initargs=(engine.spec, threads)) as ex:
        futs = {ex.submit(_worker_eval, key, at, fam["lattices"], target_atoms, seeds, do_elastic, do_hull): (i, key)
                for i, key, at in todo}
        done = 0
        for fut in as_completed(futs):
            i, key = futs[fut]
            done += 1
            try:
                _, r, secs = fut.result()
            except Exception as e:  # noqa: BLE001
                r = {"formula": key, "error": f"{e.__class__.__name__}: {e}", "novelty": {"is_new": False}, "seconds": 0}
                secs = 0
            _dump_json(out / f"{key}.json", r)
            log(f"[{i}/{len(short)}] {key} — {summary_line(r)}  ({done}/{len(todo)} done, {(time.time()-t0)/60:.0f} min)")
            results.append(r)
            write_report(out, results, family, objective)
    engine.refresh()
    return out, results


def score(r, objective):
    r = view(r)
    if r.get("error") or "strength" not in r and objective not in ("stability", "stiff_stable"):
        return None
    try:
        return float(OBJECTIVES[objective][1](r))
    except Exception:  # noqa: BLE001
        return None


def summary_line(r):
    if r.get("error"):
        return "ERROR " + r["error"]
    r = view(r)
    m = r.get("elastic") or {}
    s = (r.get("strength") or {}).get("sigma_y_MPa") or {}
    h = r.get("hull") or {}
    lc = r.get("lattice_check") or {}
    lat = r.get("lattice_view", r["lattice"]) + ("" if lc.get("stable", True) else f" (would transform: −{1000*lc.get('e_drop_eV', 0):.0f} meV)")
    cal = (r.get("calibrated") or {}).get("sigma_y_cal_MPa") or {}
    cal_txt = f" (cal. {cal['300']:.0f})" if cal.get("300") is not None and s else ""
    notes = r.get("notes") or []
    return (f"{lat} | E_form {r['e_form_eV']:+.3f} eV | ΔE_dec {h.get('de_dec', float('nan')):+.3f} eV (T* {h.get('T_star_K', 0):.0f} K) | "
            f"ρ {r['density_gcc']:.2f} | G {m.get('G_GPa', float('nan')):.0f} GPa B/G {m.get('pugh_B_over_G', float('nan')):.2f} | "
            f"σy 300K {s.get('300', 0):.0f} MPa{cal_txt}, 900K {s.get('900', 0):.0f} | {new_text(r, short=True)}"
            + (f" | {'; '.join(notes)}" if notes else "") + f" | {r['seconds']} s")


def write_report(out, results, family, objective):
    desc = OBJECTIVES[objective][0]
    scored = [(score(r, objective), r) for r in results]
    scored = [(s, r) for s, r in scored if s is not None]
    scored.sort(key=lambda t: -t[0])
    lines = [f"# {family} — ranked by {objective}", "", f"objective: {desc}", f"engine: {results[0]['engine'] if results else '?'} · candidates evaluated: {len(results)}", "",
             "| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (s, r0) in enumerate(scored, 1):
        r = view(r0)
        m = r.get("elastic") or {}
        sy = (r.get("strength") or {}).get("sigma_y_MPa") or {}
        h = r.get("hull") or {}
        dg = dg_service(r, 300)
        new = new_text(r)
        lat = r.get("lattice_view", r["lattice"]) + ("" if (r.get("lattice_check") or {}).get("stable", True) else "⚠")
        cal = r.get("calibrated") or CAL.calibrated_yield(r) or {}
        cal_v = (cal.get("sigma_y_cal_MPa") or {}).get("300")
        cal_txt = "—" if (cal_v is None or not sy) else (f"{cal_v:.0f}" + ("?" if cal.get("uncalibrated") else ""))
        cm = r.get("calibrated_moduli") or CAL.calibrated_moduli(r)
        g_txt = f"{m.get('G_GPa', float('nan')):.0f}" + (f" ({cm['G_cal_GPa']:.0f} cal.)" if cm else "")
        notes = r.get("notes") if r.get("notes") is not None else CAL.notes(r)
        lines.append(f"| {i} | {r['formula']} | {new} | {lat} | {r['e_form_eV']:+.3f} | {h.get('de_dec', float('nan')):+.3f} | "
                     f"{float('nan') if dg is None else dg:+.3f} | {h.get('T_star_K') or 0:.0f} | {r['density_gcc']:.2f} | {g_txt} | {m.get('pugh_B_over_G', float('nan')):.2f} | "
                     f"{sy.get('300', 0):.0f} | {sy.get('900', 0):.0f} | {cal_txt} | {s:.1f} | {'; '.join(notes) if notes else ''} |")
    lines += ["", "ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the",
              "model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:",
              "≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to",
              "decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for",
              "ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that",
              "would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would",
              "transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,",
              "precipitates and interstitials would add to it. 'NEW' = no alloy of the reference database within 6 at%",
              "(per element, summed/2); 'n/a' = no reference database was supplied (docs/DATABASE.md).",
              "**σy cal.** (v2, 2026-10-05) = σy read as an annealed handbook yield through the validation's calibration (docs/RESULTS.md,",
              "the calibration table): ÷ the host/solute factor (tin in copper 5.6, zinc or aluminium in copper 1.4, nickel 0.45, silicon 0.4,",
              "molybdenum in nickel 2.35 …; aluminium: 33 MPa + 1.5 × σy), each solute weighted by its share of the strengthening; a '?' means",
              "half or more of the strengthening comes from a solute the table has no factor for (factor 1 used). **G (cal.)** = ×1.45 for",
              "hexagonal zinc and cadmium cells (the PBE shear softness). **notes**: 'soft / unstable cell' (G under 10 GPa or B/G over 8),",
              "'Zn-eq N %: β brass in reality' (Guillet zinc equivalent over 37 % — the fcc cell is not the real alloy), 'Zn-rich on fcc: a",
              "two-phase casting in reality', 'B2-ordered cell' (the random bcc cell was unstable; the row shows the ordered cell the alloy",
              "really is, the random cell's numbers stay in the JSON). The *_cal objectives rank by σy cal. and count a soft cell as unstable.", ""]
    for i, (s, r0) in enumerate(scored[:10], 1):
        r = view(r0)
        h = r.get("hull") or {}
        mix = ", ".join(f"{n} {x:.2f}" for n, x in (h.get("mixture") or [])[:4])
        near = "; ".join(f"{d} {name} ({fam})" for d, rid, name, fam in r["novelty"]["nearest"][:3])
        cal = r.get("calibrated") or CAL.calibrated_yield(r) or {}
        cal_v = (cal.get("sigma_y_cal_MPa") or {}).get("300")
        cal_txt = "" if cal_v is None or not r.get("strength") else f"; σy cal. {cal_v:.0f} MPa (÷ {cal.get('factor')}" + (f" + {cal.get('floor_MPa'):.0f}" if cal.get("floor_MPa") else "") + (f"; uncalibrated {'/'.join(cal['uncalibrated'])}" if cal.get("uncalibrated") else "") + ")"
        lines.append(f"{i}. **{r['formula']}** — wt% {r['wt_pct']}; rules: dH {r['screen']['dH_mix_kJmol']} kJ/mol, δ {r['screen']['delta_pct']} %, Ω {r['screen']['omega']}, VEC {r['screen']['vec']}; "
                     f"would rather be: {mix or '—'}; nearest known: {near or '—'}{cal_txt}")
    unranked = [r for r in results if score(r, objective) is None]            # v2: the cells that fell out, with their notes
    if unranked:
        lines += ["", f"Not ranked ({len(unranked)}: no stable cell, or no strength on this lattice):"]
        for r0 in unranked:
            r = view(r0)
            notes = r.get("notes") if r.get("notes") is not None else CAL.notes(r)
            why = r.get("error") or "; ".join(notes) or ("no yield model for " + str(r.get("lattice")))
            lines.append(f"- {r.get('formula', '?')} — {r.get('lattice_view', r.get('lattice', '?'))}: {why}")
    tmp = out / "DISCOVERIES.md.tmp"
    tmp.write_text("\n".join(lines) + "\n")
    os.replace(tmp, out / "DISCOVERIES.md")
