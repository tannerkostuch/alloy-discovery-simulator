# backyard_hea — ranked by strong_ductile_cal

objective: CALIBRATED yield at 300 K (the validation's host/solute factors + floor) times the ductility factor, single phase at 300 K favoured; soft cells count as unstable
engine: mace-medium-mpa-0-cpu · candidates evaluated: 12

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Zn39Cu34Al22Mg5 | NEW | fcc | -0.077 | +0.056 | +0.024 | 530 | 6.44 | 31 | 2.85 | 307 | 95 | 307? | 167.9 | uncalibrated: Al/Cu/Mg in Zn |
| 2 | Cu51Mn18Zn17Al9Mg5 | NEW | fcc | -0.045 | +0.078 | +0.044 | 686 | 7.17 | 39 | 2.54 | 481 | 191 | 481? | 160.6 | Zn-eq 51 %: β brass in reality; uncalibrated: Mg/Mn in Cu |
| 3 | Cu59Mn21Zn15Mg5 | NEW | fcc | +0.022 | +0.083 | +0.055 | 899 | 7.65 | 42 | 2.56 | 486 | 197 | 486? | 121.7 | uncalibrated: Mg/Mn in Cu |
| 4 | Cu40Zn30Al24Si6 | NEW | fcc | -0.063 | +0.066 | +0.034 | 619 | 6.46 | 28 | 3.40 | 173 | 34 | 125 | 53.3 | Zn-eq 75 %: γ brass in reality |
| 5 | Cu51Al19Zn16Mn10Ni4 | NEW | fcc | -0.101 | +0.094 | +0.060 | 830 | 7.13 | 41 | 2.74 | 312 | 103 | 232 | 51.8 | Zn-eq 56 %: β brass in reality |
| 6 | Cu39Al24Zn18Mn9Si6Ni4 | NEW | fcc | -0.108 | +0.123 | +0.084 | 935 | 6.53 | 39 | 2.63 | 311 | 102 | 236 | 28.9 | Zn-eq 73 %: γ brass in reality |
| 7 | Cu35Zn34Al17Mn9Si5 | NEW | fcc | -0.043 | +0.120 | +0.083 | 990 | 6.86 | 35 | 2.68 | 220 | 55 | 159 | 19.7 | Zn-eq 75 %: γ brass in reality |
| 8 | Cu38Zn35Mn23Si4 | NEW | fcc | +0.017 | +0.131 | +0.100 | 1264 | 7.76 | 41 | 2.47 | 211 | 54 | 156 | 12.9 | Zn-eq 63 %: γ brass in reality |
| 9 | Cu32Zn25Al24Mn19 | NEW | fcc | -0.028 | +0.155 | +0.120 | 1318 | 6.64 | 41 | 2.27 | 300 | 101 | 214 | 10.6 | Zn-eq 75 %: γ brass in reality |
| 10 | Cu33Mn25Al17Zn17Sn4Si4 | NEW | fcc | -0.017 | +0.172 | +0.132 | 1272 | 6.90 | 37 | 2.46 | 608 | 263 | 128 | 4.8 | Zn-eq 76 %: γ brass in reality |
| 11 | Cu49Mn25Al18Si8 | NEW | fcc | -0.043 | +0.189 | +0.158 | 1821 | 6.85 | 46 | 2.31 | 317 | 108 | 241 | 4.6 | Zn-eq 65 %: γ brass in reality |

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

1. **Zn39Cu34Al22Mg5** — wt% {'Cu': 39.81, 'Mg': 2.24, 'Al': 10.94, 'Zn': 47.01}; rules: dH -0.03 kJ/mol, δ 5.84 %, Ω 336.12, VEC 9.18; would rather be: L21-Cu2ZnAl 0.46, D019-ZnCu 0.23, C1-CuAl 0.16, C14-MgZn 0.15; nearest known: —; σy cal. 307 MPa (÷ 1.0; uncalibrated Al/Cu/Mg)
2. **Cu51Mn18Zn17Al9Mg5** — wt% {'Cu': 56.8, 'Zn': 19.49, 'Al': 4.26, 'Mn': 17.33, 'Mg': 2.13}; rules: dH -0.39 kJ/mol, δ 6.04 %, Ω 34.12, VEC 9.28; would rather be: B2-CuZn 0.34, D019-CuAl 0.32, Mn(hcp) 0.17, C15-MgCu 0.15; nearest known: 0.192 C86200 manganese bronze (cast, 90 ksi) (copper); 0.193 C86300 manganese bronze (cast, high strength) (copper); 0.22 Heusler alloy Cu2MnAl (ferromagnetic without ferromagnetic elements) (magnetic_electrical); σy cal. 481 MPa (÷ 1.0; uncalibrated Mg/Mn)
3. **Cu59Mn21Zn15Mg5** — wt% {'Mg': 2.02, 'Zn': 16.34, 'Mn': 19.21, 'Cu': 62.43}; rules: dH 1.53 kJ/mol, δ 5.51 %, Ω 7.43, VEC 9.86; would rather be: L12-CuZn 0.60, Mn(hcp) 0.21, C15-MgCu 0.15, Cu(fcc) 0.04; nearest known: 0.222 C86200 manganese bronze (cast, 90 ksi) (copper); 0.224 C86300 manganese bronze (cast, high strength) (copper); 0.249 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory); σy cal. 486 MPa (÷ 1.0; uncalibrated Mg/Mn)
4. **Cu40Zn30Al24Si6** — wt% {'Cu': 47.78, 'Al': 12.17, 'Zn': 36.88, 'Si': 3.17}; rules: dH -3.83 kJ/mol, δ 6.12 %, Ω 2.89, VEC 8.96; would rather be: L21-Cu2ZnAl 0.62, D019-ZnCu 0.19, C1-CuAl 0.13, Si(diamond) 0.06; nearest known: —; σy cal. 125 MPa (÷ 1.388)
5. **Cu51Al19Zn16Mn10Ni4** — wt% {'Cu': 58.04, 'Mn': 9.84, 'Ni': 4.2, 'Al': 9.18, 'Zn': 18.74}; rules: dH -1.65 kJ/mol, δ 4.6 %, Ω 7.93, VEC 9.2; would rather be: D019-CuAl 0.47, B2-CuZn 0.32, B2-AlNi 0.08, L10-MnAl 0.07; nearest known: 0.157 C86300 manganese bronze (cast, high strength) (copper); 0.197 C86200 manganese bronze (cast, 90 ksi) (copper); 0.2 Cu-Al-Mn shape-memory alloy (shape_memory); σy cal. 232 MPa (÷ 1.35)
6. **Cu39Al24Zn18Mn9Si6Ni4** — wt% {'Mn': 9.51, 'Si': 3.24, 'Ni': 4.51, 'Cu': 47.65, 'Al': 12.45, 'Zn': 22.64}; rules: dH -7.37 kJ/mol, δ 6.34 %, Ω 2.05, VEC 8.44; would rather be: L21-Cu2ZnAl 0.30, D019-CuAl 0.22, L21-Al2CuNi 0.16, D019-ZnCu 0.14; nearest known: —; σy cal. 236 MPa (÷ 1.321)
7. **Cu35Zn34Al17Mn9Si5** — wt% {'Si': 2.53, 'Zn': 40.13, 'Mn': 8.92, 'Cu': 40.14, 'Al': 8.28}; rules: dH -4.93 kJ/mol, δ 5.57 %, Ω 2.58, VEC 9.27; would rather be: L21-Cu2ZnAl 0.46, D019-ZnCu 0.30, L10-MnSi 0.10, L10-MnAl 0.08; nearest known: —; σy cal. 159 MPa (÷ 1.384)
8. **Cu38Zn35Mn23Si4** — wt% {'Cu': 39.72, 'Si': 1.85, 'Mn': 20.78, 'Zn': 37.65}; rules: dH -3.82 kJ/mol, δ 3.83 %, Ω 3.07, VEC 10.15; would rather be: B2-CuZn 0.67, A15-MnSi 0.16, Mn(hcp) 0.11, L12-CuZn 0.06; nearest known: —; σy cal. 156 MPa (÷ 1.352)
9. **Cu32Zn25Al24Mn19** — wt% {'Cu': 37.94, 'Zn': 30.51, 'Mn': 19.47, 'Al': 12.08}; rules: dH -3.38 kJ/mol, δ 4.7 %, Ω 3.77, VEC 8.57; would rather be: L10-MnAl 0.38, B2-CuZn 0.26, D019-CuAl 0.20, D019-ZnCu 0.16; nearest known: 0.25 Heusler alloy Cu2MnAl (ferromagnetic without ferromagnetic elements) (magnetic_electrical); σy cal. 214 MPa (÷ 1.4)
10. **Cu33Mn25Al17Zn17Sn4Si4** — wt% {'Cu': 37.26, 'Al': 8.15, 'Mn': 24.4, 'Sn': 8.44, 'Zn': 19.76, 'Si': 2.0}; rules: dH -6.47 kJ/mol, δ 5.82 %, Ω 2.41, VEC 8.25; would rather be: B2-CuZn 0.34, L10-MnAl 0.23, D019-CuAl 0.21, A15-MnSi 0.16; nearest known: —; σy cal. 128 MPa (÷ 4.757)

Not ranked (1: no stable cell, or no strength on this lattice):
- Cu50Mn24Ni11Ag8Si7 — bcc: soft / unstable cell
