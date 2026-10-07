# backyard_al — ranked by strong_ductile_cal

objective: CALIBRATED yield at 300 K (the validation's host/solute factors + floor) times the ductility factor, single phase at 300 K favoured; soft cells count as unstable
engine: mace-medium-mpa-0-cpu · candidates evaluated: 12

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Al88Mg9Si2Mn1 | near Aluminium casting 520.0 (Al-10Mg) | fcc | +0.023 | +0.041 | +0.030 | 1059 | 2.66 | 27 | 2.91 | 124 | 25 | 218 | 104.1 |  |
| 2 | Al91Mg7Si2 | near Magsimal-59 (AlMg5Si2Mn structural die casting) | fcc | +0.026 | +0.034 | +0.025 | 1135 | 2.65 | 26 | 2.96 | 91 | 15 | 170 | 90.6 |  |
| 3 | Al91Mg4Zn4Si1 | near Aluminium 7068 | fcc | +0.019 | +0.030 | +0.020 | 898 | 2.82 | 26 | 3.07 | 56 | 7 | 117 | 71.0 |  |
| 4 | Al91Mg4Zn2Cu2Mn1 | near Aluminium 7178 | fcc | +0.016 | +0.041 | +0.030 | 1144 | 2.86 | 26 | 3.02 | 77 | 11 | 148 | 69.3 |  |
| 5 | Al89Zn4Mg4Cu3 | near Aluminium 7068 | fcc | +0.015 | +0.040 | +0.028 | 1006 | 2.99 | 25 | 3.15 | 71 | 10 | 140 | 68.9 |  |
| 6 | Al90Mg5Si2Zn2Mn1 | near Magsimal-59 (AlMg5Si2Mn structural die casting) | fcc | +0.025 | +0.044 | +0.032 | 1141 | 2.78 | 27 | 2.95 | 80 | 12 | 153 | 68.2 |  |
| 7 | Al89Mg6Si2Mn2Cu1 | near Magsimal-59 (AlMg5Si2Mn structural die casting) | fcc | +0.025 | +0.055 | +0.043 | 1342 | 2.78 | 27 | 2.94 | 108 | 20 | 195 | 67.2 |  |
| 8 | Al88Cu5Zn5Mn2 | NEW | fcc | -0.014 | +0.030 | +0.018 | 714 | 3.25 | 25 | 3.23 | 45 | 4 | 100 | 64.6 |  |
| 9 | Al89Cu5Si4Zn2 | near A380.0 aluminium | fcc | +0.009 | +0.037 | +0.025 | 927 | 3.08 | 24 | 3.29 | 30 | 2 | 79 | 42.3 |  |
| 10 | Al88Zn5Cu3Si2Mg2 | near Aluminium 7055 | fcc | +0.026 | +0.050 | +0.036 | 1107 | 3.06 | 24 | 3.30 | 45 | 4 | 100 | 40.4 |  |
| 11 | Al90Zn4Cu2Si2Mn2 | near Aluminium 7055 | fcc | +0.028 | +0.055 | +0.043 | 1401 | 3.08 | 26 | 3.05 | 32 | 2 | 80 | 27.1 |  |
| 12 | Al88Zn9Si3 | NEW | fcc | +0.031 | +0.031 | +0.020 | 840 | 3.12 | 23 | 3.32 | 5 | 0 | 41 | 24.7 |  |

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

1. **Al88Mg9Si2Mn1** — wt% {'Al': 87.8, 'Mn': 2.03, 'Mg': 8.09, 'Si': 2.08}; rules: dH -2.83 kJ/mol, δ 4.91 %, Ω 1.27, VEC 2.97; would rather be: Al(fcc) 0.75, C14-MgAl 0.15, C1-SiMg 0.06, D022-AlMn 0.04; nearest known: 0.029 Aluminium casting 520.0 (Al-10Mg) (aluminium); 0.029 Aluminium casting 518.0 (Al-Mg die casting) (aluminium); 0.036 Magsimal-59 (AlMg5Si2Mn structural die casting) (aluminium); σy cal. 218 MPa (÷ 0.667 + 33)
2. **Al91Mg7Si2** — wt% {'Al': 91.56, 'Si': 2.09, 'Mg': 6.34}; rules: dH -2.04 kJ/mol, δ 4.5 %, Ω 1.35, VEC 2.95; would rather be: Al(fcc) 0.85, C14-MgAl 0.09, C1-SiMg 0.06; nearest known: 0.009 Magsimal-59 (AlMg5Si2Mn structural die casting) (aluminium); 0.019 Aluminium casting 535.0 (Almag 35) (aluminium); 0.02 Hydronalium (Al-Mg marine, German historic) (other); σy cal. 170 MPa (÷ 0.667 + 33)
3. **Al91Mg4Zn4Si1** — wt% {'Al': 86.39, 'Si': 0.99, 'Mg': 3.42, 'Zn': 9.21}; rules: dH -0.93 kJ/mol, δ 3.54 %, Ω 3.23, VEC 3.33; would rather be: Al(fcc) 0.91, C14-MgZn 0.06, C1-SiMg 0.03; nearest known: 0.025 Aluminium 7068 (aluminium); 0.026 Aluminium 7049 (aluminium); 0.027 Aluminium 7178 (aluminium); σy cal. 117 MPa (÷ 0.667 + 33)
4. **Al91Mg4Zn2Cu2Mn1** — wt% {'Al': 85.69, 'Zn': 4.57, 'Mg': 3.39, 'Cu': 4.44, 'Mn': 1.92}; rules: dH -0.99 kJ/mol, δ 3.15 %, Ω 3.3, VEC 3.34; would rather be: Al(fcc) 0.78, C14-MgAl 0.09, C1-CuAl 0.06, D022-AlMn 0.04; nearest known: 0.028 Aluminium 7178 (aluminium); 0.03 Aluminium 7068 (aluminium); 0.033 Aluminium 7150 (aluminium); σy cal. 148 MPa (÷ 0.667 + 33)
5. **Al89Zn4Mg4Cu3** — wt% {'Al': 81.38, 'Cu': 6.46, 'Zn': 8.87, 'Mg': 3.29}; rules: dH -0.28 kJ/mol, δ 3.25 %, Ω 12.77, VEC 3.56; would rather be: Al(fcc) 0.79, C1-CuAl 0.09, C14-MgAl 0.06, C14-MgZn 0.06; nearest known: 0.036 Aluminium 7068 (aluminium); 0.039 Aluminium 7178 (aluminium); 0.04 Aluminium 7449 (aluminium); σy cal. 140 MPa (÷ 0.667 + 33)
6. **Al90Mg5Si2Zn2Mn1** — wt% {'Al': 86.98, 'Si': 2.01, 'Zn': 4.69, 'Mn': 1.97, 'Mg': 4.35}; rules: dH -2.51 kJ/mol, δ 4.45 %, Ω 1.41, VEC 3.19; would rather be: Al(fcc) 0.87, C1-SiMg 0.06, D022-AlMn 0.04, C14-MgZn 0.03; nearest known: 0.027 Magsimal-59 (AlMg5Si2Mn structural die casting) (aluminium); 0.042 Aluminium 5059 (Alustar) (aluminium); 0.045 Aluminium 5456 (aluminium); σy cal. 153 MPa (÷ 0.667 + 33)
7. **Al89Mg6Si2Mn2Cu1** — wt% {'Mg': 5.25, 'Al': 86.48, 'Si': 2.02, 'Mn': 3.96, 'Cu': 2.29}; rules: dH -3.34 kJ/mol, δ 4.77 %, Ω 1.14, VEC 3.12; would rather be: Al(fcc) 0.77, D022-AlMn 0.08, C1-SiMg 0.06, C14-MgAl 0.06; nearest known: 0.027 Magsimal-59 (AlMg5Si2Mn structural die casting) (aluminium); 0.044 Aluminium 5059 (Alustar) (aluminium); 0.047 1570 aluminium (Al-Mg-Sc) (aluminium); σy cal. 195 MPa (÷ 0.667 + 33)
8. **Al88Cu5Zn5Mn2** — wt% {'Mn': 3.51, 'Al': 75.88, 'Cu': 10.15, 'Zn': 10.45}; rules: dH -1.34 kJ/mol, δ 3.01 %, Ω 2.91, VEC 3.93; would rather be: Al(fcc) 0.72, C1-CuAl 0.15, D022-AlMn 0.08, Zn(hcp) 0.05; nearest known: 0.074 Aluminium 7055 (aluminium); 0.077 Aluminium 7449 (aluminium); 0.077 Aluminium 7068 (aluminium); σy cal. 100 MPa (÷ 0.667 + 33)
9. **Al89Cu5Si4Zn2** — wt% {'Al': 81.07, 'Si': 3.79, 'Cu': 10.73, 'Zn': 4.42}; rules: dH -3.02 kJ/mol, δ 5.09 %, Ω 1.24, VEC 3.62; would rather be: Al(fcc) 0.79, C1-CuAl 0.15, Si(diamond) 0.04, Zn(hcp) 0.02; nearest known: 0.052 A380.0 aluminium (aluminium); 0.053 Aluminium casting 380.0 / A380.0 (die casting) (aluminium); 0.053 Aluminium casting 319.0 (aluminium); σy cal. 79 MPa (÷ 0.667 + 33)
10. **Al88Zn5Cu3Si2Mg2** — wt% {'Cu': 6.36, 'Zn': 10.91, 'Al': 79.23, 'Si': 1.87, 'Mg': 1.62}; rules: dH -1.58 kJ/mol, δ 4.28 %, Ω 2.61, VEC 3.69; would rather be: Al(fcc) 0.82, C1-CuAl 0.09, C14-MgZn 0.06, Si(diamond) 0.02; nearest known: 0.054 Aluminium 7055 (aluminium); 0.056 Aluminium 7449 (aluminium); 0.056 Aluminium 7068 (aluminium); σy cal. 100 MPa (÷ 0.667 + 33)
