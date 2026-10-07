# medium_entropy_fcc — ranked by strong_ductile

objective: yield stress at 300 K times a ductility factor (Pugh ratio, Cauchy pressure), single phase at 300 K favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 2

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ni40Fe29Cr17V14 | NEW | fcc | -0.007 | +0.091 | +0.057 | 811 | 8.03 | 59 | 2.72 | 218 | 60 | 52.0 |
| 2 | Co33.33Cr33.33Ni33.33 | near CoCrNi medium-entropy alloy (equiatomic, FCC) | fcc | +0.085 | +0.087 | +0.058 | 916 | 8.50 | 94 | 2.05 | 151 | 45 | 35.2 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Ni40Fe29Cr17V14** — wt% {'Ni': 42.19, 'Fe': 29.1, 'Cr': 15.89, 'V': 12.82}; rules: dH -8.39 kJ/mol, δ 2.6 %, Ω 2.44, VEC 8.04; would rather be: A15-NiV 0.53, Fe(bcc) 0.29, Cr(bcc) 0.17, L21-V2CrFe 0.01; nearest known: 0.14 Incoloy 825 (Ni-Fe-Cr-Mo-Cu) (nickel); 0.14 Nimonic PE16 (Ni-Fe-Cr, nuclear) (nickel); 0.14 Inconel 706 (nickel)
2. **Co33.33Cr33.33Ni33.33** — wt% {'Co': 34.74, 'Cr': 30.65, 'Ni': 34.6}; rules: dH -4.89 kJ/mol, δ 1.35 %, Ω 3.54, VEC 8.33; would rather be: L12-NiCr 0.44, Co(hcp) 0.33, Cr(bcc) 0.22; nearest known: 0.012 CoCrNi medium-entropy alloy (equiatomic, FCC) (high_entropy); 0.095 Haynes HR-160 (nickel); 0.108 MP35N (35Co-35Ni-20Cr-10Mo multiphase) (cobalt)
