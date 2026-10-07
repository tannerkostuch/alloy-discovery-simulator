"""alloysim — a physics pipeline that screens, simulates and ranks candidate alloys (2026).

Written by an AI coding agent (Claude) under the direction of the repository's author; two other models (Gemini and
Grok) reviewed the physics and checked the constants against the literature — see README.md and docs/DESIGN.md.

Three layers, cheap to expensive:
  screen.py     composition physics in milliseconds — Miedema mixing enthalpy, mixing entropy, atomic-size mismatch δ,
                Ω, VEC, electronegativity spread → solid solution / intermetallic / glass tendency, FCC vs BCC guess
  atomistic.py  the atoms themselves — a universal machine-learned interatomic potential (MACE, trained on DFT for the
                whole periodic table) relaxes random solid-solution cells: formation energy, which lattice wins, the
                competing intermetallic compounds it would rather form (convex-hull-lite + the temperature above which
                mixing entropy wins), elastic constants (B, G, E, ν, Pugh ductility), lattice distortion, density
  strength.py   from those numbers to a yield strength: Varvenne–Curtin (FCC) and Maresca–Curtin (BCC) solute-
                strengthening theory — the physics of dislocations pushing through a random lattice
search.py runs the funnel over thousands of candidate compositions and ranks what survives; DISCOVERIES.md is the output.
"""
__version__ = "0.1"
