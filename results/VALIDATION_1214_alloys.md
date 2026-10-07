# The simulation against the alloys database — scorecard (1214 alloys so far, 2026-10-05 11:15)

Every usable record of the reference database (1 482 records, not part of this repository) run through the same chain as the discovery runs (tier 1: the solid solution on
its expected lattice, and the rival lattice where it matters; tier 2: elastic constants and the solute-strengthening yield;
tier 3: the hull) and compared with the measured values in the database. **lattice right** = the lattice the record
implies came out lowest in energy (where the record implies two — α+β titanium, duplex stainless, α+β brass, Co-Cr —
either counts); quenched-in phases (austenitic stainless, β-Ti…) are counted separately below, because at 0 K the model
may rightly prefer the low-temperature lattice. **ρ** = model density of the real phase vs measured (the model has no
interstitials and no porosity). **E, G** = model (0 K, single crystal averaged) vs measured room-temperature moduli.
**σy ratio** = the chain's solute-strengthening yield ÷ the measured annealed yield, only for records whose annealed state
is a solid solution — the chain leaves out grain-boundary, precipitate, carbide and interstitial strengthening on purpose,
so a ratio well under 1 is expected wherever those carry the load; the point is how consistent the ratio is within a family.
(v2.4) The E/G medians leave out records whose measured modulus is a placeholder (copper alloys at pure copper's 117 GPa,
high-entropy alloys at 200) and two-phase castings run as one solution (ZA-27-type zinc, Al-Si); n = rows counted. The yield
test leaves out leaded copper, Al-Si castings and the zinc eutectics. The per-record file validation.csv (written when the validation is run) carries the flags (moduli_comparable); it is not part of this repository.

| family | n | lattice right | median ρ error | median E error | median G error | σy ratio (median, n) | worst σy ratio |
|---|---|---|---|---|---|---|---|
| aluminium | 117 | 117/117 (100 %) | 0.7 % | +7 % (n=38) | +6 % | 0.31 (n=33) | 0.00 |
| cast_iron | 66 | 61/61 (100 %) | 7.4 % (0.4 % with graphite) | — | — | — | — |
| cobalt | 27 | 27/27 (100 %) | 4.5 % | — | — | — | — |
| copper | 121 | 119/119 (100 %) | 1.5 % | +4 % (n=19) | +3 % | 1.29 (n=60) | 0.00 |
| high_entropy | 22 | 16/22 (73 %) | 1.8 % | -12 % (n=6) | -20 % | 1.10 (n=14) | 0.42 |
| magnesium | 41 | 41/41 (100 %) | 1.9 % | +7 % (n=24) | +9 % | — | — |
| magnetic_electrical | 62 | 56/58 (97 %) | 0.9 % | +11 % (n=39) | +9 % | 0.93 (n=28) | 0.00 |
| nickel | 89 | 89/89 (100 %) | 0.8 % | -7 % (n=37) | -8 % | 1.37 (n=35) | 0.00 |
| other | 27 | 27/27 (100 %) | 1.6 % | — | — | — | — |
| precious_metal | 56 | 56/56 (100 %) | 5.0 % | -6 % (n=43) | -3 % | 1.26 (n=43) | 0.00 |
| refractory | 56 | 56/56 (100 %) | 1.2 % | -38 % (n=29) | -38 % | 0.17 (n=17) | 0.00 |
| shape_memory | 14 | 4/4 (100 %) | 1.2 % | +5 % (n=5) | +1 % | — | — |
| stainless_steel | 131 | 82/82 (100 %) | 0.6 % | -38 % (n=50) | -42 % | 0.54 (n=44) | 0.21 |
| steel | 167 | 167/167 (100 %) | 0.9 % | — | — | — | — |
| titanium | 55 | 35/36 (97 %) | 2.0 % | -15 % (n=33) | -20 % | 0.27 (n=6) | 0.01 |
| tool_steel | 102 | 102/102 (100 %) | 0.7 % | — | — | — | — |
| uranium_zirconium_nuclear | 33 | 33/33 (100 %) | 1.1 % | — | — | — | — |
| zinc | 28 | 28/28 (100 %) | 0.8 % | -32 % (n=10) | -34 % | — | — |
| **all** | 1214 | 1116/1125 (99 %) | 1.0 % | -5 % (n=333) | -7 % | 0.74 (n=280) | 0.00 |

## Retained high-temperature phases (89: austenitic stainless under 25 at% Ni, β-Ti, Hadfield/TWIP, Ni-Resist, NiTi / Ti-Nb β)

These are quenched-in phases; at 0 K the model may put the low-temperature lattice lower, as the real phase diagram does.
The model keeps the retained lattice lowest in 32 of 89; where it does not, the margin says how far the
retained phase sits above (a few tens of meV/atom is the normal price of a metastable phase, hundreds would be a model error).

