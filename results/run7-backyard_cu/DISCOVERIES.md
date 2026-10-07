# backyard_cu — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 16

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cu97.2Sn2.8 | near C51000 phosphor bronze A (5 % Sn) | fcc | +0.006 | +0.007 | +0.004 | 648 | 8.78 | 44 | 2.91 | 588 | 250 | 534.2 |
| 2 | Cu93Sn7 | near C90700 tin bronze (89-11) | fcc | +0.032 | +0.034 | +0.027 | 1538 | 8.76 | 38 | 3.16 | 964 | 477 | 490.2 |
| 3 | Cu62Zn31Sn6Ni1 | near C85700 yellow brass casting (63/1/1/35) | fcc | -0.032 | +0.044 | +0.021 | 585 | 8.40 | 31 | 3.37 | 653 | 270 | 381.6 |
| 4 | Cu61Zn18Al14Mn7 | NEW | fcc | -0.106 | +0.040 | +0.012 | 432 | 7.53 | 40 | 2.82 | 265 | 80 | 195.6 |
| 5 | Cu85Al15 | near C61300 aluminium bronze (7 % Al, weldable) | fcc | -0.091 | +0.028 | +0.017 | 769 | 7.83 | 43 | 2.94 | 263 | 78 | 171.6 |
| 6 | Cu90Al10 | NEW | fcc | -0.063 | +0.017 | +0.008 | 602 | 8.12 | 44 | 2.89 | 209 | 52 | 169.0 |
| 7 | Cu63Zn25Mn8Ag4 | NEW | fcc | -0.023 | +0.038 | +0.013 | 459 | 8.32 | 38 | 2.89 | 232 | 60 | 166.4 |
| 8 | Cu70Zn30 | near C26000 cartridge brass (70/30) | fcc | -0.063 | +0.008 | -0.007 | 161 | 8.44 | 37 | 3.07 | 164 | 33 | 163.7 |
| 9 | Cu66Mn20Sn10Mg4 | NEW | fcc | +0.075 | +0.098 | +0.073 | 1190 | 7.94 | 32 | 3.06 | 983 | 483 | 157.5 |
| 10 | Cu59Zn34Al7 | near C86500 manganese bronze (cast, 65 ksi) | fcc | -0.074 | +0.046 | +0.024 | 622 | 7.97 | 34 | 3.14 | 202 | 46 | 111.1 |
| 11 | Cu83Mn10Si5Mg2 | NEW | fcc | +0.010 | +0.068 | +0.052 | 1289 | 8.13 | 45 | 2.85 | 275 | 85 | 74.6 |
| 12 | Cu88Ni9Si2Al1 | near C72500 copper-nickel-tin (CuNi9Sn2) | fcc | -0.018 | +0.034 | +0.023 | 883 | 8.66 | 48 | 2.81 | 63 | 8 | 35.9 |
| 13 | Cu68Mn18Ni10Ag4 | NEW | fcc | +0.086 | +0.102 | +0.078 | 1277 | 8.39 | 50 | 2.55 | 231 | 71 | 32.6 |
| 14 | Cu92.3Si6.6Mn1.1 | near C65500 high-silicon bronze A (Everdur) | fcc | -0.001 | +0.020 | +0.012 | 767 | 8.44 | 42 | 3.13 | 42 | 3 | 30.8 |
| 15 | Cu65Mn15Zn14Si6 | NEW | fcc | +0.010 | +0.112 | +0.086 | 1287 | 7.98 | 42 | 2.81 | 153 | 32 | 17.9 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Cu97.2Sn2.8** — wt% {'Cu': 94.89, 'Sn': 5.11}; rules: dH 0.76 kJ/mol, δ 2.18 %, Ω 1.86, VEC 10.8; would rather be: Cu(fcc) 0.89, D019-CuSn 0.11; nearest known: 0.005 C51000 phosphor bronze A (5 % Sn) (copper); 0.01 C51900 phosphor bronze (6 % Sn) (copper); 0.021 C52100 phosphor bronze C (8 % Sn) (copper)
2. **Cu93Sn7** — wt% {'Cu': 87.67, 'Sn': 12.33}; rules: dH 1.82 kJ/mol, δ 3.36 %, Ω 1.5, VEC 10.51; would rather be: Cu(fcc) 0.72, D019-CuSn 0.28; nearest known: 0.009 C90700 tin bronze (89-11) (copper); 0.014 C52400 phosphor bronze D (10 % Sn) (copper); 0.015 C90800 / C91100 high-tin bronze (12-16 % Sn) (copper)
3. **Cu62Zn31Sn6Ni1** — wt% {'Cu': 58.47, 'Ni': 0.87, 'Zn': 30.09, 'Sn': 10.57}; rules: dH 1.86 kJ/mol, δ 3.47 %, Ω 4.31, VEC 10.88; would rather be: L12-CuZn 0.62, B2-CuZn 0.31, Sn(fcc) 0.04, C1-NiSn 0.03; nearest known: 0.059 C85700 yellow brass casting (63/1/1/35) (copper); 0.066 C48500 (Leaded Naval Brass) (copper); 0.068 CW511L CuZn38As (dezincification-resistant brass, DZR) (copper)
4. **Cu61Zn18Al14Mn7** — wt% {'Zn': 20.24, 'Al': 6.49, 'Cu': 66.65, 'Mn': 6.61}; rules: dH -0.17 kJ/mol, δ 4.06 %, Ω 64.02, VEC 9.78; would rather be: D019-CuAl 0.56, B2-CuZn 0.35, Mn(hcp) 0.07, L12-CuZn 0.02; nearest known: 0.064 C86300 manganese bronze (cast, high strength) (copper); 0.089 C86200 manganese bronze (cast, 90 ksi) (copper); 0.111 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory)
5. **Cu85Al15** — wt% {'Cu': 93.03, 'Al': 6.97}; rules: dH -0.51 kJ/mol, δ 4.11 %, Ω 8.92, VEC 9.8; would rather be: D019-CuAl 0.60, Cu(fcc) 0.40; nearest known: 0.031 C61300 aluminium bronze (7 % Al, weldable) (copper); 0.033 C61400 aluminium bronze (7 % Al, 2 % Fe) (copper); 0.042 C64200 aluminium-silicon bronze (copper)
6. **Cu90Al10** — wt% {'Cu': 95.49, 'Al': 4.51}; rules: dH -0.36 kJ/mol, δ 3.47 %, Ω 9.88, VEC 10.2; would rather be: Cu(fcc) 0.60, D019-CuAl 0.40; nearest known: 0.062 Nordic gold (Cu-Al-Zn-Sn coinage) (copper); 0.081 C61300 aluminium bronze (7 % Al, weldable) (copper); 0.083 C61400 aluminium bronze (7 % Al, 2 % Fe) (copper)
7. **Cu63Zn25Mn8Ag4** — wt% {'Cu': 61.5, 'Ag': 6.63, 'Mn': 6.75, 'Zn': 25.12}; rules: dH 1.16 kJ/mol, δ 2.99 %, Ω 8.29, VEC 10.93; would rather be: L12-CuZn 0.76, B2-CuZn 0.12, Mn(hcp) 0.08, Ag(fcc) 0.04; nearest known: 0.12 C44500 admiralty brass (P) (copper); 0.12 C36000 free-cutting brass (61.5/35.5/3) (copper); 0.12 C44300 admiralty brass (arsenical) (copper)
8. **Cu70Zn30** — wt% {'Cu': 69.39, 'Zn': 30.61}; rules: dH 0.84 kJ/mol, δ 2.12 %, Ω 7.0, VEC 11.3; would rather be: L12-CuZn 0.80, B2-CuZn 0.20; nearest known: 0.007 C26000 cartridge brass (70/30) (copper); 0.026 C44300 admiralty brass (arsenical) (copper); 0.03 C44400 admiralty brass (Sb) (copper)
9. **Cu66Mn20Sn10Mg4** — wt% {'Cu': 63.77, 'Sn': 18.05, 'Mn': 16.71, 'Mg': 1.48}; rules: dH 3.26 kJ/mol, δ 6.04 %, Ω 3.14, VEC 9.14; would rather be: Cu(fcc) 0.58, Mn(hcp) 0.15, C16-MnSn 0.15, C15-MgCu 0.12; nearest known: 0.204 Manganin (copper); 0.204 Manganin Precision Resistor Alloy (Cu-12Mn-4Ni) (magnetic_electrical); 0.204 Manganin (Cu-12Mn-2Ni, precision resistance alloy) (magnetic_electrical)
10. **Cu59Zn34Al7** — wt% {'Cu': 60.84, 'Zn': 36.09, 'Al': 3.07}; rules: dH 0.73 kJ/mol, δ 3.28 %, Ω 10.81, VEC 10.78; would rather be: B2-CuZn 0.64, D019-CuAl 0.28, L12-CuZn 0.08; nearest known: 0.046 C86500 manganese bronze (cast, 65 ksi) (copper); 0.06 C85700 yellow brass casting (63/1/1/35) (copper); 0.068 C67500 manganese bronze (wrought, 'A') (copper)
