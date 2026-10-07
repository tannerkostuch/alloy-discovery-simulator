# backyard_mg — ranked by stiff_stable

objective: shear modulus times the phase and ductility factors — for lattices the strengthening model does not cover (HCP zinc, magnesium)
engine: mace-medium-mpa-0-cpu · candidates evaluated: 16

| # | alloy (at%) | new? | lattice | E_form eV | ΔE_dec eV | ΔG₃₀₀ eV | T* K | ρ g/cm³ | G GPa | B/G | σy 300 K MPa | σy 900 K MPa | σy cal. 300 K | score | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Mg91Al8Zn1 | near AZ92A (Mg-9Al-2Zn, sand casting and filler) | hcp | +0.002 | +0.006 | -0.002 | 217 | 1.87 | 19 | 2.14 | 0 | 0 | — | 19.0 |  |
| 2 | Mg98Zn2 | near ZK60A (Mg-6Zn-0.5Zr high-strength wrought) | hcp | -0.000 | +0.004 | +0.002 | 529 | 1.85 | 19 | 2.05 | 0 | 0 | — | 17.8 |  |
| 3 | Mg96Zn4 | near ZK61A | hcp | -0.000 | +0.009 | +0.005 | 626 | 1.93 | 18 | 2.10 | 0 | 0 | — | 16.4 |  |
| 4 | Mg94.5Al5.5 | near AM60B (Mg-6Al-0.3Mn, ductile die casting) | hcp | +0.013 | +0.014 | +0.009 | 788 | 1.81 | 19 | 2.13 | 0 | 0 | — | 15.0 |  |
| 5 | Mg97Ca3 | near Mg-1Ca / Mg-Zn-Ca biodegradable implant alloys (ZX10, ZX50) | hcp | +0.001 | +0.012 | +0.008 | 992 | 1.77 | 17 | 2.10 | 0 | 0 | — | 14.0 |  |
| 6 | Mg88Al10Si2 | near AZ92A (Mg-9Al-2Zn, sand casting and filler) | hcp | +0.007 | +0.017 | +0.006 | 465 | 1.87 | 16 | 2.10 | 0 | 0 | — | 13.7 |  |
| 7 | Mg95.4Al3.7Si0.9 | near AS41B (Mg-4Al-1Si, creep-resistant die casting) | hcp | +0.016 | +0.020 | +0.014 | 1094 | 1.81 | 18 | 2.15 | 0 | 0 | — | 12.9 |  |
| 8 | Mg88Al5Zn4Mn2Sn1 | near AZ63A (Mg-6Al-3Zn, sand casting and anodes) | hcp | +0.002 | +0.033 | +0.020 | 748 | 2.11 | 20 | 2.06 | 0 | 0 | — | 12.1 |  |
| 9 | Mg85Al12Zn3 | near AZ92A (Mg-9Al-2Zn, sand casting and filler) | hcp | +0.022 | +0.032 | +0.019 | 750 | 1.98 | 19 | 2.26 | 0 | 0 | — | 11.6 |  |
| 10 | Mg90Zn5Sn3Si1Mn1 | NEW | hcp | -0.006 | +0.032 | +0.020 | 829 | 2.23 | 17 | 2.28 | 0 | 0 | — | 10.5 |  |
| 11 | Mg90Sn3Cu3Zn3Si1 | NEW | hcp | -0.006 | +0.032 | +0.020 | 815 | 2.24 | 17 | 2.34 | 0 | 0 | — | 10.3 |  |
| 12 | Mg86Al12Cu2 | near AZ92A (Mg-9Al-2Zn, sand casting and filler) | hcp | +0.025 | +0.038 | +0.026 | 962 | 1.94 | 19 | 2.26 | 0 | 0 | — | 9.6 |  |
| 13 | Mg89Zn5Ca3Cu2Mn1 | NEW | hcp | +0.007 | +0.036 | +0.023 | 854 | 2.08 | 16 | 2.39 | 0 | 0 | — | 8.9 |  |
| 14 | Mg89Zn5Ca4Sn2 | NEW | hcp | -0.011 | +0.038 | +0.026 | 951 | 2.09 | 16 | 2.32 | 0 | 0 | — | 8.3 |  |
| 15 | Mg89Al7Ca2Mn2 | near MRI 153M / MRI 230D (Mg-Al-Ca-Sr creep-resistant die casting) | hcp | +0.012 | +0.045 | +0.034 | 1176 | 1.89 | 18 | 2.18 | 0 | 0 | — | 7.7 |  |
| 16 | Mg89Ca4Sn3Mn2Cu2 | NEW | hcp | -0.003 | +0.048 | +0.035 | 1129 | 2.12 | 15 | 2.37 | 0 | 0 | — | 6.4 |  |

