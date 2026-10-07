# smoke test — 2026-09-29 04:59

engine: **mace-medium-mpa-0-cpu**

## lattice constants (Å)

| element | lattice | model | experiment | error |
|---|---|---|---|---|
| Al | fcc (model ground: fcc) | 4.039 | 4.05 | -0.3 % |
| Cu | fcc (model ground: fcc) | 3.640 | 3.615 | +0.7 % |
| Ni | fcc (model ground: fcc) | 3.521 | 3.52 | +0.0 % |
| Fe | bcc (model ground: bcc) | 2.877 | 2.867 | +0.3 % |
| W | bcc (model ground: bcc) | 3.175 | 3.165 | +0.3 % |
| Nb | bcc (model ground: bcc) | 3.317 | 3.3 | +0.5 % |
| Ti | hcp (model ground: hcp) | 2.902 | 2.95 | -1.6 % |

## formation energies (eV/atom)

| compound | model | reference (DFT/expt) |
|---|---|---|
| NiAl (B2) | -0.659 | -0.62 |
| Ni3Al (L12) | -0.426 | -0.45 |

## elastic constants (GPa)

| element | C11 | C12 | C44 | expt C11/C12/C44 | B | G | B/G |
|---|---|---|---|---|---|---|---|
| Cu | 157 | 118 | 79 | 168/121/75 | 131 | 45 | 2.88 |
| Ni | 292 | 179 | 136 | 247/147/125 | 216 | 96 | 2.27 |
| Fe | 295 | 163 | 130 | 230/135/117 | 207 | 99 | 2.08 |
| W | 589 | 256 | 142 | 523/203/160 | 367 | 151 | 2.43 |

## two known alloys through the whole chain

- **CoCrFeMnNi (Cantor; expt: FCC, σy ≈ 200 MPa at RT, G ≈ 80 GPa)**: fcc | E_form +0.056 eV | ΔE_dec +0.117 eV (T* 842 K) | ρ 8.29 | G 75 GPa B/G 1.71 | σy 300K 92 MPa, 900K 18 | known | 676.1 s
  - cells: { fcc: -7.9686 eV/atom, bcc: -7.9400 eV/atom }; free-cell check on the winner: energy drop 0.1 meV/atom, shape change 0.003 → stays fcc
  - σy(T) MPa: {'77': 159.47343555780017, '300': 91.95914401108183, '600': 40.409086565301756, '900': 17.756736370287147, '1200': 7.802742237549612}; τ_y0 68 MPa, ΔE_b 0.92 eV, misfit volumes Å³ { Co: -0.33, Cr: +0.84, Fe: -0.93, Mn: +0.07, Ni: -0.32 }
  - hull-lite: ΔE_dec 0.11684289689842142, T* 842.4714640929034, would rather be [('B2-CoFe', 0.3466666666666668), ('L12-NiMn', 0.26666666666666666), ('Cr(bcc)', 0.2), ('L12-MnCo', 0.10666666666666647), ('SIGMA-FeMn', 0.07999999999999985)]
- **NbMoTaW (expt: BCC, σy ≈ 1000 MPa at RT)**: bcc | E_form -0.076 eV | ΔE_dec +0.040 eV (T* 333 K) | ρ 13.55 | G 83 GPa B/G 3.24 | σy 300K 832 MPa, 900K 469 | known | 687.0 s
  - cells: { bcc: -11.5028 eV/atom, fcc: -11.2410 eV/atom }; free-cell check on the winner: energy drop 0.0 meV/atom, shape change 0.000 → stays bcc
  - σy(T) MPa: {'77': 1056.2438156346445, '300': 832.3654389904259, '600': 611.7636204286816, '900': 469.2077812368538, '1200': 342.35295386759697}; τ_y0 442 MPa, ΔE_b 2.40 eV, misfit volumes Å³ { Nb: +1.29, Mo: -1.31, Ta: +1.32, W: -0.96 }
  - hull-lite: ΔE_dec 0.039840101582102605, T* 333.49712279592217, would rather be [('B2-NbMo', 0.5), ('B2-TaW', 0.5)]

took 756 s
