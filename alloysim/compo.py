"""compo.py — compositions: atomic fractions in, out, and from the wt% records of a reference database of known
alloys (optional; the format is in docs/DATABASE.md)."""
import json
import os
import re
from pathlib import Path

from pymatgen.core import Composition

from .elements import info

SIM = Path(__file__).resolve().parent.parent           # the repository root
# the reference database of known alloys: $ALLOYS_DB, else data/alloys.json. It is optional — without it the novelty
# column of a discovery run reads "n/a" and run_validate.py / run_screen_db.py have nothing to run on.
DB_FINAL = Path(os.environ["ALLOYS_DB"]).expanduser() if os.environ.get("ALLOYS_DB") else SIM / "data" / "alloys.json"


def have_db():
    return Path(DB_FINAL).is_file()


def normalize(frac):
    """{el: x} -> atomic fractions summing to 1, tiny ones dropped."""
    frac = {k: float(v) for k, v in frac.items() if float(v) > 0}
    s = sum(frac.values())
    return {k: v / s for k, v in frac.items()} if s > 0 else {}


def wt_to_at(wt):
    """{el: wt%} -> {el: atomic fraction}."""
    moles = {el: w / info(el)["mass"] for el, w in wt.items() if w > 0}
    return normalize(moles)


def at_to_wt(at):
    grams = {el: x * info(el)["mass"] for el, x in at.items()}
    s = sum(grams.values())
    return {el: 100 * g / s for el, g in grams.items()}


def formula(at, digits=2):
    """'Co20Cr20Fe20Mn20Ni20' style, atomic %, largest first."""
    parts = sorted(at.items(), key=lambda kv: -kv[1])
    return "".join(f"{el}{round(100 * x, digits):g}" for el, x in parts)


def parse(text):
    """'CoCrFeMnNi', 'Al0.3CoCrFeNi', 'Ni60Cr20Fe20' (numbers > 1.5 are read as at%) -> atomic fractions."""
    c = Composition(text)
    d = {str(el): float(v) for el, v in c.get_el_amt_dict().items()}
    return normalize(d)


def composition(at):
    return Composition({el: x for el, x in at.items()})


def db_record_at(rec):
    """a database record -> (atomic fractions, notes). Uses nominal wt% per element; the balance element takes
    what is left to 100. Returns None when the record has no usable composition."""
    comp = rec.get("composition") or {}
    elems = comp.get("elements") or []
    if not elems:
        return None
    basis = (comp.get("basis") or "wt%").lower()
    wt = {}
    balance = None
    for e in elems:
        sym = e.get("element")
        if not sym or not re.fullmatch(r"[A-Z][a-z]?", sym):
            continue
        try:
            info(sym)
        except Exception:
            continue
        if e.get("balance"):
            balance = sym
        v = e.get("nominal")
        if v is None:
            lo, hi = e.get("min"), e.get("max")
            if lo is not None and hi is not None:
                v = (float(lo) + float(hi)) / 2
            elif hi is not None:
                v = float(hi) / 2
            elif lo is not None:
                v = float(lo)
        if v is None:
            continue
        wt[sym] = max(0.0, float(v))
    if not wt:
        return None
    if balance:
        others = sum(v for k, v in wt.items() if k != balance)
        wt[balance] = max(wt.get(balance, 0.0), 100.0 - others)
    if "at" in basis:
        return normalize(wt)
    return wt_to_at(wt)


def load_db(path=DB_FINAL):
    """[(id, name, family, atomic fractions)] for every record with a composition."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data.get("alloys") or data.get("records") or list(data.values())
    out = []
    for r in recs:
        if not isinstance(r, dict):
            continue
        at = db_record_at(r)
        if at:
            out.append((r.get("id"), r.get("name"), r.get("family"), at))
    return out


def distance(a, b):
    """composition distance in atomic fraction: half the L1 norm (0 = identical, 1 = nothing in common)."""
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)
