# backyard_cu — ranked by strong_ductile_cal

objective: CALIBRATED yield at 300 K (the validation's host/solute factors + floor) times the ductility factor, single phase at 300 K favoured; soft cells count as unstable
engine: mace-medium-mpa-0-cpu · candidates evaluated: 12

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cu80Zn15Ag5 | near C24000 low brass (80/20) | fcc | -0.023 | +0.016 | +0.001 | 312 | 8.68 | 40 | 2.97 | 242 | 64 | 242? | 238.6 | uncalibrated: Ag in Cu |
| 2 | Cu65Zn23Ni9Ag3 | near C74500 nickel silver 65-10 | fcc | -0.041 | +0.040 | +0.016 | 494 | 8.60 | 42 | 2.87 | 254 | 75 | 200 | 135.0 |  |
| 3 | Cu65Zn24Al11 | near Cu-Zn-Al (Copper-Zinc-Aluminium Shape Memory Alloy) | fcc | -0.089 | +0.047 | +0.024 | 627 | 7.79 | 36 | 3.07 | 239 | 60 | 171 | 92.8 | Zn-eq 45 %: α+β brass in reality |
| 4 | Cu76Ni10Al8Si6 | NEW | fcc | -0.073 | +0.062 | +0.041 | 883 | 8.02 | 45 | 2.93 | 252 | 69 | 213 | 77.2 |  |
| 5 | Cu63Mn20Zn12Ag5 | NEW | fcc | +0.043 | +0.075 | +0.049 | 855 | 8.22 | 43 | 2.63 | 256 | 79 | 256? | 75.9 | uncalibrated: Ag/Mn in Cu |
| 6 | Cu71Zn19Sn9Ni1 | NEW | fcc | +0.001 | +0.059 | +0.038 | 834 | 8.50 | 30 | 3.58 | 821 | 366 | 150 | 58.3 | Zn-eq 42 %: α+β brass in reality |
| 7 | Cu67Mn19Al14 | NEW | fcc | -0.042 | +0.069 | +0.047 | 938 | 7.48 | 46 | 2.46 | 262 | 82 | 187 | 57.5 | Zn-eq 40 %: α+β brass in reality |
| 8 | Cu70Zn10Al10Mn10 | NEW | fcc | -0.039 | +0.068 | +0.043 | 834 | 7.73 | 42 | 2.75 | 237 | 64 | 170 | 57.4 |  |
| 9 | Cu59Zn30Si6Mn5 | NEW | fcc | -0.023 | +0.085 | +0.060 | 999 | 8.00 | 36 | 3.07 | 169 | 35 | 129 | 29.0 | Zn-eq 50 %: β brass in reality |
| 10 | Cu58Zn24Mn18 | NEW | fcc | +0.044 | +0.103 | +0.078 | 1232 | 8.06 | 42 | 2.63 | 187 | 46 | 134 | 19.2 |  |

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

1. **Cu80Zn15Ag5** — wt% {'Cu': 76.98, 'Zn': 14.86, 'Ag': 8.17}; rules: dH 0.68 kJ/mol, δ 3.02 %, Ω 9.38, VEC 11.15; would rather be: L12-CuZn 0.60, Cu(fcc) 0.35, Ag(fcc) 0.05; nearest known: 0.05 C24000 low brass (80/20) (copper); 0.054 Pinchbeck, Prince's metal and Mannheim gold (imitation-gold brasses, Cu-11 to 25 Zn) (other); 0.055 C23000 red brass (85/15) (copper); σy cal. 242 MPa (÷ 1.0; uncalibrated Ag)
2. **Cu65Zn23Ni9Ag3** — wt% {'Zn': 23.19, 'Ni': 8.14, 'Ag': 4.99, 'Cu': 63.68}; rules: dH 1.0 kJ/mol, δ 3.01 %, Ω 9.68, VEC 11.14; would rather be: L12-CuZn 0.56, Cu(fcc) 0.23, L10-ZnNi 0.18, Ag(fcc) 0.03; nearest known: 0.03 C74500 nickel silver 65-10 (copper); 0.045 C75700 nickel silver 65-12 (copper); 0.06 Nickel brass (UK £1 coin, 70-24.5-5.5) (copper); σy cal. 200 MPa (÷ 1.271)
3. **Cu65Zn24Al11** — wt% {'Cu': 68.87, 'Al': 4.95, 'Zn': 26.18}; rules: dH 0.44 kJ/mol, δ 3.72 %, Ω 18.68, VEC 10.36; would rather be: D019-CuAl 0.44, B2-CuZn 0.40, L12-CuZn 0.16; nearest known: 0.02 Cu-Zn-Al (Copper-Zinc-Aluminium Shape Memory Alloy) (shape_memory); 0.035 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory); 0.077 C86200 manganese bronze (cast, 90 ksi) (copper); σy cal. 171 MPa (÷ 1.4)
4. **Cu76Ni10Al8Si6** — wt% {'Cu': 83.26, 'Ni': 10.12, 'Al': 3.72, 'Si': 2.9}; rules: dH -4.52 kJ/mol, δ 4.89 %, Ω 2.06, VEC 9.84; would rather be: Cu(fcc) 0.47, D019-CuAl 0.32, L21-Ni2CuSi 0.19, C1-NiSi 0.02; nearest known: 0.122 C64200 aluminium-silicon bronze (copper); 0.139 C96200 cast 90-10 cupronickel (copper); 0.14 C72500 copper-nickel-tin (CuNi9Sn2) (copper); σy cal. 213 MPa (÷ 1.182)
5. **Cu63Mn20Zn12Ag5** — wt% {'Cu': 62.3, 'Mn': 17.1, 'Zn': 12.21, 'Ag': 8.39}; rules: dH 2.42 kJ/mol, δ 3.05 %, Ω 4.56, VEC 10.32; would rather be: L12-CuZn 0.48, Cu(fcc) 0.27, Mn(hcp) 0.20, Ag(fcc) 0.05; nearest known: 0.216 9 Karat Gold (375 Gold) (precious_metal); 0.216 9 k gold (Au 375, Au-Ag-Cu-Zn) (precious_metal); 0.234 Manganin (copper); σy cal. 256 MPa (÷ 1.0; uncalibrated Ag/Mn)
6. **Cu71Zn19Sn9Ni1** — wt% {'Zn': 18.06, 'Ni': 0.85, 'Cu': 65.56, 'Sn': 15.53}; rules: dH 2.43 kJ/mol, δ 3.91 %, Ω 3.26, VEC 10.55; would rather be: L12-CuZn 0.76, D019-CuSn 0.19, C1-NiSn 0.03, Sn(fcc) 0.02; nearest known: 0.095 C44400 admiralty brass (Sb) (copper); 0.095 C44300 admiralty brass (arsenical) (copper); 0.095 C44500 admiralty brass (P) (copper); σy cal. 150 MPa (÷ 5.476)
7. **Cu67Mn19Al14** — wt% {'Mn': 18.38, 'Cu': 74.97, 'Al': 6.65}; rules: dH -0.36 kJ/mol, δ 4.08 %, Ω 26.37, VEC 9.12; would rather be: D019-CuAl 0.56, Cu(fcc) 0.25, Mn(hcp) 0.19; nearest known: 0.076 C95700 manganese-aluminium bronze (Cu-Mn-Al propeller alloy, 'Novoston') (copper); 0.08 Cu-Al-Mn shape-memory alloy (shape_memory); 0.11 Cu-Al-Mn (Ductile Copper-Aluminium-Manganese Superelastic Alloy) (shape_memory); σy cal. 187 MPa (÷ 1.4)
8. **Cu70Zn10Al10Mn10** — wt% {'Cu': 75.12, 'Zn': 11.05, 'Al': 4.56, 'Mn': 9.28}; rules: dH 0.16 kJ/mol, δ 3.62 %, Ω 61.82, VEC 9.9; would rather be: L12-CuZn 0.40, D019-CuAl 0.40, Mn(hcp) 0.10, Cu(fcc) 0.10; nearest known: 0.115 Cu-Al-Mn shape-memory alloy (shape_memory); 0.123 Cu-Al-Mn (Ductile Copper-Aluminium-Manganese Superelastic Alloy) (shape_memory); 0.138 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory); σy cal. 170 MPa (÷ 1.4)
9. **Cu59Zn30Si6Mn5** — wt% {'Si': 2.74, 'Mn': 4.46, 'Zn': 31.88, 'Cu': 60.92}; rules: dH -3.71 kJ/mol, δ 4.25 %, Ω 2.64, VEC 10.68; would rather be: L12-CuZn 0.52, B2-CuZn 0.34, L10-MnSi 0.10, D019-CuSi 0.04; nearest known: 0.104 C86500 manganese bronze (cast, 65 ksi) (copper); 0.106 C67500 manganese bronze (wrought, 'A') (copper); 0.11 C36000 free-cutting brass (61.5/35.5/3) (copper); σy cal. 129 MPa (÷ 1.31)
10. **Cu58Zn24Mn18** — wt% {'Cu': 59.02, 'Zn': 25.14, 'Mn': 15.84}; rules: dH 1.19 kJ/mol, δ 2.08 %, Ω 8.29, VEC 10.52; would rather be: L12-CuZn 0.68, Mn(hcp) 0.18, B2-CuZn 0.14; nearest known: 0.151 C86200 manganese bronze (cast, 90 ksi) (copper); 0.174 C86500 manganese bronze (cast, 65 ksi) (copper); 0.176 C86300 manganese bronze (cast, high strength) (copper); σy cal. 134 MPa (÷ 1.4)

Not ranked (2: no stable cell, or no strength on this lattice):
- Cu70Mn18Zn8Mg4 — bcc: soft / unstable cell
- Cu63Mn17Ni10Sn10 — bcc: would transform with a free cell; soft / unstable cell
