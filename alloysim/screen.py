"""screen.py — layer 1: the physics you can do from the composition alone, in milliseconds.

For a composition {element: atomic fraction}:
  dH_mix      enthalpy of mixing (kJ/mol) = Σ 4·dH_ij·c_i·c_j over Miedema's liquid pair table (Takeuchi & Inoue 2005 —
              the table the high-entropy-alloy rules were calibrated on; shipped with matminer)
  dS_mix      ideal configurational entropy, -R Σ c ln c (J/mol K)
  delta       atomic-size mismatch, 100·sqrt(Σ c (1 - r/r̄)²) in %   (Zhang/Yang)
  omega       Tm·dS_mix / |dH_mix|  (Yang & Zhang 2012; Ω ≥ 1.1 and δ ≤ 6.6 % → a solid solution is likely)
  vec         valence electron concentration (Guo, Ng, Lu & Liu 2011: VEC ≥ 8 → FCC, < 6.87 → BCC, between → duplex)
  Rule thresholds checked against the papers by a second model (Grok, 2026-09-29): all confirmed; the
  -22..7 kJ/mol dH window is Guo & Liu 2011's wide one (Zhang 2008: -15..5, see strict()).
  dchi        Pauling electronegativity spread
  tm_mix      rule-of-mixtures melting point (K)
  rho_mix     rule-of-mixtures density from the elements' atomic volumes (g/cm³, rough)
  phase_guess "solid solution" | "intermetallic-prone" | "amorphous-prone", and the lattice guess from VEC
The numbers are the standard empirical design rules of the high-entropy-alloy literature; the atomistic layer then
checks them with real interatomic physics. Also: features for every alloy in the database (run_screen_db.py), which
is how the rules are validated against what is known before they steer a search.
"""
import math
import warnings

import pandas as pd

from .compo import composition, formula
from .elements import info

R_GAS = 8.314462618

_PAIRS = None


def pair_table():
    """{(A, B): dH_AB} — Miedema's liquid-mixing enthalpy of the equiatomic pair in kJ/mol (the table the high-entropy
    literature uses, Takeuchi & Inoue 2005; shipped with matminer as MiedemaLiquidDeltaHf.tsv, 2 628 pairs)."""
    global _PAIRS
    if _PAIRS is not None:
        return _PAIRS
    _PAIRS = {}
    try:
        import matminer.utils.data_files as dfiles
        from pathlib import Path as _P
        path = _P(dfiles.__file__).parent / "MiedemaLiquidDeltaHf.tsv"
        for line in path.read_text().splitlines()[1:]:
            a, b, v = line.split()[:3]
            _PAIRS[(a, b)] = float(v); _PAIRS[(b, a)] = float(v)
    except Exception:  # noqa: BLE001
        pass
    return _PAIRS


def _miedema(at):
    """dH_mix = Σ_{i<j} 4 dH_ij c_i c_j (kJ/mol), the regular-solution sum over the pair table; None if a pair is missing."""
    if len(at) < 2:
        return 0.0
    t = pair_table()
    els = list(at)
    total = 0.0
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            v = t.get((els[i], els[j]))
            if v is None:
                return None
            total += 4.0 * v * at[els[i]] * at[els[j]]
    return total