| alloy | family | retained phase | model's lowest | margin of the retained phase (meV/atom) |
|---|---|---|---|---|
| Ductile Ni-Resist D-2 (ASTM A439) | cast_iron | fcc | bcc | fcc +19 |
| Ni-Resist Type 1 (ASTM A436) | cast_iron | fcc | fcc | 0 (lowest) |
| Ni-Resist Type 2 (ASTM A436) | cast_iron | fcc | bcc | fcc +15 |
| Ni-Resist Type 3 (ASTM A436) | cast_iron | fcc | fcc | 0 (lowest) |
| Ni-Resist Type 5 (low-expansion, ASTM A436) | cast_iron | fcc | fcc | 0 (lowest) |
| C86200 manganese bronze (cast, 90 ksi) | copper | bcc | fcc | bcc +15 |
| C86300 manganese bronze (cast, high strength) | copper | bcc | bcc | 0 (lowest) |
| Elinvar (Fe-36Ni-12Cr, constant-modulus) | magnetic_electrical | fcc | fcc | 0 (lowest) |
| Invar 36 (Fe-36Ni, low thermal expansion) | magnetic_electrical | fcc | bcc | fcc +6 |
| Kovar (Fe-29Ni-17Co, glass-sealing alloy) | magnetic_electrical | fcc | bcc | fcc +21 |
| Super Invar (Fe-32Ni-5Co) | magnetic_electrical | fcc | bcc | fcc +14 |
| Ni-Ti-Cu (Nitinol-Cu Narrow Hysteresis Thermal Actuator Alloy) | shape_memory | bcc | bcc | 0 (lowest) |
| Ni-Ti-Hf (High-Temperature Shape Memory Alloy / HTSMA) | shape_memory | bcc | bcc | 0 (lowest) |
| Ni-Ti-Nb (CryoFit Wide-Hysteresis Hydraulic Coupling Alloy) | shape_memory | bcc | bcc | 0 (lowest) |
| NiTiCu (Ni-Ti-5 to 10 wt% Cu) narrow-hysteresis actuator alloy | shape_memory | bcc | bcc | 0 (lowest) |
| NiTiNb (Ni-Ti-9Nb wide-hysteresis coupling alloy) | shape_memory | bcc | bcc | 0 (lowest) |
| NiTiPd (high-T SMA) | shape_memory | bcc | fcc | bcc +22 |
| Nitinol (NiTi, near-equiatomic — superelastic 55.8 wt% Ni / shape-memory 54.5-55.5 wt% Ni) | shape_memory | bcc | bcc | 0 (lowest) |
| Nitinol 55 (Equiatomic 55Ni-45Ti Shape Memory and Superelastic Alloy) | shape_memory | bcc | bcc | 0 (lowest) |
| Nitinol 56 (higher-Ni, superelastic) | shape_memory | bcc | bcc | 0 (lowest) |
| Nitinol 60 (60Ni-40Ti High-Hardness Non-Galling Structural Alloy) | shape_memory | bcc | bcc | 0 (lowest) |
| 21-4N valve steel (EV8) | stainless_steel | fcc | bcc | fcc +64 |
| 21-6-9 (Nitronic 40) | stainless_steel | fcc | bcc | fcc +44 |
| 23-8N valve steel (EV16) | stainless_steel | fcc | bcc | fcc +39 |
| 253 MA (S30815) | stainless_steel | fcc | bcc | fcc +54 |
| 254 SMO (6 % Mo super-austenitic) | stainless_steel | fcc | bcc | fcc +46 |
| 316LN nitrogen-strengthened austenitic stainless steel | stainless_steel | fcc | bcc | fcc +15 |
| 654 SMO (7 % Mo hyper-austenitic) | stainless_steel | fcc | bcc | fcc +22 |
| A-286 (iron-base superalloy) | stainless_steel | fcc | bcc | fcc +11 |
| AISI Type 309S Stainless Steel | stainless_steel | fcc | bcc | fcc +57 |
| AISI Type 310S Stainless Steel | stainless_steel | fcc | bcc | fcc +18 |
| AL-6XN | stainless_steel | fcc | bcc | fcc +5 |
| Alloy 904L (super-austenitic) | stainless_steel | fcc | fcc | 0 (lowest) |
| CF3M (cast 316L) | stainless_steel | fcc | bcc | fcc +60 |
| CF8 (cast 304) | stainless_steel | fcc | bcc | fcc +60 |
| CF8M (cast 316) | stainless_steel | fcc | bcc | fcc +60 |
| HH (25Cr-12Ni heat-resistant casting) | stainless_steel | fcc | bcc | fcc +19 |
| HK40 (heat-resistant casting) | stainless_steel | fcc | bcc | fcc +7 |
| Myodo H1 | stainless_steel | fcc | bcc | fcc +54 |
| N08926 (1925hMo / 25-6MO) super-austenitic stainless steel | stainless_steel | fcc | bcc | fcc +5 |
| Nitronic 30 | stainless_steel | fcc | bcc | fcc +70 |
| Nitronic 50 (XM-19) | stainless_steel | fcc | bcc | fcc +51 |
| Nitronic 60 | stainless_steel | fcc | bcc | fcc +2 |
| Type 201 stainless | stainless_steel | fcc | bcc | fcc +57 |
| Type 202 stainless | stainless_steel | fcc | bcc | fcc +45 |
| Type 204Cu (J4-type) | stainless_steel | fcc | bcc | fcc +90 |
| Type 301 stainless | stainless_steel | fcc | bcc | fcc +35 |
| Type 302 stainless | stainless_steel | fcc | bcc | fcc +43 |
| Type 303 free-machining stainless | stainless_steel | fcc | bcc | fcc +45 |
| Type 304 stainless (18-8) | stainless_steel | fcc | bcc | fcc +46 |
| Type 304H stainless | stainless_steel | fcc | bcc | fcc +52 |
| Type 304L stainless | stainless_steel | fcc | bcc | fcc +73 |
| Type 304N stainless | stainless_steel | fcc | bcc | fcc +48 |
| Type 305 stainless | stainless_steel | fcc | bcc | fcc +53 |
| Type 308 stainless | stainless_steel | fcc | bcc | fcc +52 |
| Type 309 stainless | stainless_steel | fcc | bcc | fcc +57 |
| Type 310 stainless (25-20) | stainless_steel | fcc | bcc | fcc +11 |
| Type 314 stainless | stainless_steel | fcc | fcc | 0 (lowest) |
| Type 316 stainless | stainless_steel | fcc | bcc | fcc +60 |
| Type 316H stainless | stainless_steel | fcc | bcc | fcc +14 |
| Type 316L stainless | stainless_steel | fcc | bcc | fcc +60 |
| Type 316N stainless | stainless_steel | fcc | bcc | fcc +14 |
| Type 316Ti stainless | stainless_steel | fcc | bcc | fcc +34 |
| Type 317 stainless | stainless_steel | fcc | bcc | fcc +63 |
| Type 317L stainless | stainless_steel | fcc | bcc | fcc +53 |
| Type 317LMN stainless | stainless_steel | fcc | bcc | fcc +38 |
| Type 321 stainless | stainless_steel | fcc | bcc | fcc +46 |
| Type 347 stainless | stainless_steel | fcc | bcc | fcc +55 |
| Type 348 stainless (nuclear 347) | stainless_steel | fcc | bcc | fcc +51 |
| Type 384 stainless | stainless_steel | fcc | bcc | fcc +12 |
| Beta C + Pd (Grade 20) | titanium | bcc | bcc | 0 (lowest) |
| Gum Metal (Ti-23Nb-0.7Ta-2Zr-1.2O, at%) | titanium | bcc | bcc | 0 (lowest) |
| Ti-10V-2Fe-3Al (Ti-10-2-3) | titanium | bcc | bcc | 0 (lowest) |
| Ti-10V-2Fe-3Al (Ti-10-2-3) | titanium | bcc | hcp | bcc +8 |
| Ti-12Mo-6Zr-2Fe (TMZF, ASTM F1813) | titanium | bcc | bcc | 0 (lowest) |
| Ti-13V-11Cr-3Al | titanium | bcc | bcc | 0 (lowest) |
| Ti-13V-11Cr-3Al (B120VCA, the SR-71 alloy) | titanium | bcc | bcc | 0 (lowest) |
| Ti-15Mo (ASTM F2066 implant β alloy) | titanium | bcc | hcp | bcc +8 |
| Ti-15Mo-3Nb-3Al-0.2Si (Beta 21S, Grade 21) | titanium | bcc | bcc | 0 (lowest) |
| Ti-15V-3Cr-3Sn-3Al (Ti-15-3) | titanium | bcc | bcc | 0 (lowest) |
| Ti-2.7Al-13V-7Sn-2Zr (Transage 134) | titanium | bcc | bcc | 0 (lowest) |
| Ti-35Nb-7Zr-5Ta (TNZT / Tiadyne 1610) | titanium | bcc | bcc | 0 (lowest) |
| Ti-3Al-8V-6Cr-4Mo-4Zr (Beta C, Grade 19) | titanium | bcc | bcc | 0 (lowest) |
| Ti-5Al-5Mo-5V-3Cr (Ti-5553) | titanium | bcc | bcc | 0 (lowest) |
| Ti-5Al-5V-5Mo-3Cr | titanium | bcc | bcc | 0 (lowest) |
| Ti-5Al-5V-5Mo-3Cr (Ti-5553) | titanium | bcc | hcp | bcc +0 |
| Titanium Grade 20 (Beta C + Pd) | titanium | bcc | bcc | 0 (lowest) |
| Titanium Grade 36 (Ti-45Nb) | titanium | bcc | bcc | 0 (lowest) |
| Titanium Grade 36 (Ti-45Nb) | titanium | bcc | bcc | 0 (lowest) |

