# refractory — ranked by high_temp

objective: yield stress at 900 K, with a high melting point and a stable single phase at 900 K
engine: mace-medium-mpa-0-cpu · candidates evaluated: 13

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Nb32W27Hf17Mo14Ta10 | NEW | bcc | +0.015 | +0.135 | +0.096 | 1027 | 13.21 | 55 | 3.87 | 1354 | 798 | 525.6 |
| 2 | Nb25Mo25Ta25W25 | near NbMoTaW | bcc | -0.076 | +0.040 | +0.004 | 333 | 13.55 | 83 | 3.24 | 832 | 469 | 469.2 |
| 3 | Ti29V22Mo21Hf14Ta14 | NEW | bcc | +0.025 | +0.126 | +0.085 | 928 | 9.47 | 34 | 4.03 | 1051 | 479 | 435.4 |
| 4 | Mo40W31Hf18Zr11 | NEW | bcc | +0.028 | +0.174 | +0.141 | 1574 | 13.18 | 77 | 3.03 | 3090 | 2195 | 341.5 |
| 5 | Nb29W25Zr18Hf16Ta12 | NEW | bcc | +0.078 | +0.145 | +0.104 | 1075 | 12.27 | 37 | 4.39 | 1042 | 528 | 293.1 |
| 6 | Mo39W34Hf27 | NEW | bcc | +0.030 | +0.174 | +0.146 | 1854 | 14.26 | 83 | 2.94 | 3042 | 2174 | 232.5 |
| 7 | Ti40Nb21Cr16V12Zr11 | NEW | bcc | +0.090 | +0.130 | +0.092 | 1016 | 6.33 | 24 | 4.94 | 843 | 302 | 208.0 |
| 8 | V37Ti37Cr16W10 | NEW | bcc | +0.036 | +0.079 | +0.046 | 729 | 7.25 | 30 | 4.51 | 645 | 204 | 204.0 |
| 9 | Ti31V26Ta16W15Hf12 | NEW | bcc | +0.069 | +0.158 | +0.118 | 1185 | 10.52 | 37 | 3.60 | 1090 | 516 | 199.7 |
| 10 | Ti40Zr27Nb21Cr12 | NEW | bcc | +0.098 | +0.117 | +0.084 | 1046 | 6.33 | 22 | 4.82 | 778 | 285 | 189.2 |
| 11 | Ti33V28Nb21Cr18 | NEW | bcc | +0.061 | +0.124 | +0.089 | 1056 | 6.46 | 25 | 5.44 | 652 | 196 | 124.2 |
| 12 | Ti31Zr23V18Hf17Ta11 | NEW | bcc | +0.119 | +0.153 | +0.113 | 1142 | 8.38 | 22 | 4.48 | 754 | 277 | 123.2 |
| 13 | Zr39Mo33Ta28 | NEW | bcc | +0.053 | +0.171 | +0.143 | 1819 | 10.37 | 34 | 4.61 | 1198 | 613 | 71.0 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Nb32W27Hf17Mo14Ta10** — wt% {'Ta': 12.81, 'W': 35.14, 'Mo': 9.51, 'Nb': 21.05, 'Hf': 21.48}; rules: dH -5.28 kJ/mol, δ 4.79 %, Ω 7.29, VEC 5.24; would rather be: C15-HfW 0.40, Nb(bcc) 0.32, B2-MoTa 0.20, C15-HfMo 0.06; nearest known: —
2. **Nb25Mo25Ta25W25** — wt% {'Nb': 16.78, 'Mo': 17.33, 'Ta': 32.68, 'W': 33.21}; rules: dH -6.5 kJ/mol, δ 2.46 %, Ω 5.6, VEC 5.5; would rather be: B2-NbMo 0.50, B2-TaW 0.50; nearest known: 0.0 NbMoTaW (high_entropy); 0.1 NbMoTaW / VNbMoTaW refractory HEA (BCC, 1600 °C strength) (high_entropy); 0.2 VNbMoTaW (high_entropy)
3. **Ti29V22Mo21Hf14Ta14** — wt% {'V': 11.73, 'Hf': 26.15, 'Mo': 21.08, 'Ta': 26.51, 'Ti': 14.53}; rules: dH -2.52 kJ/mol, δ 5.46 %, Ω 12.78, VEC 4.78; would rather be: C15-TaV 0.33, Ti(hcp) 0.29, C15-HfMo 0.27, B2-MoTa 0.06; nearest known: —
4. **Mo40W31Hf18Zr11** — wt% {'Zr': 7.3, 'W': 41.44, 'Mo': 27.9, 'Hf': 23.36}; rules: dH -4.77 kJ/mol, δ 6.38 %, Ω 6.67, VEC 5.42; would rather be: C15-HfMo 0.50, C15-ZrW 0.33, B2-MoW 0.13, C15-HfW 0.04; nearest known: —
5. **Nb29W25Zr18Hf16Ta12** — wt% {'Zr': 11.76, 'Ta': 15.55, 'Hf': 20.46, 'W': 32.92, 'Nb': 19.3}; rules: dH -3.67 kJ/mol, δ 5.48 %, Ω 10.25, VEC 4.91; would rather be: C15-HfW 0.37, B2-NbTa 0.24, Zr(hcp) 0.18, Nb(bcc) 0.17; nearest known: —
6. **Mo39W34Hf27** — wt% {'W': 42.2, 'Hf': 32.54, 'Mo': 25.26}; rules: dH -3.89 kJ/mol, δ 6.15 %, Ω 7.12, VEC 5.46; would rather be: C15-HfMo 0.44, C15-HfW 0.37, B2-MoW 0.19; nearest known: —
7. **Ti40Nb21Cr16V12Zr11** — wt% {'Ti': 30.33, 'Zr': 15.9, 'Nb': 30.91, 'Cr': 13.18, 'V': 9.68}; rules: dH -3.39 kJ/mol, δ 6.44 %, Ω 8.02, VEC 4.65; would rather be: Ti(hcp) 0.32, C15-TiCr 0.24, C15-NbV 0.18, Nb(bcc) 0.15; nearest known: —
8. **V37Ti37Cr16W10** — wt% {'Cr': 13.15, 'V': 29.79, 'Ti': 28.0, 'W': 29.06}; rules: dH -4.2 kJ/mol, δ 5.21 %, Ω 5.6, VEC 4.89; would rather be: Ti(hcp) 0.29, V(bcc) 0.27, C15-TiCr 0.24, B2-VW 0.20; nearest known: —
9. **Ti31V26Ta16W15Hf12** — wt% {'Hf': 20.2, 'Ti': 13.99, 'V': 12.49, 'W': 26.01, 'Ta': 27.31}; rules: dH -3.01 kJ/mol, δ 5.39 %, Ω 10.9, VEC 4.72; would rather be: C15-TaV 0.39, Ti(hcp) 0.31, C15-HfW 0.22, Hf(hcp) 0.05; nearest known: —
10. **Ti40Zr27Nb21Cr12** — wt% {'Zr': 35.43, 'Cr': 8.97, 'Nb': 28.06, 'Ti': 27.54}; rules: dH -2.03 kJ/mol, δ 6.34 %, Ω 11.71, VEC 4.45; would rather be: Ti(hcp) 0.34, Zr(hcp) 0.27, Nb(bcc) 0.21, C15-TiCr 0.18; nearest known: —
