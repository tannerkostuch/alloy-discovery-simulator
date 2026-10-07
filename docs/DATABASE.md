# The reference database of known alloys (optional)

Two things in the simulator compare its output with alloys that already exist:

- **novelty** — a discovery run marks a candidate `NEW` when no known alloy lies within 6 at% of it, and otherwise names
  the nearest one;
- **validation** — `run_validate.py` runs every known alloy through the same physics chain and scores the result
  against what was measured (lattice, density, moduli, annealed yield, phases).

Both read one JSON file of known alloys. The results in this repository were computed against a database of 1 482
alloys that is **not part of this repository**. Without a database a discovery run still works — its "new?" column
reads `n/a` — and the validation has nothing to run on.

## Where the file goes

`$ALLOYS_DB` if that environment variable is set, otherwise `data/alloys.json` (git-ignored on purpose).

`data/alloys.example.json` holds ten well-known alloys with typical handbook values, enough to try the machinery:

```
ALLOYS_DB=data/alloys.example.json python run_validate.py --list              # what would run, and why
ALLOYS_DB=data/alloys.example.json python run_validate.py --tier 1 --atoms 32   # lattice + density, small cells: minutes
```

Those ten are an example of the format, not a data source. One of them, the Cantor alloy, is skipped by the
validation's own rule (an element with a complex ground-state structure, here manganese, at 10 at% or more) — that
is what a skipped record looks like in the listing. The validation writes into `results/validation/`, which is
git-ignored; the scorecard of the 1 482-alloy database is kept separately as `results/VALIDATION_1214_alloys.md`.

## Format

A list of records, or an object with the list under `"alloys"` or `"records"`:

```json
{
  "id": "cu-c26000",
  "name": "C26000 cartridge brass (70/30)",
  "family": "copper",
  "subfamily": "alpha brass",
  "composition": {
    "basis": "wt%",
    "elements": [
      {"element": "Cu", "nominal": 70.0, "balance": true},
      {"element": "Zn", "nominal": 30.0, "min": 28.5, "max": 31.5}
    ],
    "notes": "single-phase alpha (fcc) brass"
  },
  "properties": {
    "density_g_cm3": 8.53,
    "youngs_modulus_gpa": 110,
    "shear_modulus_gpa": 40,
    "poissons_ratio": 0.375,
    "mechanical": [
      {"condition": "annealed (OS050)", "yield_strength_mpa": 105}
    ]
  }
}
```

| field | used for |
|---|---|
| `id` | file names of the validation results; must be unique |
| `name`, `subfamily` | read for phase words when deciding which lattice the alloy should have ("austenitic", "duplex", "beta", "alpha-beta", …; Greek letters are spelled out before matching) |
| `family` | the first rule for the expected lattice, and the grouping of the scorecard. Names the code knows: `aluminium`, `copper`, `nickel`, `stainless_steel`, `steel`, `tool_steel`, `cast_iron`, `titanium`, `magnesium`, `zinc`, `cobalt`, `refractory`, `precious_metal`, `magnetic_electrical`, `high_entropy`, `shape_memory`, `uranium_zirconium_nuclear`; `amorphous`, `low_melting` and `tin_lead_solder` are skipped; anything else takes the lattice of its base element |
| `composition.basis` | `"wt%"` (default) or `"at%"` |
| `composition.elements[]` | `nominal`, or the middle of `min`/`max`, per element; the element marked `balance` takes what is left to 100 |
| `composition.notes` | only for `high_entropy` records: the words "fcc", "bcc" or "hcp" here set the expected lattice |
| `properties.density_g_cm3`, `youngs_modulus_gpa`, `shear_modulus_gpa`, `poissons_ratio` | the measured values the model is compared with; leave out or `null` what is not known |
| `properties.mechanical[]` | `condition` + `yield_strength_mpa`. Only annealed-like conditions are compared with the solute-strengthening yield (annealed, solution-treated, O, as-cast, hot-rolled, recrystallised, …); aged, cold-worked, tempered and T-/H-temper entries are ignored |

What the validation does with a record — which interstitials and traces it drops, which families and record kinds
it skips, how the expected lattice is read where the record carries no phase word (Bania's molybdenum equivalent for
titanium, Guillet's zinc equivalent for brass, nickel content for cast stainless grades), and which records count
as "retained high-temperature phases" scored by margin instead of right/wrong — is in `alloysim/validate.py`
(`select`, `expected_lattices`, `retained_phase`, `yield_is_solid_solution`) and described in `DESIGN.md`.

Placeholders hurt: a database that lists pure copper's 117 GPa for every copper alloy, or a round 200 GPa for
every high-entropy alloy, is flagged by `moduli_comparable` and left out of the modulus medians — better to leave
an unknown value out than to fill it in.
