# Results — what the validation and the discovery runs found

*Status: 2026-10-05. Nothing here has been melted or measured: every "candidate" is a computational prediction.
Compositions are atomic %. The table behind every statement is in `results/` (`results/README.md` lists them); how the
numbers are computed, and what they leave out, is in `DESIGN.md`.*

## In short

- **Lattice and density can be trusted.** Over 1 214 known alloys the right crystal lattice comes out lowest in energy
  for 1 116 of the 1 125 that have a single right answer (99 %), and the median density error is 1.0 %.
- **Stiffness is good where the potential is good** — aluminium, magnesium, copper and nickel alloys within about
  10 % — and systematically off where it is not: iron and chromium on an fcc lattice (no magnetism in the model),
  niobium, tantalum, β-titanium, and zinc (a consistent third low).
- **The yield strength is a ranking until it is calibrated.** The solute-strengthening model is right within one
  host/solute pair and off by up to a factor of five between pairs. With one measured factor per pair, known alloys
  land within about ±30 % of their annealed handbook yield (within 10 % for aluminium).
- **The phase prediction names the right compound nearly every time**; its temperature scale reads about 30 % high.
- **Two candidates** hold up under all three readings they were given (the ranking, a check of the benchmarks
  against measured values, a melt-and-cast review): **Ti45Mo35V11Zr9**, a β-titanium alloy, and **Ni40Fe29Cr17V14**,
  a cobalt-free fcc alloy in CoCrNi's class. They are candidates for a literature search and a furnace, with the
  caveats below.
- **The well-mined families gave nothing new** — aluminium, copper, zinc, magnesium, a "high-entropy brass" pool and
  the Cantor space, the backyard ones sampled twice: every classic was re-found at its handbook value. That is the
  result one should want from a sound model on families where the answers are known.

## 1. The smoke test — known physics first (`results/SMOKE_REPORT.md`)

Before any search: lattice constants of Al, Cu, Ni, Fe, W and Nb within 0.7 % of experiment (titanium −1.6 %, and
−1.1 % since hexagonal cells relax their own c/a); the formation
energies of NiAl (−0.659 eV/atom against −0.62) and Ni₃Al (−0.426 against −0.45); copper's elastic constants within
7 %, those of nickel, iron and tungsten mostly 10–30 % stiff. Then two famous alloys through the whole chain.
CoCrFeMnNi (the Cantor alloy) comes out fcc with G 75 GPa (measured ~80), and below about 840 K the model says it
would rather be a B2 Fe-Co phase, an ordered Ni-Mn phase and bcc chromium with a little σ phase — close to the
phases reported after very long anneals of this alloy at intermediate temperatures. NbMoTaW comes out bcc with a
yield of 832 MPa (measured ~1050). The Cantor alloy's yield, 92 MPa, is about half the measured one; section 2 says
what the yields are worth and why.

## 2. The validation — 1 214 known alloys through the same chain

The question was how robust the simulator is on alloys whose answers are known, before computer time goes into
unknown ones. Every record of a 1 482-alloy reference database that the chain can hold was run as a random solid
solution on the lattice the record implies — plus the rival lattice where the question is real — and compared with
what was measured. Left out: solders, metallic glasses, low-melting alloys and anything built on a non-cubic metal;
composites, intermetallic compounds and "group" records; interstitial elements (C, N, O, H, B, P, S) and traces
under 0.4 at% are dropped from the cells. Three tiers: lattice and density for all (tier 1), elastic constants and
yield for the alloys whose annealed state is a solid solution (tier 2, 385 records), the phase prediction for 150
alloys with a known phase story (tier 3). On the order of thirty hours of computing on a 16-thread desktop CPU.
Scorecard: `results/VALIDATION_1214_alloys.md`.

### Lattice and density