def features(at):
    """the screening numbers for one composition (atomic fractions)."""
    at = {k: float(v) for k, v in at.items() if v > 0}
    s = sum(at.values()); at = {k: v / s for k, v in at.items()}
    els = [info(k) for k in at]
    cs = [at[k] for k in at]
    rbar = sum(c * e["radius"] for c, e in zip(cs, els))
    delta = 100.0 * math.sqrt(sum(c * (1 - e["radius"] / rbar) ** 2 for c, e in zip(cs, els))) if rbar else None
    ds = -R_GAS * sum(c * math.log(c) for c in cs if c > 0)
    tm = sum(c * (e["tm_k"] or 0) for c, e in zip(cs, els))
    vec = sum(c * (e["vec"] or 0) for c, e in zip(cs, els))
    chibar = sum(c * (e["chi"] or 0) for c, e in zip(cs, els))
    dchi = math.sqrt(sum(c * ((e["chi"] or 0) - chibar) ** 2 for c, e in zip(cs, els)))
    dh = _miedema(at)
    omega = (tm * ds / 1000.0) / abs(dh) if (dh not in (None, 0.0)) else (float("inf") if dh == 0.0 else None)
    # rough density: mass-weighted over atomic volumes from the metallic radius (r → 4/3 π r³ / 0.74 packing)
    vol = sum(c * (4 / 3 * math.pi * (e["radius"] * 1e-8) ** 3 / 0.74) for c, e in zip(cs, els))   # cm³ per atom
    mass = sum(c * e["mass"] for c, e in zip(cs, els)) / 6.02214076e23                                  # g per atom
    rho = mass / vol if vol else None
    price = sum(c * e["price"] for c, e in zip(cs, els))
    # castability: elements that boil not far above the mixture's melting point boil off in the furnace (from Gemini's design review)
    volatile = []
    for k, e in zip(at, els):
        try:
            from pymatgen.core import Element
            bp = Element(k).boiling_point
            if bp and float(bp) < 1.3 * tm:
                volatile.append(k)
        except Exception:  # noqa: BLE001
            pass
    # the rules
    if dh is None or delta is None:
        phase = "unknown"
    elif delta > 8.0 and dh < -10:
        phase = "amorphous-prone"          # big misfit + strong attraction: glass former / brittle compounds
    elif omega is not None and omega >= 1.1 and delta <= 6.6:
        phase = "solid solution"
    elif omega is not None and omega < 1.1:
        phase = "intermetallic-prone"
    else:
        phase = "mixed / segregation-prone" if dh > 5 else "intermetallic-prone"
    lattice = "fcc" if vec >= 8.0 else ("bcc" if vec <= 6.87 else "fcc+bcc")
    return {
        "formula": formula(at), "n_elements": len(at), "dH_mix_kJmol": None if dh is None else round(dh, 2),
        "dS_mix_JmolK": round(ds, 2), "delta_pct": None if delta is None else round(delta, 2),
        "omega": None if omega is None else (round(omega, 2) if omega != float("inf") else 999.0),
        "vec": round(vec, 2), "dchi": round(dchi, 3), "tm_mix_K": round(tm), "rho_mix_gcc": None if rho is None else round(rho, 2),
        "price_class": round(price, 2), "phase_guess": phase, "lattice_guess": lattice, "volatile_elements": volatile,
    }


def features_table(items):
    """[(label, at)] -> DataFrame of features, one row per composition."""
    rows = []
    for label, at in items:
        f = features(at); f["label"] = label; rows.append(f)
    return pd.DataFrame(rows).set_index("label")


def passes(f, omega_min=1.1, delta_max=6.6, dh_range=(-22.0, 7.0)):
    """the solid-solution window: -22 ≤ dH ≤ 7 kJ/mol (the wide window of Guo & Liu 2011), δ ≤ 6.6 %, Ω ≥ 1.1
    (Yang & Zhang 2012). Grok's check (2026-09-29): δ and Ω confirmed; for dH the usual citation is Zhang 2008's
    tighter -15 ≤ dH ≤ 5 — kept the wide window for the funnel (the database check passes with it), and `strict(f)`
    below reports the tight one so a candidate can say which window it sits in."""
    dh, d, o = f.get("dH_mix_kJmol"), f.get("delta_pct"), f.get("omega")
    if dh is None or d is None or o is None:
        return False
    return dh_range[0] <= dh <= dh_range[1] and d <= delta_max and o >= omega_min


def strict(f):
    """Zhang et al. 2008's tighter solid-solution window: -15 ≤ dH_mix ≤ 5 kJ/mol and δ ≤ 6.6 % (Grok's note)."""
    return passes(f, dh_range=(-15.0, 5.0))
