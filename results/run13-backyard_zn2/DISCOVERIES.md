# backyard_zn — ranked by stiff_stable

objective: shear modulus times the phase and ductility factors — for lattices the strengthening model does not cover (HCP zinc, magnesium)
engine: mace-medium-mpa-0-cpu · candidates evaluated: 4

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Zn95Al5 | near Zinc anode alloy (MIL-DTL-18001 / ASTM B418 Type I, Zn-0.5Al-0.1Cd) | hcp | +0.000 | +0.000 | -0.005 | 4 | 6.91 | 22 (32 cal.) | 2.66 | 0 | 0 | — | 22.0 |  |
| 2 | Zn77Al16Cu5Ag2 | near Kayem 2 Press Tool Zinc Alloy | hcp | +0.002 | +0.032 | +0.014 | 519 | 6.65 | 20 (29 cal.) | 3.33 | 0 | 0 | — | 14.4 |  |
| 3 | Zn81Al15Cu4 | near ZA-8 Zinc-Aluminum Alloy | hcp | +0.011 | +0.033 | +0.017 | 648 | 6.56 | 20 (30 cal.) | 3.14 | 0 | 0 | — | 13.2 |  |
| 4 | Zn74Al22Mg2Ag2 | near ZA-12 Zinc-Aluminum Alloy | hcp | +0.019 | +0.030 | +0.012 | 494 | 6.08 | 16 (24 cal.) | 3.92 | 0 | 0 | — | 12.2 |  |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).
**σy cal.** (v2, 2026-10-05) = σy read as an annealed handbook yield through the validation's calibration (docs/RESULTS.md,
the calibration table): ÷ the host/solute factor (tin in copper 5.6, zinc or aluminium in copper 1.4, nickel 0.45, silicon 0.4,
molybdenum in nickel 2.35 …; aluminium: 33 MPa + 1.5 × σy), each solute weighted by its share of the strengthening; a '?' means
half or more of the strengthening comes from a solute the table has no factor for (factor 1 used). **G (cal.)** = ×1.45 for
hexagonal zinc and cadmium cells (the PBE shear softness). **notes**: 'soft / unstable cell' (G under 10 GPa or B/G over 8),
'Zn-eq N %: β brass in reality' (Guillet zinc equivalent over 37 % — the fcc cell is not the real alloy), 'Zn-rich on fcc: a
two-phase casting in reality', 'B2-ordered cell' (the random bcc cell was unstable; the row shows the ordered cell the alloy
really is, the random cell's numbers stay in the JSON). The *_cal objectives rank by σy cal. and count a soft cell as unstable.

1. **Zn95Al5** — wt% {'Zn': 97.88, 'Al': 2.12}; rules: dH 0.19 kJ/mol, δ 1.46 %, Ω 6.12, VEC 11.55; would rather be: Zn(hcp) 0.95, Al(fcc) 0.05; nearest known: 0.043 Zinc anode alloy (MIL-DTL-18001 / ASTM B418 Type I, Zn-0.5Al-0.1Cd) (zinc); 0.043 Zamak 7 (Zn-4Al-0.012Mg-0.01Ni, alloy 7 / AG40B) (zinc); 0.044 Zamak 3 (Zn-4Al-0.04Mg, alloy 3 / AG40A) (zinc)
2. **Zn77Al16Cu5Ag2** — wt% {'Al': 7.19, 'Cu': 5.29, 'Ag': 3.59, 'Zn': 83.92}; rules: dH 0.33 kJ/mol, δ 2.86 %, Ω 14.32, VEC 10.49; would rather be: Zn(hcp) 0.71, C1-CuAl 0.15, D019-ZnAg 0.08, Al(fcc) 0.06; nearest known: 0.053 Kayem 2 Press Tool Zinc Alloy (zinc); 0.061 ZA-8 Zinc-Aluminum Alloy (zinc); 0.061 ZA-8 (Zn-8Al-1Cu-0.02Mg) (zinc)
3. **Zn81Al15Cu4** — wt% {'Al': 6.79, 'Zn': 88.94, 'Cu': 4.27}; rules: dH 0.59 kJ/mol, δ 2.6 %, Ω 6.2, VEC 10.61; would rather be: Zn(hcp) 0.81, C1-CuAl 0.12, Al(fcc) 0.07; nearest known: 0.032 ZA-8 Zinc-Aluminum Alloy (zinc); 0.033 ZA-8 (Zn-8Al-1Cu-0.02Mg) (zinc); 0.063 Kayem 2 Press Tool Zinc Alloy (zinc)
4. **Zn74Al22Mg2Ag2** — wt% {'Zn': 84.94, 'Al': 10.42, 'Mg': 0.85, 'Ag': 3.79}; rules: dH 0.06 kJ/mol, δ 3.73 %, Ω 80.5, VEC 9.8; would rather be: Zn(hcp) 0.72, Al(fcc) 0.21, L21-Ag2MgAl 0.04, C14-MgZn 0.03; nearest known: 0.04 ZA-12 Zinc-Aluminum Alloy (zinc); 0.04 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.047 Kayem 2 Press Tool Zinc Alloy (zinc)
