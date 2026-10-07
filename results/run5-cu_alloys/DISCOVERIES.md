# cu_alloys — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 14

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cu58Zn32Al10 | NEW | fcc | -0.104 | +0.025 | +0.001 | 315 | 7.76 | 36 | 3.03 | 229 | 57 | 222.5 |
| 2 | Cu70Zn30 | near C26000 cartridge brass (70/30) | fcc | -0.065 | +0.008 | -0.007 | 161 | 8.44 | 37 | 3.07 | 164 | 33 | 163.7 |
| 3 | Cu60Zn19Al12Mn9 | NEW | fcc | -0.077 | +0.050 | +0.021 | 527 | 7.56 | 41 | 2.76 | 254 | 76 | 149.1 |
| 4 | Cu55Zn35Mn6Co4 | NEW | fcc | -0.032 | +0.047 | +0.021 | 548 | 8.23 | 38 | 2.87 | 196 | 46 | 115.1 |
| 5 | Cu50Zn33Ni17 | NEW | fcc | -0.060 | +0.068 | +0.042 | 777 | 8.49 | 43 | 2.74 | 261 | 78 | 92.0 |
| 6 | Cu55Ni45 | near Constantan Precision Resistance Alloy (Cu-44Ni) | fcc | +0.014 | +0.014 | -0.004 | 237 | 8.89 | 63 | 2.42 | 79 | 13 | 78.6 |
| 7 | Cu55Zn24Al17Ni4 | NEW | fcc | -0.100 | +0.082 | +0.053 | 861 | 7.43 | 38 | 2.93 | 285 | 87 | 75.1 |
| 8 | Cu59Mn20Al17Fe4 | NEW | fcc | -0.032 | +0.095 | +0.068 | 1039 | 7.31 | 48 | 2.36 | 328 | 116 | 60.5 |
| 9 | Cu52Ni38Mn7Co3 | NEW | fcc | +0.006 | +0.041 | +0.015 | 475 | 8.67 | 63 | 2.36 | 75 | 12 | 51.2 |
| 10 | Cu72Ni28 | near C71300 copper-nickel 75/25 (coinage cupronickel) | fcc | +0.013 | +0.013 | -0.003 | 248 | 8.85 | 56 | 2.55 | 51 | 6 | 51.2 |
| 11 | Cu58Mn16Al16Zn10 | NEW | fcc | -0.025 | +0.112 | +0.082 | 1144 | 7.33 | 43 | 2.56 | 288 | 93 | 36.7 |
| 12 | Cu58Ni34Fe4Co4 | NEW | fcc | +0.046 | +0.061 | +0.036 | 749 | 8.83 | 63 | 2.43 | 85 | 14 | 34.1 |
| 13 | Cu51Zn32Mn13Fe4 | NEW | fcc | +0.036 | +0.106 | +0.078 | 1119 | 8.05 | 41 | 2.71 | 213 | 54 | 30.5 |
| 14 | Cu58Ni20Al17Fe5 | NEW | fcc | -0.085 | +0.145 | +0.117 | 1549 | 7.71 | 52 | 2.60 | 457 | 185 | 24.4 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Cu58Zn32Al10** — wt% {'Cu': 60.93, 'Zn': 34.6, 'Al': 4.46}; rules: dH 0.64 kJ/mol, δ 3.6 %, Ω 13.08, VEC 10.52; would rather be: B2-CuZn 0.60, L12-CuAl 0.32, L21-Cu2ZnAl 0.08; nearest known: 0.076 C86500 manganese bronze (cast, 65 ksi) (copper); 0.089 Cu-Zn-Al (Copper-Zinc-Aluminium Shape Memory Alloy) (shape_memory); 0.09 C85700 yellow brass casting (63/1/1/35) (copper)
2. **Cu70Zn30** — wt% {'Cu': 69.39, 'Zn': 30.61}; rules: dH 0.84 kJ/mol, δ 2.12 %, Ω 7.0, VEC 11.3; would rather be: L12-CuZn 0.80, B2-CuZn 0.20; nearest known: 0.007 C26000 cartridge brass (70/30) (copper); 0.026 C44300 admiralty brass (arsenical) (copper); 0.03 C44400 admiralty brass (Sb) (copper)
3. **Cu60Zn19Al12Mn9** — wt% {'Cu': 64.91, 'Mn': 8.42, 'Al': 5.51, 'Zn': 21.16}; rules: dH -0.11 kJ/mol, δ 3.88 %, Ω 100.57, VEC 9.87; would rather be: L12-CuAl 0.48, B2-CuZn 0.33, L12-CuZn 0.10, Mn(hcp) 0.09; nearest known: 0.064 C86300 manganese bronze (cast, high strength) (copper); 0.082 C86200 manganese bronze (cast, 90 ksi) (copper); 0.111 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory)
4. **Cu55Zn35Mn6Co4** — wt% {'Cu': 55.04, 'Co': 3.71, 'Mn': 5.19, 'Zn': 36.05}; rules: dH 0.99 kJ/mol, δ 2.35 %, Ω 9.57, VEC 11.03; would rather be: B2-CuZn 0.50, L12-CuZn 0.40, B2-CoMn 0.06, L12-MnCo 0.04; nearest known: 0.094 C86500 manganese bronze (cast, 65 ksi) (copper); 0.096 C67500 manganese bronze (wrought, 'A') (copper); 0.1 C36000 free-cutting brass (61.5/35.5/3) (copper)
5. **Cu50Zn33Ni17** — wt% {'Cu': 50.17, 'Zn': 34.08, 'Ni': 15.75}; rules: dH 0.0 kJ/mol, δ 2.78 %, Ω 25310.14, VEC 11.16; would rather be: L12-CuZn 0.64, L10-ZnNi 0.34, Cu(fcc) 0.02; nearest known: 0.077 C77000 nickel silver 55-18 (spring grade) (copper); 0.104 C79200 leaded nickel silver 59-12 (free-cutting) (copper); 0.156 C75700 nickel silver 65-12 (copper)
6. **Cu55Ni45** — wt% {'Cu': 56.96, 'Ni': 43.04}; rules: dH 3.96 kJ/mol, δ 1.58 %, Ω 2.2, VEC 10.55; would rather be: Cu(fcc) 0.55, Ni(fcc) 0.45; nearest known: 0.023 Constantan Precision Resistance Alloy (Cu-44Ni) (magnetic_electrical); 0.023 Constantan (Cu-45Ni, thermocouple and resistance alloy) (magnetic_electrical); 0.026 Constantan (copper)
7. **Cu55Zn24Al17Ni4** — wt% {'Cu': 60.7, 'Al': 7.97, 'Ni': 4.08, 'Zn': 27.26}; rules: dH -0.27 kJ/mol, δ 4.35 %, Ω 38.01, VEC 9.84; would rather be: B2-CuZn 0.40, L12-CuAl 0.36, L21-Cu2ZnAl 0.16, B2-AlNi 0.08; nearest known: 0.108 C86300 manganese bronze (cast, high strength) (copper); 0.12 Cu-Zn-Al (Copper-Zinc-Aluminium Shape Memory Alloy) (shape_memory); 0.125 C86200 manganese bronze (cast, 90 ksi) (copper)
8. **Cu59Mn20Al17Fe4** — wt% {'Mn': 19.87, 'Al': 8.29, 'Fe': 4.04, 'Cu': 67.8}; rules: dH -0.17 kJ/mol, δ 4.44 %, Ω 69.8, VEC 8.72; would rather be: L12-CuAl 0.68, SIGMA-FeMn 0.12, Mn(hcp) 0.12, Cu(fcc) 0.08; nearest known: 0.091 C95700 manganese-aluminium bronze (Cu-Mn-Al propeller alloy, 'Novoston') (copper); 0.115 Heusler alloy Cu2MnAl (ferromagnetic without ferromagnetic elements) (magnetic_electrical); 0.13 Cu-Al-Mn shape-memory alloy (shape_memory)
9. **Cu52Ni38Mn7Co3** — wt% {'Cu': 54.2, 'Mn': 6.31, 'Co': 2.9, 'Ni': 36.59}; rules: dH 3.23 kJ/mol, δ 1.5 %, Ω 3.92, VEC 10.28; would rather be: Cu(fcc) 0.52, L12-NiMn 0.28, Ni(fcc) 0.17, Co(hcp) 0.03; nearest known: 0.089 Constantan Precision Resistance Alloy (Cu-44Ni) (magnetic_electrical); 0.089 Constantan (Cu-45Ni, thermocouple and resistance alloy) (magnetic_electrical); 0.094 Constantan (copper)
10. **Cu72Ni28** — wt% {'Cu': 73.57, 'Ni': 26.43}; rules: dH 3.23 kJ/mol, δ 1.42 %, Ω 2.23, VEC 10.72; would rather be: Cu(fcc) 0.72, Ni(fcc) 0.28; nearest known: 0.015 C71300 copper-nickel 75/25 (coinage cupronickel) (copper); 0.051 C71500 copper-nickel 70/30 (CuNi30Mn1Fe) (copper); 0.067 C97800 cast nickel silver (25% Ni) (copper)
