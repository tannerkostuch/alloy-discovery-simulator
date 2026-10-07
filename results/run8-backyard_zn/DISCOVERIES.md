# backyard_zn — ranked by stiff_stable

objective: shear modulus times the phase and ductility factors — for lattices the strengthening model does not cover (HCP zinc, magnesium)
engine: mace-medium-mpa-0-cpu · candidates evaluated: 15

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Zn89.7Al9.3Cu1 | near Zamak 5 (Zn-4Al-1Cu-0.04Mg, alloy 5 / AC41A) | hcp | +0.004 | +0.010 | +0.000 | 315 | 6.73 | 22 | 2.74 | 0 | 0 | 21.9 |
| 2 | Zn90.7Al9.3 | near Zamak 7 (Zn-4Al-0.012Mg-0.01Ni, alloy 7 / AG40B) | hcp | +0.008 | +0.008 | -0.000 | 296 | 6.71 | 21 | 2.80 | 0 | 0 | 21.4 |
| 3 | Zn88Al12 | near Galfan Coating Alloy | hcp | +0.001 | +0.001 | -0.009 | 26 | 6.56 | 20 | 2.98 | 0 | 0 | 20.5 |
| 4 | Zn94Cu6 | near Bidri Zinc Art Alloy | hcp | -0.020 | -0.004 | -0.010 | 0 | 7.48 | 19 | 3.52 | 0 | 0 | 19.4 |
| 5 | Zn97Mg3 | near Rolled zinc Zn-Cu-Ti (Zn-0.7Cu-0.1Ti, EN 988) | hcp | -0.003 | +0.009 | +0.006 | 784 | 6.95 | 19 | 2.71 | 0 | 0 | 16.3 |
| 6 | Zn73Al24Cu3 | near Kayem 2 Press Tool Zinc Alloy | hcp | +0.013 | +0.029 | +0.012 | 499 | 6.10 | 17 | 3.78 | 0 | 0 | 13.1 |
| 7 | Zn74Al19Cu6Ag1 | near Kayem 2 Press Tool Zinc Alloy | hcp | +0.003 | +0.037 | +0.017 | 565 | 6.44 | 19 | 3.34 | 0 | 0 | 12.6 |
| 8 | Zn70Al30 | NEW | hcp | +0.024 | +0.024 | +0.008 | 460 | 5.73 | 14 | 4.62 | 0 | 0 | 11.4 |
| 9 | Zn71Al21Cu6Mg2 | near Kayem 2 Press Tool Zinc Alloy | hcp | -0.000 | +0.041 | +0.019 | 575 | 6.15 | 17 | 3.65 | 0 | 0 | 10.5 |
| 10 | Zn71Al25Mg3Ag1 | near ZA-12 Zinc-Aluminum Alloy | hcp | +0.020 | +0.033 | +0.014 | 517 | 5.82 | 14 | 4.62 | 0 | 0 | 9.7 |
| 11 | Zn52.4Al46Cu1.6 | near ZA-27 Zinc-Aluminum Alloy | fcc | +0.015 | +0.024 | +0.004 | 359 | 5.00 | 8 | 8.33 | 1 | 0 | 7.6 |
| 12 | Zn79Al18Ag2Mg1 | near ZA-8 Zinc-Aluminum Alloy | fcc | +0.012 | +0.019 | +0.003 | 363 | 6.31 | 4 | 16.02 | 0 | 0 | 0.4 |
| 13 | Zn78Al16Mg3Cu3 | near ZA-8 Zinc-Aluminum Alloy | fcc | +0.006 | +0.034 | +0.016 | 572 | 6.24 | 5 | 14.03 | 0 | 0 | 0.3 |
| 14 | Zn77Al20Mg3 | near ZA-12 Zinc-Aluminum Alloy | fcc | +0.016 | +0.028 | +0.012 | 520 | 6.01 | 3 | 19.60 | 0 | 0 | 0.2 |
| 15 | Zn84Al13Mg3 | near Galfan Coating Alloy | fcc | +0.022 | +0.034 | +0.021 | 765 | 6.37 | 3 | 23.93 | 0 | 0 | 0.2 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Zn89.7Al9.3Cu1** — wt% {'Zn': 94.91, 'Al': 4.06, 'Cu': 1.03}; rules: dH 0.37 kJ/mol, δ 2.0 %, Ω 5.98, VEC 11.15; would rather be: Zn(hcp) 0.90, Al(fcc) 0.07, C1-CuAl 0.03; nearest known: 0.002 Zamak 5 (Zn-4Al-1Cu-0.04Mg, alloy 5 / AC41A) (zinc); 0.01 Zamak 3 (Zn-4Al-0.04Mg, alloy 3 / AG40A) (zinc); 0.011 Zamak 7 (Zn-4Al-0.012Mg-0.01Ni, alloy 7 / AG40B) (zinc)
2. **Zn90.7Al9.3** — wt% {'Zn': 95.94, 'Al': 4.06}; rules: dH 0.34 kJ/mol, δ 1.94 %, Ω 5.45, VEC 11.16; would rather be: Zn(hcp) 0.91, Al(fcc) 0.09; nearest known: 0.001 Zamak 7 (Zn-4Al-0.012Mg-0.01Ni, alloy 7 / AG40B) (zinc); 0.003 Zamak 3 (Zn-4Al-0.04Mg, alloy 3 / AG40A) (zinc); 0.012 Zamak 5 (Zn-4Al-1Cu-0.04Mg, alloy 5 / AC41A) (zinc)
3. **Zn88Al12** — wt% {'Zn': 94.67, 'Al': 5.33}; rules: dH 0.42 kJ/mol, δ 2.17 %, Ω 5.21, VEC 10.92; would rather be: Zn(hcp) 0.88, Al(fcc) 0.12; nearest known: 0.007 Galfan Coating Alloy (zinc); 0.007 Galfan Zn-5Al-mischmetal (hot-dip coating alloy) (zinc); 0.028 Zamak 7 (Zn-4Al-0.012Mg-0.01Ni, alloy 7 / AG40B) (zinc)
4. **Zn94Cu6** — wt% {'Zn': 94.16, 'Cu': 5.84}; rules: dH 0.23 kJ/mol, δ 1.07 %, Ω 6.13, VEC 11.94; would rather be: Zn(hcp) 0.76, D019-ZnCu 0.24; nearest known: 0.009 Bidri Zinc Art Alloy (zinc); 0.019 Bidri (Zn-4Cu Indian metalwork alloy) (zinc); 0.052 US One-Cent Coin Zinc Core Alloy (zinc)
5. **Zn97Mg3** — wt% {'Zn': 98.86, 'Mg': 1.14}; rules: dH -0.47 kJ/mol, δ 3.29 %, Ω 1.68, VEC 11.7; would rather be: Zn(hcp) 0.91, C14-MgZn 0.09; nearest known: 0.03 Rolled zinc Zn-Cu-Ti (Zn-0.7Cu-0.1Ti, EN 988) (zinc); 0.03 Copper-plated zinc coinage (US cent 1982-, Zn-0.8Cu core) (zinc); 0.03 Zinc anode alloy (MIL-DTL-18001 / ASTM B418 Type I, Zn-0.5Al-0.1Cd) (zinc)
6. **Zn73Al24Cu3** — wt% {'Al': 11.54, 'Zn': 85.07, 'Cu': 3.4}; rules: dH 0.76 kJ/mol, δ 3.0 %, Ω 5.71, VEC 9.81; would rather be: Zn(hcp) 0.73, Al(fcc) 0.18, C1-CuAl 0.09; nearest known: 0.028 Kayem 2 Press Tool Zinc Alloy (zinc); 0.032 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.033 ZA-12 Zinc-Aluminum Alloy (zinc)
7. **Zn74Al19Cu6Ag1** — wt% {'Zn': 82.85, 'Ag': 1.85, 'Al': 8.78, 'Cu': 6.53}; rules: dH 0.55 kJ/mol, δ 2.99 %, Ω 8.92, VEC 10.22; would rather be: Zn(hcp) 0.71, C1-CuAl 0.18, Al(fcc) 0.07, D019-ZnAg 0.04; nearest known: 0.034 Kayem 2 Press Tool Zinc Alloy (zinc); 0.062 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.063 ZA-12 Zinc-Aluminum Alloy (zinc)
8. **Zn70Al30** — wt% {'Al': 15.02, 'Zn': 84.98}; rules: dH 0.84 kJ/mol, δ 3.02 %, Ω 4.63, VEC 9.3; would rather be: Zn(hcp) 0.70, Al(fcc) 0.30; nearest known: 0.07 ZA-12 Zinc-Aluminum Alloy (zinc); 0.07 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.088 Kayem 2 Press Tool Zinc Alloy (zinc)
9. **Zn71Al21Cu6Mg2** — wt% {'Al': 10.05, 'Zn': 82.33, 'Mg': 0.86, 'Cu': 6.76}; rules: dH 0.44 kJ/mol, δ 3.92 %, Ω 12.14, VEC 9.85; would rather be: Zn(hcp) 0.67, C1-CuAl 0.18, Al(fcc) 0.09, C14-MgZn 0.06; nearest known: 0.043 Kayem 2 Press Tool Zinc Alloy (zinc); 0.072 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.073 ZA-12 Zinc-Aluminum Alloy (zinc)
10. **Zn71Al25Mg3Ag1** — wt% {'Zn': 84.45, 'Mg': 1.33, 'Al': 12.27, 'Ag': 1.96}; rules: dH 0.14 kJ/mol, δ 4.11 %, Ω 32.83, VEC 9.44; would rather be: Zn(hcp) 0.66, Al(fcc) 0.24, C14-MgZn 0.07, L21-Ag2MgAl 0.02; nearest known: 0.059 ZA-12 Zinc-Aluminum Alloy (zinc); 0.059 ZA-12 (Zn-11Al-0.8Cu-0.02Mg) (zinc); 0.077 Kayem 2 Press Tool Zinc Alloy (zinc)