| family | records | lattice right | density, median error | E, median error | yield, model ÷ measured |
|---|---|---|---|---|---|
| aluminium | 117 | 117 / 117 | 0.7 % | +7 % | 0.31 |
| copper | 121 | 119 / 119 | 1.5 % | +4 % | 1.29 |
| nickel | 89 | 89 / 89 | 0.8 % | −7 % | 1.37 |
| steel, tool steel | 269 | 269 / 269 | 0.7–0.9 % | — | — |
| stainless steel | 131 | 82 / 82 | 0.6 % | −38 % | 0.54 |
| cast iron | 66 | 61 / 61 | 7.4 % (0.4 % with the carbon counted as graphite) | — | — |
| titanium | 55 | 35 / 36 | 2.0 % | −15 % | 0.27 |
| magnesium | 41 | 41 / 41 | 1.9 % | +7 % | — |
| zinc | 28 | 28 / 28 | 0.8 % | −32 % | — |
| refractory | 56 | 56 / 56 | 1.2 % | −38 % | 0.17 |
| magnetic / electrical | 62 | 56 / 58 | 0.9 % | +11 % | 0.93 |
| precious metals | 56 | 56 / 56 | 5.0 % | −6 % | 1.26 |
| high-entropy | 22 | 16 / 22 | 1.8 % | −12 % | 1.10 |
| cobalt, shape-memory, Zr/U nuclear, other | 101 | 91 / 91 | 1.1–4.5 % | — | — |
| **all** | **1 214** | **1 116 / 1 125 (99 %)** | **1.0 %** | −5 % | 0.74 |

E and yield are medians over the records that have a real measurement to compare with (the scorecard gives the
counts). "Lattice right" counts only records with a single right answer. The other 89 are **retained high-temperature
phases** — austenitic stainless steel, β-titanium, Invar, NiTi — where the real alloy is a quenched-in phase and at
0 K a model may rightly put another lattice lower; for those the energy margin is the result. The margins follow the
phase diagram: ferrite sits below austenite in 47 of 49 austenitic stainless grades by 2–90 meV/atom (median 46), and
the margin falls with nickel content the way real austenite stability does; bcc stays lowest in 16 of 19 β-titanium
alloys, the other three being ties.

**The nine misses are all magnetism or ordering.** Six are aluminium-bearing high-entropy alloys (the model flips the
fcc/bcc boundary of Al-Co-Cr-Fe-Ni: the real bcc phase is ordered B2 and magnetic, a random non-magnetic bcc cell is
the wrong contender); two are Alnico magnets (ferromagnetism holds their bcc lattice together); one is a titanium
alloy off by 6 meV, inside the noise.

**The noise floor was measured by accident.** One titanium alloy sits in the database twice under two names; one copy
came out bcc by 45 meV/atom, the other hcp by a hair. A single random arrangement of 108 atoms can land 20–45 meV
either way on a lattice that is mechanically soft for the metal, so a single-arrangement margin under about 40 meV is
a tie. Candidates therefore get three arrangements (the confirmation pass below).

**Density misses.** Everything made of gold, silver, platinum or palladium reads about 5 % light — the model inherits
the slightly too large noble-metal lattice constants of the quantum-chemical method it was trained on (PBE). Cast
irons read 7 % heavy as bare cells and within 0.4 % once the dropped carbon is counted as graphite.

### Stiffness

- Aluminium +7 %, magnesium +7 %, copper and nickel alloys within about ±10–17 % where the database holds a real
  measurement.
- **Iron and chromium on an fcc lattice come out soft, and by a law:** over 79 austenitic stainless and nickel
  alloys, E error ≈ +9 % − 56 % × (Fe fraction) − 55 % × (Cr fraction) (r 0.92, ±7 %). Chromium-free Fe-Ni alloys
  (Invar, permalloy) read 3–30 % *stiff* instead, because the real ones are magnetically softened. Both signs are the
  same missing physics: the model has no magnetism.
- **Niobium and tantalum are where the potential gives out:** bcc niobium is mechanically unstable in the model
  (negative moduli for the pure metal and its dilute alloys), tantalum half as stiff as measured. Molybdenum and
  tungsten alloys are within about 20 %.
