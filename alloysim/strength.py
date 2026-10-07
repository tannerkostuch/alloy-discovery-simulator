"""strength.py — layer 3: from the atomistic numbers to a yield strength.

Solute-strengthening theory for random solid solutions — a dislocation line bending through a field of misfitting
atoms — as parametrised by Curtin's group:
  FCC: Varvenne, Luque & Curtin, Acta Materialia 118 (2016) 164   ("reduced" model, w_c = 5b)
  BCC: Maresca & Curtin, Acta Materialia 182 (2020) 235          (edge-dislocation model for BCC HEAs)
Inputs, all from the atomistic layer: the alloy's shear modulus μ and Poisson ratio ν (Hill averages), its volume per
atom V̄ (→ Burgers vector b), and each element's misfit volume ΔV_n = V_n − V̄ with V_n the element's volume on the same
lattice (Vegard's law).  Outputs: the zero-temperature strength τ_y0, the energy barrier ΔE_b, and the yield stress
σ_y(T, strain rate) = M·τ_y with the Taylor factor of a random polycrystal: M = 3.06 for FCC, 2.73 for BCC (pencil
glide) — the BCC value is Grok's correction (2026-09-29), it was 3.06 for both before.

  τ_y0 = A1 α^(-1/3) μ ((1+ν)/(1−ν))^(4/3) [Σ c_n ΔV_n² / b⁶]^(2/3)
  ΔE_b = A2 α^(1/3)  μ b³ ((1+ν)/(1−ν))^(2/3) [Σ c_n ΔV_n² / b⁶]^(1/3)
  τ_y(T,ε̇) = τ_y0 [1 − (kT/ΔE_b · ln(ε̇0/ε̇))^(2/3)]            while τ_y/τ_y0 > 0.5
           = τ_y0 exp(−(1/0.55) kT/ΔE_b · ln(ε̇0/ε̇))            otherwise (high T)
  FCC: A1 = 0.051·0.35, A2 = 0.274·5.70, α = 0.123, b = a/√2, a = (4V̄)^(1/3)
  BCC: A1 = 0.040,      A2 = 2.00,       α = 1/12,  b = a√3/2, a = (2V̄)^(1/3)
  ε̇0 = 10⁴ s⁻¹.   A second model (Grok) checked every constant above against the papers (from what it knows of
  them, not from the PDFs — 2026-09-29): all confirmed; folded in, the FCC prefactors are 0.01785 and 1.562.
Caveats: the theory is for random solid solutions; ordering, precipitates, grain size (Hall–Petch) and interstitials
add strength on top and are not in this number. HCP alloys are not covered (reported as None).
"""
import math

KB_EV = 8.617333262e-5
EV_A3_TO_GPA = 160.21766208
TAYLOR_M = {"fcc": 3.06, "bcc": 2.73}     # random polycrystal; BCC 2.73 per Grok's check (2026-09-29)
EDOT0 = 1e4

MODELS = {
    "fcc": {"A1": 0.051 * 0.35, "A2": 0.274 * 5.70, "alpha": 0.123},
    "bcc": {"A1": 0.040, "A2": 2.00, "alpha": 1.0 / 12.0},
}


def burgers(lattice, vbar):
    if lattice == "fcc":
        a = (4 * vbar) ** (1 / 3)
        return a / math.sqrt(2), a
    if lattice == "bcc":
        a = (2 * vbar) ** (1 / 3)
        return a * math.sqrt(3) / 2, a
    return None, None


def solute_strength(lattice, at, vbar, v_el, mu_gpa, nu, temps=(77, 300, 600, 900, 1200), edot=1e-3):
    """-> dict: tau_y0_MPa, dE_b_eV, sigma_y_MPa per temperature (K), misfit parameter, b (Å). None for hcp."""
    if lattice not in MODELS:
        return None
    m = MODELS[lattice]
    b, a = burgers(lattice, vbar)
    misfit = sum(c * (v_el[el] - vbar) ** 2 for el, c in at.items()) / b ** 6     # Σ c ΔV² / b⁶ (dimensionless)
    mu = mu_gpa / EV_A3_TO_GPA                                                     # eV/Å³
    nuf = (1 + nu) / (1 - nu)
    tau0 = m["A1"] * m["alpha"] ** (-1 / 3) * mu * nuf ** (4 / 3) * misfit ** (2 / 3)      # eV/Å³
    deb = m["A2"] * m["alpha"] ** (1 / 3) * mu * b ** 3 * nuf ** (2 / 3) * misfit ** (1 / 3)   # eV
    M = TAYLOR_M[lattice]
    out = {"lattice": lattice, "b_A": b, "a_A": a, "misfit_param": misfit, "tau_y0_MPa": tau0 * EV_A3_TO_GPA * 1000,
           "dE_b_eV": deb, "sigma_y_MPa": {}, "edot_per_s": edot, "taylor_M": M,
           "misfit_volumes_A3": {el: v_el[el] - vbar for el in at}}
    for T in temps:
        if deb <= 0 or tau0 <= 0:
            out["sigma_y_MPa"][T] = 0.0
            continue
        x = KB_EV * T / deb * math.log(EDOT0 / edot)
        ratio = 1 - x ** (2 / 3)
        if ratio > 0.5:
            tau = tau0 * ratio
        else:
            tau = tau0 * math.exp(-x / 0.55)
        out["sigma_y_MPa"][T] = M * tau * EV_A3_TO_GPA * 1000
    return out
