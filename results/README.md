# Results — the tables

Everything here was computed on one desktop CPU between 2026-09-29 and 2026-10-05 with MACE-MPA-0. The tables are as
the code wrote them (three file references were pointed at files that exist in this repository). What they mean, and
how far to trust them, is in [`../docs/RESULTS.md`](../docs/RESULTS.md).

Nothing in these tables has been melted or measured. "NEW" means only that a 1 482-alloy reference database holds
nothing within 6 at% of the composition.

| folder or file | family | ranked by | alloys | notes |
|---|---|---|---|---|
| `SMOKE_REPORT.md` | — | — | — | the engine against known physics: lattice constants, formation energies, elastic constants, two famous alloys. Written on 2026-09-29; since hexagonal cells relax their own c/a (10-04), a fresh run gives titanium −1.1 % instead of −1.6 % |
| `VALIDATION_1214_alloys.md` | 1 214 known alloys | — | 1 214 | the scorecard: lattice, density, moduli, yield ratio per family; the misses and the worst offenders by name |
| `run1-medium_entropy_fcc` | Ni-Co-Cr-Fe-Cu-Mn-Al-V | `strong_ductile` | 13 | benchmark CoCrNi; `SFE.md` = stacking-fault energies of its top six |
| `run2-refractory` | Nb-Mo-Ta-W-V-Ti-Zr-Hf-Cr | `high_temp` | 13 | benchmark NbMoTaW |
| `run3-ti_light_bcc` | Ti ≥ 35 % with Zr-Nb-V-Ta-Hf-Mo-Al-Cr | `specific_strength` | 13 | benchmark Ti-35Nb-7Zr-5Ta; two cells dropped as mechanically unstable |
| `confirm-*` | the candidates and benchmarks of runs 1–3 | as the run | 9 | three random arrangements per lattice instead of one |
| `run4-3d_hea` | Co-Cr-Fe-Mn-Ni-Al-Cu-V-Ti | `strong_ductile` | 14 | benchmark CoCrFeMnNi |
| `run5-cu_alloys` | Cu ≥ 50 % with Ni-Zn-Al-Mn-Fe-Co-Cr | `strong_ductile` | 14 | fcc cells only — its top rows are β/γ brass in reality, see RESULTS.md |
| `run6-backyard_al` | Al ≥ 88 % with Cu-Mg-Si-Zn-Mn-Ag | `strong_ductile` | 15 | |
| `run7-backyard_cu` | Cu ≥ 58 % with Zn-Sn-Al-Si-Mn-Ni-Ag-Mg | `strong_ductile` | 16 | raw yields; read with the calibration |
| `run9-backyard_hea` | Cu ≥ 30 % plus three to five of Zn-Al-Mn-Sn-Ni-Ag-Mg-Si | `strong_ductile` | 14 | four bcc cells unstable (random cells of ordered alloys) |
| `run8-backyard_zn` | Zn ≥ 70 % with Al-Cu-Mg-Ag | `stiff_stable` | 15 | hexagonal cells; moduli read × 1.45 |
| `run10-backyard_al2` | second pass of run 6 | `strong_ductile_cal` | 12 | first tables with the calibrated-yield and notes columns |
| `run11-backyard_cu2` | second pass of run 7 | `strong_ductile_cal` | 12 | two bcc cells unstable; the top row's "242?" is silver, which has no calibration factor |
| `run12-backyard_hea2` | second pass of run 9 | `strong_ductile_cal` | 12 | one bcc cell unstable; the three top rows carry a "?" (uncalibrated solutes), see RESULTS.md |
| `run13-backyard_zn2` | second pass of run 8 | `stiff_stable` | 4 | all that was left of the family's space |
| `run14-backyard_mg` | Mg ≥ 85 % with Al-Zn-Mn-Ca-Si-Sn-Cu | `stiff_stable` | 16 | hexagonal cells, no yield model: ranked by stiffness and stability; benchmarks AZ91, AM60, AS41, Mg-2Zn |
| `SFE_VALIDATION.md` | — | — | 5 | the stacking-fault step against Cu, Ni, Al, CoCrNi, CoCrFeMnNi |

Not included: the per-candidate JSON files (every number of every cell), the validation's per-record results and
`validation.csv`, caches and logs. Your own runs write next to these: a discovery run into `results/<run name>/`,
the validation into `results/validation/` (git-ignored), the smoke test into `SMOKE_REPORT.md` at the top level.

Runs 1–9 were ranked on the raw solute-strengthening yield; their tables do not have the calibrated column that
runs 10 and later carry.