- **β-titanium:** one arrangement of a near-unstable bcc lattice is ±50 %.
- **Zinc:** a consistent third low after a fix to the cell shape — section 4.

### Yield strength, and its calibration

The chain's yield is solute strengthening alone (Varvenne–Curtin for fcc, Maresca–Curtin for bcc): no grain
boundaries, precipitates or interstitials. The validation shows what that number is worth. **Within one host/solute
pair it ranks sensibly — more magnesium, more zinc, more molybdenum, more strength, at a constant factor. Across
pairs it is off by up to ×5**, because the theory's only handle is the misfit volume: solutes much bigger or smaller
than the host come out far too strong, near-size solutes far too weak (they strengthen through modulus misfit and
short-range order, which the model has no term for).

**The calibration table** — model ÷ measured annealed yield, the median over clean records (no castings with second
phases, no leaded, sintered or aged records):

| host | solute | n | factor | | host | solute | n | factor |
|---|---|---|---|---|---|---|---|---|
| Cu | Sn | 10 | **5.6** | | Ni | Mo | 4 | **2.35** |
| Cu | Au | 9 | 1.9 | | Ni | Cr (with Mo) | 18 | 1.5 |
| Cu | Al | 8 | 1.4 | | Ni | Fe | 5 | 1.3 |
| Cu | Zn | 16 | 1.4 | | Ni | Cu | 2 | 0.45 |
| Cu | Ni | 10 | 0.45 | | Fe (fcc) | Ni | 23 | 1.0 |
| Cu | Si | 4 | 0.4 | | Fe (fcc) | Cr | 38 | 0.5 |
| Al | Mg | 18 | 0.5, plus a 33 MPa floor | | Fe (bcc) | Si | 5 | 1.5 |
| Au | Cu | 9 | 1.5 | | Pt | Co | 3 | 3.0 |
| Au | Ni | 2 | 2.9 | | Ta | W | 4 | 0.33 |
| Au | Ag | 4 | 0.85 | | Pt | Ir, Pd, Ru, W | 1 each | 0.02–0.25 |
| Au | Pd | 3 | 0.5 | | Mo | Re | 3 | 0.16 |
| Ag | Cu | 5 | 0.8 | | Ti (β) | V / Mo | 3 / 2 | 0.4 / 0.08 |

For aluminium one rule covers every solute: measured ≈ 33 MPa + 1.5 × model (r 0.96 over 27 wrought records); the
33 MPa is grain boundaries and trace elements the cell does not hold. bcc solid solutions are under-predicted across
the board — bcc solute hardening is a screw-dislocation story this model only half captures; the equiatomic
refractory alloys it was built for (NbMoTaW, VNbMoTaW) come out at 0.7–1.2.

The table is in the code (`alloysim/calibrate.py`): every newer DISCOVERIES table carries a **σy cal.** column next
to the raw number, each solute weighted by its share of the strengthening, with a "?" when half or more of it comes
from a solute the table does not know. Some factors rest on two to five alloys; they are a reading aid, not a law.

### Phases

For 150 alloys with a known phase story, the question was whether the mixture the model says a solid solution "would
rather be" is what metallurgy knows the alloy to do. It names the right compound or separation nearly every time:
θ-Al₂Cu, MgZn₂ and Mg₂Si under the age-hardening aluminium alloys; CuBe under beryllium copper, with the solution
temperature within 80 K of the real solvus; γ″ Ni₃Nb in Inconel 718 and γ′ in Waspaloy; B2 for NiTi and Fe-Co; the
spinodal products of Alnico; ordered Ni₃Fe in permalloy; AuCu in rose gold; the Zn-Al eutectic under Zamak; the
Fe-Cr miscibility gap behind 475 °C embrittlement.

