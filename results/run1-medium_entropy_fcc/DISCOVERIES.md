# medium_entropy_fcc — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 13

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Co33.33Cr33.33Ni33.33 | near CoCrNi medium-entropy alloy (equiatomic, FCC) | fcc | +0.085 | +0.087 | +0.058 | 916 | 8.50 | 94 | 2.05 | 151 | 45 | 35.2 |
| 2 | Ni40Fe29Cr17V14 | NEW | fcc | +0.005 | +0.103 | +0.070 | 920 | 8.02 | 53 | 3.05 | 197 | 49 | 34.6 |
| 3 | Fe47Cu28Ni14Al11 | NEW | fcc | -0.009 | +0.141 | +0.110 | 1335 | 7.66 | 52 | 2.70 | 471 | 191 | 30.4 |
| 4 | Fe41Co30Cu17Al12 | NEW | fcc | -0.025 | +0.148 | +0.115 | 1340 | 7.68 | 51 | 2.87 | 495 | 201 | 27.9 |
| 5 | Cr45Ni44Co11 | NEW | fcc | +0.083 | +0.084 | +0.060 | 1018 | 8.25 | 65 | 2.60 | 103 | 19 | 23.2 |
| 6 | Ni47Mn33Co20 | NEW | fcc | +0.003 | +0.098 | +0.071 | 1087 | 8.34 | 81 | 1.49 | 53 | 8 | 5.5 |
| 7 | Mn33Co29Cu28Al10 | NEW | fcc | +0.024 | +0.188 | +0.155 | 1667 | 7.67 | 56 | 1.89 | 304 | 107 | 4.5 |
| 8 | Co47Cr38V15 | NEW | bcc | +0.080 | +0.180 | +0.154 | 2078 | 8.09 | 34 | 5.23 | 196 | 23 | 4.1 |
| 9 | Ni44Cr44Fe12 | NEW | fcc | +0.112 | +0.155 | +0.130 | 1846 | 8.12 | 60 | 2.70 | 104 | 19 | 4.0 |
| 10 | Co44Cu30Mn26 | NEW | fcc | +0.111 | +0.135 | +0.107 | 1462 | 8.38 | 67 | 1.80 | 82 | 15 | 3.9 |
| 11 | Fe34Cr28Mn25Cu13 | NEW | bcc | +0.151 | +0.157 | +0.123 | 1366 | 7.86 | 66 | 1.83 | 97 | 12 | 3.2 |
| 12 | Cr36Ni28Cu26Al10 | NEW | fcc | +0.057 | +0.224 | +0.190 | 1993 | 7.57 | 48 | 2.73 | 290 | 93 | 2.5 |
| 13 | Fe45Cr43Cu12 | NEW | bcc | +0.143 | +0.143 | +0.118 | 1696 | 7.76 | 72 | 2.07 | 10 | 0 | 0.6 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Co33.33Cr33.33Ni33.33** — wt% {'Co': 34.74, 'Cr': 30.65, 'Ni': 34.6}; rules: dH -4.89 kJ/mol, δ 1.35 %, Ω 3.54, VEC 8.33; would rather be: L12-NiCr 0.44, Co(hcp) 0.33, Cr(bcc) 0.22; nearest known: 0.012 CoCrNi medium-entropy alloy (equiatomic, FCC) (high_entropy); 0.095 Haynes HR-160 (nickel); 0.108 MP35N (35Co-35Ni-20Cr-10Mo multiphase) (cobalt)
2. **Ni40Fe29Cr17V14** — wt% {'Ni': 42.19, 'Cr': 15.89, 'V': 12.82, 'Fe': 29.1}; rules: dH -8.39 kJ/mol, δ 2.6 %, Ω 2.44, VEC 8.04; would rather be: A15-NiV 0.53, Fe(bcc) 0.29, Cr(bcc) 0.17, L21-V2CrFe 0.01; nearest known: 0.14 Incoloy 825 (Ni-Fe-Cr-Mo-Cu) (nickel); 0.14 Nimonic PE16 (Ni-Fe-Cr, nuclear) (nickel); 0.14 Inconel 706 (nickel)
3. **Fe47Cu28Ni14Al11** — wt% {'Cu': 32.22, 'Fe': 47.53, 'Ni': 14.88, 'Al': 5.37}; rules: dH 3.19 kJ/mol, δ 4.19 %, Ω 5.05, VEC 8.57; would rather be: Fe(bcc) 0.47, Cu(fcc) 0.28, B2-NiAl 0.19, L12-NiAl 0.06; nearest known: 0.232 Alnico 2 (magnetic_electrical)
4. **Fe41Co30Cu17Al12** — wt% {'Cu': 19.78, 'Co': 32.37, 'Al': 5.93, 'Fe': 41.92}; rules: dH -0.63 kJ/mol, δ 4.37 %, Ω 27.52, VEC 8.21; would rather be: L21-Co2AlFe 0.48, Fe(bcc) 0.23, Cu(fcc) 0.17, B2-CoFe 0.12; nearest known: 0.214 Alnico 8 (Cast High Coercivity Fe-Co-Ni-Al-Ti Permanent Magnet) (magnetic_electrical); 0.224 Alnico 9 (magnetic_electrical); 0.233 Alnico 5 (Fe-24Co-14Ni-8Al-3Cu, cast anisotropic magnet) (magnetic_electrical)
5. **Cr45Ni44Co11** — wt% {'Ni': 46.36, 'Co': 11.64, 'Cr': 42.0}; rules: dH -6.34 kJ/mol, δ 1.52 %, Ω 2.45, VEC 8.09; would rather be: L12-NiCr 0.59, Cr(bcc) 0.30, Co(hcp) 0.11; nearest known: 0.11 Alloy 671 (Ni-48Cr, fuel-ash corrosion) (nickel); 0.185 Inconel 740H (nickel); 0.19 Hastelloy G-35 (nickel)
6. **Ni47Mn33Co20** — wt% {'Ni': 47.97, 'Mn': 31.53, 'Co': 20.5}; rules: dH -6.28 kJ/mol, δ 1.06 %, Ω 2.3, VEC 8.81; would rather be: L12-NiMn 0.63, B2-CoMn 0.35, Co(hcp) 0.03; nearest known: 0.214 Ni-Mn-Ga magnetic shape-memory alloy (Ni2MnGa Heusler, Ni-29Mn-21Ga at%) (shape_memory)
7. **Mn33Co29Cu28Al10** — wt% {'Mn': 32.54, 'Co': 30.68, 'Cu': 31.94, 'Al': 4.84}; rules: dH -3.31 kJ/mol, δ 3.92 %, Ω 4.9, VEC 8.3; would rather be: L21-Co2MnAl 0.40, L12-MnCo 0.28, Cu(fcc) 0.28, B2-CoMn 0.04; nearest known: —
8. **Co47Cr38V15** — wt% {'Co': 50.27, 'Cr': 35.86, 'V': 13.87}; rules: dH -7.26 kJ/mol, δ 2.4 %, Ω 2.29, VEC 7.26; would rather be: L12-CoV 0.60, Cr(bcc) 0.38, Co(hcp) 0.02; nearest known: 0.2 Stellite 3 (Co-31Cr-12.5W-2.4C, PM) (cobalt); 0.207 Stellite 12 (Co-30Cr-8W-1.4C) (cobalt); 0.209 Stellite 6B (cobalt)
9. **Ni44Cr44Fe12** — wt% {'Ni': 46.61, 'Cr': 41.29, 'Fe': 12.1}; rules: dH -6.05 kJ/mol, δ 1.49 %, Ω 2.6, VEC 8.0; would rather be: L12-NiFe 0.48, Cr(bcc) 0.41, L12-NiCr 0.11; nearest known: 0.115 Alloy 671 (Ni-48Cr, fuel-ash corrosion) (nickel); 0.132 Hastelloy G-30 (Ni-Cr-Fe-Mo-Cu-Nb, phosphoric acid) (nickel); 0.152 Inconel 690 (Ni-Cr-Fe 30 % Cr, nuclear) (nickel)
10. **Co44Cu30Mn26** — wt% {'Mn': 24.1, 'Co': 43.74, 'Cu': 32.16}; rules: dH 2.13 kJ/mol, δ 1.04 %, Ω 6.62, VEC 9.08; would rather be: B2-CoMn 0.52, Cu(fcc) 0.30, Co(hcp) 0.18; nearest known: —
