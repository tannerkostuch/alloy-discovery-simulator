# Design — the physics of how alloys hold together, used to look for new ones

*Status: 2026-10-05.* The brief was a full simulation of the physics of how alloys hold together, with the goal of
discovering new ones. The code was written by an AI coding agent (Claude) under the author's direction; two other
models (Gemini and Grok) reviewed the physics and brought ideas, and what was taken from them is credited where it
went in ("Who did what", at the end). The simulator only reads its reference database of known alloys
(`DATABASE.md`); the database itself is not part of this repository.

## What "the physics" is, honestly

An alloy is a crystal lattice with different atoms on its sites. Everything you care about — does it stay one phase or
fall apart into compounds, how stiff is it, how strong, how heavy, when does it melt — comes from the energy of those
atoms as a function of where they sit. The exact physics of that is quantum mechanics (density-functional theory, DFT),
which costs hours per structure. The way the field does it in 2026: a **universal machine-learned interatomic
potential** — a neural network trained on millions of DFT calculations across the whole periodic table — that gives
DFT-quality energies and forces in milliseconds. We use **MACE** (MACE-MPA-0: trained on ~3.5 M structures; errors
~0.02–0.03 eV/atom on formation energies, typical lattice constants within ~1 %). Everything reported here ran on a desktop CPU (Ryzen 7 5800X, 16 threads,
2.2 s per force call on a 108-atom cell): PyTorch's ROCm wheels do see that machine's AMD RX 9070 XT and MACE's
*energies* are right on it, but its *forces* came out wrong there (garbage in float64, NaN in float32 —
`diag_cantor.py` is the check; 2026-09-29, gfx1201 under ROCm 7.0), so `--device cuda` stays a thing to retry after
updates.

That engine only gives energies and forces. The *physics of alloys* is what we compute with it:

| question | what is computed | how |
|---|---|---|
| does this composition form a solid solution or compounds? | formation energy of a random solid-solution cell vs the lowest-energy mixture of pure elements and ordered pair compounds (B2, L1₂, L1₀, C15 Laves, A15) | relax ~100-atom random cells on FCC/BCC/HCP; relax the compounds; a linear programme finds the cheapest mixture = a *convex-hull-lite*; ΔE_dec and the temperature T* above which mixing entropy wins |
| which lattice? | FCC vs BCC vs HCP energy of the same composition | same cells |
| how stiff, how ductile? | elastic constants C_ij → bulk B, shear G, Young's E, Poisson ν, Pugh B/G (> 1.75 ductile), Cauchy pressure, Born stability | ±0.5 % strains with internal relaxation |
| how strong? | yield stress at 77–1200 K | Curtin's solute-strengthening theory: a dislocation dragged through misfitting atoms; inputs are G, ν, the alloy volume and each element's misfit volume — all from the cells above (Varvenne–Curtin FCC 2016, Maresca–Curtin BCC 2020; Taylor factor 3.06 FCC / 2.73 BCC). A second model (Grok) checked the constants against the papers |
| how heavy, how distorted? | density; mean displacement of atoms off their ideal sites (the "lattice distortion" that makes high-entropy alloys strong) | from the relaxed cell |
| will it twin / work-harden? (FCC) | intrinsic stacking-fault energy γ_SF — < 20 mJ/m² twinning/TRIP (tough), ~20–40 CoCrNi-like, > 80 Al/Ni-like easy cross-slip | tilted-cell method: one Shockley partial of shear across a 108-atom (111)-stacked cell, atoms relaxed along z, every fault plane sampled → mean ± spread (`alloysim/sfe.py`, `run_sfe.py`; a follow-up step on the FCC candidates. Checked on Cu/Ni/Al/CoCrNi/Cantor: the pure metals come out 30–50 % low and the two alloys negative, so it is a ranking at best — `RESULTS.md`) |
| rough thermodynamics in milliseconds | mixing enthalpy (Miedema pair table), mixing entropy, size mismatch δ, Ω, VEC, electronegativity spread → the standard solid-solution / FCC-vs-BCC design rules | `screen.py`, used to sift thousands of compositions before the expensive part |