ΔE_dec = energy of the solid solution above the best mixture of pure elements and the ordered compounds the
model knows (pairs: B2, L1₂, L1₀, C15/C14 Laves, A15, σ; triples: L2₁ Heusler); ΔG₃₀₀ = ΔE_dec − 300 K·S_ideal:
≤ 0 means the random solid solution is the stable state at room temperature, > 0 how badly it wants to
decompose (the model's own error is ~0.03 eV/atom); T* = temperature above which mixing entropy pays for
ΔE_dec. The score multiplies strength by exp(−ΔG/0.04 eV) and a ductility factor, so a strong alloy that
would fall apart into compounds ranks below a weaker one that stays one phase. ⚠ = the lattice would
transform with a free cell. σy from solute-strengthening theory (random solid solution, 10⁻³/s); grain size,
precipitates and interstitials would add to it. 'NEW' = no alloy in the 1 482-record database within 6 at%
(per element, summed/2).
**σy cal.** (v2, 2026-10-05) = σy read as an annealed handbook yield through the validation's calibration (docs/RESULTS.md,
the calibration table): ÷ the host/solute factor (tin in copper 5.6, zinc or aluminium in copper 1.4, nickel 0.45, silicon 0.4,
molybdenum in nickel 2.35 …; aluminium: 33 MPa + 1.5 × σy), each solute weighted by its share of the strengthening; a '?' means
half or more of the strengthening comes from a solute the table has no factor for (factor 1 used). **G (cal.)** = ×1.45 for
hexagonal zinc and cadmium cells (the PBE shear softness). **notes**: 'soft / unstable cell' (G under 10 GPa or B/G over 8),
'Zn-eq N %: β brass in reality' (Guillet zinc equivalent over 37 % — the fcc cell is not the real alloy), 'Zn-rich on fcc: a
two-phase casting in reality', 'B2-ordered cell' (the random bcc cell was unstable; the row shows the ordered cell the alloy
really is, the random cell's numbers stay in the JSON). The *_cal objectives rank by σy cal. and count a soft cell as unstable.

