#!/usr/bin/env python3
"""run_screen_db.py — the composition rules for every alloy of the reference database ($ALLOYS_DB or data/alloys.json,
format in docs/DATABASE.md) → data/db_features.csv
and a check of the rules against what is known: how many of each family land in the 'solid solution' window."""
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd  # noqa: E402

from alloysim import compo, screen  # noqa: E402


def main():
    if not compo.have_db():
        sys.exit(f"no reference database at {compo.DB_FINAL} — set ALLOYS_DB=/path/to/alloys.json (format: docs/DATABASE.md; "
                 "an example: data/alloys.example.json)")
    db = compo.load_db()
    rows = []
    for rid, name, fam, at in db:
        f = screen.features(at); f.update({"id": rid, "name": name, "family": fam}); rows.append(f)
    df = pd.DataFrame(rows)
    out = Path(__file__).resolve().parent / "data"; out.mkdir(exist_ok=True)
    df.to_csv(out / "db_features.csv", index=False)
    print(f"{len(df)} alloys featurised -> {out / 'db_features.csv'}")
    tab = df.groupby("family")["phase_guess"].value_counts().unstack(fill_value=0)
    print(tab.to_string())
    lines = ["# the composition rules against the database", "", f"{len(df)} alloys; per family, where the rules put them:", "", tab.to_markdown(), "",
             "Expected: the single-phase families (stainless, nickel, copper, high_entropy) mostly 'solid solution'; the compound-based",
             "ones (amorphous, shape_memory, low_melting solders, precious dental alloys) elsewhere. Dilute alloys stretch the rules,",
             "which were built for concentrated ones — that is why the search starts with multi-principal families."]
    (out / "DB_RULES_CHECK.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
