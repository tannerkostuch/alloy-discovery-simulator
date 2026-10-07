#!/usr/bin/env python3
"""run_smoke.py — does the physics engine agree with what is known? (run once per machine/engine; ~10-40 min on CPU,
a few minutes on a GPU whose forces can be trusted). Writes SMOKE_REPORT.md.
  * lattice constants of Al, Cu, Ni, Fe, W, Ti (vs experiment)
  * formation energy of B2 NiAl and L1₂ Ni₃Al (vs DFT / experiment)
  * elastic constants of Cu, Ni, Fe, W (vs experiment)
  * the Cantor alloy CoCrFeMnNi: lattice preference, E_mix, elastic moduli, predicted yield stress at 300 K (expt ~200 MPa)
  * NbMoTaW: BCC, yield stress (expt ~1000 MPa at RT)
"""
import argparse
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from alloysim import atomistic as A, compo, search as S  # noqa: E402

EXPT_A = {"Al": ("fcc", 4.05), "Cu": ("fcc", 3.615), "Ni": ("fcc", 3.52), "Fe": ("bcc", 2.867), "W": ("bcc", 3.165), "Nb": ("bcc", 3.30), "Ti": ("hcp", 2.95)}
EXPT_C = {"Cu": (168, 121, 75), "Ni": (247, 147, 125), "Fe": (230, 135, 117), "W": (523, 203, 160)}
EXPT_EF = {"NiAl (B2)": -0.62, "Ni3Al (L12)": -0.45}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="auto"); ap.add_argument("--model", default="medium-mpa-0"); ap.add_argument("--device", default=None)
    ap.add_argument("--quick", action="store_true", help="skip the elastic constants and the alloys")
    ap.add_argument("--alloys-only", action="store_true", help="only the two alloys (elements and compounds are cached anyway)")
    ap.add_argument("--workers", type=int, default=2, help="the two alloys at once in worker processes (CPU); 1 = serial")
    a = ap.parse_args()
    t0 = time.time()
    lines = [f"# smoke test — {time.strftime('%Y-%m-%d %H:%M')}", ""]
    log = print
    eng = A.Engine(kind=a.engine, model=a.model, device=a.device, log=log)
    lines.append(f"engine: **{eng.name}**"); lines.append("")
    lines += ["## lattice constants (Å)", "", "| element | lattice | model | experiment | error |", "|---|---|---|---|---|"]
    for el, (L, aexp) in ([] if a.alloys_only else EXPT_A.items()):
        try:
            r = eng.reference(el, L); g = eng.ground(el)
            lines.append(f"| {el} | {L} (model ground: {g[0]}) | {r['a']:.3f} | {aexp} | {100*(r['a']-aexp)/aexp:+.1f} % |")
            log(f"{el} {L}: a = {r['a']:.3f} (expt {aexp})")
        except Exception as e:
            lines.append(f"| {el} | {L} | failed: {e} | | |")
    lines += ["", "## formation energies (eV/atom)", "", "| compound | model | reference (DFT/expt) |", "|---|---|---|"]
    for name, ref in ([] if a.alloys_only else EXPT_EF.items()):
        try:
            kind = "b2" if "B2" in name else "l12"
            comp = {"Ni": 0.5, "Al": 0.5} if kind == "b2" else {"Ni": 0.75, "Al": 0.25}
            vbar = sum(c * eng.ground(el)[1]["v"] for el, c in comp.items())
            at = A.prototype(kind, "Ni", "Al", ((2 if kind == "b2" else 4) * vbar) ** (1 / 3))
            eng.relax(at, fmax=0.01, steps=200, cell=True)
            e = eng.energy(at) / len(at)
            ef, _ = A.formation_energy(eng, comp, e)
            lines.append(f"| {name} | {ef:+.3f} | {ref:+.2f} |"); log(f"{name}: E_form = {ef:+.3f} eV/atom (ref {ref})")
        except Exception as e:
            lines.append(f"| {name} | failed: {e} | {ref} |")
    if not a.quick:
        lines += ["", "## elastic constants (GPa)", "", "| element | C11 | C12 | C44 | expt C11/C12/C44 | B | G | B/G |", "|---|---|---|---|---|---|---|---|"]
        for el, (c11, c12, c44) in ([] if a.alloys_only else EXPT_C.items()):
            try:
                L = EXPT_A[el][0]
                cell = A.elemental_cell(el, L, eng.reference(el, L)["a"]).repeat((2, 2, 2))
                eng.relax(cell, cell=True)
                C, m = A.elastic(eng, cell)
                lines.append(f"| {el} | {m['C11']:.0f} | {m['C12']:.0f} | {m['C44']:.0f} | {c11}/{c12}/{c44} | {m['B_GPa']:.0f} | {m['G_GPa']:.0f} | {m['pugh_B_over_G']:.2f} |")
                log(f"{el}: C11 {m['C11']:.0f} C12 {m['C12']:.0f} C44 {m['C44']:.0f} (expt {c11}/{c12}/{c44})")
            except Exception as e:
                lines.append(f"| {el} | failed: {e} | | | | | | |")
        lines += ["", "## two known alloys through the whole chain", ""]
        alloys = (("CoCrFeMnNi (Cantor; expt: FCC, σy ≈ 200 MPa at RT, G ≈ 80 GPa)", "CoCrFeMnNi", ("fcc", "bcc")),
                  ("NbMoTaW (expt: BCC, σy ≈ 1000 MPa at RT)", "NbMoTaW", ("bcc", "fcc")))
        results = {}
        if a.workers > 1 and eng.kind == "mace":            # both at once, half the threads each
            import os
            from concurrent.futures import ProcessPoolExecutor
            from multiprocessing import get_context
            for el in ("Co", "Cr", "Fe", "Mn", "Ni", "Nb", "Mo", "Ta", "W"):
                eng.ground(el)
            threads = max(1, (os.cpu_count() or 4) // a.workers)
            with ProcessPoolExecutor(max_workers=a.workers, mp_context=get_context("spawn"), initializer=S._worker_init,
                                     initargs=(eng.spec, threads)) as ex:
                futs = {ex.submit(S._worker_eval, f, compo.parse(f), lat, 108, (0,), True, True): f for _, f, lat in alloys}
                for fut in futs:
                    try:
                        _, r, _ = fut.result()
                    except Exception as e:  # noqa: BLE001
                        r = {"error": f"{e.__class__.__name__}: {e}"}
                    results[futs[fut]] = r
            eng.refresh()
        for name, f, lat in alloys:
            try:
                r = results.get(f) or S.evaluate(eng, compo.parse(f), lattices=lat, target_atoms=108, seeds=(0,), log=log)
                if r.get("error"):
                    raise RuntimeError(r["error"])
                lines.append(f"- **{name}**: {S.summary_line(r)}")
                lc = r.get("lattice_check") or {}
                cells = ", ".join("%s: %.4f eV/atom" % (k, v["e_per_atom"]) for k, v in r["cells"].items())
                verdict = ("stays " + r["lattice"]) if lc.get("stable", True) else "WOULD TRANSFORM"
                lines.append(f"  - cells: {{ {cells} }}; free-cell check on the winner: energy drop {1000*lc.get('e_drop_eV', 0):.1f} meV/atom, shape change {lc.get('shape_change', 0):.3f} → {verdict}")
                logs = Path(__file__).resolve().parent / "logs"
                logs.mkdir(exist_ok=True)
                (logs / f"smoke_{f}.json").write_text(json.dumps(r, indent=1, default=float))
                st = r.get("strength") or {}
                if st:
                    lines.append(f"  - σy(T) MPa: {st['sigma_y_MPa']}; τ_y0 {st['tau_y0_MPa']:.0f} MPa, ΔE_b {st['dE_b_eV']:.2f} eV, misfit volumes Å³ {{ {', '.join(f'{k}: {v:+.2f}' for k, v in st['misfit_volumes_A3'].items())} }}")
                h = r.get("hull") or {}
                lines.append(f"  - hull-lite: ΔE_dec {h.get('de_dec')}, T* {h.get('T_star_K')}, would rather be {h.get('mixture')}")
            except Exception as e:
                lines.append(f"- {name}: failed: {e}")
    lines += ["", f"took {time.time()-t0:.0f} s"]
    out = Path(__file__).resolve().parent / "SMOKE_REPORT.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("->", out)


if __name__ == "__main__":
    main()