What it does **not** do (yet, or at all): interstitials (C, N, B — the physics of steels is interstitial carbon and
precipitates; a random substitutional cell cannot see that), precipitation hardening and grain size (Hall–Petch),
magnetism (MACE has none — Fe's moduli come out ~25 % stiff), short-range order (the cells are fully random), BCC
screw-dislocation/kink-pair physics (Gemini's point; the BCC model is Curtin's edge model), real melting points (would
need MD at temperature — possible later, slow), the liquidus–solidus gap / castability beyond a volatility flag,
corrosion (electrochemistry), fatigue. The hull-lite has pair prototypes (B2, L1₂, L1₀, C15, C14, A15, σ) and the L2₁
Heusler triple; true ternary/quaternary compounds beyond that are not in it. Every number carries the model's own
error (the smoke test says how much); a "discovery" is a candidate for the literature and, eventually, a furnace —
not a fact.

## The funnel (`search.py`)

1. **sample** thousands of compositions inside a family's rules (element pool, 2–6 elements, bounds, price class)
2. **screen** them with the composition rules (−22 ≤ ΔH_mix ≤ 7 kJ/mol, δ ≤ 6.6 %, Ω ≥ 1.1) — milliseconds each
3. **shortlist** ~12 by a cheap score (misfit up to ~3 %, a clear lattice, cheaper elements, no volatile elements, the
   tight ΔH window preferred) — breadth first: one composition per element set, no element in more than 60 % of the
   picks (except a family's "must" element), no two closer than 10 at% (2026-09-29: before that the score drifted to
   "everything + 12 % Al"); per-element solubility caps in `FAMILIES` keep a family what it says it is
4. **evaluate** each with the atomistic chain above (20–40 min on the CPU; 4 candidates at once in worker processes)
5. **rank** by an objective — `specific_strength` (σy/ρ), `high_temp` (σy at 900 K + melting point), `strong_ductile`,
   `stability`, `stiff_stable` (G × phase × ductility, for HCP families without a strengthening model) — with the
   phase-stability and ductility factors applied
6. **novelty**: every candidate is compared with a reference database of known alloys (1 482 records for the runs
   reported here); NEW = nothing within 6 at%
7. `results/<run>/DISCOVERIES.md` + one JSON per candidate (all the numbers, so nothing has to be recomputed)

Families to start with (concentrated alloys, where random cells are the right model): `3d_hea` (Co-Cr-Fe-Mn-Ni-Al-Cu-V-Ti),
`refractory` (Nb-Mo-Ta-W-V-Ti-Zr-Hf-Cr), `medium_entropy_fcc`, `ti_light_bcc` (≥ 35 at% Ti), `cu_alloys` (≥ 50 at% Cu).
The first three runs, Gemini's choice: run 1 medium_entropy_fcc /
strong_ductile (must re-find CoCrNi), run 2 refractory / high_temp (NbMoTaW), run 3 ti_light_bcc / specific_strength
(Ti-35Nb-7Zr-5Ta wt% = Ti69.7Nb23.7Zr4.8Ta1.8 at%).

## Validation before anyone believes a number (`run_smoke.py`)

Lattice constants of Al/Cu/Ni/Fe/W/Nb/Ti vs experiment; formation energies of NiAl (B2, −0.62 eV/atom) and Ni₃Al (L1₂);
elastic constants of Cu/Ni/Fe/W vs experiment; then two famous alloys through the whole chain: CoCrFeMnNi (must come
out FCC, single-phase, G ≈ 80 GPa, σy ≈ 200 MPa at RT) and NbMoTaW (BCC, σy ≈ 1 GPa). The report is `SMOKE_REPORT.md`
(the one behind the results reported here is kept as `results/SMOKE_REPORT.md`).
`run_screen_db.py` puts every database alloy through the composition rules (`data/DB_RULES_CHECK.md`): the known
single-phase families must land in the solid-solution window, or the rules are wrong before the search starts.

## The whole database as the test (`run_validate.py`, 2026-09-30)

How robust is the simulator on alloys whose answers are known, before computer time goes into unknown ones? Every
record of the reference database the chain can hold — 1 264 of 1 482; the
solders, low-melting Bi/In/Cd alloys, metallic glasses and uranium alloys are built on non-cubic metals or on no
lattice at all; interstitials (C, N, O, H, B, P, S) and traces under 0.4 at% are dropped, the cells are substitutional —
goes through the same chain as a discovery run, in three tiers, and is compared with what the database says was
measured (`alloysim/validate.py`; it writes the scorecard `results/validation/VALIDATION.md` and a `validation.csv` with every
number, both rebuilt after every alloy so they can be read while it runs; the scorecard of the run reported here is
kept as `results/VALIDATION_1214_alloys.md`):

- **tier 1, all 1 264**: the solid solution on the lattice the record implies (austenitic → FCC, β-Ti → BCC, Zn/Mg/Ti/Zr
  → HCP, …) and, where the question is real, the rival lattice → *lattice right?* and *density error*. Quenched-in
  phases (austenitic stainless, β-Ti, Hadfield steel, Co-Cr, β shape-memory alloys) are scored separately: at 0 K the
  model may rightly put the low-temperature lattice lower, so for them the *margin* is the result. ~8 h.
- **tier 2, the ~400 records whose annealed yield is a solid solution** (no precipitates, martensite or carbides):
  elastic constants → E, G, ν errors; the solute-strengthening yield → the ratio model ÷ measured per family. The chain
  leaves out grain-boundary, precipitate and interstitial strengthening on purpose, so the ratio is expected below 1
  where those carry the load (a first brass came out *above* 1 — the misfit model over-does dilute FCC Cu-Zn); what the
  scorecard is for is how consistent the ratio is inside a family, i.e. what a discovery run's MPa are worth. ~14 h.
- **tier 3, ~150 alloys with a phase story** (α vs α+β brass, austenitic / ferritic / duplex stainless, NiTi, γ' superalloys,
  θ in Al-Cu, Alnico, Invar/Kovar/permalloy, the HEAs): the hull → does "would rather be" match what is known. ~7 h.

**What "expected lattice" is read from.** The family first; then the subfamily and name with the Greek
letters spelled out (the database writes β, α, `near_beta`, "beta-rich"); where a record has no phase word, the
composition: Bania's molybdenum equivalent for titanium (Mo + 0.67 V + 0.44 W + 0.28 Nb + 0.22 Ta + 2.9 Fe + 1.6 Cr +
1.25 Ni + 1.7 Mn + 1.7 Co − Al − Sn/3 − Zr/6, wt%: ≥ 7 → β, 3–7 → either, below → α), Guillet's zinc equivalent for
brass (Zn + 6 Al + 10 Si + 2 Sn + 2 Mg + Pb + 0.9 Fe + 0.5 Mn − 1.3 Ni: ≥ 48 → β, 37.5–48 → either, ≥ 30 → α with
BCC as the rival; aluminium bronzes: either above 9.5 wt% Al; silicon bronzes: α), and nickel for the cast stainless
grades that carry no phase word (≥ ~8 wt% Ni → austenitic). Two lattices in the expectation (α+β titanium, duplex,
α+β brass, Co-Cr) mean either counts. Retained phases — austenitic stainless under 25 at% Ni, β-Ti, Hadfield/TWIP,
Ni-Resist (austenite held by the carbon the cell cannot hold), the B2/β of NiTi and Ti-Nb — are scored by margin. The
first scorecard (v1) had 12 "wrong" lattices, ten of which were this mapping, not the model; v2 re-labels every stored
result from the current rules whenever the scorecard is rebuilt, and a tier-1 result whose stored cells lack a
lattice the rules now ask for (the brasses: BCC) is run again after tier 3.