Two habits to read around. The model **over-orders fcc solid solutions**: α-brass, nickel silver and 7 % aluminium
bronze are disordered at every working temperature, and the model puts an ordered compound 10–45 meV below them — it
turns short-range order into a phase. And its **temperature scale is high**: T\* comes from energy and mixing entropy
alone (no vibrational entropy, no magnetism) and reads roughly 30 % above the real transition where one is known.

**Reading rules for a discovery table:** a ΔG₃₀₀ under about 50 meV whose product is an ordered compound means "solid
solution with some order", not "falls apart" — CoCrNi, the Cantor alloy and 304 stainless all sit at +0.06 to +0.11
and are made every day. A product that is a different lattice of the base element is the retained-phase story.
A T\* is to be discounted by about 30 %.

## 3. The discovery runs

A run samples a few thousand compositions inside a family's rules, screens them with composition rules, keeps about a
dozen that are far apart from each other, puts each through the atomistic chain, and ranks them. Each run carries
its family's benchmark alloy, which it has to re-find.

### Runs 1–3 and the confirmation pass

| run | family, objective | benchmark, re-found | what it turned up |
|---|---|---|---|
| 1 | medium-entropy fcc, strong and ductile | CoCrNi: fcc, G 94 GPa (measured 87) | **Ni40Fe29Cr17V14** |
| 2 | refractory bcc, strength at 900 K | NbMoTaW: bcc, 830 MPa at room temperature, stable | Nb32W27Hf17Mo14Ta10, Ti29V22Mo21Hf14Ta14, V37Ti37Cr16W10 |
| 3 | Ti-rich bcc, specific strength | Ti-35Nb-7Zr-5Ta: bcc, only 2.6 meV/atom below hcp — a metastable β alloy, which is what it is | **Ti45Mo35V11Zr9**, Ti40Zr32Mo28 |

Every candidate and benchmark was then run again with **three random atom arrangements per lattice**. Energies moved
by 1–15 meV/atom and strengths by 0–11 %, the benchmarks by as much as the candidates — the soft β-titanium benchmark
aside, whose tiny shear modulus swings with the arrangement. No ranking rested on one lucky arrangement.

| candidate | ΔG₃₀₀ (eV/atom) | reading |
|---|---|---|
| **Ti45Mo35V11Zr9** | +0.019 | bcc by a wide margin (35 % Mo is a strong β stabiliser), ductile by the Pugh criterion, density 6.9 g/cm³. As stable as the benchmark β alloy. The best-founded candidate of the set. About 49 wt% molybdenum, so not cheap. Its yield is a ranking only, as for every β-titanium alloy here (real β-Ti strength is oxygen and fine precipitates), and its modulus is one arrangement's number on a soft lattice |
| **Ni40Fe29Cr17V14** | +0.057 | fcc, as stable as CoCrNi by the same yardstick (+0.058) and about 45 % stronger on the same scale; no cobalt. Needs a quench from the solution temperature, like CoCrNi. Its 45 % margin stands; its absolute 218 MPa does not, and its moduli read 10–20 % low by the iron/chromium law above. At 29 % iron it also carries the model's magnetism caveat |
| V37Ti37Cr16W10 | +0.037 | the light, cheap one (7.25 g/cm³); TiCr₂ Laves phase is the competitor |
| Ti40Zr32Mo28 | +0.049 | ZrMo₂ Laves phase is a real risk at 28 % Mo; weaker case than Ti45Mo35V11Zr9 |
| Nb32W27Hf17Mo14Ta10 | +0.091 | "1 370 MPa", but the model says 40 % of it would rather be a HfW₂-type Laves phase, and the strength is the misfit model extrapolated past the range it was checked in |
| Ti29V22Mo21Hf14Ta14 | +0.080 | two Laves-phase traps at once; its "edge over NbMoTaW at 900 K" is inside the model error |

Two more turned up in run 1 at 470–500 MPa and were set aside at once: the model says they decompose into a Heusler
compound plus iron and copper, and their nearest known alloys are Alnico magnets, which decompose on purpose.

### What the two reviewing models made of them

