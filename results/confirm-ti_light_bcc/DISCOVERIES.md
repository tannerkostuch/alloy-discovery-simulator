# ti_light_bcc — ranked by specific_strength

objective: yield stress at 300 K per density (MPa per g/cm³), single-phase and ductile favoured
engine: mace-medium-mpa-0-cpu · candidates evaluated: 3

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ti45Mo35V11Zr9 | NEW | bcc | -0.019 | +0.050 | +0.019 | 488 | 6.91 | 35 | 3.91 | 828 | 345 | 74.0 |
| 2 | Ti40Zr32Mo28 | NEW | bcc | +0.020 | +0.077 | +0.049 | 821 | 6.78 | 29 | 4.10 | 922 | 403 | 40.1 |
| 3 | Ti69.7Nb23.7Zr4.8Ta1.8 | near Ti-35Nb-7Zr-5Ta (TNZT / Tiadyne 1610) | bcc | +0.045 | +0.045 | +0.024 | 642 | 5.89 | 16 | 7.43 | 84 | 6 | 7.8 |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).

1. **Ti45Mo35V11Zr9** — wt% {'Ti': 31.25, 'Mo': 48.71, 'V': 8.13, 'Zr': 11.91}; rules: dH -3.83 kJ/mol, δ 4.75 %, Ω 5.97, VEC 4.81; would rather be: Ti(hcp) 0.39, C15-ZrMo 0.27, B2-VMo 0.22, B2-MoTi 0.12; nearest known: —
2. **Ti40Zr32Mo28** — wt% {'Ti': 25.46, 'Zr': 38.82, 'Mo': 35.72}; rules: dH -3.94 kJ/mol, δ 5.55 %, Ω 5.2, VEC 4.56; would rather be: C15-ZrMo 0.42, Ti(hcp) 0.40, Zr(hcp) 0.18; nearest known: —
3. **Ti69.7Nb23.7Zr4.8Ta1.8** — wt% {'Ti': 52.94, 'Nb': 34.94, 'Zr': 6.95, 'Ta': 5.17}; rules: dH 1.56 kJ/mol, δ 1.95 %, Ω 9.34, VEC 4.25; would rather be: Ti(hcp) 0.70, Nb(bcc) 0.22, Zr(hcp) 0.05, B2-NbTa 0.04; nearest known: 0.008 Ti-35Nb-7Zr-5Ta (TNZT / Tiadyne 1610) (titanium); 0.049 Ti-Nb shape-memory/superelastic biomedical alloys (Ti-26Nb at%, Ti-Nb-Zr-Ta 'gum-type') (shape_memory); 0.056 Gum Metal (Ti-23Nb-0.7Ta-2Zr-1.2O, at%) (titanium)