**Cast-iron density.** The 12–15 at% carbon of a grey or ductile iron is dropped from the cell and is graphite
(2.26 g/cc) in the casting; the scorecard reports the cell's density (+8 %) and, next to it, the density with the
dropped carbon put back as graphite volume (within ~0.5 %) — white irons excluded, their carbon is cementite.

## What the validation taught, and what it changes (2026-10-03, after tiers 1–2 and most of tier 3)

The plain-language reading is in `RESULTS.md`; this is the part that changes how the chain's numbers
are to be read and what gets added to it. Nothing below alters a number already in `results/run*/` — additions only.

**1. Lattice and density (tier 1): trust them.** 1 116 of 1 125 single-answer records on the right lattice (99 %), density
within 1 % (cast irons once the dropped carbon is counted as graphite; the noble metals a systematic −5 %, the PBE
lattice-constant habit the potential inherited). The nine misses are all magnetism/ordering (Al-bearing Cantor alloys,
Alnico). A single 108-atom arrangement on a lattice that is mechanically soft for the metal (bcc Ti, fcc Fe) scatters
±20–45 meV/atom between arrangements — a margin under ~40 meV is a tie, which is why candidates get three arrangements.

**2. Moduli (tier 2): a law for fcc Fe/Ni/Cr, and four places where the potential gives out.**
- Over the 79 austenitic stainless and nickel alloys with a measured modulus, **E error ≈ +9 % − 56 % × x(Fe) − 55 % ×
  x(Cr)** (atomic fractions; r 0.92, ±7 %), G the same — fcc iron and chromium are modelled soft, most likely for lack
  of magnetism; chromium-free Fe-Ni (Invar, permalloy) reads +3 to +30 % *stiff* because the real alloys are magnetically
  softened. Aluminium +7 %, magnesium +6 %, copper and nickel alloys within ±10–17 % where the database has a real
  value (the copper records mostly carry a 117 GPa placeholder, the high-entropy ones 200 GPa — database gaps, not
  results).