## Lattice wrong (9, retained phases not counted)

| alloy | family | expected | model | margin (meV/atom) | note |
|---|---|---|---|---|---|
| Al0.3CoCrFeNi (Ductile Single-Phase FCC High-Entropy Alloy) | high_entropy | fcc | bcc | {'fcc': 25} | True |
| AlCoCrFeNi (x=1) | high_entropy | bcc | fcc | {'bcc': 23} | False |
| Al0.3CoCrFeNi | high_entropy | fcc | bcc | {'fcc': 3} | True |
| AlCoCrCuFeNi (Yeh 2004 Benchmark 6-Component High-Entropy Alloy) | high_entropy | bcc | fcc | {'bcc': 64} | False |
| AlCoCrFeNi (equiatomic, BCC + B2) | high_entropy | bcc | fcc | {'bcc': 13} | True |
| AlCoCrFeNi (High-Strength BCC/B2 High-Entropy Alloy) | high_entropy | bcc | fcc | {'bcc': 19} | False |
| Alnico 9 | magnetic_electrical | bcc | fcc | {'bcc': 37} | True |
| Alnico 8 (Cast High Coercivity Fe-Co-Ni-Al-Ti Permanent Magnet) | magnetic_electrical | bcc | fcc | {'bcc': 29} | False |
| Ti-8Al-1Mo-1V (Ti-8-1-1) | titanium | hcp | bcc | {'hcp': 6} |  |

## Density off by more than 3 % (208)

Cast irons with the dropped carbon put back as graphite (2.26 g/cc): median error 0.4 % over 55 (white irons excluded — their carbon is cementite).

- BAg-24 (Ag-50Cu20-Zn28-Ni2, Cd-free) (precious_metal): -14.7 % — Ag37.4Zn34.5Cu25.4Ni2.7
- Re-Mo (Mo-rich rhenium, ~50/50 research) (refractory): -14.4 % — Mo66Re34
- Pd-Ag dental alloy (precious_metal): -11.6 % — Pd51.5Ag32.4Sn7.7Zn2.5In2.3Ga2.3Au1.4
- Ni-Resist Type 5 (low-expansion, ASTM A436) (cast_iron): +9.1 % (with graphite +3.7 %) — Fe61.8Ni34.3Si3.1Mn0.8; dropped {'C': 0.0948, 'Cu': 0.002, 'Cr': 0.0005, 'P': 0.0017, 'S': 0.001}
- Ni-Resist Type 3 (ASTM A436) (cast_iron): +8.7 % (with graphite +2.8 %) — Fe63.5Ni29.3Cr3.3Si3.1Mn0.8; dropped {'C': 0.1023, 'Cu': 0.002, 'P': 0.0017, 'S': 0.001}
- AlLiMgScTi / Al20Li20Mg10Sc20Ti30 light-weight HEA (high_entropy): +8.7 % — Ti30.3Sc20Al20Li19.8Mg9.9
- Platinum 950 and Pt-10Ir (jewellery / instrument platinum) (precious_metal): -8.6 % — Pt78.6Co6.8Cu6.4Ir4.2Ru4
- St 707 getter (Zr-V-Fe) (other): +8.6 % — Zr57V35.9Fe7.2
- EN-GJL-150 gray iron (cast_iron): +8.6 % (with graphite -0.0 %) — Fe94Si5.2Mn0.7; dropped {'C': 0.1463, 'P': 0.0012, 'S': 0.0009}
- BAg-8 (Ag-Cu eutectic 72/28) (precious_metal): -8.5 % — Ag60.2Cu39.8
- Ferro-Titanit / Ferro-TiC steel-bonded titanium carbide (33 % TiC in tool-steel matrix) (other): +8.5 % — Fe44.7Ti27.1Cr13Ni8.5Co4.2Mo1.6Si0.9; dropped {'C': 0.2369, 'Mn': 0.0035}
- Cylinder-liner grey iron (alloyed pearlitic, Cr-Cu-Mo) (cast_iron): +8.5 % (with graphite +1.8 %) — Fe94.3Si4.3Mn0.8Cu0.6; dropped {'C': 0.1307, 'Cr': 0.0028, 'Mo': 0.0015, 'Ni': 0.0025, 'P': 0.0032, 'S': 0.0008, 'B': 0.0011}
- CPM M4 high-speed steel (tool_steel): +8.4 % — Fe84.9V4.7Cr4.6Mo3.3W1.8Si0.7; dropped {'C': 0.0619, 'Mn': 0.0031}
- 22 k gold (Au 916 — crown gold Au-Ag-Cu, Krugerrand) (precious_metal): -8.4 % — Au75.3Cu21.2Ag3.5
- Chromium heat-resisting grey iron (1-3 % Cr) (cast_iron): +8.4 % (with graphite +1.5 %) — Fe92.3Si4Cr2.2Mn0.8Ni0.7; dropped {'C': 0.1234, 'Mo': 0.0013, 'P': 0.0012, 'S': 0.0008}
- Grey cast iron, ASTM A48 Class 25 (cast_iron): +8.4 % (with graphite +0.5 %) — Fe95.1Si4.2Mn0.7; dropped {'C': 0.1361, 'P': 0.0016, 'S': 0.0012}
- Grey cast iron, ASTM A48 Class 20 (cast_iron): +8.4 % (with graphite +0.1 %) — Fe94.6Si4.7Mn0.7; dropped {'C': 0.143, 'P': 0.0016, 'S': 0.0012}
- High-phosphorus grey iron (steadite iron) (cast_iron): +8.4 % (with graphite +1.2 %) — Fe95.1Si4.3Mn0.6; dropped {'C': 0.1371, 'P': 0.0156, 'S': 0.0009}
- Meehanite GA/GM (process-controlled grey iron) (cast_iron): +8.4 % (with graphite +0.8 %) — Fe95Si4.2Mn0.8; dropped {'C': 0.1307, 'P': 0.0012, 'S': 0.0009, 'Ca': 0.0003}
- Ductile iron 120-90-02 (quenched and tempered) (cast_iron): +8.3 % (with graphite +0.1 %) — Fe93.4Si4.5Mn0.8Ni0.7Cu0.7; dropped {'C': 0.1436, 'Mg': 0.0009, 'P': 0.0004, 'S': 0.0001, 'Mo': 0.0015}
- EN-GJS-350-22-LT (low-temperature ferritic ductile iron) (cast_iron): +8.3 % (with graphite -0.3 %) — Fe95.7Si4.3; dropped {'C': 0.1487, 'Mn': 0.0009, 'Mg': 0.0009, 'P': 0.0004, 'S': 0.0002, 'Cu': 0.0004, 'Cr': 0.0002}
- Ductile iron 100-70-03 (pearlitic) (cast_iron): +8.2 % (with graphite +0.2 %) — Fe93.9Si5.1Mn0.5Ni0.5; dropped {'C': 0.1449, 'Mg': 0.0009, 'P': 0.0004, 'S': 0.0001, 'Cu': 0.0038, 'Mo': 0.0008}
- C87850 lead-free silicon brass casting (EcoBrass C87850) (copper): -8.1 % — Cu74.4Zn19Si6.6; dropped {'P': 0.002, 'Pb': 0.0001, 'Fe': 0.0006, 'Sn': 0.0008, 'Al': 0.0011, 'Ni': 0.001}
- ASTM A48 Class 20 gray iron (cast_iron): +8.1 % (with graphite -0.3 %) — Fe94.3Si4.9Mn0.7; dropped {'C': 0.1429, 'P': 0.0012, 'S': 0.0009}
- Compacted graphite iron, ASTM A842 Grade 450 (EN-GJV-450, pearlitic) (cast_iron): +8.1 % (with graphite +0.0 %) — Fe94.8Si4.5Cu0.7; dropped {'C': 0.1453, 'Mn': 0.004, 'Sn': 0.0002, 'Mg': 0.0003, 'P': 0.0004, 'S': 0.0001, 'Ti': 0.0002, 'Ce': 0.0}