1. **Mg91Al8Zn1** — wt% {'Mg': 88.72, 'Al': 8.66, 'Zn': 2.62}; rules: dH -0.72 kJ/mol, δ 3.3 %, Ω 3.53, VEC 2.18; would rather be: Mg(hcp) 0.85, C14-MgAl 0.12, C16-ZnMg 0.03; nearest known: 0.006 AZ92A (Mg-9Al-2Zn, sand casting and filler) (magnesium); 0.007 AZ91D / AM60B thixomoulded and AM-lite (Mg-Al-Zn-Ca decorative die casting) (magnesium); 0.007 AZ91D (Mg-9Al-1Zn die casting) (magnesium)
2. **Mg98Zn2** — wt% {'Mg': 94.79, 'Zn': 5.21}; rules: dH -0.31 kJ/mol, δ 2.28 %, Ω 2.39, VEC 2.2; would rather be: Mg(hcp) 0.94, C16-ZnMg 0.06; nearest known: 0.003 ZK60A (Mg-6Zn-0.5Zr high-strength wrought) (magnesium); 0.006 ZK61A (magnesium); 0.006 ZE41A (Mg-4Zn-1RE-0.7Zr sand casting) (magnesium)
3. **Mg96Zn4** — wt% {'Mg': 89.92, 'Zn': 10.08}; rules: dH -0.61 kJ/mol, δ 3.21 %, Ω 2.08, VEC 2.4; would rather be: Mg(hcp) 0.88, C16-ZnMg 0.12; nearest known: 0.017 ZK61A (magnesium); 0.017 ZE63A (magnesium); 0.019 ZK60A (Mg-6Zn-0.5Zr high-strength wrought) (magnesium)
4. **Mg94.5Al5.5** — wt% {'Mg': 93.93, 'Al': 6.07}; rules: dH -0.42 kJ/mol, δ 2.44 %, Ω 3.93, VEC 2.05; would rather be: Mg(hcp) 0.92, C14-MgAl 0.08; nearest known: 0.002 AM60B (Mg-6Al-0.3Mn, ductile die casting) (magnesium); 0.003 AM60B (magnesium); 0.009 AJ62 (Mg-6Al-2Sr, BMW engine-block alloy) (magnesium)
5. **Mg97Ca3** — wt% {'Mg': 95.15, 'Ca': 4.85}; rules: dH -0.7 kJ/mol, δ 3.92 %, Ω 1.49, VEC 2.0; would rather be: Mg(hcp) 0.91, C14-CaMg 0.09; nearest known: 0.026 Mg-1Ca / Mg-Zn-Ca biodegradable implant alloys (ZX10, ZX50) (magnesium); 0.028 Mg-Zn-Ca (ZX11 class biomedical) (magnesium); 0.029 M1A (Mg-1.2Mn, corrosion-resistant wrought) (magnesium)
6. **Mg88Al10Si2** — wt% {'Mg': 86.77, 'Si': 2.28, 'Al': 10.95}; rules: dH -2.69 kJ/mol, δ 5.38 %, Ω 1.22, VEC 2.14; would rather be: Mg(hcp) 0.79, C14-MgAl 0.15, C1-SiMg 0.06; nearest known: 0.036 AZ92A (Mg-9Al-2Zn, sand casting and filler) (magnesium); 0.037 AZX911 (Mg-9Al-1Zn-1Ca) (magnesium); 0.037 AZ91D (Mg-9Al-1Zn die casting) (magnesium)
7. **Mg95.4Al3.7Si0.9** — wt% {'Mg': 94.88, 'Al': 4.09, 'Si': 1.03}; rules: dH -1.2 kJ/mol, δ 3.56 %, Ω 1.35, VEC 2.06; would rather be: Mg(hcp) 0.92, C14-MgAl 0.06, C1-SiMg 0.03; nearest known: 0.003 AS41B (Mg-4Al-1Si, creep-resistant die casting) (magnesium); 0.009 AE42 (magnesium); 0.01 AM50A (Mg-5Al-0.3Mn, high ductility) (magnesium)
8. **Mg88Al5Zn4Mn2Sn1** — wt% {'Mg': 77.38, 'Zn': 9.47, 'Al': 4.88, 'Mn': 3.98, 'Sn': 4.29}; rules: dH -0.61 kJ/mol, δ 4.85 %, Ω 6.46, VEC 2.57; would rather be: Mg(hcp) 0.78, C16-ZnMg 0.12, D022-AlMn 0.06, C1-SnMg 0.03; nearest known: 0.058 AZ63A (Mg-6Al-3Zn, sand casting and anodes) (magnesium); 0.062 AZ92A (Mg-9Al-2Zn, sand casting and filler) (magnesium); 0.065 AZ61A (Mg-6Al-1Zn extrusion / welding filler) (magnesium)
9. **Mg85Al12Zn3** — wt% {'Mg': 79.89, 'Al': 12.52, 'Zn': 7.59}; rules: dH -1.21 kJ/mol, δ 4.36 %, Ω 3.14, VEC 2.42; would rather be: Mg(hcp) 0.73, C14-MgAl 0.18, C16-ZnMg 0.09; nearest known: 0.059 AZ92A (Mg-9Al-2Zn, sand casting and filler) (magnesium); 0.063 AZX911 (Mg-9Al-1Zn-1Ca) (magnesium); 0.064 AZ91D / AM60B thixomoulded and AM-lite (Mg-Al-Zn-Ca decorative die casting) (magnesium)
10. **Mg90Zn5Sn3Si1Mn1** — wt% {'Sn': 12.06, 'Si': 0.95, 'Mn': 1.86, 'Zn': 11.07, 'Mg': 74.06}; rules: dH -2.35 kJ/mol, δ 5.31 %, Ω 1.43, VEC 2.63; would rather be: Mg(hcp) 0.74, C16-ZnMg 0.15, C1-SnMg 0.09, L10-MnSi 0.02; nearest known: 0.077 ZK61A (magnesium); 0.077 ZE63A (magnesium); 0.079 ZK60A (Mg-6Zn-0.5Zr high-strength wrought) (magnesium)
