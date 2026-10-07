# 3d_hea — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 14

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fe30Mn25Cu15Ti11Co11Ni8 | NEW | bcc | +0.032 | +0.179 | +0.135 | 1233 | 7.68 | 40 | 3.20 | 807 | 274 | 27.5 |
| 2 | Ni34Mn32Co20Cr8Al6 | NEW | fcc | -0.038 | +0.119 | +0.082 | 971 | 8.01 | 75 | 1.48 | 301 | 114 | 22.8 |
| 3 | Fe32Mn22Cu20Co16Ti10 | NEW | bcc | +0.074 | +0.193 | +0.153 | 1449 | 7.78 | 47 | 2.73 | 847 | 310 | 18.6 |
| 4 | Mn33Fe30Ni25Cu7Ti5 | NEW | bcc | +0.050 | +0.166 | +0.129 | 1366 | 7.88 | 35 | 3.28 | 433 | 91 | 17.0 |
| 5 | Mn32Fe30Cu16Ni16Al6 | NEW | fcc | +0.036 | +0.148 | +0.110 | 1162 | 7.80 | 66 | 1.73 | 331 | 126 | 14.6 |
| 6 | Ni33Cr30Co23Al14 | NEW | fcc | -0.026 | +0.198 | +0.163 | 1714 | 7.60 | 71 | 2.30 | 722 | 370 | 12.2 |
| 7 | Fe30Co23Cu17Mn17Al8V5 | NEW | fcc | +0.022 | +0.182 | +0.140 | 1281 | 7.70 | 53 | 2.42 | 365 | 134 | 11.1 |
| 8 | Mn31Fe23Cu18Ni11Al10Co7 | NEW | fcc | +0.014 | +0.174 | +0.131 | 1210 | 7.59 | 62 | 1.83 | 402 | 164 | 10.7 |
| 9 | Co20Cr20Fe20Mn20Ni20 | near Cantor alloy CoCrFeMnNi (equiatomic, FCC) | fcc | +0.056 | +0.117 | +0.075 | 842 | 8.29 | 75 | 1.71 | 92 | 18 | 9.6 |
| 10 | Mn34Fe26Cu18Co16Al6 | NEW | fcc | +0.057 | +0.159 | +0.120 | 1240 | 7.88 | 59 | 1.74 | 272 | 91 | 9.3 |
| 11 | Fe22Cu20Ni18Cr17Al14Co9 | NEW | fcc | +0.018 | +0.221 | +0.176 | 1462 | 7.47 | 59 | 2.33 | 525 | 232 | 6.5 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Fe30Mn25Cu15Ti11Co11Ni8** — wt% {'Ti': 9.33, 'Co': 11.48, 'Cu': 16.88, 'Ni': 8.32, 'Fe': 29.67, 'Mn': 24.32}; rules: dH -4.29 kJ/mol, δ 5.1 %, Ω 5.45, VEC 8.03; would rather be: SIGMA-FeMn 0.27, B2-CoFe 0.22, Cu(fcc) 0.15, C15-TiFe 0.15; nearest known: —
2. **Ni34Mn32Co20Cr8Al6** — wt% {'Ni': 36.22, 'Cr': 7.55, 'Co': 21.39, 'Mn': 31.91, 'Al': 2.94}; rules: dH -9.93 kJ/mol, δ 3.46 %, Ω 1.98, VEC 8.1; would rather be: L12-NiMn 0.45, L21-Co2MnAl 0.24, L12-MnCo 0.13, B2-CoMn 0.09; nearest known: —
3. **Fe32Mn22Cu20Co16Ti10** — wt% {'Co': 16.58, 'Ti': 8.42, 'Cu': 22.34, 'Mn': 21.25, 'Fe': 31.42}; rules: dH -1.5 kJ/mol, δ 4.84 %, Ω 14.21, VEC 8.14; would rather be: B2-CoFe 0.32, Cu(fcc) 0.20, SIGMA-FeMn 0.18, C14-TiMn 0.15; nearest known: —
4. **Mn33Fe30Ni25Cu7Ti5** — wt% {'Mn': 32.15, 'Fe': 29.71, 'Ti': 4.24, 'Ni': 26.02, 'Cu': 7.89}; rules: dH -4.92 kJ/mol, δ 3.74 %, Ω 3.97, VEC 8.18; would rather be: SIGMA-FeMn 0.45, L12-NiTi 0.20, Fe(bcc) 0.15, L12-NiMn 0.13; nearest known: —
5. **Mn32Fe30Cu16Ni16Al6** — wt% {'Fe': 30.18, 'Cu': 18.32, 'Al': 2.92, 'Mn': 31.67, 'Ni': 16.92}; rules: dH -1.43 kJ/mol, δ 3.25 %, Ω 13.58, VEC 8.18; would rather be: SIGMA-FeMn 0.37, L21-Ni2AlMn 0.24, Fe(bcc) 0.18, Cu(fcc) 0.16; nearest known: —
6. **Ni33Cr30Co23Al14** — wt% {'Ni': 37.03, 'Cr': 29.83, 'Al': 7.22, 'Co': 25.92}; rules: dH -12.07 kJ/mol, δ 4.87 %, Ω 1.63, VEC 7.59; would rather be: L12-NiAl 0.44, Cr(bcc) 0.30, Co(hcp) 0.20, L10-CoAl 0.06; nearest known: 0.139 CoNiCrAlY (Co-32Ni-21Cr-8Al-0.5Y, Amdry 995 / LCO-22 overlay coating) (other); 0.14 CoCrNi medium-entropy alloy (equiatomic, FCC) (high_entropy); 0.148 Haynes HR-160 (nickel)
7. **Fe30Co23Cu17Mn17Al8V5** — wt% {'V': 4.62, 'Co': 24.58, 'Cu': 19.59, 'Al': 3.91, 'Fe': 30.37, 'Mn': 16.93}; rules: dH -1.73 kJ/mol, δ 3.76 %, Ω 12.88, VEC 8.02; would rather be: L21-Co2MnAl 0.32, Fe(bcc) 0.21, Cu(fcc) 0.17, B2-CoFe 0.14; nearest known: —
8. **Mn31Fe23Cu18Ni11Al10Co7** — wt% {'Co': 7.56, 'Ni': 11.83, 'Fe': 23.53, 'Al': 4.94, 'Mn': 31.2, 'Cu': 20.95}; rules: dH -3.07 kJ/mol, δ 3.99 %, Ω 6.96, VEC 8.02; would rather be: SIGMA-FeMn 0.35, Cu(fcc) 0.18, L21-Ni2AlMn 0.18, L21-Co2MnAl 0.14; nearest known: —
9. **Co20Cr20Fe20Mn20Ni20** — wt% {'Co': 21.02, 'Cr': 18.54, 'Fe': 19.92, 'Mn': 19.59, 'Ni': 20.93}; rules: dH -4.16 kJ/mol, δ 1.12 %, Ω 5.79, VEC 8.0; would rather be: B2-CoFe 0.35, L12-NiMn 0.27, Cr(bcc) 0.20, L12-MnCo 0.11; nearest known: 0.0 Cantor alloy CoCrFeMnNi (equiatomic, FCC) (high_entropy); 0.001 Cantor Alloy (Equiatomic CoCrFeMnNi High-Entropy Alloy) (high_entropy); 0.02 CrMnFeCoNi-C (interstitial Cantor) (high_entropy)
10. **Mn34Fe26Cu18Co16Al6** — wt% {'Cu': 20.54, 'Al': 2.91, 'Mn': 33.54, 'Fe': 26.07, 'Co': 16.93}; rules: dH -0.16 kJ/mol, δ 3.15 %, Ω 121.42, VEC 8.06; would rather be: SIGMA-FeMn 0.42, L21-Co2MnAl 0.24, Cu(fcc) 0.18, Fe(bcc) 0.08; nearest known: —