## Yield, solid-solution records (280): model ÷ measured

| alloy | family | condition | measured MPa | model MPa | ratio |
|---|---|---|---|---|---|
| Aluminium 1050 (99.5 %) | aluminium | O | 30 | 0 | 0.00 |
| Aluminium 1060 (99.6 %) | aluminium | O | 28 | 0 | 0.00 |
| Aluminium 1070 (99.7 %) | aluminium | O | 25 | 0 | 0.00 |
| Aluminium 1100 (99.0 %) | aluminium | O | 34 | 0 | 0.00 |
| Aluminium 1199 (99.99 % super-purity) | aluminium | O | 10 | 0 | 0.00 |
| Aluminium 1235 (foil grade) | aluminium | O (annealed foil) | 30 | 0 | 0.00 |
| Aluminium 1350 (EC, electrical conductor) | aluminium | O (annealed) | 30 | 0 | 0.00 |
| Aluminium 8011 (foil / fin stock) | aluminium | O (annealed soft foil) | 45 | 0 | 0.00 |
| C10100 oxygen-free electronic copper (OFE) | copper | O60 annealed | 69 | 0 | 0.00 |
| C10200 oxygen-free copper (OF / OFHC) | copper | O60 annealed | 69 | 0 | 0.00 |
| C11000 electrolytic tough-pitch copper (ETP) | copper | O60 annealed | 69 | 0 | 0.00 |
| C12000 phosphorus-deoxidised low-residual-phosphorus copper (DLP) | copper | O60 (soft anneal) | 69 | 0 | 0.00 |
| C12200 phosphorus-deoxidised high-residual-phosphorus copper (DHP) | copper | O60 annealed | 69 | 0 | 0.00 |
| C14500 tellurium copper (free-machining) | copper | O60 annealed | 69 | 0 | 0.00 |
| Nickel 200 (commercially pure) | nickel | annealed | 105 | 0 | 0.00 |
| Nickel 201 (low-carbon pure nickel) | nickel | annealed | 80 | 0 | 0.00 |
| Nickel 205 / 270 (electronic nickels) | nickel | annealed | 105 | 0 | 0.00 |
| Fine gold 24 k (Au 999 / 999.9) | precious_metal | annealed | 30 | 0 | 0.00 |
| 18 Karat Green Gold (Electrum) | precious_metal | Annealed | 110 | 0 | 0.00 |
| Molybdenum-lanthana ML (Mo-0.3 to 0.7 % La2O3) | refractory | recrystallised (stays ductile at RT — unlike pure Mo) | 400 | 0 | 0.00 |
| Molybdenum, commercially pure (PM / arc-cast) | refractory | recrystallised (RT) | 350 | 0 | 0.00 |
| Tantalum, commercially pure (unalloyed) | refractory | annealed sheet | 170 | 0 | 0.00 |
| Ta-40Nb (KBI-40 / UNS R05240 related) | refractory | annealed | 200 | 0 | 0.00 |
| Pure iron / Armco magnetic ingot iron / Consumet (Fe ≥ 99.85) | magnetic_electrical | annealed | 120 | 0 | 0.00 |
| Ti-15Mo-3Nb-3Al-0.2Si (Beta 21S, Grade 21) | titanium | solution treated | 830 | 12 | 0.01 |
| Titanium Grade 36 (Ti-45Nb) | titanium | annealed | 450 | 9 | 0.02 |
| Pt-Pd (jewellery / catalyst) | precious_metal | annealed | 150 | 3 | 0.02 |
| FS-85 (Nb-28Ta-10W-1Zr) | refractory | annealed | 480 | 17 | 0.04 |
| 712.0 aluminium | aluminium | F | 170 | 9 | 0.05 |
| C19400 copper-iron (HSM alloy, lead frames) | copper | O61 (annealed) | 165 | 9 | 0.05 |
| 950 Palladium Jewelry Alloy (Pd950Ru) | precious_metal | Annealed | 220 | 13 | 0.06 |
| Pt-W (5–8 W, high-T / electrical) | precious_metal | annealed | 300 | 20 | 0.07 |
| Aluminium 3103 | aluminium | O (annealed) | 45 | 4 | 0.08 |
| Aluminium 3003 | aluminium | O | 41 | 4 | 0.09 |
| 950 Platinum-Iridium Alloy (Pt950Ir) | precious_metal | Annealed | 180 | 16 | 0.09 |
| Aluminium casting 201.0 (A201.0) | aluminium | F | 180 | 17 | 0.10 |
| Aluminium 3105 | aluminium | O (annealed) | 55 | 6 | 0.11 |
| Tantalum-2.5 % tungsten (Ta-2.5W, Tantaloy 63) | refractory | annealed | 240 | 26 | 0.11 |
| C96200 cast 90-10 cupronickel | copper | as-cast | 170 | 25 | 0.15 |
| Ti-12Mo-6Zr-2Fe (TMZF, ASTM F1813) | titanium | β-annealed | 900 | 134 | 0.15 |
| Mo-47.5Re | refractory | annealed | 800 | 120 | 0.15 |
| Molybdenum-41 % rhenium (Mo-41Re) | refractory | annealed | 700 | 110 | 0.16 |
| Re-Mo (Mo-rich rhenium, ~50/50 research) | refractory | annealed | 700 | 122 | 0.17 |
| Aluminium 3005 | aluminium | O | 55 | 11 | 0.20 |
| Nitronic 30 | stainless_steel | annealed | 415 | 89 | 0.21 |
| C70600 copper-nickel 90/10 (CuNi10Fe1Mn) | copper | O61 annealed | 105 | 25 | 0.24 |
| C65100 low-silicon bronze B | copper | O60 (soft anneal) | 105 | 27 | 0.25 |
| Pt-5Ru (95/5) | precious_metal | annealed | 250 | 63 | 0.25 |
| Tantalum-40 % niobium (Ta-40Nb, KBI-40) | refractory | annealed | 190 | 47 | 0.25 |
| 21-6-9 (Nitronic 40) | stainless_steel | annealed | 415 | 111 | 0.27 |
| Aluminium 5005 | aluminium | O | 41 | 11 | 0.27 |
| Alloy 671 (Ni-48Cr, fuel-ash corrosion) | nickel | annealed | 400 | 108 | 0.27 |
| Type 201 stainless | stainless_steel | annealed | 310 | 89 | 0.29 |
| Aluminium 3104 (can body stock) | aluminium | O | 70 | 20 | 0.29 |
| Tantalum-10 % tungsten (Ta-10W) | refractory | annealed | 480 | 142 | 0.30 |
| Type 204Cu (J4-type) | stainless_steel | annealed | 330 | 104 | 0.31 |
| Aluminium 3004 | aluminium | O | 69 | 21 | 0.31 |
| Type 202 stainless | stainless_steel | annealed | 310 | 100 | 0.32 |
| Type 301 stainless | stainless_steel | annealed | 275 | 90 | 0.33 |
| C65500 high-silicon bronze A (Everdur) | copper | O60 annealed | 145 | 50 | 0.35 |
| C72200 copper-nickel 84/16 with chromium (CuNi16Fe1Cr) | copper | O61 annealed | 125 | 44 | 0.35 |
| WC-3009 (Nb-30Hf-9W) | refractory | annealed | 550 | 195 | 0.35 |
| Tungsten-25 % rhenium (W-25Re / W-26Re) | refractory | recrystallized sheet | 850 | 302 | 0.36 |
| Aluminium 5454 | aluminium | O | 117 | 43 | 0.37 |
| T-111 (Ta-8W-2Hf) | refractory | annealed | 550 | 201 | 0.37 |
| Type 304N stainless | stainless_steel | annealed | 240 | 94 | 0.39 |
| Aluminium 5251 | aluminium | O | 80 | 31 | 0.39 |
| C71300 copper-nickel 75/25 (coinage cupronickel) | copper | O61 annealed | 125 | 49 | 0.39 |
| Ti-3Al-8V-6Cr-4Mo-4Zr (Beta C, Grade 19) | titanium | solution treated | 830 | 320 | 0.39 |
| Type 302 stainless | stainless_steel | annealed | 240 | 95 | 0.40 |
| Type 303 free-machining stainless | stainless_steel | annealed | 240 | 96 | 0.40 |
| arsenical copper | copper | O60 (annealed axe blank) | 80 | 32 | 0.40 |
| Inconel MA754 (ODS Ni-20Cr-Y2O3) | nickel | zone annealed (coarse elongated grains along axis) | 580 | 232 | 0.40 |
| Aluminium 5083 | aluminium | O at −196 °C | 165 | 67 | 0.41 |
| Inconel 690 (Ni-Cr-Fe 30 % Cr, nuclear) | nickel | annealed | 300 | 124 | 0.41 |
| Ti-13V-11Cr-3Al (B120VCA, the SR-71 alloy) | titanium | solution treated | 900 | 376 | 0.42 |
| CoCrNi medium-entropy alloy (equiatomic, FCC) | high_entropy | annealed | 350 | 146 | 0.42 |
| 253 MA (S30815) | stainless_steel | annealed | 310 | 133 | 0.43 |
| Nitronic 50 (XM-19) | stainless_steel | annealed | 415 | 177 | 0.43 |
| Aluminium 5052 | aluminium | O | 90 | 39 | 0.43 |
| Aluminium 5024 / AA5028 (Al-Mg-Sc-Zr wrought) | aluminium | O | 160 | 70 | 0.43 |
| C71500 copper-nickel 70/30 (CuNi30Mn1Fe) | copper | O61 annealed | 140 | 60 | 0.43 |
| C87300 silicon bronze casting (statuary) | copper | as cast | 125 | 55 | 0.44 |
| Monel R-405 (free-machining Ni-Cu) | nickel | annealed | 240 | 106 | 0.44 |
| HfNbTaTiZr refractory HEA (Senkov alloy, BCC, ductile) | high_entropy | as cast + HIP (RT) | 930 | 407 | 0.44 |
| Monel 400 (Ni-Cu 67/30) | nickel | annealed | 240 | 108 | 0.45 |
| Green gold / electrum (Au-25Ag) | precious_metal | annealed | 100 | 45 | 0.45 |
| T-222 (Ta-9.6W-2.4Hf-0.01C) | refractory | annealed | 550 | 249 | 0.45 |
| TiZrNbHfTa | high_entropy | annealed | 900 | 403 | 0.45 |
| Type 304 stainless (18-8) | stainless_steel | annealed (ASTM A240 minimum) | 205 | 94 | 0.46 |
| Type 304H stainless | stainless_steel | annealed | 205 | 95 | 0.46 |
| Type 347 stainless | stainless_steel | annealed | 240 | 111 | 0.46 |
| Type 348 stainless (nuclear 347) | stainless_steel | annealed | 240 | 111 | 0.46 |
| AISI Type 309S Stainless Steel | stainless_steel | annealed | 260 | 119 | 0.46 |
| Aluminium 5154 | aluminium | O | 117 | 54 | 0.46 |
| C71640 copper-nickel 66/30/2/2 (CuNi30Fe2Mn2) | copper | O61 annealed tube | 170 | 78 | 0.46 |
| HfNbTaTiZr (Senkov refractory HEA) | high_entropy | as-cast / annealed | 900 | 419 | 0.47 |
| Type 304L stainless | stainless_steel | annealed | 200 | 95 | 0.48 |
| Type 309 stainless | stainless_steel | annealed | 240 | 117 | 0.49 |
| Aluminium 5754 | aluminium | O (annealed) | 100 | 49 | 0.49 |
| Aluminium 5456 | aluminium | O | 159 | 77 | 0.49 |
| C96400 copper-nickel 70/30 casting | copper | as cast | 255 | 125 | 0.49 |
| 18 Karat Palladium White Gold | precious_metal | Annealed | 220 | 108 | 0.49 |
| Type 308 stainless | stainless_steel | annealed | 205 | 103 | 0.50 |
| C87600 silicon brass | copper | as-cast | 220 | 111 | 0.50 |
| AgPd (contacts / thick film) | magnetic_electrical | annealed | 150 | 75 | 0.50 |
| Type 310 stainless (25-20) | stainless_steel | annealed | 275 | 141 | 0.51 |
| 1570 aluminium (Al-Mg-Sc) | aluminium | annealed | 170 | 86 | 0.51 |
| Inconel 600 (Ni-Cr-Fe 72/16/8) | nickel | annealed | 240 | 122 | 0.51 |
| Constantan (Cu-45Ni, thermocouple and resistance alloy) | magnetic_electrical | annealed | 150 | 77 | 0.51 |
| Type 314 stainless | stainless_steel | annealed | 345 | 179 | 0.52 |
| 18 k white gold, palladium type (Au-15Pd-10Ag) | precious_metal | annealed | 250 | 130 | 0.52 |
| Nitronic 60 | stainless_steel | annealed | 380 | 200 | 0.53 |
| Aluminium 5086 | aluminium | O | 117 | 62 | 0.53 |
| Aluminium 5182 (can-end stock) | aluminium | O (annealed) | 130 | 69 | 0.53 |
| Kovar (Fe-29Ni-17Co, glass-sealing alloy) | magnetic_electrical | annealed | 340 | 180 | 0.53 |
| Type 321 stainless | stainless_steel | annealed | 240 | 131 | 0.55 |
| AISI Type 310S Stainless Steel | stainless_steel | annealed | 275 | 154 | 0.56 |
| Type 305 stainless | stainless_steel | annealed | 205 | 117 | 0.57 |
| Type 384 stainless | stainless_steel | annealed | 240 | 139 | 0.58 |
| Ti-15V-3Cr-3Sn-3Al (Ti-15-3) | titanium | solution treated strip | 770 | 450 | 0.58 |
| Aluminium casting 518.0 (Al-Mg die casting) | aluminium | F die cast | 190 | 115 | 0.61 |
| Type 316 stainless | stainless_steel | annealed | 240 | 148 | 0.62 |
| Aluminium 5356 (welding filler) | aluminium | O (filler rod) | 120 | 75 | 0.63 |
| Nichrome 60/16 (Ni-16Cr-24Fe heating alloy) | magnetic_electrical | annealed | 300 | 192 | 0.64 |
| Argentium 960 | precious_metal | annealed | 80 | 52 | 0.65 |
| Type 316L stainless | stainless_steel | annealed | 220 | 148 | 0.67 |
| Type 316N stainless | stainless_steel | annealed | 240 | 161 | 0.67 |
| CoCrFeNi (equiatomic quaternary, FCC) | high_entropy | annealed | 200 | 135 | 0.67 |
| Type 316Ti stainless | stainless_steel | annealed | 240 | 166 | 0.69 |
| Type 317LMN stainless | stainless_steel | annealed | 310 | 212 | 0.69 |
| NbMoTaW | high_entropy | as-cast | 1200 | 832 | 0.69 |
| C87500 silicon brass casting (Tombasil) | copper | as cast | 205 | 144 | 0.70 |
| Aluminium casting 535.0 (Almag 35) | aluminium | F (as-cast without heat treatment) | 140 | 99 | 0.71 |
| 654 SMO (7 % Mo hyper-austenitic) | stainless_steel | annealed | 430 | 311 | 0.72 |
| Aluminium casting 514.0 (Al-Mg) | aluminium | F sand | 85 | 62 | 0.72 |
| Hiperco 50 / Permendur / Vacoflux 50 (Fe-49Co-2V, highest saturation) | magnetic_electrical | annealed 850 °C (magnetic optimum) | 350 | 251 | 0.72 |
| C21000 gilding metal (95/5) | copper | O60 (soft anneal) | 69 | 50 | 0.73 |
| Argentium silver 935 / 960 (Ag-Cu-Ge) | precious_metal | annealed | 100 | 73 | 0.73 |
| Alloy 330 (RA330) | stainless_steel | annealed | 260 | 192 | 0.74 |
| 316LN nitrogen-strengthened austenitic stainless steel | stainless_steel | annealed (A240 min) | 205 | 151 | 0.74 |
| Type 317 stainless | stainless_steel | annealed | 240 | 185 | 0.77 |
| Type 317L stainless | stainless_steel | annealed | 240 | 184 | 0.77 |
| Elinvar (Fe-36Ni-12Cr, constant-modulus) | magnetic_electrical | annealed | 300 | 230 | 0.77 |
| Type 316H stainless | stainless_steel | annealed | 205 | 161 | 0.78 |
| 18k palladium white gold | precious_metal | annealed | 180 | 143 | 0.79 |
| Super Invar (Fe-32Ni-5Co) | magnetic_electrical | annealed | 250 | 198 | 0.79 |
| Britannia silver (Ag 958) | precious_metal | annealed | 90 | 73 | 0.82 |
| Dental casting gold Type III / IV (Au-Ag-Cu-Pd-Pt, ADA/ISO 22674) | precious_metal | softened (Type III) | 280 | 232 | 0.83 |
| Alloy 52 (Fe-52Ni) | magnetic_electrical | annealed | 250 | 208 | 0.83 |
| Alloy 42 (Fe-42Ni Controlled Expansion Alloy) | magnetic_electrical | Annealed strip | 260 | 217 | 0.83 |
| Haynes HR-160 | nickel | solution annealed | 380 | 323 | 0.85 |
| Alloy 48 (Fe-48Ni) | magnetic_electrical | annealed | 250 | 212 | 0.85 |
| 254 SMO (6 % Mo super-austenitic) | stainless_steel | annealed | 310 | 274 | 0.88 |
| Alloy 46 (Fe-46Ni) | magnetic_electrical | annealed | 250 | 220 | 0.88 |
| Alloy 46 (Fe-46Ni Controlled Expansion Alloy) | magnetic_electrical | Annealed | 250 | 219 | 0.88 |
| Hastelloy G-35 | nickel | solution annealed | 365 | 326 | 0.89 |
| EN AC-51300 AlMg5 | aluminium | F | 90 | 81 | 0.90 |
| Incoloy DS (Fe-Ni-Cr-Si, cyclic heat) | nickel | annealed | 240 | 215 | 0.90 |
| Alloy 42 (Fe-42Ni, lead-frame and sealing alloy) | magnetic_electrical | annealed | 240 | 220 | 0.91 |
| Platinum-10 % rhodium (Pt-10Rh: thermocouple, glass bushings) | precious_metal | annealed | 90 | 83 | 0.92 |
| Invar 36 (Fe-36Ni, low thermal expansion) | magnetic_electrical | annealed | 240 | 226 | 0.94 |
| Karma / Evanohm (Ni-20Cr-3Al-3Fe precision resistance alloy) | magnetic_electrical | annealed | 500 | 476 | 0.95 |
| C86500 manganese bronze (cast, 65 ksi) | copper | as cast | 195 | 187 | 0.96 |
| AL-6XN | stainless_steel | annealed | 310 | 304 | 0.98 |
| C63200 nickel-aluminium bronze (weldable NAB, MIL-C-15726) | copper | HR50 hot rolled + stress relieved | 365 | 357 | 0.98 |
| Sterling silver (Ag 925 / Ag-7.5Cu) | precious_metal | annealed | 125 | 122 | 0.98 |
| N08926 (1925hMo / 25-6MO) super-austenitic stainless steel | stainless_steel | annealed (A240 min) | 295 | 293 | 0.99 |
| VNbMoTaW | high_entropy | as-cast | 1400 | 1430 | 1.02 |
| Inconel 693 (Ni-Cr-Fe-Al, metal dusting resistant) | nickel | solution annealed | 450 | 465 | 1.03 |
| Shakudo (Japanese Cu-Au patina alloy) | copper | annealed | 60 | 62 | 1.04 |
| C68700 aluminium brass (arsenical) | copper | O61 annealed tube | 185 | 194 | 1.05 |
| Coin silver (Ag 900 / Ag-10Cu) | precious_metal | annealed | 140 | 147 | 1.05 |
| C63000 nickel-aluminium bronze (wrought, 10 % Al) | copper | O60 annealed | 345 | 368 | 1.07 |
| Hipernik (Ni-50Fe) | magnetic_electrical | annealed | 200 | 213 | 1.07 |
| Inconel 601 (Ni-Cr-Fe-Al, oxidation resistant) | nickel | solution annealed | 275 | 300 | 1.09 |
| 45 Permalloy (Ni-45Fe) | magnetic_electrical | annealed | 200 | 219 | 1.10 |
| C17200 beryllium copper (alloy 25) | copper | TB00 solution annealed (A) | 205 | 227 | 1.11 |
| C28000 Muntz metal (60/40) | copper | O60 annealed | 145 | 161 | 1.11 |
| Alloy 31 (N08031) | stainless_steel | annealed | 276 | 321 | 1.16 |
| Alloy 20 (Carpenter 20Cb-3) | stainless_steel | annealed | 240 | 282 | 1.17 |
| Incoloy 800 / 800H / 800HT (Fe-Ni-Cr) | nickel | solution annealed (800H, grain ≥ ASTM 5) | 205 | 242 | 1.18 |
| NbMoTaW / VNbMoTaW refractory HEA (BCC, 1600 °C strength) | high_entropy | as cast (RT, compression) | 1050 | 1243 | 1.18 |
| Dental gold Type III | precious_metal | Softened (annealed and quenched from 700°C) | 220 | 262 | 1.19 |
| 18 Karat Yellow Gold (750 Yellow Gold) | precious_metal | Annealed (quenched from 650°C) | 210 | 251 | 1.19 |
| Alloy 904L (super-austenitic) | stainless_steel | annealed | 220 | 265 | 1.21 |
| C67500 manganese bronze (wrought, 'A') | copper | O60 annealed | 205 | 248 | 1.21 |
| 22 karat yellow gold | precious_metal | annealed | 80 | 99 | 1.24 |
| 45/50 Permalloy and Deltamax (Ni-50Fe, high saturation) | magnetic_electrical | annealed | 180 | 223 | 1.24 |
| Eutectic HEA AlCoCrFeNi2.1 (lamellar FCC + B2) | high_entropy | as cast (lamellar) | 620 | 767 | 1.24 |
| Electrum / green gold (Au-Ag) | precious_metal | annealed | 80 | 101 | 1.26 |
| C46400 naval brass (60/39/1) | copper | O60 annealed | 170 | 218 | 1.28 |
| Incoloy 825 (Ni-Fe-Cr-Mo-Cu) | nickel | annealed | 240 | 313 | 1.30 |
| C75200 nickel silver 65-18 | copper | O60 (soft anneal) | 170 | 223 | 1.31 |
| A-286 (iron-base superalloy) | stainless_steel | solution treated | 275 | 366 | 1.33 |
| Mumetal (Ni-77Fe-Cu-Mo) | magnetic_electrical | hydrogen-annealed | 150 | 199 | 1.33 |
| MA 6000 | nickel | recrystallised + age | 850 | 1149 | 1.35 |
| Incoloy 800H | nickel | solution annealed | 170 | 234 | 1.37 |
| C95500 nickel-aluminium bronze casting (11 % Al, 4 % Ni) | copper | as cast | 275 | 377 | 1.37 |
| Grain-Oriented Silicon Steel M-6 (Fe-3.2Si Goss Textured Electrical Steel) | magnetic_electrical | Stress-relief annealed sheet (0.35 mm thickness) | 320 | 441 | 1.38 |
| C61300 aluminium bronze (7 % Al, weldable) | copper | O60 annealed | 205 | 285 | 1.39 |
| 18 k yellow gold (Au 750 — Au-12.5Ag-12.5Cu type) | precious_metal | annealed | 180 | 249 | 1.39 |
| C34000 medium-leaded brass | copper | O60 (soft anneal) | 115 | 161 | 1.40 |
| Incoloy 800HT | nickel | solution annealed | 170 | 241 | 1.42 |
| Fe-Cr-Co ductile permanent magnet (Fe-28Cr-15Co, Arnokrome / Chromindur) | magnetic_electrical | solution treated | 400 | 568 | 1.42 |
| C27200 (Yellow Brass 63%) | copper | O60 (soft anneal) | 115 | 165 | 1.44 |
| 14 Karat White Gold | precious_metal | As-cast | 390 | 570 | 1.46 |
| C95800 nickel-aluminium bronze casting (propeller NAB) | copper | as cast | 240 | 352 | 1.47 |
| Dental gold Type I (soft, ISO 1562) | precious_metal | as-cast / softened | 80 | 117 | 1.47 |
| M-6 grain-oriented silicon steel | magnetic_electrical | GO annealed sheet | 300 | 443 | 1.48 |
| Grain-oriented electrical steel M-6 / M-4 (Fe-3.1Si, transformer core) | magnetic_electrical | annealed strip (rolling direction) | 300 | 443 | 1.48 |
| Haynes 214 (Ni-Cr-Al-Fe, alumina former) | nickel | solution annealed (1100 C) | 415 | 617 | 1.49 |
| Hastelloy C-22 (Ni-Cr-Mo-W, high Cr) | nickel | solution annealed 1120 °C | 360 | 541 | 1.50 |
| Dental gold Type II | precious_metal | as-cast | 150 | 227 | 1.51 |
| 14 k white gold, nickel type (Au-58.5, Ni-Cu-Zn) | precious_metal | annealed | 350 | 532 | 1.52 |
| AlCoCrCuFeNi (Yeh 2004) | high_entropy | as-cast | 400 | 609 | 1.52 |
| Al0.3CoCrFeNi (FCC, precipitation-hardenable) | high_entropy | homogenised FCC | 300 | 462 | 1.54 |
| 9 Karat Gold (375 Gold) | precious_metal | As-cast | 260 | 403 | 1.55 |
| Hastelloy S (Ni-Cr-Mo-La, low expansion sheet) | nickel | solution annealed | 400 | 624 | 1.56 |
| Al0.5CoCrFeNi | high_entropy | as-cast duplex | 400 | 624 | 1.56 |
| Hastelloy C-2000 (Ni-Cr-Mo-Cu) | nickel | solution annealed | 350 | 549 | 1.57 |
| AlCoCrFeNi2.1 eutectic HEA | high_entropy | as-cast eutectic | 500 | 791 | 1.58 |
| C75700 nickel silver 65-12 | copper | O60 (soft anneal) | 145 | 233 | 1.61 |
| C26800 / C27000 yellow brass (65/35 and 63/37) | copper | O60 (soft anneal) | 100 | 161 | 1.61 |
| Pd-Cu (40–60 Cu, H2 membrane / electrical) | precious_metal | annealed | 200 | 322 | 1.61 |
| 18 Karat Rose Gold (750 Rose Gold) | precious_metal | Annealed and quenched | 230 | 378 | 1.64 |
| Inconel 686 (Ni-Cr-Mo-W, highest PREN) | nickel | solution annealed | 365 | 603 | 1.65 |
| Alloy 59 (Nicrofer 5923 hMo, Ni-Cr-Mo) | nickel | solution annealed | 340 | 566 | 1.66 |
| Pd-Ag dental alloy | precious_metal | as-cast | 300 | 498 | 1.66 |
| Non-Oriented Silicon Steel M-19 (Fe-3.0Si Isotropic Electrical Steel) | magnetic_electrical | Fully processed / final annealed (0.35 mm sheet) | 360 | 618 | 1.72 |
| CW-6MC (A494, cast 625) | nickel | solution annealed (1175 C) | 345 | 608 | 1.76 |
| Rose / red gold 18 k 5N (Au-20.5Cu-4.5Ag) | precious_metal | annealed | 200 | 357 | 1.78 |
| C74500 nickel silver 65-10 | copper | O60 (soft anneal) | 125 | 225 | 1.80 |
| Hastelloy C-4 (Ni-Cr-Mo, thermally stable) | nickel | solution annealed | 345 | 623 | 1.81 |
| 14 k yellow gold (Au 585 — Au-Ag-Cu-Zn) | precious_metal | annealed | 200 | 375 | 1.87 |
| 10k yellow gold | precious_metal | annealed | 200 | 380 | 1.90 |
| C85700 yellow brass casting (63/1/1/35) | copper | as cast | 125 | 241 | 1.92 |
| 22 k gold (Au 916 — crown gold Au-Ag-Cu, Krugerrand) | precious_metal | annealed | 100 | 192 | 1.92 |
| Arsenical copper / arsenical bronze | copper | O60 annealed (C14200) | 70 | 136 | 1.94 |
| C95200 aluminium bronze casting (9 % Al, 3 % Fe) | copper | as cast | 170 | 330 | 1.94 |
| Al0.3CoCrFeNi | high_entropy | annealed FCC | 250 | 486 | 1.94 |
| C44300 admiralty brass (arsenical) | copper | O61 annealed tube | 125 | 244 | 1.95 |
| Cu-Al-Ni shape-memory alloy | copper | beta-quenched austenite | 200 | 396 | 1.98 |
| CW-2M (A494, cast C-4) | nickel | solution annealed (1200 C water quench) | 310 | 618 | 1.99 |
| Non-oriented electrical steel M-19 / M-27 (Fe-2 to 3.5Si-Al, motor lamination) | magnetic_electrical | annealed sheet | 300 | 599 | 2.00 |
| Nordic gold (Cu-Al-Zn-Sn coinage) | copper | coin blank, annealed | 150 | 308 | 2.05 |
| 18k rose gold | precious_metal | annealed | 180 | 378 | 2.10 |
| C26000 cartridge brass (70/30) | copper | O60 annealed | 76 | 161 | 2.11 |
| 9 k gold (Au 375, Au-Ag-Cu-Zn) | precious_metal | annealed | 180 | 381 | 2.12 |
| Permalloy 80 / Mumetal (Ni-80Fe-5Mo / Ni-77Fe-5Cu-2Cr, high-permeability) | magnetic_electrical | annealed | 150 | 318 | 2.12 |
| Inconel 625 (Ni-Cr-Mo-Nb) | nickel | solution annealed (Grade 2, 1095-1205 °C) | 275 | 619 | 2.25 |
| 9k yellow gold | precious_metal | annealed | 180 | 408 | 2.27 |
| Hastelloy N (Ni-Mo-Cr, molten fluoride salt) | nickel | solution annealed | 315 | 717 | 2.28 |
| Supermalloy (Ni-79Fe-5Mo) | magnetic_electrical | hydrogen-annealed | 150 | 348 | 2.32 |
| Hastelloy B-2 (Ni-Mo, reducing acids) | nickel | solution annealed 1065 °C | 410 | 963 | 2.35 |
| CW-12MW / CW-2M (cast Hastelloy C) | nickel | solution annealed 1200 °C (CW-12MW) | 275 | 649 | 2.36 |
| Hastelloy B-3 (Ni-Mo, thermally stable) | nickel | solution annealed | 400 | 944 | 2.36 |
| Duranickel 301 (age-hardenable nickel) | nickel | annealed | 310 | 742 | 2.39 |
| 97W-2.1Ni-0.9Fe (ASTM B777 Class 4) | refractory | sintered and annealed | 650 | 1577 | 2.43 |
| Pt-5Co (95/5) | precious_metal | annealed | 200 | 538 | 2.69 |
| 18k nickel white gold | precious_metal | annealed | 200 | 569 | 2.85 |
| Tumbaga (pre-Columbian Au-Cu alloy, depletion gilded) | precious_metal | annealed | 150 | 445 | 2.97 |
| Platinum-cobalt (Pt-5Co casting alloy; Pt-23Co 'Platinax' permanent magnet) | precious_metal | Pt-5Co annealed | 180 | 538 | 2.99 |
| N-12MV (A494, cast B-type) | nickel | solution treated (1180 C water quench) | 310 | 935 | 3.02 |
| Platinum 950 and Pt-10Ir (jewellery / instrument platinum) | precious_metal | Pt-5Ir annealed | 140 | 440 | 3.14 |
| C94700 nickel-tin bronze (88-5-2-5, heat-treatable) | copper | as cast | 160 | 628 | 3.93 |
| Cr-5Fe-1Y2O3 (Ducropure-type ODS Cr) | refractory | sintered and hot-rolled sheet | 450 | 1856 | 4.12 |
| Hepatizon | copper | M01 (as-cast / chemically patinated) | 130 | 538 | 4.14 |
| C51900 phosphor bronze (6 % Sn) | copper | O60 (soft anneal) | 150 | 662 | 4.41 |
| C51000 phosphor bronze A (5 % Sn) | copper | O60 annealed | 130 | 598 | 4.60 |
| Shibuichi (Japanese Cu-Ag alloy) | copper | annealed | 80 | 381 | 4.76 |
| C52100 phosphor bronze C (8 % Sn) | copper | O60 annealed | 165 | 809 | 4.90 |
| C90300 tin bronze (88-8-4) | copper | as cast | 145 | 774 | 5.34 |
| C89833 bismuth-selenium lead-free red brass (SeBiLOY / Federalloy) | copper | as cast | 125 | 724 | 5.80 |
| C92300 Navy G bronze | copper | as-cast | 140 | 819 | 5.85 |
| C90500 gun metal / G bronze (88-10-2) | copper | as cast | 150 | 891 | 5.94 |
| C90800 / C91100 high-tin bronze (12-16 % Sn) | copper | as cast (C90800) | 170 | 1012 | 5.96 |
| C90700 tin bronze (89-11) | copper | as cast | 150 | 935 | 6.23 |
| Classical bronze (88-12 Cu-Sn, ancient/'true' bronze) | copper | as cast (modern CuSn12 equivalent) | 150 | 961 | 6.40 |
| C92200 Navy M bronze (steam bronze, 88-6-1.5-4.5) | copper | as cast | 110 | 751 | 6.82 |

## Not run (268 records)

reasons: family tin_lead_solder: not a crystallin (65), family amorphous: not a crystalline soli (36), compound / intermetallic record not a so (29), family low_melting: not a crystalline so (26), elements after cleaning — cell too small (20), non-cubic metal Si (19), group record (several alloys in one) com (18), non-cubic metal Mn (17), composite record (two materials) not an  (9), non-cubic metal Cd (7), non-cubic metal Mn Si (6), non-cubic metal U (6), non-cubic metal Si Mn (3), non-cubic metal Sn (2), non-cubic metal Sn As (1), non-cubic metal In (1), non-cubic metal Mn Ga (1), non-cubic metal In Cd (1), non-cubic metal Hg Sn (1)