- **Zinc**: pure Zn E = 3 GPa against 85, Zamak negative (Mg, Ti, Hf on the same hcp routine are within 10 %). At this
  point it read as the potential's failure; it turned out to be mostly the shape of the cell — the zinc section below. **Niobium and tantalum**: bcc Nb mechanically unstable (negative moduli for the
  pure metal and its dilute alloys), Ta half-stiff; Mo, W, Mo-Re, W-Re within 10–20 %. **β-titanium**: one arrangement
  of the near-unstable bcc lattice is ±50 % (TNZT 55 GPa one day, 98 the next). **β-brass** random bcc cells: unstable
  (the real phase is ordered B2 CuZn, held by temperature). Run 8 (zinc, `stiff_stable`) was held back for this reason until that fix;
  Nb-rich and β-Ti candidates keep their stability results and lose their stiffness numbers.

**3. The solute yield (tier 2): right within a host/solute pair, wrong by up to ×5 across pairs.** The Varvenne–Curtin
model's only handle is the misfit volume, so solutes much bigger or smaller than the host come out far too strong and
near-size solutes far too weak (they strengthen through modulus misfit and short-range order, which the model has no
term for); on top sits what the cell cannot hold (N, C, eutectic Si, undissolved Pb) and the 30–100 MPa grain-boundary
floor of every annealed metal. The medians of model ÷ measured, by pair (clean records only — no castings with second
phases, no leaded, sintered, ODS or aged records):

| host | solute | n | model ÷ measured | | host | solute | n | model ÷ measured |
|---|---|---|---|---|---|---|---|---|
| Cu | Sn | 10 | 5.6 | | Ni | Mo | 4 | 2.35 |
| Cu | Au | 9 | 1.9 | | Ni | Cr (with Mo) | 18 | 1.5 |
| Cu | Al | 8 | 1.4 | | Ni | Fe | 5 | 1.3 |
| Cu | Zn | 16 | 1.4 | | Ni | Cu | 2 | 0.45 |
| Cu | Ni | 10 | 0.45 | | Fe (fcc) | Ni | 23 | 1.0 |
| Cu | Si | 4 | 0.4 | | Fe (fcc) | Cr (N/C unmodelled) | 38 | 0.5 |
| Al | Mg | 18 | 0.5, plus a 33 MPa floor (measured ≈ 33 + 1.5 × model, r 0.96) | | Fe (bcc) | Si | 5 | 1.5 |
| Au | Cu | 9 | 1.5 | | Pt | Co | 3 | 3.0 |
| Au | Ni | 2 | 2.9 | | Pt | Ir, Pd, Ru, W | 1 each | 0.02–0.25 |
| Au | Ag | 4 | 0.85 | | Ta | W | 4 | 0.33 |
| Au | Pd | 3 | 0.5 | | Mo | Re | 3 | 0.16 |
| Ag | Cu | 5 | 0.8 | | Ti (β) | V / Mo | 3 / 2 | 0.4 / 0.08 |
| equiatomic refractory HEAs (NbMoTaW, VNbMoTaW) | | 3 | 0.7–1.2 | | HfNbTaTiZr | | 3 | 0.45 |
| CoCrNi, CoCrFeNi | | 2 | 0.4–0.7 | | Al-bearing fcc HEAs | | 4 | 1.5–1.9 |

What went into the chain (`calibrate.py` and `search.py`, additive): a **calibrated σy** column — the chain's σy divided
by the pair factor (weighted over the solutes present) plus the host's floor — printed next to the raw number in every
DISCOVERIES table written since; the raw number stays the one runs 1–9 were ranked on. A pair that has no row keeps
factor 1 and says so.

