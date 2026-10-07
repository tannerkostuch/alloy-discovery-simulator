# backyard_hea — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 14

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cu56Zn24Ni20 | near C77000 nickel silver 55-18 (spring grade) | fcc | -0.067 | +0.042 | +0.017 | 496 | 8.61 | 48 | 2.64 | 275 | 87 | 180.8 |
| 2 | Cu50Zn25Al17Si8 | NEW | fcc | -0.059 | +0.078 | +0.047 | 754 | 6.92 | 33 | 3.25 | 221 | 52 | 68.6 |
| 3 | Cu47Zn27Mn15Mg6Ni5 | NEW | fcc | +0.026 | +0.123 | +0.089 | 1085 | 7.51 | 38 | 2.64 | 480 | 188 | 52.3 |
| 4 | Cu59Mn24Al12Mg5 | NEW | fcc | +0.007 | +0.124 | +0.096 | 1356 | 7.07 | 44 | 2.41 | 566 | 246 | 50.9 |
| 5 | Cu60Al21Ni10Sn9 | NEW | fcc | -0.073 | +0.150 | +0.122 | 1606 | 7.49 | 29 | 3.94 | 863 | 384 | 41.2 |
| 6 | Cu43Zn23Al19Sn7Ni4Ag4 | NEW | fcc | -0.036 | +0.140 | +0.103 | 1116 | 7.25 | 22 | 4.17 | 430 | 134 | 33.0 |
| 7 | Cu43Zn25Mn21Si6Sn5 | NEW | fcc | +0.024 | +0.151 | +0.116 | 1296 | 7.69 | 33 | 2.86 | 577 | 233 | 31.5 |
| 8 | Cu50Zn32Mn11Si7 | NEW | fcc | -0.004 | +0.126 | +0.097 | 1284 | 7.85 | 38 | 2.80 | 181 | 41 | 16.1 |
| 9 | Cu43Zn20Mn16Al14Si7 | NEW | fcc | -0.022 | +0.173 | +0.136 | 1396 | 6.98 | 39 | 2.61 | 253 | 75 | 8.5 |
| 10 | Cu56Al22Mn14Si8 | NEW | fcc | -0.057 | +0.179 | +0.150 | 1830 | 6.64 | 43 | 2.65 | 325 | 110 | 7.7 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Cu56Zn24Ni20** — wt% {'Cu': 56.47, 'Ni': 18.63, 'Zn': 24.91}; rules: dH 0.6 kJ/mol, δ 2.63 %, Ω 17.39, VEC 11.04; would rather be: Cu(fcc) 0.44, L10-ZnNi 0.40, L12-CuZn 0.16; nearest known: 0.016 C77000 nickel silver 55-18 (spring grade) (copper); 0.07 C79200 leaded nickel silver 59-12 (free-cutting) (copper); 0.091 C75200 nickel silver 65-18 (copper)
2. **Cu50Zn25Al17Si8** — wt% {'Cu': 57.81, 'Si': 4.09, 'Al': 8.35, 'Zn': 29.75}; rules: dH -5.18 kJ/mol, δ 6.24 %, Ω 2.2, VEC 9.33; would rather be: D019-CuAl 0.40, L21-Cu2ZnAl 0.28, D019-ZnCu 0.24, Si(diamond) 0.08; nearest known: 0.163 C86300 manganese bronze (cast, high strength) (copper); 0.169 Cu-Zn-Al (Copper-Zinc-Aluminium Shape Memory Alloy) (shape_memory); 0.18 C86200 manganese bronze (cast, 90 ksi) (copper)
3. **Cu47Zn27Mn15Mg6Ni5** — wt% {'Cu': 49.64, 'Zn': 29.36, 'Mg': 2.42, 'Ni': 4.88, 'Mn': 13.7}; rules: dH 0.03 kJ/mol, δ 6.0 %, Ω 465.32, VEC 10.08; would rather be: B2-CuZn 0.31, L12-CuZn 0.26, C15-MgCu 0.18, Mn(hcp) 0.15; nearest known: 0.212 C79200 leaded nickel silver 59-12 (free-cutting) (copper); 0.225 C77000 nickel silver 55-18 (spring grade) (copper); 0.241 Nickel brass (UK £1 coin, 70-24.5-5.5) (copper)
4. **Cu59Mn24Al12Mg5** — wt% {'Al': 5.87, 'Mg': 2.2, 'Mn': 23.92, 'Cu': 68.01}; rules: dH -0.13 kJ/mol, δ 6.31 %, Ω 90.7, VEC 8.63; would rather be: D019-CuAl 0.48, Mn(hcp) 0.24, C15-MgCu 0.15, Cu(fcc) 0.13; nearest known: 0.125 Heusler alloy Cu2MnAl (ferromagnetic without ferromagnetic elements) (magnetic_electrical); 0.168 C95700 manganese-aluminium bronze (Cu-Mn-Al propeller alloy, 'Novoston') (copper); 0.18 Cu-Al-Mn shape-memory alloy (shape_memory)
5. **Cu60Al21Ni10Sn9** — wt% {'Cu': 63.18, 'Ni': 9.73, 'Sn': 17.7, 'Al': 9.39}; rules: dH 0.28 kJ/mol, δ 5.68 %, Ω 39.68, VEC 8.59; would rather be: D019-CuAl 0.62, Cu(fcc) 0.14, C1-NiSn 0.13, B2-AlNi 0.11; nearest known: 0.147 C63000 nickel-aluminium bronze (wrought, 10 % Al) (copper); 0.153 C95500 nickel-aluminium bronze casting (11 % Al, 4 % Ni) (copper); 0.153 Cu-Al-Ni shape-memory alloy (copper)
6. **Cu43Zn23Al19Sn7Ni4Ag4** — wt% {'Cu': 43.74, 'Sn': 13.3, 'Ni': 3.76, 'Zn': 24.08, 'Al': 8.21, 'Ag': 6.91}; rules: dH 0.53 kJ/mol, δ 5.14 %, Ω 24.83, VEC 9.18; would rather be: D019-CuAl 0.40, D019-ZnCu 0.28, L21-Al2CuNi 0.16, C16-AgSn 0.10; nearest known: 0.227 C86300 manganese bronze (cast, high strength) (copper); 0.245 Cu-Zn-Al shape-memory brass (Cu-25Zn-4Al type) (shape_memory); 0.245 C86200 manganese bronze (cast, 90 ksi) (copper)
7. **Cu43Zn25Mn21Si6Sn5** — wt% {'Cu': 43.49, 'Sn': 9.45, 'Mn': 18.36, 'Si': 2.68, 'Zn': 26.02}; rules: dH -4.47 kJ/mol, δ 5.02 %, Ω 3.03, VEC 9.64; would rather be: L12-CuZn 0.36, B2-CuZn 0.32, A15-MnSi 0.24, C16-MnSn 0.07; nearest known: —
8. **Cu50Zn32Mn11Si7** — wt% {'Si': 3.24, 'Mn': 9.95, 'Zn': 34.48, 'Cu': 52.33}; rules: dH -4.98 kJ/mol, δ 4.54 %, Ω 2.26, VEC 10.39; would rather be: B2-CuZn 0.46, L12-CuZn 0.36, L10-MnSi 0.10, A15-MnSi 0.08; nearest known: 0.174 C86500 manganese bronze (cast, 65 ksi) (copper); 0.176 C67500 manganese bronze (wrought, 'A') (copper); 0.18 C36000 free-cutting brass (61.5/35.5/3) (copper)
9. **Cu43Zn20Mn16Al14Si7** — wt% {'Cu': 49.74, 'Al': 6.88, 'Si': 3.58, 'Zn': 23.81, 'Mn': 16.0}; rules: dH -7.21 kJ/mol, δ 5.86 %, Ω 2.02, VEC 8.95; would rather be: B2-CuZn 0.40, D019-CuAl 0.31, L10-MnAl 0.13, L10-MnSi 0.11; nearest known: 0.202 C86300 manganese bronze (cast, high strength) (copper); 0.242 C86200 manganese bronze (cast, 90 ksi) (copper)
10. **Cu56Al22Mn14Si8** — wt% {'Cu': 69.15, 'Al': 11.54, 'Si': 4.37, 'Mn': 14.95}; rules: dH -8.34 kJ/mol, δ 6.57 %, Ω 1.49, VEC 8.12; would rather be: D019-CuAl 0.75, L10-MnSi 0.13, L10-MnAl 0.07, A15-MnSi 0.05; nearest known: 0.125 Heusler alloy Cu2MnAl (ferromagnetic without ferromagnetic elements) (magnetic_electrical); 0.125 Cu-Al-Mn shape-memory alloy (shape_memory); 0.14 Cu-Al-Mn (Ductile Copper-Aluminium-Manganese Superelastic Alloy) (shape_memory)