Grok put the benchmark rows next to measured values from the literature: lattice constants within 1 %,
room-temperature moduli within about 10 %, yields 20–30 % below the grain-boundary-free values they should match —
and it marked the three large-misfit bcc yields as the shakiest numbers in the set. Gemini gave a melt-and-cast
verdict per candidate: yes to Ti45Mo35V11Zr9 (melt from a Ti-Mo master alloy, or molybdenum stays unmelted) and to
Ni40Fe29Cr17V14 (solution anneal and water quench; not for hot air, vanadium oxide fluxes the scale), maybe to the
two lighter ones, no to the two heavy refractory ones (Laves phases, and miserable to cast). Their numbers were
checked against the stored results before being used. Two of Gemini's statements went past the data and are not
taken: that Ti45Mo35V11Zr9 is thermodynamically stable (it is a *retained* β phase), and a projected proof stress
that would beat Ti-6Al-4V on specific strength (a projection, not a result).

The ranking, the benchmark check and the melt verdict land on the same two alloys. No literature search for these
exact compositions has been done: "new" here means only that the reference database holds nothing within 6 at%.

### Run 4 — the Cantor space; run 5 — copper

Run 4 (Co-Cr-Fe-Mn-Ni with Al, Cu, V, Ti) re-found the Cantor alloy and nothing new worth a furnace: the unexplored
corners of that pool are manganese- and copper-rich mixes the model says decompose — which is what they do in
practice. The space has been mined for two decades; the model agrees little is left.

