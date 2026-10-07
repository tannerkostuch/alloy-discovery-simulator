"""validate.py — the simulation against a whole database of known alloys (2026-09-30): how robust is the chain on
alloys whose answers are known, before computer time goes into unknown ones?

Every record of the reference database (docs/DATABASE.md; $ALLOYS_DB or data/alloys.json) with a composition the
chain can hold (interstitials C/N/O/H/B/P/S dropped — the cells are substitutional — trace elements under 0.4 at%
dropped, the rest renormalised; families built on non-cubic metals skipped: solders, low-melting Bi/In/Cd alloys,
metallic glasses, uranium) is run and compared with what the database says was measured:

  tier 1  every usable record: the solid solution on its EXPECTED lattice (from family / subfamily / name, with the
          Greek letters spelled out; Bania's Mo-equivalent for titanium and Guillet's Zn-equivalent for brass where the
          record carries no phase word; nickel for the cast stainless grades) and, where the question is real (stainless,
          Ti, Fe-Ni, brass, HEA, "either" cases), the rival lattice  → lattice right or wrong, density error
  tier 2  the records whose measured yield is an annealed/solution-treated solid solution (no precipitates, no
          martensite, no carbides), plus every record with a measured modulus in the families the chain is for
          → elastic constants (E, G, ν) and the solute-strengthening yield
  tier 3  a phase subset: alloys whose known phase story the hull-lite should reproduce (α vs α+β brass, austenitic
          vs ferritic vs duplex stainless, NiTi (B2), γ' superalloys, θ in Al-Cu, Alnico, the HEAs) → hull

One JSON per record under results/validation/tier<N>/<id>.json (resumable, written atomically), and the scorecard
results/validation/VALIDATION.md + validation.csv rebuilt after every result: per family how often the lattice is
right, the density / modulus errors, the yield ratio model:measured, and the worst offenders. What "right" means is
written next to every number — the chain leaves out grain size, precipitates, interstitials and magnetism on purpose,
and the scorecard is meant to show where that bites.

v2.3 (10-02): every stored result is re-compared with the current compare() at each scorecard (v2.2 only did that when
the labels had moved, so the graphite-corrected density reached 5 of 66 cast irons); the family table shows the cast
irons' density error both ways; and the scorecard row of a record is MERGED from its tiers — tier 1 keeps the lattice
verdict and margins (it ran the rival lattice), tier 2 adds moduli and yield, tier 3 the hull — where v2.2 let the
tier-2 result (expected lattice only) overwrite tier 1's, which turned every retained-phase stainless grade that
reached tier 2 into "lowest, margin 0".

v2.4 (2026-10-05, after the backyard runs): E and G get a 'comparable' flag — False for the copper records whose measured
modulus is pure copper's 117 GPa placeholder, the high-entropy records at the 200 GPa placeholder, and the two-phase
castings run as one solution (ZA-27 / Galvalume-type zinc with ≥ 15 at% Al, Al-Si castings) — and the family medians
use only comparable rows; the yield test drops leaded copper (lead is not in solution), the Al-Si castings by
composition, and the zinc family (the Zn-Al alloys are a eutectic). Stored results are re-read under these rules at
every scorecard rebuild (_refresh), nothing is recomputed.
"""
import csv
import json
import math
import os
import re
import statistics
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

from . import atomistic as A
from . import compo
from .search import _dump_json, _load_json, _worker_init, _W, auto_workers, evaluate

RESULTS = Path(__file__).resolve().parent.parent / "results" / "validation"

INTERSTITIAL = {"C", "N", "O", "H", "B", "P", "S"}
NONCUBIC = {"Sn", "Bi", "In", "Cd", "U", "Ga", "Sb", "Pu", "Np", "Si", "Ge", "Se", "Te", "Mn", "Hg", "As", "Tl"}
SKIP_FAMILIES = {"amorphous", "low_melting", "tin_lead_solder"}
ELEMENT_LATTICE = {
    **{e: "fcc" for e in "Al Cu Ni Ag Au Pt Pd Pb Ir Rh Ca Sr Yb".split()},
    **{e: "bcc" for e in "Fe W Mo Ta Nb V Cr Li Na K Ba Eu".split()},
    **{e: "hcp" for e in "Mg Zn Ti Zr Hf Co Re Ru Os Cd Be Sc Y Tc Gd Tb Dy Ho Er Tm Lu".split()},
}
# annealed-like conditions (a solid solution, for the chain's yield) vs everything the chain does not model
ANNEALED = [r"solution[- ]?(anneal|treat)", r"\bannealed?\b", r"\bO\b", r"\bO[- ]temper", r"soft", r"homogeni", r"as[- ]?cast",
            r"hot[- ]?rolled", r"as[- ]?rolled", r"normali", r"\bF\b", r"recrystalli", r"mill[- ]anneal", r"as[- ]?die[- ]?cast",
            r"sand[- ]cast", r"quenched\b(?!.*temper)"]
NOT_ANNEALED = [r"aged", r"\bT[3-9]\d*\b", r"\bH\d", r"hard", r"temper", r"cold", r"drawn", r"spring", r"work", r"rupture",
                r"at \d+ ?°?c", r"carburi", r"nitrid", r"peak", r"precipitat", r"STA\b", r"strain", r"extru", r"forged", r"wire"]


# ------------------------------------------------------------------ what the database says
def clean_composition(at):
    """drop interstitials and traces, renormalise. -> (at, dropped)"""
    dropped = {el: round(x, 4) for el, x in at.items() if el in INTERSTITIAL or x < 0.004}
    keep = {el: x for el, x in at.items() if el not in dropped}
    if not keep:
        return None, dropped
    s = sum(keep.values())
    return {el: x / s for el, x in keep.items()}, dropped