**4. The hull (tier 3): the right compound nearly every time, the temperature a few hundred kelvin high.** θ-Al₂Cu,
MgZn₂ and Mg₂Si in the aluminium alloys; CuBe (T* within 80 K of the real solvus); γ″ D0₂₂-Ni₃Nb in 718 and γ′ in
Waspaloy; B2 for NiTi and Fe-Co; the Alnico spinodal products (bcc Fe + NiAl B2 + the Co₂AlFe Heusler); L1₂ Ni₃Fe in
permalloy; L1₀ AuCu; the Au-Ni and Ag-Cu gaps; the Zn-Al eutectic; B2 CuZn under Muntz metal; TiCr₂ Laves and α₂ in
titanium; the Fe-Cr miscibility gap at T* 510–670 K (real ~750 K) — all called. Two habits to read around: **(a)** fcc
solid solutions that are disordered at every working temperature (α-brass, nickel silver, 7 % Al bronze, Au-Pd) come
out 10–45 meV *above* an ordered compound — the model turns short-range order into a phase; **(b)** T* is energy over
mixing entropy alone (no vibrational entropy, no short-range order, no magnetism) and reads ~30 % high (304: 1 200–
1 700 K for a phase that is stable above ~1 000 K; Nichrome 1 200 K against 860). Reading rules, now in the summary:
a ΔG₃₀₀ under ~50 meV whose product is an *ordered compound* means "solid solution with order"; a product that is a
*different lattice of the base* is the retained-phase story; a T* is to be discounted by ~30 %.

**5. Small fixes this led to (all made since).** `lattice_check` flagged every hexagonal cell as "unstable" (the c/a
relaxation counted as a shape change) — fixed with the hexagonal cells below; a cell whose modulus comes out near or
below zero now carries a "soft / unstable cell" note instead of passing as a number; in the reference database the
copper and high-entropy modulus placeholders (117 / 200 GPa) are flagged as not comparable, two records with wrong
compositions were corrected (an 18 k yellow gold with a stray nickel line, the brazing alloy BAg-24), and the yield
test leaves out the Al-Si/Cu/Zn castings and the leaded bronzes.

## Zinc, and what it taught about hexagonal cells (2026-10-04, atomistic.py v6)

The validation's zinc rows were off by 50–120 % (pure Zn E 3 GPa against 85; Zamak negative). Diagnosis with 2-atom cells: the chain built every hcp cell at the ideal c/a 1.633 and
relaxed its volume only (the rule that keeps cubic cells off the Bain path). Zinc's c/a is 1.856; the ideal-shape cell
sits on a slope 6 meV/atom above the model's minimum, and the ± strains of the elastic step, taken on a cell that is not
at equilibrium, come out Born-unstable. Shape free, MACE-MPA-0's own zinc is a 2.652 Å, c 4.985, c/a 1.880, V 15.18 (all
within 1 % of experiment) with C11 129, C12 54, C13 44, C33 46, C44 18, C66 37 against 165/31/50/62/40/67 — stable,
~40 % soft in shear: that part is the PBE-level description of zinc (filled 3d band near E_F; PBE over-stretches c/a and
under-binds the basal shear) and every PBE-trained potential tested inherits it (MACE-OMAT-0 and MP-0 do not even find
zinc's shape; MH-1's r2SCAN/OMat/MP heads E 47–65; MatterSim G 9). Gemini and Grok (same brief) concur: keep MPA-0, fix
the cell, a per-element factor for Zn/Cd now, a 2NN-MEAM Zn-Al-Cu-Mg potential for the zinc family if the last third
matters; fine-tuning on PBE/r2SCAN data would reproduce the soft floor.

**What v6 changes** (`atomistic.py`):
- `Engine.relax(..., mask=)` and `HCP_MASK = [1,1,1,0,0,0]`: hexagonal cells relax a and c independently, no shear; cubic
  cells keep the hydrostatic relaxation (the Bain-path reason stands).
- `reference()` for hcp: a c/a scan (1.57 … 1.94, volume-relaxed each) before the free relaxation — the ideal c/a is a
  *flat saddle* for zinc and cadmium where an optimizer started from the guessed volume stops with the stress under its
  tolerance; the reference stores the model's own c/a ("ca": Zn 1.88, Mg 1.62, Ti 1.60). Cached hcp references without
  "ca" are made again (seconds). The old pure-Zn reference energy was 4 meV/atom too high for the same reason.
- `hcp_ca()`, `vegard_a()`, `random_cell()`: an hcp alloy cell is built with the base element's c/a; `solid_solution()`
  relaxes it with the mask; the nearest-neighbour distance comes from the relaxed cell.
- `lattice_check()` compares cell angles with the *starting* cell — it used to compare with 90° and call every hexagonal
  cell "unstable" (pure titanium included).
Tested on 96-atom cells with the chain's own functions: Zn E 3.4 → 59.4 GPa, Zamak 3 −17.8 → 57.5, Mg
49.3 → 50.9, Ti 99.6 → 97.7, all Born-stable, `lattice_check` stable. In the validation, run again on 10-04: every hcp zinc record
−29 to −45 % (median −32 %), densities within 0.1–3 %, titanium/magnesium/hafnium unchanged within noise; ZA-27 (fcc,
two-phase) stays −69 %. **Zinc's E and G read about a third low, consistently: ×1.45 (×1.8 against single-crystal
values) in the calibration column; a ranking inside the family is sound.** Run 8 (backyard zinc) runs on that basis.

