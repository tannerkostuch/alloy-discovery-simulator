# ti_light_bcc — ranked by specific_strength

objective: yield stress at 300 K per density (MPa per g/cm³), single-phase and ductile favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 13

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ti45Mo35V11Zr9 | NEW | bcc | -0.015 | +0.055 | +0.024 | 536 | 6.93 | 34 | 3.97 | 795 | 321 | 62.8 |
| 2 | Ti40Zr32Mo28 | NEW | bcc | +0.020 | +0.077 | +0.049 | 821 | 6.78 | 29 | 4.10 | 922 | 403 | 40.1 |
| 3 | Ti54Zr34Ta6Cr6 | NEW | bcc | +0.078 | +0.090 | +0.063 | 1002 | 6.24 | 21 | 4.72 | 645 | 220 | 21.6 |
| 4 | Ti52Zr20Al10Ta10Nb8 | NEW | bcc | -0.016 | +0.100 | +0.066 | 880 | 6.47 | 26 | 4.03 | 508 | 167 | 15.0 |
| 5 | Ti52Zr35V13 | NEW | bcc | +0.090 | +0.090 | +0.065 | 1078 | 5.59 | 14 | 5.91 | 412 | 85 | 14.4 |
| 6 | Ti48Al15Mo13Cr12V12 | NEW | bcc | -0.087 | +0.128 | +0.091 | 1052 | 5.62 | 44 | 2.88 | 761 | 317 | 13.8 |
| 7 | Ti69.7Nb23.7Zr4.8Ta1.8 | near Ti-35Nb-7Zr-5Ta (TNZT / Tiadyne 1610) | bcc | +0.046 | +0.046 | +0.025 | 662 | 5.89 | 19 | 5.94 | 125 | 14 | 11.3 |
| 8 | Ti51V35Nb14 | NEW | bcc | +0.063 | +0.096 | +0.070 | 1126 | 5.79 | 22 | 4.92 | 343 | 68 | 10.2 |
| 9 | Ti49Zr15V13Cr13Al10 | NEW | bcc | +0.023 | +0.158 | +0.122 | 1311 | 5.33 | 31 | 3.46 | 1117 | 494 | 10.0 |
| 10 | Ti51Nb24Cr15Al10 | NEW | bcc | -0.009 | +0.122 | +0.091 | 1181 | 5.83 | 31 | 3.96 | 548 | 180 | 9.6 |
| 11 | Ti47Nb21Al14Cr11Mo7 | NEW | bcc | -0.061 | +0.126 | +0.090 | 1051 | 5.93 | 36 | 3.55 | 528 | 182 | 9.4 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Ti45Mo35V11Zr9** — wt% {'Zr': 11.91, 'Ti': 31.25, 'Mo': 48.71, 'V': 8.13}; rules: dH -3.83 kJ/mol, δ 4.75 %, Ω 5.97, VEC 4.81; would rather be: Ti(hcp) 0.39, C15-ZrMo 0.27, B2-VMo 0.22, B2-MoTi 0.12; nearest known: —
2. **Ti40Zr32Mo28** — wt% {'Ti': 25.46, 'Zr': 38.82, 'Mo': 35.72}; rules: dH -3.94 kJ/mol, δ 5.55 %, Ω 5.2, VEC 4.56; would rather be: C15-ZrMo 0.42, Ti(hcp) 0.40, Zr(hcp) 0.18; nearest known: —
3. **Ti54Zr34Ta6Cr6** — wt% {'Ti': 36.49, 'Zr': 43.78, 'Ta': 15.33, 'Cr': 4.4}; rules: dH -1.61 kJ/mol, δ 5.52 %, Ω 11.23, VEC 4.18; would rather be: Ti(hcp) 0.54, Zr(hcp) 0.34, C15-TaCr 0.09, Ta(bcc) 0.03; nearest known: —
4. **Ti52Zr20Al10Ta10Nb8** — wt% {'Ti': 34.88, 'Al': 3.78, 'Ta': 25.36, 'Zr': 25.57, 'Nb': 10.42}; rules: dH -10.06 kJ/mol, δ 3.77 %, Ω 2.27, VEC 4.08; would rather be: Ti(hcp) 0.42, L12-ZrAl 0.27, B2-NbTa 0.16, L12-TiAl 0.13; nearest known: —
5. **Ti52Zr35V13** — wt% {'Ti': 39.23, 'V': 10.44, 'Zr': 50.33}; rules: dH -1.27 kJ/mol, δ 5.7 %, Ω 12.99, VEC 4.13; would rather be: Ti(hcp) 0.52, Zr(hcp) 0.35, V(bcc) 0.13; nearest known: —
6. **Ti48Al15Mo13Cr12V12** — wt% {'Ti': 44.31, 'Cr': 12.03, 'Al': 7.81, 'V': 11.79, 'Mo': 24.06}; rules: dH -14.09 kJ/mol, δ 4.7 %, Ω 1.64, VEC 4.47; would rather be: L21-Ti2AlMo 0.52, C15-TiCr 0.18, V(bcc) 0.12, Ti(hcp) 0.10; nearest known: 0.247 Ti-13V-11Cr-3Al (titanium); 0.248 Ti-13V-11Cr-3Al (B120VCA, the SR-71 alloy) (titanium)
7. **Ti69.7Nb23.7Zr4.8Ta1.8** — wt% {'Ti': 52.94, 'Nb': 34.94, 'Zr': 6.95, 'Ta': 5.17}; rules: dH 1.56 kJ/mol, δ 1.95 %, Ω 9.34, VEC 4.25; would rather be: Ti(hcp) 0.70, Nb(bcc) 0.22, Zr(hcp) 0.05, B2-NbTa 0.04; nearest known: 0.008 Ti-35Nb-7Zr-5Ta (TNZT / Tiadyne 1610) (titanium); 0.049 Ti-Nb shape-memory/superelastic biomedical alloys (Ti-26Nb at%, Ti-Nb-Zr-Ta 'gum-type') (shape_memory); 0.056 Gum Metal (Ti-23Nb-0.7Ta-2Zr-1.2O, at%) (titanium)
8. **Ti51V35Nb14** — wt% {'Ti': 44.19, 'Nb': 23.54, 'V': 32.27}; rules: dH -1.05 kJ/mol, δ 4.29 %, Ω 16.66, VEC 4.49; would rather be: Ti(hcp) 0.51, C15-NbV 0.42, V(bcc) 0.07; nearest known: —
9. **Ti49Zr15V13Cr13Al10** — wt% {'Ti': 44.07, 'Al': 5.07, 'V': 12.44, 'Cr': 12.7, 'Zr': 25.71}; rules: dH -13.55 kJ/mol, δ 6.54 %, Ω 1.65, VEC 4.29; would rather be: Ti(hcp) 0.27, L12-TiAl 0.20, L12-ZrAl 0.20, C15-TiCr 0.19; nearest known: 0.231 Ti-13V-11Cr-3Al (titanium); 0.238 Ti-13V-11Cr-3Al (B120VCA, the SR-71 alloy) (titanium)
10. **Ti51Nb24Cr15Al10** — wt% {'Cr': 13.63, 'Ti': 42.67, 'Nb': 38.98, 'Al': 4.72}; rules: dH -10.62 kJ/mol, δ 4.61 %, Ω 1.95, VEC 4.44; would rather be: L12-TiAl 0.40, Nb(bcc) 0.24, C15-TiCr 0.22, Ti(hcp) 0.13; nearest known: 0.15 Ti2AlNb orthorhombic alloy (Ti-22Al-25Nb, at%) (titanium); 0.25 Niobium-titanium superconductor (Nb-47Ti) (refractory); 0.25 Titanium Grade 36 (Ti-45Nb) (titanium)