MO_EQ = {"Mo": 1.0, "V": 0.67, "W": 0.44, "Nb": 0.28, "Ta": 0.22, "Fe": 2.9, "Cr": 1.6, "Ni": 1.25, "Mn": 1.7, "Co": 1.7, "Cu": 1.0,
         "Al": -1.0, "Sn": -0.33, "Zr": -0.17}                    # titanium: molybdenum equivalent, wt% (Bania; Al/Sn/Zr as α stabilisers)
ZN_EQ = {"Zn": 1.0, "Si": 10.0, "Al": 6.0, "Sn": 2.0, "Mg": 2.0, "Pb": 1.0, "Fe": 0.9, "Mn": 0.5, "Ni": -1.3}   # copper: Guillet zinc equivalent, wt%


def _wt(at):
    try:
        return compo.at_to_wt(at)
    except Exception:  # noqa: BLE001
        return {}


def _phase_text(rec, notes=False):
    """subfamily + name (+ notes), lower-case, Greek letters spelled out, so 'β alloy', 'near_beta', 'α-β' all read."""
    parts = [rec.get("subfamily") or "", rec.get("name") or ""]
    if notes:
        parts.append((rec.get("composition") or {}).get("notes") or "")
    t = " ".join(parts).lower()
    return t.replace("β", "beta").replace("α", "alpha").replace("γ", "gamma").replace("ε", "epsilon").replace("ω", "omega")


def expected_lattices(rec, at):
    """(expected lattices, the rival worth testing) from family / subfamily / name / composition.
    Two entries in the list = either counts (α+β titanium, duplex stainless, α+β brass, Co-Cr…)."""
    fam = (rec.get("family") or "").lower()
    text = _phase_text(rec)                                        # subfamily + name only: notes talk about 'retained austenite' etc.
    base = max(at, key=at.get)
    ni = at.get("Ni", 0.0)
    wt = _wt(compo.db_record_at(rec) or at)                        # the nominal wt% (traces included) for the equivalents
    if fam in ("aluminium", "precious_metal", "nickel"):
        return ["fcc"], None
    if fam == "copper":
        zn, al, si = wt.get("Zn", 0.0), wt.get("Al", 0.0), wt.get("Si", 0.0)
        if zn < 15:                                                # bronzes: no zinc to speak of — Guillet does not apply
            if al >= 9.5:
                return ["fcc", "bcc"], None                        # aluminium bronzes above ~9.5 wt% Al: α + β/κ
            return ["fcc"], "bcc" if (al >= 7 or si >= 4) else None  # α bronzes (Al-Si, Si, Sn, Ni…)
        if si >= 2.5:                                              # silicon brasses (EcoBrass, Tombasil): α + κ
            return ["fcc", "bcc"], None
        zn_eq = sum(ZN_EQ.get(el, 0.0) * w for el, w in wt.items())   # brasses: Guillet's zinc equivalent decides α / α+β / β
        if zn_eq >= 48:
            return ["bcc"], "fcc"                                  # β brass / manganese bronze (scored as retained: B2-ordered in reality)
        if zn_eq >= 37.5:
            return ["fcc", "bcc"], None
        return ["fcc"], "bcc" if zn_eq >= 30 else None
    if fam == "stainless_steel":
        if "duplex" in text:
            return ["fcc", "bcc"], None
        if "semi-austenit" in text:                                # 17-7 PH, AM-350…: austenite conditioned to martensite
            return ["bcc", "fcc"], None
        if "austenit" in text:
            return ["fcc"], "bcc"
        if re.search(r"martensit|ferrit|\bph\b|precipitation|hardening|knife|cutlery|secondary", text):
            return ["bcc"], "fcc"
        return (["fcc"], "bcc") if ni >= 0.07 else (["bcc"], "fcc")   # cast ACI / H-series grades carry no phase word: Ni ≥ ~8 wt% is austenitic
    if fam == "cast_iron":
        if "austenit" in text or "ni-resist" in text or "ni_resist" in text:
            return ["fcc"], "bcc"                                  # Ni-Resist: austenite held by Ni + carbon (the carbon is dropped here)
        return ["bcc"], "fcc" if ni > 0.15 else None
    if fam in ("steel", "tool_steel"):
        if re.search(r"austenitic|hadfield|twip", text) or (at.get("Mn", 0) > 0.10 and "mn" in text):
            return ["fcc"], "bcc"
        return ["bcc"], "fcc" if ni > 0.15 else None
    if fam == "magnetic_electrical":
        if base == "Fe":
            return (["fcc"], "bcc") if ni >= 0.25 else (["bcc"], "fcc")
        if base in ("Ni", "Cu"):
            return ["fcc"], "bcc" if base == "Ni" and at.get("Fe", 0) > 0.2 else None
        if base == "Co":
            return ["hcp", "fcc"], None
    if fam == "refractory":
        return [ELEMENT_LATTICE.get(base, "bcc")], None
    if fam == "titanium":
        if re.search(r"aluminide|tial|ti3al|ti2alnb", text):        # the intermetallics: γ-TiAl is L1₀ (fcc-based) with α₂ (hcp-based) beside it
            if "ti2alnb" in text or "orthorhombic" in text:
                return ["hcp", "bcc"], None
            return (["fcc", "hcp"], None) if at.get("Al", 0) >= 0.40 else (["hcp"], "bcc")
        mo_eq = sum(MO_EQ.get(el, 0.0) * w for el, w in wt.items())
        if re.search(r"near[ _-]?alpha|commercially pure|\bcp\b|cp_alpha|alpha alloy|alpha \(|\(alpha\)", text) and "beta" not in text:
            return ["hcp"], "bcc"
        if re.search(r"alpha[ _-]?(\+|-|_)?[ _]?beta|alpha_beta|beta-rich|beta rich|alpha \/ alpha-beta", text) or ("alpha" in text and "beta" in text):
            return ["hcp", "bcc"], None                            # α+β: either lattice is a fair answer for a solid-solution proxy
        if "beta" in text:
            return ["bcc"], "hcp"                                  # β / near-β / metastable β
        if mo_eq >= 7.0:                                           # no phase word (e.g. 'ultra-high strength landing gear alloy'): Bania's Mo-eq
            return ["bcc"], "hcp"
        if mo_eq >= 3.0:
            return ["hcp", "bcc"], None
        return ["hcp"], "bcc"
    if fam == "magnesium":
        return ["hcp"], None
    if fam == "zinc":
        return (["hcp", "fcc"], None) if at.get("Al", 0) > 0.2 else (["hcp"], None)
    if fam == "cobalt":
        return ["hcp", "fcc"], None
    if fam == "high_entropy":
        t2 = _phase_text(rec, notes=True)
        if "bcc" in t2 and "fcc" not in t2:
            return ["bcc"], "fcc"
        if "fcc" in t2 and "bcc" not in t2:
            return ["fcc"], "bcc"
        if "hcp" in t2:
            return ["hcp"], "fcc"
        return ["fcc", "bcc"], None
    if fam == "shape_memory":
        if base in ("Ni", "Ti") and at.get("Ti", 0) > 0.3:
            return ["bcc"], ("fcc" if ni >= 0.3 else "hcp")       # NiTi: B2 = ordered bcc; Ti-Nb: β
        return ["bcc", "fcc"], None                                # Cu-based β SMAs are metastable bcc; Fe-Mn-Si is γ
    if fam == "uranium_zirconium_nuclear":
        return [ELEMENT_LATTICE.get(base, "hcp")], "bcc" if base in ("Zr", "Hf", "Ti") else None
    L = ELEMENT_LATTICE.get(base)
    return ([L], None) if L else (None, None)


