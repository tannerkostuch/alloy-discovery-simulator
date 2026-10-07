"""calibrate.py — reading the chain's numbers as handbook numbers (2026-10-05, after the validation against 1 214 alloys).

The validation (results/VALIDATION_1214_alloys.md; docs/RESULTS.md, "The calibration table") showed that the
solute-strengthening model ranks by misfit volume too steeply: within one host/solute pair the chain's yield is a
constant multiple of the measured annealed yield (tin in copper ×5.6, zinc or aluminium in copper ×1.4, nickel in
copper ×0.45 …), across pairs it is off by up to ×5. Nothing here changes a computed number — this module adds the
reading next to it:

  calibrated_yield(r)   σy ÷ the factor of the host/solute pair(s), each solute weighted by its share of the model's own
                        strengthening (c·ΔV²), plus the host's floor (aluminium: measured ≈ 33 MPa + 1.5 × model, r 0.96)
  calibrated_moduli(r)  E and G × 1.45 for hexagonal zinc and cadmium cells (the PBE shear softness of zinc, a
                        consistent third low over 16 records after the c/a fix)
  zinc_equivalent(wt)   Guillet's zinc equivalent of a copper alloy (wt%: Si ×10, Al ×6, Sn ×2, Mg ×2, Mn ×0.5, Ni −1.3)
                        — over ~37 % the real alloy is α+β, over ~45 % β, over ~60 % γ-brass, whatever lattice the
                        cell was built on (run 5's Cu58Zn32Al10 and run 9's Cu50Zn25Al17Si8 were fcc cells of β/γ alloys)
  notes(r)              the flags a DISCOVERIES row carries: a soft or unstable cell, a β/γ-brass composition, a zinc-
                        or magnesium-rich alloy that landed on a cubic lattice (a two-phase casting in reality),
                        solutes the table has no factor for

A factor is model ÷ measured (the median over the validation's clean records), so calibrated = model ÷ factor + floor.
Pairs not in the table get factor 1 and the row says "uncalibrated: <solutes>" — a reading, never a silent guess.
"""
import math

# (host, solute) -> model ÷ measured; a dict value keys the factor by the host lattice where that matters
FACTORS = {
    ("Cu", "Sn"): 5.6, ("Cu", "Au"): 1.9, ("Cu", "Al"): 1.4, ("Cu", "Zn"): 1.4, ("Cu", "Ni"): 0.45, ("Cu", "Si"): 0.4,
    # nickel: Mo 2.35 measured; the Ni-Cr-Mo Hastelloys come out 1.5–3.0 as a whole because Mo (and Nb, W — 2.35 by
    # analogy) carry the strengthening; chromium ALONE in nickel is 0.3–0.5 (Nichrome, the Cr-only grades), Monel 0.45
    ("Ni", "Mo"): 2.35, ("Ni", "Cr"): 0.4, ("Ni", "Fe"): 1.3, ("Ni", "Cu"): 0.45, ("Ni", "W"): 2.35, ("Ni", "Nb"): 2.35,
    ("Fe", "Ni"): {"fcc": 1.0}, ("Fe", "Cr"): {"fcc": 0.5}, ("Fe", "Si"): {"bcc": 1.5}, ("Fe", "Mn"): {"fcc": 0.5},
    ("Au", "Cu"): 1.5, ("Au", "Ni"): 2.9, ("Au", "Ag"): 0.85, ("Au", "Pd"): 0.5,
    ("Ag", "Cu"): 0.8,
    ("Pt", "Co"): 3.0, ("Pt", "Ir"): 0.1, ("Pt", "Pd"): 0.1, ("Pt", "Ru"): 0.1, ("Pt", "W"): 0.1,
    ("Ta", "W"): 0.33, ("Mo", "Re"): 0.16, ("W", "Re"): 0.16,
    ("Ti", "V"): {"bcc": 0.4}, ("Ti", "Mo"): {"bcc": 0.08},
}
# hosts with one rule for every solute: (factor, floor MPa) — aluminium: measured ≈ 33 + 1.5 × model (27 wrought
# records, r 0.96; the 33 MPa is grain boundaries, dislocations and the trace Fe/Si below the 0.4 at% cutoff)
HOST_RULES = {"Al": (1 / 1.5, 33.0)}
# hexagonal zinc and cadmium: E and G read a third low (PBE); ×1.45 against polycrystal handbook values (×1.8 vs single crystal)
MODULI_FACTOR = {"Zn": 1.45, "Cd": 1.45}
# Guillet zinc equivalents (wt%), copper alloys
ZN_EQ = {"Zn": 1.0, "Si": 10.0, "Al": 6.0, "Sn": 2.0, "Mg": 2.0, "Pb": 1.0, "Fe": 0.9, "Mn": 0.5, "Ni": -1.3}
HCP_HOSTS = {"Zn", "Cd", "Mg"}          # a cubic cell of one of these at > 60 at% is a two-phase casting in reality, not a solution
SOFT_G_GPA, SOFT_PUGH = 10.0, 8.0       # a cell softer than this (or B/G above this) is unstable in all but name


def factor_for(host, solute, lattice=None):
    f = FACTORS.get((host, solute))
    if isinstance(f, dict):
        return f.get(lattice)
    return f