Run 5 exposed a blind spot. Its top "new" copper alloy, Cu58Zn32Al10, looked like a stable fcc brass 40 % stronger
than cartridge brass. Brass metallurgy counts aluminium at six times zinc (Guillet's zinc equivalent), which puts
that alloy at about 62 % zinc-equivalent — deep in the hard, brittle β/γ-brass field. The run had only tried fcc
cells. **Run 5's copper candidates are not to be trusted**; the code now computes the zinc equivalent of every copper
candidate and says "β brass in reality" on the row.

### The backyard runs (6, 7, 9, 8)

Four families of metals a hobby foundry can pour: aluminium with Mg, Si, Cu, Zn and Mn; copper with Zn, Sn, Al, Si,
Mn, Ni and Mg; a "high-entropy brass" pool of copper plus three to five of those; and zinc with Al, Cu and Mg (a
little silver is allowed in each). Sixty candidates, 25 of them not in the reference database, **none worth a
furnace** — and every benchmark re-found at its calibrated handbook value:

| alloy | model → calibrated (MPa) | handbook, annealed or as cast (MPa) |
|---|---|---|
| Al-5Mg (5083 / 5182) | 73 → 143 | 130–145 |
| Al-1Mg-0.6Si (6061) | 15 → 55 | 55 |
| Al-Zn-Mg-Cu (7075) | 44 → 99 | 103 |
| Cu-30Zn (cartridge brass) | 164 → 117 | 75–110 |
| Cu-12Sn (tin bronze) | 964 → 172 | 150–190 |
| Cu-7Al (aluminium bronze) | 263 → 188 | 210–230 |
| Cu-3Si-1Mn (silicon bronze) | 42 → 105 | 145 |

What the runs did give:

- **Aluminium:** the strongest single-phase alloy the model can make is Al90Mg10 (about 9 wt% magnesium), which is
  the Al-Mg casting family — the alloys that are strong without heat treatment. For the age-hardening alloys the
  model gets the annealed value right and names the kind of precipitate that does the rest (MgZn₂ under 7075, a
  copper-aluminium compound under the 2xxx alloys): the "would rather be" column reads as *what strengthens it on
  ageing*.
- **Copper:** raw, the run is a ranking by tin content; calibrated, the order is the handbook's. Manganese-rich
  copper is a dead corner — every such mix decomposes in the model into the compounds the phase diagrams show.
- **"High-entropy brass" fails on thermodynamics, not on strength.** Mixing entropy for a four-to-six-element copper
  alloy is worth 0.03–0.04 eV/atom at room temperature; the model's deficit for every such mix is 0.08–0.18,
  because copper's partners form compounds with copper and with each other. The one alloy left standing is nickel
  silver — three elements, known for two centuries.
- **Zinc:** the model's ranking is the handbook's (Zamak 5 > Zamak 3 > Zn-5Al > Zn-Cu, Zn-Mg > ZA-12 > ZA-27) and
  the search space is tiny; there is no new zinc alloy to find with these five elements.
- **Two habits that went into the code as notes on every row:** an fcc cell of a composition that is β or γ brass in
  reality, and a random bcc cell standing in for an ordered B2 phase and going unstable — the second now triggers a
  rebuild of the cell as ordered B2.

### The second pass (runs 10–13) and magnesium (run 14)

A second sample of each backyard family with another random seed, kept clear of the first pass's alloys and ranked by
the calibrated yield (zinc by stiffness); then a first pass over magnesium (Mg ≥ 85 % with Al, Zn, Mn, Ca, Si, Sn,
Cu). Fifty-six alloys, 28 of them not in the reference database, **none worth a furnace** — fresh compositions gave
the first pass's answers again:

- **Aluminium (run 10):** Al-Mg(-Si) on top again. Rank 1, Al88Mg9Si2Mn1, reads 218 MPa calibrated — a ceiling, since
  2 wt% manganese is more than aluminium dissolves. Rank 2, Al91Mg7Si2, lands within 1 at% of the die-casting alloy
  Magsimal-59 (AlMg5Si2Mn) at 170 MPa against a measured 160–190 as cast: the calibration working outside the wrought
  grades it was fitted on. The two compositions not in the database are weak (100 and 41 MPa).
- **Copper (run 11):** nine of twelve not in the database, none a find. Every row with 10 at% manganese or more sits
  at least 68 meV above its decomposition products, and two of them have no stable cell. The one new composition that
  is calibrated end to end, Cu76Ni10Al8Si6 (Cu-10Ni-3.7Al-2.9Si by weight, 213 MPa), sits 62 meV above copper plus
  Cu-Al and Ni-Si compounds — the precipitation-hardening signal of the Cu-Ni-Si family. It lies next to an alloy
  studied in the literature (Cu-10Ni-3Al-0.8Si, hardened by Ni₃Al and Ni₂Si precipitates) with three and a half times
  its silicon: a known family's over-alloyed corner, not a discovery.
- **"High-entropy brass" (run 12):** twelve new compositions, the lowest 56 meV above its products, the others
  66–189; ten of the eleven ranked rows are β or γ brass by zinc equivalent. Over two passes, 26 compositions and one
  that holds up: nickel silver.
- **Zinc (run 13):** the family is used up — 334 of 350 sampled compositions lie within the search's spread of a
  first-pass alloy, and the four that were evaluated sit next to Zamak, ZA-8, Kayem 2 and ZA-12.
- **Magnesium (run 14):** the four benchmarks (AZ91-, AM60-, AS41- and ZK60-type) land where the validation puts
  magnesium — density 1–2 % high, stiffness 6–10 % high. The hexagonal lattice has no yield model here, so the run
  ranks by stiffness and stability. Stiffness hardly moves with alloying (G 16–20 GPa over the whole table), the
  commercial families take the top seven places, and the five new compositions — rich in tin, zinc and calcium — are
  heavier, no stiffer and less stable. Two limits: magnesium's strength (grain size, texture, precipitates) is
  outside the model; and the phase prediction understates Mg-Al, because the compound list has no Mg₁₇Al₁₂ and a
  Laves phase stands in for it.

**What the second pass showed about the reading rules** — none of it changes a computed number:

- A solute without a calibration factor is counted at factor 1, which ranks it *first*: silver in copper (run 11's
  top row, "242?") and magnesium in copper (run 12's "481?" and "486?"). Read by solute size — silver at gold's
  factor, magnesium between gold and tin — those rows are about 140–160 MPa.
- The brass note is written for copper-base alloys and misses a Cu-Zn alloy in which zinc outweighs copper (run 12's
  top row: 75 % zinc equivalent by the same arithmetic, a γ brass).
- The rebuild of an unstable bcc cell as ordered B2 had no case: the three unstable cells of this pass have no B2
  compound among their products.

The first two are open issues in the code.

## 4. Zinc — a failure worth keeping

The first validation had pure zinc at E = 3 GPa against a measured 85, and Zamak negative. Two causes, found in that
order:

1. **The cell, not the potential.** Every hexagonal cell was built at the ideal shape (c/a = 1.633) and relaxed in
   volume only — a rule that keeps cubic cells from wandering onto another lattice. For magnesium (1.624) and titanium
   (1.587) that never mattered. Zinc's c/a is 1.856: the ideal-shape cell sits on a slope of the energy surface, and
   stiffness measured there is meaningless. Letting hexagonal cells relax a and c independently fixed it: zinc comes
   out at a 2.652 Å, c/a 1.880 (measured 2.665, 1.856), stable, E 59 GPa. The same work found that the stability
   check had been calling every hexagonal cell "unstable" for not having 90° angles, and that the ideal c/a is a
   flat saddle on which an optimiser stops — so the reference now scans c/a first.
2. **What remains is the method the potential was trained on.** Zinc's shear stiffness stays 40–50 % low (E about
   30 % low); the quantum-chemical method behind the training data (PBE) describes zinc's shape and shear poorly, and
   a potential trained on it inherits that. Five other machine-learned
   potentials were tried on pure zinc; none did better than the one in use. The reading rule: **zinc's E and G read
   a third low, consistently — multiply by about 1.45; a ranking inside the family is sound.**

**A classical potential was tried and set aside** (`meam_check.py`). The one published MEAM parameter set found that
covers zinc and aluminium (Dickel and Baskes 2018, made for magnesium alloys) gets pure zinc right — shear modulus
−11 % where the machine-learned potential is −48 % — and aluminium dissolved in zinc wrong: one aluminium atom in a
hundred raises c/a by 3 %, and a Zamak cell ends about 7 % under its measured density, lower in energy than zinc
plus aluminium. It has no copper either. It did confirm the ×1.45 rule from an independent direction: a
potential fitted to experiment puts pure zinc at E 97 GPa; the machine-learned value × 1.45 is 86; handbooks say
85–96.

**What works for zinc alloys is reading them as two phases.** A zinc casting alloy is zinc plus an aluminium-rich
phase, not a solution (the model's own phase prediction says so for every one). Taking the stiffness as the
volume-weighted mixture of the two phases gives ZA-12 at 82 GPa against a measured 83 (as one solid solution: 68)
and ZA-27 at 77 against 78 (as one solution: 24), with a median error of 1 % over all 28 zinc records. Most of
those records carry the same nominal handbook value, so the test rests on the four that differ; and the rule is not
in the code yet. Run 13's four zinc alloys, read this way, are within 6 % of their handbook stiffness (as one
solution: up to 21 % low). It also says what a solid-solution search cannot find in zinc: stiffness there is set by
how much aluminium phase is mixed in.

## 5. Stacking-fault energies — a ranking at best (`results/SFE_VALIDATION.md`)

The stacking-fault step (twinning and work-hardening in fcc alloys) was checked on five known cases: copper 28 mJ/m²
(measured ~45), nickel 87 (~125), aluminium 87 (~166) — 30–50 % low — and CoCrNi −93 and the Cantor alloy −61 against
measured values of roughly +20 to +30, with a spread between fault planes larger than the value. (Published
first-principles calculations at 0 K also give CoCrNi a negative value, though a smaller one.) The step tells low
from high; it does not give a number, and the "CoCrNi's class" reading of Ni40Fe29Cr17V14 (−46) is exactly that
coarse.