def retained_phase(rec, at, expected):
    """True when the alloy's real phase is a HIGH-temperature phase kept by quenching or by an element the cell cannot hold
    (austenitic stainless with < 25 at% Ni, β-Ti, Hadfield / TWIP steel, Ni-Resist austenite held by carbon, the B2 / β of
    the NiTi and Ti-Nb shape-memory alloys): at 0 K the model may rightly put another lattice lower — what counts then is
    the margin, not a right/wrong. Two-lattice expectations (α+β, duplex, Co-Cr) are never 'retained': either lattice counts."""
    fam = (rec.get("family") or "").lower()
    if len(expected) != 1:
        return False
    if fam == "stainless_steel" and expected == ["fcc"]:
        return at.get("Ni", 0) < 0.25
    if fam == "titanium" and expected == ["bcc"]:
        return True
    if fam in ("steel", "tool_steel", "cast_iron") and expected == ["fcc"]:
        return True
    if fam == "shape_memory":
        return True
    if fam == "copper" and expected == ["bcc"]:
        return True                                                # β brass: B2-ordered + entropy; the disordered bcc cell is a proxy
    if fam == "magnetic_electrical" and expected == ["fcc"] and max(at, key=at.get) == "Fe" and at.get("Ni", 0) < 0.40:
        return True                                                # Invar / Kovar / Super Invar: austenite held by magnetism, which the model lacks
    return False


def yield_from_record(rec):
    """(yield MPa, condition) of the most solid-solution-like entry, or (None, why)."""
    best = None
    for m in (rec.get("properties") or {}).get("mechanical") or []:
        if not m or not m.get("yield_strength_mpa"):
            continue
        cond = str(m.get("condition") or "")
        if any(re.search(p, cond, re.I) for p in NOT_ANNEALED):
            continue
        rank = next((i for i, p in enumerate(ANNEALED) if re.search(p, cond, re.I)), None)
        if rank is None:
            continue
        if best is None or rank < best[0]:
            best = (rank, float(m["yield_strength_mpa"]), cond)
    if best is None:
        return None, "no annealed/solution-treated entry"
    return best[1], best[2]


def yield_is_solid_solution(rec, at):
    """is the annealed yield of this record a solid solution the chain models? (no carbides, precipitates, martensite)"""
    fam = (rec.get("family") or "").lower()
    text = _phase_text(rec)
    if fam in ("steel", "tool_steel", "cast_iron"):
        return False                                           # ferrite + pearlite/carbides: carbon does the work
    if fam == "copper" and at.get("Pb", 0) >= 0.005:
        return False                                           # v2.4: leaded brass/bronze — lead is not in solution (ratios 6–11 were that)
    if fam == "aluminium" and at.get("Si", 0) >= 0.02:
        return False                                           # v2.4: Al-Si castings — eutectic silicon carries the strength
    if fam == "zinc":
        return False                                           # v2.4: the Zn-Al alloys are a eutectic; no solid-solution yield to compare
    if fam == "stainless_steel":
        return "austenit" in text and "duplex" not in text and "ph" not in text.split()
    if fam == "nickel":
        return not any(k in text for k in ("superalloy", "gamma", "γ", "718", "waspaloy", "rené", "rene", "udimet", "x-750", "hastelloy c-276", "precipitation"))
    if fam == "aluminium":
        return not any(k in text for k in ("2xxx", "6xxx", "7xxx", "2024", "6061", "7075", "cast a3", "a356", "silicon"))  # O-temper 1xxx/3xxx/5xxx only
    if fam in ("copper", "precious_metal", "refractory", "magnesium", "zinc", "magnetic_electrical", "high_entropy"):
        return True
    if fam == "titanium":
        return "alpha" not in text or "cp" in text or "commercially pure" in text or "grade" in text
    return False