## Queues of runs

Every discovery run and every validation tier writes one JSON file per alloy, whole or not at all, and skips what is
already on disk — so a run, or a queue of them, can be stopped at any point and started again where it left off. The
scheduler that queued the runs on the machine they were computed on is not part of this repository; anything that calls
`run_validate.py` and `run_search.py` in order will do.

## What v2 of the funnel adds (2026-10-05, after the backyard runs)

The backyard runs 6, 7, 9 and 8 (`RESULTS.md`) found no new alloy and re-found every classic at
its calibrated handbook value; what they showed was *how to read* a table, so the reading went into the code, next to
the numbers, never instead of them (`alloysim/calibrate.py`, `search.py` v2, `atomistic.py` v7, `validate.py` v2.4):

- **The calibrated yield** (`calibrate.calibrated_yield`; the column *σy cal.* in every new DISCOVERIES table and the
  *strong_ductile_cal* objective). σy ÷ the host/solute factor of §3's table (tin in copper 5.6, zinc or aluminium in
  copper 1.4, nickel 0.45, silicon 0.4; molybdenum in nickel 2.35, chromium alone in nickel 0.4, iron 1.3, Monel 0.45;
  the gold, silver, platinum, tantalum, molybdenum and β-titanium pairs likewise), each solute weighted by its share of
  the model's own strengthening (c·ΔV², which is what the Varvenne sum is made of), plus the host's floor — aluminium has
  one rule for every solute, measured ≈ 33 MPa + 1.5 × σy. A pair the table does not know gets factor 1 and the row is
  marked "uncalibrated: X in host" when half or more of the strengthening comes from such solutes; a "?" after the
  number says the same. The raw σy stays in the table; runs 1–9 were ranked on it and that does not change.
- **Zinc and cadmium moduli ×1.45** (`calibrated_moduli`; "G 22 (32 cal.)") for hexagonal cells of those hosts — the
  consistent third the PBE description leaves out (the MEAM branch below did not change that).