def calibrated_yield(r):
    """-> {sigma_y_cal_MPa: {T: value}, factor, floor, covered, uncalibrated: [solutes], host} or None when the record
    has no strength. covered = the share of the model's strengthening (Σ c·ΔV²) that has a factor; under 50 % the
    factor is 1 and the row reads as uncalibrated."""
    if not isinstance(r, dict):
        return None
    st = r.get("strength") or {}
    sy = st.get("sigma_y_MPa") or {}
    at = r.get("at") or {}
    if not sy or not at:
        return None
    host = max(at, key=at.get)
    lattice = r.get("lattice")
    if host in HOST_RULES:
        f, floor = HOST_RULES[host]
        weights = {el: 1.0 for el in at if el != host}
        known = dict(weights)
        f_eff, covered, unknown = f, 1.0, []
    else:
        floor = 0.0
        dv = st.get("misfit_volumes_A3") or {}
        weights = {el: at[el] * (dv.get(el, 0.0) ** 2) for el in at if el != host}
        tot = sum(weights.values())
        if tot <= 0:                                           # no misfit at all (pure metal): nothing to calibrate
            weights = {el: at[el] for el in at if el != host}
            tot = sum(weights.values()) or 1.0
        known = {el: w for el, w in weights.items() if factor_for(host, el, lattice) is not None}
        unknown = sorted(el for el in weights if el not in known)
        covered = sum(known.values()) / tot if tot else 0.0
        if covered >= 0.5 and known:
            f_eff = sum(w * factor_for(host, el, lattice) for el, w in known.items()) / sum(known.values())
        else:
            f_eff = 1.0
    out = {"host": host, "factor": round(float(f_eff), 3), "floor_MPa": floor, "covered": round(float(covered), 2),
           "uncalibrated": unknown if covered < 0.5 else [], "sigma_y_cal_MPa": {}}
    for T, v in sy.items():
        out["sigma_y_cal_MPa"][str(T)] = round(float(v) / f_eff + (floor if str(T) == "300" else floor * _floor_scale(T)), 1)
    return out


def _floor_scale(T):
    """the 33 MPa aluminium floor is a room-temperature number; it fades like the solute part does (rough: ∝ 300/T above 300 K)."""
    try:
        T = float(T)
    except (TypeError, ValueError):
        return 1.0
    return 1.0 if T <= 300 else max(0.0, 300.0 / T)


def calibrated_moduli(r):
    """{E_cal_GPa, G_cal_GPa, factor} for hexagonal cells of zinc / cadmium; None otherwise."""
    if not isinstance(r, dict):
        return None
    at = r.get("at") or {}
    m = r.get("elastic") or {}
    if not at or not m or m.get("error"):
        return None
    host = max(at, key=at.get)
    f = MODULI_FACTOR.get(host)
    if f is None or r.get("lattice") != "hcp":
        return None
    return {"factor": f, "E_cal_GPa": round(float(m.get("E_GPa") or 0) * f, 1), "G_cal_GPa": round(float(m.get("G_GPa") or 0) * f, 1)}


def zinc_equivalent(wt):
    """Guillet zinc equivalent (%) of a copper alloy from wt%; None when copper is not the base."""
    if not wt or max(wt, key=wt.get) != "Cu":
        return None
    z = sum(ZN_EQ.get(el, 0.0) * x for el, x in wt.items() if el != "Cu")
    cu = wt.get("Cu", 0.0)
    return 100.0 * z / (cu + z) if (cu + z) > 0 else None


def brass_phase(zn_eq):
    if zn_eq is None:
        return None
    if zn_eq < 37:
        return None                                            # α: the fcc cell is the real thing
    if zn_eq < 45:
        return "α+β"
    if zn_eq < 60:
        return "β"
    return "γ"


def soft_cell(r):
    """True when the elastic step says the cell has (almost) no stiffness: a negative or tiny G, a huge Pugh ratio,
    a failed Born check — the four zinc-rich fcc cells of run 8 (G 3–5, B/G 14–24) read like this."""
    m = r.get("elastic") or {}
    if not m or m.get("error"):
        return False
    g = m.get("G_GPa")
    pugh = m.get("pugh_B_over_G")
    if g is None or (isinstance(g, float) and math.isnan(g)):
        return False
    return bool(g < SOFT_G_GPA or (pugh is not None and pugh > SOFT_PUGH) or not m.get("born_stable", True))


def notes(r):
    """the flags of a DISCOVERIES row, short, in reading order."""
    out = []
    if not isinstance(r, dict):
        return out
    at = r.get("at") or {}
    host = max(at, key=at.get) if at else None
    lat = r.get("lattice")
    if r.get("ordered"):
        o = r["ordered"]
        out.append(f"{o['kind']}-ordered cell ({'stable' if o.get('stable') else 'still unstable'}; the random bcc cell was not)")
    if not (r.get("lattice_check") or {}).get("stable", True):
        out.append("would transform with a free cell")
    if soft_cell(r):
        out.append("soft / unstable cell")
    zq = zinc_equivalent(r.get("wt_pct") or {})
    ph = brass_phase(zq)
    if ph and lat == "fcc":
        out.append(f"Zn-eq {zq:.0f} %: {ph} brass in reality")
    elif ph and lat == "bcc" and ph == "γ":
        out.append(f"Zn-eq {zq:.0f} %: γ brass in reality")
    if host in HCP_HOSTS and lat in ("fcc", "bcc") and at.get(host, 0) > 0.60:
        out.append(f"{host}-rich on {lat}: a two-phase casting in reality")
    cal = calibrated_yield(r)
    if cal and cal.get("uncalibrated"):
        out.append("uncalibrated: " + "/".join(cal["uncalibrated"]) + " in " + cal["host"])
    return out
