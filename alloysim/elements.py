"""elements.py — per-element facts the other layers need, from pymatgen's tables, plus the house rules about which
elements a candidate alloy may use (a family's pool in search.py may name any of them explicitly)."""
from functools import lru_cache

from pymatgen.core import Element

# elements the SEARCH leaves out by default: toxic or radioactive ones, gases and interstitials (C, B, N, O, H — real
# alloying elements, but their physics is interstitial, which random substitutional cells do not capture; a later
# version), semimetals and the low-melting metals (a family of their own). A search pool may name any of them explicitly.
EXCLUDED = {"Be", "Cd", "Hg", "Tl", "Pb", "As", "Os", "Po", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf",
          "Es", "Fm", "Md", "No", "Lr", "Rn", "Xe", "Kr", "Ar", "Ne", "He", "H", "N", "O", "F", "Cl", "Br", "I", "At",
          "S", "Se", "Te", "P", "C", "B", "Si", "Ge", "Sb", "Bi", "Ga", "In", "Sn", "Tc", "Pm", "Fr", "Cs", "Rb", "K",
          "Na", "Li", "Ca", "Sr", "Ba", "Eu"}
# rough 2026 price class, only to keep the search honest (0 = cheap, 1 = ordinary, 2 = dear, 3 = precious)
PRICE_CLASS = {
    "Fe": 0, "Al": 0, "Mn": 0, "Cr": 0, "Cu": 0, "Zn": 0, "Mg": 0, "Si": 0, "Ti": 1, "Ni": 1, "V": 1, "Nb": 1, "Mo": 1,
    "Zr": 1, "Co": 1, "W": 1, "Sn": 1, "Ag": 2, "Ta": 2, "Hf": 2, "Y": 2, "Sc": 3, "Re": 3, "Ru": 3, "Rh": 3, "Pd": 3,
    "Ir": 3, "Pt": 3, "Au": 3, "Ge": 2, "Ga": 2, "In": 2, "La": 1, "Ce": 1, "Nd": 1, "Gd": 2, "Dy": 2, "Tb": 3,
    "Ca": 0,                                     # 2026-10-05: a magnesium alloying element (backyard_mg), not a dear one
}
# the crystal structure each element takes at room temperature (for reference cells and Vegard volumes)
GROUND = {
    "Al": "fcc", "Ni": "fcc", "Cu": "fcc", "Ag": "fcc", "Au": "fcc", "Pt": "fcc", "Pd": "fcc", "Rh": "fcc", "Ir": "fcc",
    "Pb": "fcc", "Ca": "fcc", "Sr": "fcc", "Fe": "bcc", "Cr": "bcc", "V": "bcc", "Nb": "bcc", "Mo": "bcc", "Ta": "bcc",
    "W": "bcc", "Li": "bcc", "Na": "bcc", "K": "bcc", "Ba": "bcc", "Eu": "bcc", "Mn": "bcc", "Mg": "hcp", "Ti": "hcp",
    "Zr": "hcp", "Hf": "hcp", "Co": "hcp", "Zn": "hcp", "Cd": "hcp", "Sc": "hcp", "Y": "hcp", "Re": "hcp", "Ru": "hcp",
    "Os": "hcp", "Tc": "hcp", "Be": "hcp", "Gd": "hcp", "Tb": "hcp", "Dy": "hcp", "La": "hcp", "Nd": "hcp",
    "Ce": "fcc", "Sn": "bcc", "In": "fcc", "Ga": "fcc", "Ge": "fcc", "Si": "fcc",
}


@lru_cache(maxsize=None)
def info(sym):
    """dict: Z, mass, metallic radius (Å), VEC, Pauling electronegativity, melting point (K), ground lattice, price."""
    e = Element(sym)
    try:
        vec = _vec(e)
    except Exception:
        vec = None
    try:
        r = float(e.metallic_radius) if e.metallic_radius else float(e.atomic_radius or 0)
    except Exception:
        r = float(e.atomic_radius or 0)
    return {
        "symbol": sym, "Z": e.Z, "mass": float(e.atomic_mass),
        "radius": r, "vec": vec, "chi": float(e.X) if e.X else None,
        "tm_k": float(e.melting_point) if e.melting_point else None,
        "ground": GROUND.get(sym, "fcc"), "price": PRICE_CLASS.get(sym, 2), "excluded": sym in EXCLUDED,
    }


def _vec(e):
    """valence electron concentration used in the HEA rules: number of s+d (or s+p) electrons of the neutral atom."""
    g = e.group
    if e.block == "d":
        return g                         # Sc 3 … Cu 11, Zn 12
    if e.block == "s":
        return g                         # alkali 1, alkaline earth 2
    if e.block == "p":
        return g - 10                    # Al 3, Si 4, Ga 3, Sn 4 …
    if e.block == "f":
        return 3
    return None


def allowed(sym):
    return not info(sym)["excluded"]