- **Notes** on every row (`calibrate.notes`): *soft / unstable cell* (G under 10 GPa or B/G over 8 — the zinc-rich fcc
  cells of run 8 passed the Born check with G 3–5 GPa); *Zn-eq N %: α+β / β / γ brass in reality* (Guillet's zinc
  equivalent of a copper alloy, Si ×10, Al ×6, Sn ×2, Mg ×2, Mn ×0.5, Ni −1.3, over 37 / 45 / 60 % — run 5's Cu58Zn32Al10 and
  run 9's Cu50Zn25Al17Si8 were fcc cells of β and γ alloys); *Zn-/Mg-rich on fcc: a two-phase casting in reality*; and
  the ordered-cell note below. The *_cal* objective counts a soft cell as unstable (×0.1, like a Born failure).
- **The B2-ordered retry** (`atomistic.ordered_cell`, `search._ordered_retry`). Run 9 lost four bcc cells — the benchmark
  manganese bronze Cu60Zn35Mn3Al2 among them, G −4 GPa — and the validation its β-brasses, because a *random* bcc cell
  of Cu-Zn-Al at 0 K is mechanically unstable while the *ordered* B2 CuZn those alloys really are is not. Now, when a
  bcc cell comes out unstable (soft, Born-unstable or "would transform") and the hull's mixture carries a B2 compound at
  20 % or more, the cell is built again with the B2's first element on one sublattice and its second on the other
  (the rest at random on what is left), relaxed, checked and measured the same way. When that cell is stable, the row
  shows its energy, density, moduli and yield with the note "B2-XY-ordered cell (stable; the random bcc cell was not)"
  and ΔE_dec measured from the ordered cell; the random cell's numbers stay in the JSON (`cells`, `elastic`), the
  ordered ones under `ordered`. When it is not, the row keeps the random cell and says "still unstable". The solute
  yield of an ordered cell is a rough number (the theory is for random solutions); the stability verdict is the point.
- **Seeds and the second pass** (`--seed N`, `--avoid-run NAME`): a second pass of a family samples with another seed and
  sets aside every composition within the family's spread of the first pass's shortlist, so it explores new ground
  instead of re-finding the same twelve. Runs 10–13 are the second pass of the four backyard families, ranked by the
  calibrated yield (zinc stays `stiff_stable`).
- **`backyard_mg`** (run 14): Mg ≥ 85 % with Al ≤ 12, Zn ≤ 5, Mn ≤ 2, Ca ≤ 4, Si ≤ 3, Sn ≤ 4, Cu ≤ 3 at% — AZ91 / AM60 /
  AS41, Mg-Zn, Mg-Sn and Mg-Ca casting territory — hcp only (magnesium is hcp at every casting composition; the cubic
  cells of a zinc-rich alloy in run 8 were fictions), `stiff_stable`, benchmarks Mg91Al8Zn1 (AZ91), Mg94.5Al5.5 (AM60),
  Mg95.4Al3.7Si0.9 (AS41), Mg98Zn2. The hull has the compounds that matter (C14 MgZn₂ / CaMg₂, C15 MgCu₂, C1 Mg₂Si /
  Mg₂Sn, the Mg-Al Laves stand-ins). Magnesium burns; the chain only ranks.
- **validate.py v2.4**: E and G carry a *comparable* flag — false for the copper records at pure copper's 117 GPa
  placeholder, the high-entropy records at 200, the two-phase castings run as one solution (ZA-27 / Galvalume-type zinc
  with ≥ 15 at% Al, Al-Si castings) and anything leaded — and the family medians count only comparable rows (n shown);
  the yield test drops leaded copper, Al-Si castings by composition and the zinc family (eutectics). Nothing is
  recomputed: the stored results are re-read under the new rules at the scorecard rebuild. The reference database itself got two corrections: 18 k yellow gold's stray nickel line and BAg-24's composition.
- **The MEAM branch for zinc — tested and closed (10-05).** A classical potential fitted to experiment was both
  reviewers' suggestion for zinc. LAMMPS (22 Jul 2025) and MPICH 5.0.2 went into the venv as PyPI wheels
  (`pip install lammps mpich`; the MPICH wheel carries the `libmpi.so.12` the LAMMPS wheel links — run with
  `LD_LIBRARY_PATH=.venv/lib`). The only published LAMMPS-ready parameter set with zinc and aluminium that turned up
  is Dickel–Baskes 2018 Mg-Al-Zn (NIST Interatomic Potentials Repository; its files are not redistributed here). `meam_check.py` says: **pure zinc is right** (a 2.668, c/a 1.852, G 38 GPa =
  −11 % against MACE's −48 %; no flat saddle), magnesium and aluminium are right — and **aluminium dissolved in zinc is
  wrong**: one Al atom in a hundred stretches c/a by 3 %, the Zamak-3 cell ends at c/a 2.15 and 7 % under density with a
  negative C13, below Zn + Al in energy. The set was fitted for dilute magnesium alloys; its Zn–Al term was never meant
  for the zinc side, and it has no copper. NIST's repository listed nothing else for Al–Zn when it was checked (2026-10-05). So no `Engine(kind="meam")`: there is no
  potential to put in it. Kept: the ×1.45 zinc reading, confirmed by a potential fitted to experiment (MEAM pure Zn
  E 97, MACE × 1.45 = 86, handbook 85–96), and LAMMPS as a tool (seconds per alloy) for cross-checks on Mg-Al-Zn and —
  with the Jelinek 2012 Al-Si-Mg-Cu-Fe set inside the wheel — on aluminium castings.
- **Zinc is read as two phases** (10-05). A zinc casting alloy is η-zinc plus an aluminium phase, not a
  solution (the hull says so for every one). Its stiffness is the volume-weighted mixture of the two — zinc phase 86 GPa
  (MACE pure Zn × 1.45), aluminium phase 69 (MACE pure Al ÷ 1.07), mean of the series and parallel mixtures: ZA-12 82
  against 83 measured (one solid solution: 68), ZA-27 77 against 78 (one solid solution: 24), all 28 zinc records at a
  median error of 1 %. To add to `calibrate.py` as a "two-phase E" for alloys the hull splits into elemental phases;
  until then it is a reading rule. The solid-solution funnel has nothing to find in zinc's stiffness — it is set by how
  much aluminium phase is mixed in.

## The backyard families (2026-09-30)

The brief: novel ways to mix the commonly available metals — something a hobbyist could pour in a back yard. Four
families in
`FAMILIES` of metals a propane or charcoal furnace and a clay-graphite crucible can pour (everything melts or dissolves
below ~1150 °C): `backyard_al` (Al ≥ 88 %: Cu, Mg, Si, Zn, Mn, Ag — 2xxx/5xxx/6xxx/7xxx territory and the crossovers),
`backyard_cu` (Cu ≥ 58 %: Zn, Sn, Al, Si, Mn, Ni, Ag, Mg — brass, bronze, aluminium/silicon/manganese bronze),
`backyard_zn` (Zn ≥ 70 %: Al, Cu, Mg, Ag — Zamak/ZA, poured at 450 °C; HCP, so ranked by the new `stiff_stable`
objective, G × phase × ductility, because the strengthening model covers FCC and BCC only) and `backyard_hea` (Cu ≥ 30 %
plus four to six of Zn, Al, Mn, Sn, Ni, Ag, Mg, Si — a "high-entropy brass"). What changed underneath to make them
honest: Sn and Si may be named in a pool as solutes (they stay off the default list); the volatile-element penalty is
off for these families (zinc loss is the normal business of brass founding, `volatile_ok`); the VEC lattice rule — an
HEA rule — is not applied to an Al/Cu/Zn-based alloy (`lattice_rule: base`); the dilute families keep candidates 2.5–4
at% apart instead of 10; and the hull knows the precipitates of these alloys: **C16** θ-Al₂Cu, **C1** Mg₂Si, **D0₂₂**
Al₃Ti/Al₃Zr/Al₃V and **D0₁₉** Ti₃Al/Ni₃Sn (the stand-in for Cu₃Sn) were added to the prototype list (`atomistic.py`;
cached pairs are back-filled with the new kinds the first time they are needed) and silicon's real ground state, the
diamond lattice, is its reference — before that Si's metallic cells started so compressed (no metallic radius in the
tables → 8 Å³) that MACE relaxed them into a spurious minimum 6 eV too deep; references now start from tabulated atomic
volumes and a collapse (< 0.6× the start, or < 5 Å³) is retried and then refused. For these families "would rather be"
reads as *what strengthens it on ageing* (θ, Mg₂Si, MgZn₂, ZrAl₃…), not only as a warning.

## Files

```
README.md            what this is, how it was built, how to run it
setup_sim.sh         builds ./.venv with uv: Python 3.12, PyTorch (the CPU wheel by default), MACE, ASE, pymatgen, matminer
requirements.txt     the same list for pip
run_smoke.py         does the engine reproduce known physics? → SMOKE_REPORT.md
run_search.py        a discovery run → results/<run>/DISCOVERIES.md (+ one JSON per candidate)
run_validate.py      the chain against a reference database, --tier 1|2|3 → results/validation/VALIDATION.md (+ validation.csv)
run_sfe.py           stacking-fault energies: --validate → data/SFE_VALIDATION.md; --from-run <run> --top 6 → results/<run>/SFE.md
run_screen_db.py     the composition rules over a reference database → data/db_features.csv, data/DB_RULES_CHECK.md
diag_cantor.py       one 108-atom cell on GPU and CPU: the check that showed a GPU's forces to be wrong
meam_check.py        a classical MEAM parameter set against experiment (pure elements + one alloy cell) through LAMMPS — seconds
alloysim/            elements.py compo.py screen.py atomistic.py strength.py calibrate.py search.py sfe.py validate.py
docs/                DESIGN.md (this), RESULTS.md (what came out), DATABASE.md (the reference-database format)
data/                alloys.example.json — ten well-known alloys in the database format
results/             the tables of the runs read in RESULTS.md, the scorecard of the 1 214-alloy validation, the smoke-test and SFE reports
cache/, logs/        written at run time (elemental references and pair compounds per engine, shared by the workers; logs)
```

## Who did what

- **The author** set the goals and chose the directions: a full simulation of the physics rather than rules fitted to a
  table; test the simulator on every known alloy before computer time goes into unknown ones; the "backyard" families;
  find out why zinc failed and fix it; try the MEAM route; run the second passes. The author read and judged what came out.
- **Claude** (Anthropic) wrote the code, ran the validation and the discovery runs, and wrote these documents.
- **Gemini** (Google) reviewed the physics chain and the objectives, proposed the first three families, and gave a
  melt-and-cast verdict on each candidate. Taken from it: the σ, C14 and L2₁ competitors in the hull, stability
  reported at 300 / 900 / 1200 K, the volatility flag.
- **Grok** (xAI) checked the strength-model constants and the rule thresholds against the papers, as far as it knows
  them, and put the benchmark rows next to measured values from the literature. Taken from it: the BCC Taylor factor
  2.73, both ΔH windows reported per candidate, and which of the yield numbers are rankings rather than strengths.

The reviewers' numbers were checked against the stored results before anything was taken from them, and where a review
went past the data, `RESULTS.md` says so.
