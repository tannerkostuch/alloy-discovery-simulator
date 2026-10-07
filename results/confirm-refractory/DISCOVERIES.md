# refractory — ranked by high_temp

objective: yield stress at 900 K, with a high melting point and a stable single phase at 900 K
engine: mace-medium-mpa-0-cpu · candidates evaluated: 4

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Nb32W27Hf17Mo14Ta10 | NEW | bcc | +0.010 | +0.130 | +0.091 | 989 | 13.21 | 56 | 3.73 | 1374 | 818 | 609.6 |
| 2 | Ti29V22Mo21Hf14Ta14 | NEW | bcc | +0.020 | +0.121 | +0.080 | 893 | 9.47 | 37 | 3.72 | 1118 | 533 | 532.5 |
| 3 | Nb25Mo25Ta25W25 | near NbMoTaW | bcc | -0.086 | +0.029 | -0.007 | 246 | 13.57 | 84 | 3.22 | 851 | 484 | 484.3 |
| 4 | V37Ti37Cr16W10 | NEW | bcc | +0.027 | +0.070 | +0.037 | 641 | 7.27 | 32 | 4.40 | 709 | 240 | 240.0 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Nb32W27Hf17Mo14Ta10** — wt% {'Nb': 21.05, 'W': 35.14, 'Hf': 21.48, 'Mo': 9.51, 'Ta': 12.81}; rules: dH -5.28 kJ/mol, δ 4.79 %, Ω 7.29, VEC 5.24; would rather be: C15-HfW 0.40, Nb(bcc) 0.32, B2-MoTa 0.20, C15-HfMo 0.06; nearest known: —
2. **Ti29V22Mo21Hf14Ta14** — wt% {'Ti': 14.53, 'V': 11.73, 'Mo': 21.08, 'Hf': 26.15, 'Ta': 26.51}; rules: dH -2.52 kJ/mol, δ 5.46 %, Ω 12.78, VEC 4.78; would rather be: C15-TaV 0.33, Ti(hcp) 0.29, C15-HfMo 0.27, B2-MoTa 0.06; nearest known: —
3. **Nb25Mo25Ta25W25** — wt% {'Nb': 16.78, 'Mo': 17.33, 'Ta': 32.68, 'W': 33.21}; rules: dH -6.5 kJ/mol, δ 2.46 %, Ω 5.6, VEC 5.5; would rather be: B2-NbMo 0.50, B2-TaW 0.50; nearest known: 0.0 NbMoTaW (high_entropy); 0.1 NbMoTaW / VNbMoTaW refractory HEA (BCC, 1600 °C strength) (high_entropy); 0.2 VNbMoTaW (high_entropy)
4. **V37Ti37Cr16W10** — wt% {'V': 29.79, 'Ti': 28.0, 'Cr': 13.15, 'W': 29.06}; rules: dH -4.2 kJ/mol, δ 5.21 %, Ω 5.6, VEC 4.89; would rather be: Ti(hcp) 0.29, V(bcc) 0.27, C15-TiCr 0.24, B2-VW 0.20; nearest known: —
