# backyard_al — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 15

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Al90Mg10 | near Aluminium casting 518.0 (Al-Mg die casting) | fcc | +0.014 | +0.020 | +0.011 | 708 | 2.61 | 27 | 2.90 | 119 | 24 | 89.7 |
| 2 | Al88Mg7Zn5 | near Aluminium casting 518.0 (Al-Mg die casting) | fcc | +0.011 | +0.024 | +0.012 | 622 | 2.82 | 26 | 3.03 | 88 | 14 | 64.7 |
| 3 | Al89Cu4Mg3Zn2Mn2 | near Aluminium 7178 | fcc | -0.013 | +0.031 | +0.018 | 726 | 3.06 | 26 | 3.12 | 86 | 13 | 54.4 |
| 4 | Al89Mg7Cu4 | near Aluminium casting 518.0 (Al-Mg die casting) | fcc | +0.015 | +0.041 | +0.030 | 1141 | 2.80 | 26 | 3.07 | 112 | 21 | 52.4 |
| 5 | Al90Si4Mg3Zn3 | near Aluminium 7178 | fcc | +0.004 | +0.012 | +0.001 | 333 | 2.82 | 25 | 3.07 | 45 | 4 | 43.8 |
| 6 | Al90Cu4Si3Mg3 | near Magsimal-59 (AlMg5Si2Mn structural die casting) | fcc | +0.005 | +0.032 | +0.021 | 859 | 2.92 | 24 | 3.25 | 66 | 8 | 38.9 |
| 7 | Al87Mg5Zn5Si2Cu1 | near Aluminium 7068 | fcc | +0.022 | +0.042 | +0.028 | 890 | 2.89 | 25 | 3.13 | 74 | 10 | 37.1 |
| 8 | Al94Mg2.9Zn2.4Cu0.7 | near Aluminium 7175 (premium forging 7075) | fcc | +0.011 | +0.020 | +0.013 | 833 | 2.84 | 26 | 3.04 | 44 | 4 | 32.1 |
| 9 | Al94.7Mg5Mn0.3 | near Aluminium 5182 (can-end stock) | fcc | +0.033 | +0.039 | +0.033 | 2069 | 2.66 | 28 | 2.90 | 73 | 11 | 31.7 |
| 10 | Al89Zn6Mg3Si2 | near Aluminium 7068 | fcc | +0.027 | +0.039 | +0.027 | 980 | 2.96 | 25 | 3.15 | 43 | 4 | 22.0 |
| 11 | Al95Cu5 | near Aluminium 2219 | fcc | -0.004 | +0.024 | +0.018 | 1375 | 2.93 | 26 | 3.12 | 30 | 2 | 18.7 |
| 12 | Al98.3Mg1.1Si0.6 | near Aluminium 6201 (high-strength conductor wire) | fcc | -0.004 | -0.002 | -0.005 | 0 | 2.71 | 27 | 2.96 | 15 | 1 | 14.7 |
| 13 | Al91Si3Cu3Zn3 | near Aluminium casting 319.0 | fcc | +0.011 | +0.027 | +0.017 | 794 | 2.98 | 24 | 3.28 | 19 | 1 | 12.3 |
| 14 | Al90Zn10 | NEW | fcc | +0.014 | +0.014 | +0.006 | 510 | 3.14 | 24 | 3.24 | 3 | 0 | 2.9 |
| 15 | Al91Zn6Si3 | near Aluminium 7449 | fcc | +0.034 | +0.034 | +0.024 | 1088 | 3.00 | 24 | 3.22 | 5 | 0 | 2.5 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Al90Mg10** — wt% {'Al': 90.9, 'Mg': 9.1}; rules: dH -0.72 kJ/mol, δ 3.52 %, Ω 3.5, VEC 2.9; would rather be: Al(fcc) 0.70, C14-MgAl 0.30; nearest known: 0.011 Aluminium casting 518.0 (Al-Mg die casting) (aluminium); 0.013 Aluminium casting 520.0 (Al-10Mg) (aluminium); 0.024 Aluminium casting 535.0 (Almag 35) (aluminium)
2. **Al88Mg7Zn5** — wt% {'Al': 82.69, 'Zn': 11.39, 'Mg': 5.92}; rules: dH -0.37 kJ/mol, δ 3.39 %, Ω 9.21, VEC 3.38; would rather be: Al(fcc) 0.79, C14-MgAl 0.14, C14-MgZn 0.07; nearest known: 0.05 Aluminium casting 518.0 (Al-Mg die casting) (aluminium); 0.05 Aluminium casting 520.0 (Al-10Mg) (aluminium); 0.05 Aluminium casting 535.0 (Almag 35) (aluminium)
3. **Al89Cu4Mg3Zn2Mn2** — wt% {'Zn': 4.41, 'Al': 80.88, 'Cu': 8.56, 'Mn': 3.7, 'Mg': 2.46}; rules: dH -1.63 kJ/mol, δ 3.44 %, Ω 2.41, VEC 3.55; would rather be: Al(fcc) 0.71, C1-CuAl 0.12, D022-AlMn 0.08, C14-MgAl 0.06; nearest known: 0.051 Aluminium 7178 (aluminium); 0.051 Aluminium 7068 (aluminium); 0.053 Aluminium 7150 (aluminium)
4. **Al89Mg7Cu4** — wt% {'Al': 84.98, 'Cu': 9.0, 'Mg': 6.02}; rules: dH -0.67 kJ/mol, δ 3.74 %, Ω 4.9, VEC 3.25; would rather be: Al(fcc) 0.67, C14-MgAl 0.21, C1-CuAl 0.12; nearest known: 0.04 Aluminium casting 518.0 (Al-Mg die casting) (aluminium); 0.04 Aluminium casting 535.0 (Almag 35) (aluminium); 0.04 Hydronalium (Al-Mg marine, German historic) (other)
5. **Al90Si4Mg3Zn3** — wt% {'Al': 86.42, 'Mg': 2.6, 'Si': 4.0, 'Zn': 6.98}; rules: dH -3.07 kJ/mol, δ 5.15 %, Ω 1.12, VEC 3.28; would rather be: Al(fcc) 0.90, C14-MgZn 0.04, Si(diamond) 0.03, C1-SiMg 0.02; nearest known: 0.039 Aluminium 7178 (aluminium); 0.039 Aluminium 7068 (aluminium); 0.04 Aluminium 7049 (aluminium)
6. **Al90Cu4Si3Mg3** — wt% {'Al': 85.51, 'Si': 2.97, 'Cu': 8.95, 'Mg': 2.57}; rules: dH -2.61 kJ/mol, δ 4.94 %, Ω 1.34, VEC 3.32; would rather be: Al(fcc) 0.82, C1-CuAl 0.12, C1-SiMg 0.04, Si(diamond) 0.02; nearest known: 0.049 Magsimal-59 (AlMg5Si2Mn structural die casting) (aluminium); 0.054 Aluminium casting 319.0 (aluminium); 0.059 Aluminium casting 355.0 / C355.0 (aluminium)
7. **Al87Mg5Zn5Si2Cu1** — wt% {'Mg': 4.17, 'Cu': 2.18, 'Si': 1.93, 'Zn': 11.22, 'Al': 80.51}; rules: dH -1.77 kJ/mol, δ 4.56 %, Ω 2.41, VEC 3.5; would rather be: Al(fcc) 0.85, C14-MgZn 0.07, C1-SiMg 0.04, C1-CuAl 0.03; nearest known: 0.056 Aluminium 7068 (aluminium); 0.058 Aluminium 7178 (aluminium); 0.059 Aluminium 7049 (aluminium)
8. **Al94Mg2.9Zn2.4Cu0.7** — wt% {'Al': 90.32, 'Zn': 5.59, 'Mg': 2.51, 'Cu': 1.58}; rules: dH -0.17 kJ/mol, δ 2.41 %, Ω 13.2, VEC 3.24; would rather be: Al(fcc) 0.89, C14-MgAl 0.05, C14-MgZn 0.04, C1-CuAl 0.02; nearest known: 0.003 Aluminium 7175 (premium forging 7075) (aluminium); 0.003 Aluminium 7475 (high toughness 7075) (aluminium); 0.005 Aluminium 7075 (aluminium)
9. **Al94.7Mg5Mn0.3** — wt% {'Al': 94.88, 'Mg': 4.51, 'Mn': 0.61}; rules: dH -0.59 kJ/mol, δ 2.65 %, Ω 2.89, VEC 2.96; would rather be: Al(fcc) 0.84, C14-MgAl 0.15, D022-AlMn 0.01; nearest known: 0.003 Aluminium 5182 (can-end stock) (aluminium); 0.003 Aluminium 5024 / AA5028 (Al-Mg-Sc-Zr wrought) (aluminium); 0.004 Aluminium 5083 (aluminium)
10. **Al89Zn6Mg3Si2** — wt% {'Al': 82.16, 'Zn': 13.43, 'Mg': 2.49, 'Si': 1.92}; rules: dH -1.53 kJ/mol, δ 4.15 %, Ω 2.31, VEC 3.53; would rather be: Al(fcc) 0.89, C14-MgZn 0.09, Si(diamond) 0.02; nearest known: 0.045 Aluminium 7068 (aluminium); 0.046 Aluminium 7049 (aluminium); 0.048 Aluminium 7449 (aluminium)