def select(db_path=compo.DB_FINAL, families=None, ids=None):
    """the records the chain can be tested on. -> list of dicts (see below) + the skipped list with reasons."""
    data = json.loads(Path(db_path).read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data.get("alloys") or data.get("records") or list(data.values())
    out, skipped = [], []
    for rec in recs:
        if not isinstance(rec, dict):
            continue
        rid, fam = rec.get("id"), (rec.get("family") or "")
        if families and fam not in families:
            continue
        if ids and rid not in ids:
            continue
        raw = compo.db_record_at(rec)
        if not raw:
            skipped.append((rid, "no composition")); continue
        if fam in SKIP_FAMILIES:
            skipped.append((rid, f"family {fam}: not a crystalline solid solution")); continue
        nm = rec.get("name") or ""
        if re.search(r"bimetal|cermet|cemented carbide|composite|metal matrix|\bmmc\b|\bclad\b|dumet", nm.lower()):
            skipped.append((rid, "composite record (two materials), not an alloy")); continue
        if re.search(r"quasicrystal|intermetallic|dispersion fuel|master alloy|precursor|hydride|grain refiner|modifier|"
                     r"Nd2Fe14B|SmCo5|Sm2Co17|AuAl2|AuIn2|U3Si2|Mg2Ni|LaNi5|\bTiFe\b|Fe3Al|Ni3Al|Cu2MnAl|Nb3Sn|MnBi|Al-Cu-Fe|Raney|Cu-15P|phosphor copper", nm, re.I) \
                and fam not in ("high_entropy",):
            skipped.append((rid, "compound / intermetallic record, not a solid solution")); continue
        if re.search(r"\balloys\b|\bSMAs\b", nm):
            skipped.append((rid, "group record (several alloys in one), composition is a blend")); continue
        at, dropped = clean_composition(raw)
        if not at:
            skipped.append((rid, "nothing left after dropping interstitials")); continue
        base = max(at, key=at.get)
        if base in NONCUBIC or any(x >= 0.10 and el in NONCUBIC for el, x in at.items()):
            skipped.append((rid, f"non-cubic metal {base if base in NONCUBIC else [e for e in at if e in NONCUBIC]}")); continue
        if len(at) > 8:
            skipped.append((rid, f"{len(at)} elements after cleaning — cell too small to hold them")); continue
        exp, rival = expected_lattices(rec, at)
        if not exp:
            skipped.append((rid, f"no expected lattice for base {base}")); continue
        p = rec.get("properties") or {}
        y, ycond = yield_from_record(rec)
        out.append({
            "id": rid, "name": rec.get("name"), "family": fam, "subfamily": rec.get("subfamily"), "base": base,
            "at": at, "dropped": dropped, "formula": compo.formula(at, 1),
            "expected": exp, "rival": rival, "retained": retained_phase(rec, at, exp),
            "measured": {"density_gcc": p.get("density_g_cm3"), "E_GPa": p.get("youngs_modulus_gpa"),
                         "G_GPa": p.get("shear_modulus_gpa"), "nu": p.get("poissons_ratio"),
                         "yield_MPa": y, "yield_condition": ycond, "yield_is_solid_solution": bool(y and yield_is_solid_solution(rec, at))},
        })
    return out, skipped


def tier_subset(records, tier):
    if tier == 1:
        return records
    if tier == 2:                                                  # the ~400 records whose annealed yield is a solid solution
        return [r for r in records if r["measured"]["yield_is_solid_solution"]]
    if tier == 3:                                                  # the phase stories the hull-lite should reproduce (~60)
        keys = ("c26000", "c27200", "c28000", "muntz", "naval brass", "c36000", "c51000", "phosphor bronze", "c95400", "aluminum bronze",
                "aluminium bronze", "c70600", "c71500", "cupronickel", "c17200", "beryllium copper", "nickel silver",
                "ss-304", "ss-316", "ss-430", "ss-2205", "ss-410", "ss-17-4", "duplex 2205",
                "nitinol", "inconel-718", "inconel-625", "inconel-600", "waspaloy", "x-750", "monel-400", "hastelloy-c-276", "nichrome",
                "al-2024", "al-2017", "al-6061", "al-7075", "al-5083", "al-3003", "al-a356",
                "alnico", "invar-36", "kovar", "permalloy", "constantan", "manganin", "mu-metal", "hiperco",
                "ti-6al-4v", "ti-15mo", "ti-13v-11cr-3al", "ti-10v-2fe-3al", "grade-2", "tzm", "w-re", "nb-1zr",
                "az31", "az91", "zamak", "sterling", "coin silver", "18k", "14k", "platinum-iridium")
        return [r for r in records if r["family"] == "high_entropy" or
                any(k in (r["id"] + " " + (r["name"] or "")).lower() for k in keys)]
    raise ValueError(tier)


# ------------------------------------------------------------------ running it
def _complete(j, rec, tier):
    """does a stored result hold every lattice the CURRENT mapping asks of it? (the mapping was corrected on 2026-09-30
    while tier 1 ran: β-brass, the cast austenitic grades and the β-Ti alloys changed; a tier-1 record whose stored
    cells miss a lattice it now needs is run again — tiers 2 and 3 only ever run the expected lattices)"""
    if j.get("compare", {}).get("error"):
        return True                                            # an error is an error; rerunning it is a --force job
    cells = (j.get("model") or {}).get("cells") or {}
    need = list(rec["expected"]) + ([rec["rival"]] if tier == 1 and rec.get("rival") else [])
    return all(L in cells for L in need) if cells else True


def _worker_validate(rec, tier, target_atoms):
    t0 = time.time()
    lattices = list(rec["expected"]) + ([rec["rival"]] if rec["rival"] and rec["rival"] not in rec["expected"] else [])
    if tier > 1:
        lattices = list(rec["expected"])                       # the rival question was tier 1's; moduli/yield of the REAL phase here
    if tier == 1:
        r = evaluate(_W["engine"], rec["at"], lattices=lattices, target_atoms=target_atoms, seeds=(0,),
                     do_elastic=False, do_hull=False, do_check=False, log=lambda *a, **k: None)
    elif tier == 2:
        r = evaluate(_W["engine"], rec["at"], lattices=lattices, target_atoms=target_atoms, seeds=(0,),
                     do_elastic=True, do_hull=False, do_check=True, log=lambda *a, **k: None)
    else:
        r = evaluate(_W["engine"], rec["at"], lattices=lattices, target_atoms=target_atoms, seeds=(0,),
                     do_elastic=True, do_hull=True, do_check=True, log=lambda *a, **k: None)
    return rec["id"], r, round(time.time() - t0)


GRAPHITE_A3 = 12.011 / (2.26 * 0.6022)                          # Å³ per carbon atom in graphite (2.26 g/cc)


def _density_with_graphite(rec, rho_cell):
    """cast irons: the carbon dropped from the cell is graphite in the real casting (grey, ductile, compacted, malleable,
    Ni-Resist, ADI) — put it back as graphite volume and mass; the other dropped atoms as mass only (interstitial).
    -> g/cc, or None when it does not apply (white irons: the carbon is cementite, not modelled here)."""
    if (rec.get("family") or "") != "cast_iron" or not rec.get("dropped"):
        return None
    text = _phase_text(rec)
    if "white" in text or "ni-hard" in text or "ni_hard" in text or "high-chromium" in text or "high_chromium" in text or "duriron" in text:
        return None
    try:
        from .elements import info
        at, dropped = rec["at"], rec["dropped"]
        kept = 1.0 - sum(dropped.values())                       # kept atoms per raw atom
        m_cell = sum(x * info(el)["mass"] for el, x in at.items())    # g/mol per cell atom
        v_cell = m_cell / (rho_cell * 0.6022)                    # Å³ per cell atom
        mass = kept * m_cell + sum(d * info(el)["mass"] for el, d in dropped.items())
        vol = kept * v_cell + dropped.get("C", 0.0) * GRAPHITE_A3
        return mass / (vol * 0.6022)
    except Exception:  # noqa: BLE001
        return None


def moduli_comparable(rec, m):
    """v2.4: is the record's measured E/G a real measurement of the phase the chain ran? -> (bool, why)."""
    fam, at = (rec.get("family") or "").lower(), rec.get("at") or {}
    base = max(at, key=at.get) if at else None
    if fam == "copper" and m.get("E_GPa") == 117 and at.get("Cu", 0) < 0.995:
        return False, "E = 117 GPa is pure copper's value, a placeholder in the database"
    if fam == "high_entropy" and m.get("E_GPa") == 200:
        return False, "E = 200 GPa placeholder"
    if fam == "zinc" and at.get("Al", 0) >= 0.15:
        return False, "two-phase Zn-Al casting (ZA-27 / Galvalume type) run as one solution"
    if fam == "aluminium" and at.get("Si", 0) >= 0.04:
        return False, "Al-Si casting (eutectic silicon) run as one solution"
    if base == "Pb" or at.get("Pb", 0) >= 0.02:
        return False, "lead is not in solution"
    return True, ""


def compare(rec, r, tier=1):
    """the model against the record -> dict of errors (None where not comparable)."""
    m = rec["measured"]
    cells = r.get("cells") or {}
    need = list(rec["expected"]) + ([rec["rival"]] if tier == 1 and rec.get("rival") else [])
    tested = all(L in cells for L in need) if cells else True     # a result from an older mapping may lack a lattice the new one asks for
    c = {"lattice_model": r.get("lattice"), "lattice_expected": rec["expected"],
         "lattice_ok": ((r.get("lattice") in rec["expected"]) if (r.get("lattice") and tested) else None),
         "lattice_margin_meV": {k: round(1000 * v) for k, v in (r.get("lattice_margin_eV") or {}).items()}}
    if not tested:
        c["not_tested"] = [L for L in need if L not in cells]
    exp_cell = cells.get(r.get("lattice")) if r.get("lattice") in rec["expected"] else next((cells[L] for L in rec["expected"] if L in cells), None)
    if exp_cell and m.get("density_gcc"):                        # the density of the phase the alloy really has
        c["density_err_pct"] = round(100 * (exp_cell["density_gcc"] / m["density_gcc"] - 1), 1)
        rho_g = _density_with_graphite(rec, exp_cell["density_gcc"])
        if rho_g:
            c["density_err_graphite_pct"] = round(100 * (rho_g / m["density_gcc"] - 1), 1)
    if r.get("density_gcc") and m.get("density_gcc") and r.get("lattice") not in rec["expected"]:
        c["density_err_model_lattice_pct"] = round(100 * (r["density_gcc"] / m["density_gcc"] - 1), 1)
    el = r.get("elastic") or {}
    if el.get("E_GPa") and m.get("E_GPa"):
        c["E_err_pct"] = round(100 * (el["E_GPa"] / m["E_GPa"] - 1), 1)
    if el.get("G_GPa") and m.get("G_GPa"):
        c["G_err_pct"] = round(100 * (el["G_GPa"] / m["G_GPa"] - 1), 1)
    if "E_err_pct" in c or "G_err_pct" in c:
        c["moduli_comparable"], c["moduli_note"] = moduli_comparable(rec, m)       # v2.4
    if el.get("nu") is not None and m.get("nu"):
        c["nu_model"], c["nu_measured"] = round(float(el["nu"]), 3), m["nu"]
    s = (r.get("strength") or {}).get("sigma_y_MPa") or {}
    if s.get("300") is not None and m.get("yield_MPa"):
        c["yield_model_MPa"] = round(float(s["300"]))
        c["yield_measured_MPa"] = m["yield_MPa"]
        c["yield_ratio"] = round(float(s["300"]) / m["yield_MPa"], 2)
        c["yield_comparable"] = m["yield_is_solid_solution"]
    h = r.get("hull") or {}
    if h.get("de_dec") is not None:
        c["de_dec_meV"] = round(1000 * h["de_dec"]); c["T_star_K"] = round(h.get("T_star_K") or 0); c["would_rather_be"] = h.get("mixture", [])[:4]
    return c


def run_tier(engine, tier, records, target_atoms=108, workers=0, log=print, limit=None):
    out = RESULTS / f"tier{tier}"
    out.mkdir(parents=True, exist_ok=True)
    todo = []
    n_cached = 0
    for rec in records[: limit or None]:
        p = out / f"{rec['id']}.json"
        j = _load_json(p)
        if j is not None and _complete(j, rec, tier):
            n_cached += 1
            continue
        if p.exists():
            p.unlink(missing_ok=True)
        todo.append(rec)
    workers = workers or auto_workers(engine)
    log(f"[validate] tier {tier}: {len(records)} records, {n_cached} done already, {len(todo)} to run on {workers} workers")
    if not todo:
        write_scorecard(log=log)
        return out
    pool_els = sorted({el for rec in todo for el in rec["at"]})
    for el in pool_els:                                            # elemental references once, in this process
        try:
            engine.ground(el)
        except Exception as e:  # noqa: BLE001
            log(f"[validate] reference {el} failed: {e}")
    threads = max(1, (os.cpu_count() or 4) // workers)
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn"), initializer=_worker_init,
                             initargs=(engine.spec, threads)) as ex:
        futs = {ex.submit(_worker_validate, rec, tier, target_atoms): rec for rec in todo}
        for fut in as_completed(futs):
            rec = futs[fut]
            done += 1
            try:
                _, r, secs = fut.result()
            except Exception as e:  # noqa: BLE001
                r = {"formula": rec["formula"], "error": f"{e.__class__.__name__}: {e}", "seconds": 0}
            r.pop("novelty", None)
            result = {"record": rec, "tier": tier, "model": r, "compare": compare(rec, r, tier) if not r.get("error") else {"error": r["error"]}}
            _dump_json(out / f"{rec['id']}.json", result)
            c = result["compare"]
            log(f"[{done}/{len(todo)}] {rec['id']} ({rec['family']}) {rec['formula']}: " +
                (f"ERROR {c['error'][:80]}" if c.get("error") else
                 f"{c['lattice_model']} {'✓' if c['lattice_ok'] else '✗ expected ' + '/'.join(rec['expected'])} | ρ {c.get('density_err_pct', float('nan')):+.1f} %"
                 + (f" | E {c['E_err_pct']:+.0f} %" if "E_err_pct" in c else "")
                 + (f" | σy {c['yield_model_MPa']} vs {c['yield_measured_MPa']:.0f} ({rec['measured']['yield_condition']})" if "yield_ratio" in c else ""))
                + f"  [{r.get('seconds', 0)} s, {(time.time()-t0)/60:.0f} min]")
            if done % 5 == 0 or done == len(todo):
                write_scorecard(log=lambda *a, **k: None)
    engine.refresh()
    write_scorecard(log=log)
    return out


# ------------------------------------------------------------------ the scorecard
def _current_records():
    """id -> record from the database under the CURRENT expected-lattice mapping (cached per process)."""
    if "recs" not in _W:
        try:
            _W["recs"] = {r["id"]: r for r in select()[0]}
        except Exception:  # noqa: BLE001
            _W["recs"] = {}
    return _W["recs"]


def _refresh(j, p):
    """re-label a stored result with the current mapping (expected / rival / retained / measured) and recompute the
    comparison from the stored model result with the current compare(); the file is rewritten only when something
    changed (v2.3: the comparison is always recomputed, not only when the labels moved — v2.2 left the 61 cast irons
    whose labels had not changed without the graphite-corrected density)."""
    cur = _current_records().get(j["record"]["id"])
    if not cur:
        return j
    keys = ("expected", "rival", "retained")
    changed = not (all(j["record"].get(k) == cur.get(k) for k in keys) and j["record"].get("measured") == cur.get("measured"))
    if changed:
        rec = dict(j["record"]); rec.update({k: cur[k] for k in keys}); rec["measured"] = cur["measured"]
        j["record"] = rec
    if not j["compare"].get("error"):
        new = compare(j["record"], j["model"], j.get("tier", 1))
        if new != j["compare"]:
            j["compare"] = new
            changed = True
    if changed:
        try:
            _dump_json(p, j)
        except Exception:  # noqa: BLE001
            pass
    return j


LATTICE_KEYS = ("lattice_model", "lattice_expected", "lattice_ok", "lattice_margin_meV", "not_tested",
                "density_err_pct", "density_err_graphite_pct", "density_err_model_lattice_pct")


def _merge_tiers(by_tier):
    """one row per record from its tier-1/2/3 results. Tier 1 owns the lattice contest and the density — it is the
    only tier that ran the rival lattice (v2.2 let the higher tier supersede the whole row, so every record that
    reached tier 2 read "lattice right, margin 0" whatever tier 1 had found); tier 2 adds the moduli and the yield,
    tier 3 the hull. The record labels come from the highest tier (all are refreshed to the current mapping)."""
    ok = {t: j for t, j in by_tier.items() if not j["compare"].get("error")}
    if not ok:
        return by_tier[max(by_tier)]
    base = json.loads(json.dumps(ok[min(ok)]))                       # a copy: the lowest clean tier, normally tier 1
    base["tier"] = max(by_tier)
    for t in sorted(ok):
        if t == min(ok):
            continue
        hi = ok[t]
        for k in ("elastic", "strength", "hull", "lattice_check", "sfe"):
            if k in hi["model"] and k not in base["model"]:
                base["model"][k] = hi["model"][k]
        for k, v in hi["compare"].items():
            if k not in LATTICE_KEYS and k not in base["compare"]:
                base["compare"][k] = v
        base["model"]["seconds"] = (base["model"].get("seconds") or 0) + (hi["model"].get("seconds") or 0)
    return base


def _load_all():
    found = {}
    for tier in (1, 2, 3):
        d = RESULTS / f"tier{tier}"
        if not d.is_dir():
            continue
        for p in d.glob("*.json"):
            j = _load_json(p)
            if j is None:
                continue
            j = _refresh(j, p)
            rid = j["record"]["id"]
            if _current_records() and rid not in _current_records():
                continue                                           # no longer selected under the current rules (a composite record, say)
            found.setdefault(rid, {})[tier] = j
    return [_merge_tiers(bt) for bt in found.values()]


def _median(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return statistics.median(xs) if xs else None


def _fmt(x, unit="", digits=0):
    return "—" if x is None else f"{x:+.{digits}f}{unit}" if unit == " %" else f"{x:.{digits}f}{unit}"


def write_scorecard(log=print):
    rows = _load_all()
    if not rows:
        return
    RESULTS.mkdir(parents=True, exist_ok=True)
    fams = sorted({j["record"]["family"] for j in rows})
    lines = [f"# The simulation against the alloys database — scorecard ({len(rows)} alloys so far, {time.strftime('%Y-%m-%d %H:%M')})", "",
             "Every usable record of the reference database run through the same chain as the discovery runs (tier 1: the solid solution on",
             "its expected lattice, and the rival lattice where it matters; tier 2: elastic constants and the solute-strengthening yield;",
             "tier 3: the hull) and compared with the measured values in the database. **lattice right** = the lattice the record",
             "implies came out lowest in energy (where the record implies two — α+β titanium, duplex stainless, α+β brass, Co-Cr —",
             "either counts); quenched-in phases (austenitic stainless, β-Ti…) are counted separately below, because at 0 K the model",
             "may rightly prefer the low-temperature lattice. **ρ** = model density of the real phase vs measured (the model has no",
             "interstitials and no porosity). **E, G** = model (0 K, single crystal averaged) vs measured room-temperature moduli.",
             "**σy ratio** = the chain's solute-strengthening yield ÷ the measured annealed yield, only for records whose annealed state",
             "is a solid solution — the chain leaves out grain-boundary, precipitate, carbide and interstitial strengthening on purpose,",
             "so a ratio well under 1 is expected wherever those carry the load; the point is how consistent the ratio is within a family.",
             "(v2.4) The E/G medians leave out records whose measured modulus is a placeholder (copper alloys at pure copper's 117 GPa,",
             "high-entropy alloys at 200) and two-phase castings run as one solution (ZA-27-type zinc, Al-Si); n = rows counted. The yield",
             "test leaves out leaded copper, Al-Si castings and the zinc eutectics. validation.csv carries the flags (moduli_comparable).",
             "", "| family | n | lattice right | median ρ error | median E error | median G error | σy ratio (median, n) | worst σy ratio |",
             "|---|---|---|---|---|---|---|---|"]
    csv_rows = []
    for fam in fams + ["ALL"]:
        js = [j for j in rows if fam == "ALL" or j["record"]["family"] == fam]
        cs = [j["compare"] for j in js if not j["compare"].get("error")]
        lat = [c["lattice_ok"] for j, c in zip([j for j in js if not j["compare"].get("error")], cs) if c.get("lattice_ok") is not None and not j["record"].get("retained")]
        ratios = [c["yield_ratio"] for c in cs if c.get("yield_ratio") is not None and c.get("yield_comparable")]
        lat_txt = f"{sum(lat)}/{len(lat)} ({100*sum(lat)/len(lat):.0f} %)" if lat else "—"
        rho = _median([abs(c["density_err_pct"]) for c in cs if "density_err_pct" in c])
        rho_g = _median([abs(c["density_err_graphite_pct"]) for c in cs if "density_err_graphite_pct" in c])   # cast irons, carbon back as graphite
        E = _median([c["E_err_pct"] for c in cs if "E_err_pct" in c and c.get("moduli_comparable", True)])   # v2.4: placeholders and two-phase castings out
        G = _median([c["G_err_pct"] for c in cs if "G_err_pct" in c and c.get("moduli_comparable", True)])
        nE = sum(1 for c in cs if "E_err_pct" in c and c.get("moduli_comparable", True))
        rm = _median(ratios)
        worst = None
        if ratios:
            worst = min(ratios, key=lambda x: -abs(math.log(max(x, 1e-6))))
        rho_txt = "—" if rho is None else f"{rho:.1f} %" + (f" ({rho_g:.1f} % with graphite)" if rho_g is not None and fam != "ALL" else "")
        lines.append(f"| {'**all**' if fam == 'ALL' else fam} | {len(js)} | {lat_txt} | {rho_txt} | "
                     f"{_fmt(E, ' %', 0)}{'' if E is None else f' (n={nE})'} | {_fmt(G, ' %', 0)} | {_fmt(rm, '', 2)}{'' if rm is None else f' (n={len(ratios)})'} | {_fmt(worst, '', 2)} |")
    # retained high-temperature phases: the margin is the result, not a right/wrong
    ret = [j for j in rows if j["record"].get("retained") and j["compare"].get("lattice_model")]
    if ret:
        n_ok = sum(1 for j in ret if j["compare"]["lattice_ok"])
        lines += ["", f"## Retained high-temperature phases ({len(ret)}: austenitic stainless under 25 at% Ni, β-Ti, Hadfield/TWIP, Ni-Resist, NiTi / Ti-Nb β)", "",
                  "These are quenched-in phases; at 0 K the model may put the low-temperature lattice lower, as the real phase diagram does.",
                  f"The model keeps the retained lattice lowest in {n_ok} of {len(ret)}; where it does not, the margin says how far the",
                  "retained phase sits above (a few tens of meV/atom is the normal price of a metastable phase, hundreds would be a model error).", "",
                  "| alloy | family | retained phase | model's lowest | margin of the retained phase (meV/atom) |", "|---|---|---|---|---|"]
        for j in sorted(ret, key=lambda j: (j["record"]["family"], j["record"]["name"] or "")):
            c, rec = j["compare"], j["record"]
            marg = c.get("lattice_margin_meV") or {}
            above = "0 (lowest)" if c["lattice_ok"] else ", ".join(f"{k} +{v}" for k, v in marg.items() if k in rec["expected"]) or "?"
            lines.append(f"| {rec['name']} | {rec['family']} | {'/'.join(rec['expected'])} | {c['lattice_model']} | {above} |")
    # the failures and the worst offenders
    wrong = [j for j in rows if j["compare"].get("lattice_ok") is False and not j["record"].get("retained")]
    lines += ["", f"## Lattice wrong ({len(wrong)}, retained phases not counted)", ""]
    if wrong:
        lines.append("| alloy | family | expected | model | margin (meV/atom) | note |"); lines.append("|---|---|---|---|---|---|")
        for j in sorted(wrong, key=lambda j: j["record"]["family"]):
            c, rec = j["compare"], j["record"]
            lines.append(f"| {rec['name']} | {rec['family']} | {'/'.join(rec['expected'])} | {c['lattice_model']} | {c.get('lattice_margin_meV')} | {j['model'].get('lattice_check', {}).get('stable', '')} |")
    else:
        lines.append("none so far")
    nt = [j for j in rows if j["compare"].get("not_tested")]
    if nt:
        lines += ["", f"## Not yet tested on the lattice the corrected mapping expects ({len(nt)})", "",
                  "The expected-lattice rules were corrected while tier 1 ran (β-brass by zinc equivalent, cast austenitic grades by",
                  "nickel, β-Ti by name and Mo-equivalent); these results lack a lattice the new rule asks for and are run again at the end.", ""]
        lines += [f"- {j['record']['name']} ({j['record']['family']}): expected {'/'.join(j['record']['expected'])}, stored {', '.join((j['model'].get('cells') or {}).keys())}" for j in nt[:40]]
    bad_rho = sorted([j for j in rows if abs(j["compare"].get("density_err_pct", 0)) > 3], key=lambda j: -abs(j["compare"]["density_err_pct"]))
    lines += ["", f"## Density off by more than 3 % ({len(bad_rho)})", ""]
    gi = [j["compare"]["density_err_graphite_pct"] for j in rows if "density_err_graphite_pct" in j["compare"]]
    if gi:
        lines += [f"Cast irons with the dropped carbon put back as graphite (2.26 g/cc): median error {_median([abs(x) for x in gi]):.1f} % over {len(gi)} "
                  "(white irons excluded — their carbon is cementite).", ""]
    for j in bad_rho[:25]:
        rec, c = j["record"], j["compare"]
        lines.append(f"- {rec['name']} ({rec['family']}): {c['density_err_pct']:+.1f} %" + (f" (with graphite {c['density_err_graphite_pct']:+.1f} %)" if "density_err_graphite_pct" in c else "")
                     + f" — {rec['formula']}" + (f"; dropped {rec['dropped']}" if rec["dropped"] else ""))
    ys = [j for j in rows if j["compare"].get("yield_ratio") is not None and j["compare"].get("yield_comparable")]
    if ys:
        lines += ["", f"## Yield, solid-solution records ({len(ys)}): model ÷ measured", "",
                  "| alloy | family | condition | measured MPa | model MPa | ratio |", "|---|---|---|---|---|---|"]
        for j in sorted(ys, key=lambda j: j["compare"]["yield_ratio"]):
            rec, c = j["record"], j["compare"]
            lines.append(f"| {rec['name']} | {rec['family']} | {rec['measured']['yield_condition']} | {c['yield_measured_MPa']:.0f} | {c['yield_model_MPa']} | {c['yield_ratio']:.2f} |")
    errs = [j for j in rows if j["compare"].get("error")]
    if errs:
        lines += ["", f"## Errors ({len(errs)})", ""] + [f"- {j['record']['id']}: {j['compare']['error'][:120]}" for j in errs[:30]]
    skipped_p = RESULTS / "skipped.json"
    if skipped_p.exists():
        sk = json.loads(skipped_p.read_text())
        lines += ["", f"## Not run ({len(sk)} records)", "", "reasons: " + ", ".join(f"{k} ({v})" for k, v in
                  sorted(__import__('collections').Counter(re.sub(r'[\[\]\'0-9,]', '', s[1]).strip()[:40] for s in sk).items(), key=lambda kv: -kv[1]))]
    tmp = RESULTS / ".VALIDATION.md.tmp"
    tmp.write_text("\n".join(lines) + "\n")
    os.replace(tmp, RESULTS / "VALIDATION.md")
    for j in rows:
        rec, c, m = j["record"], j["compare"], j["record"]["measured"]
        csv_rows.append({"id": rec["id"], "name": rec["name"], "family": rec["family"], "formula": rec["formula"], "tier": j["tier"],
                         "expected": "/".join(rec["expected"]), "rival": rec.get("rival"), "retained": rec.get("retained"),
                         "lattice_model": c.get("lattice_model"), "lattice_ok": c.get("lattice_ok"),
                         "margin_meV": "; ".join(f"{k} +{v}" for k, v in (c.get("lattice_margin_meV") or {}).items()),
                         "density_measured": m.get("density_gcc"), "density_model": j["model"].get("density_gcc"), "density_err_pct": c.get("density_err_pct"),
                         "density_err_graphite_pct": c.get("density_err_graphite_pct"),
                         "E_measured": m.get("E_GPa"), "E_model": (j["model"].get("elastic") or {}).get("E_GPa"), "E_err_pct": c.get("E_err_pct"),
                         "G_measured": m.get("G_GPa"), "G_model": (j["model"].get("elastic") or {}).get("G_GPa"), "G_err_pct": c.get("G_err_pct"),
                         "moduli_comparable": c.get("moduli_comparable"), "moduli_note": c.get("moduli_note"),
                         "yield_measured": c.get("yield_measured_MPa"), "yield_condition": m.get("yield_condition"), "yield_model": c.get("yield_model_MPa"),
                         "yield_ratio": c.get("yield_ratio"), "yield_comparable": c.get("yield_comparable"),
                         "de_dec_meV": c.get("de_dec_meV"), "T_star_K": c.get("T_star_K"), "seconds": j["model"].get("seconds")})
    tmp = RESULTS / ".validation.csv.tmp"
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader(); w.writerows(csv_rows)
    os.replace(tmp, RESULTS / "validation.csv")
    log(f"-> {RESULTS / 'VALIDATION.md'} ({len(rows)} alloys)")
