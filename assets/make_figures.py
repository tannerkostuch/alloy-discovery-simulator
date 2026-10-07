#!/usr/bin/env python3
"""make_figures.py — draws the README's banner and figures as SVG files next to this script.

    python assets/make_figures.py          (needs matplotlib, only for turning text into outlines)

The look — a dark card that reads on GitHub's white and near-black pages, three colours — was designed by Gemini;
this script only builds it. Text is converted to outlines, so the images look the same on every system and load no
fonts (Liberation Sans / Mono when installed, otherwise the DejaVu fonts that ship with matplotlib).

Every number drawn here is in docs/RESULTS.md:
  yield_validation.svg   the table "every benchmark re-found at its calibrated handbook value" (the backyard runs)
  zinc_fix.svg           section 4, "Zinc — a failure worth keeping"
The chart colours passed a colour-blindness and contrast check against the card colour before they were used.
"""
import math
from pathlib import Path

from matplotlib.font_manager import FontProperties, findfont, get_font
from matplotlib.textpath import TextPath

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- the palette
PAGE_DARK = "#0d1117"      # banner background (GitHub's dark page colour)
CARD = "#161b22"           # card canvas
BORDER = "#30363d"
GRID = "#21262d"
INK = "#f0f6fc"            # titles, values
MUTED = "#8b949e"          # axes, captions
BLUE = "#388bfd"           # calibrated / primary
GREEN = "#2ea043"          # handbook / measured   (the designer's #3fb950, one step darker: inside the lightness
AMBER = "#db6d28"          # raw model             (band the colour check asks of marks on this card; ditto #f0883e)
BANNER_GREEN = "#3fb950"   # the banner is not a chart: it keeps the designer's green


# ---------------------------------------------------------------- text as outlines
def _font(names, weight="normal"):
    for n in names:
        try:
            return findfont(FontProperties(family=n, weight=weight), fallback_to_default=False)
        except Exception:  # noqa: BLE001
            continue
    return findfont(FontProperties(family="DejaVu Sans", weight=weight))


SANS = _font(["Liberation Sans", "Arimo", "DejaVu Sans"])
SANS_B = _font(["Liberation Sans", "Arimo", "DejaVu Sans"], "bold")
MONO_B = _font(["Liberation Mono", "Cousine", "DejaVu Sans Mono"], "bold")


def advance(text, fname, size):
    f = get_font(fname)
    f.set_size(size, 72)
    f.set_text(text, 0.0)
    return f.get_width_height()[0] / 64.0


def _d(path):
    """matplotlib path -> SVG path data (y flipped by the caller's transform)."""
    out, v, c, i = [], path.vertices, path.codes, 0
    while i < len(c):
        k = c[i]
        if k == 1:
            out.append(f"M{v[i][0]:.2f} {v[i][1]:.2f}"); i += 1
        elif k == 2:
            out.append(f"L{v[i][0]:.2f} {v[i][1]:.2f}"); i += 1
        elif k == 3:
            out.append(f"Q{v[i][0]:.2f} {v[i][1]:.2f} {v[i+1][0]:.2f} {v[i+1][1]:.2f}"); i += 2
        elif k == 4:
            out.append(f"C{v[i][0]:.2f} {v[i][1]:.2f} {v[i+1][0]:.2f} {v[i+1][1]:.2f} {v[i+2][0]:.2f} {v[i+2][1]:.2f}"); i += 3
        else:
            out.append("Z"); i += 1
    return "".join(out)


def text(x, y, s, size, fill, font=None, anchor="start", tracking=0.0, rotate=None, opacity=None):
    """one line of text as a filled outline; x, y = baseline start (or middle / end with anchor)."""
    font = font or SANS
    prop = FontProperties(fname=font)
    if tracking:
        width = sum(advance(ch, font, size) for ch in s) + tracking * (len(s) - 1)
        parts, cx = [], 0.0
        for ch in s:
            if ch != " ":
                parts.append((cx, _d(TextPath((0, 0), ch, size=size, prop=prop))))
            cx += advance(ch, font, size) + tracking
    else:
        width = advance(s, font, size)
        parts = [(0.0, _d(TextPath((0, 0), s, size=size, prop=prop)))]
    x0 = x - (width / 2 if anchor == "middle" else width if anchor == "end" else 0)
    rot = f" rotate({rotate})" if rotate is not None else ""
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    if rotate is not None:        # rotate about the anchor point
        return "".join(f'<path transform="translate({x:.2f} {y:.2f}){rot} translate({dx - (x - x0):.2f} 0) scale(1 -1)" d="{d}" fill="{fill}"{op}/>'
                       for dx, d in parts)
    return "".join(f'<path transform="translate({x0 + dx:.2f} {y:.2f}) scale(1 -1)" d="{d}" fill="{fill}"{op}/>' for dx, d in parts)


def svg(name, w, h, title, desc, body):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>{"".join(body)}</svg>\n')
    (OUT / name).write_text(doc, encoding="utf-8")
    print(f"{name}: {len(doc) / 1000:.1f} kB")


def card(w, h, fill=CARD):
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" fill="{fill}" stroke="{BORDER}"/>'


def column(x, y_top, y_base, width, fill, r=4):
    """a column with a rounded data-end and a square foot on the baseline."""
    r = min(r, width / 2, max(0.0, y_base - y_top))
    return (f'<path d="M{x:.2f} {y_base:.2f}V{y_top + r:.2f}Q{x:.2f} {y_top:.2f} {x + r:.2f} {y_top:.2f}H{x + width - r:.2f}'
            f'Q{x + width:.2f} {y_top:.2f} {x + width:.2f} {y_top + r:.2f}V{y_base:.2f}Z" fill="{fill}"/>')


# ---------------------------------------------------------------- banner
def banner():
    w, h = 800, 180
    b = [card(w, h, PAGE_DARK)]
    # a honeycomb lattice on the right (x 520-760): a wireframe, and twelve atoms on its two sub-lattices
    a = 30.0                                              # bond length
    cx, cy = 640.0, 90.0
    verts, edges = {}, set()
    for i in range(-6, 7):
        for j in range(-6, 7):
            ox, oy = cx + a * math.sqrt(3) * (i + j / 2), cy + a * 1.5 * j
            for k, (dx, dy) in enumerate(((0.0, -a / 2), (0.0, a / 2))):     # the two atoms of a cell; bond is vertical
                verts[(i, j, k)] = (ox + dx, oy + dy)
    for (i, j, k), _ in verts.items():
        if k == 0:
            for nb in ((i, j, 1), (i, j - 1, 1), (i + 1, j - 1, 1)):
                if nb in verts:
                    edges.add(((i, j, 0), nb))
    b.append(f'<clipPath id="c"><rect x="520" y="14" width="240" height="152"/></clipPath><g clip-path="url(#c)" stroke="{GRID}" stroke-width="1.5" stroke-linecap="round">')
    for p, q in sorted(edges):
        (x1, y1), (x2, y2) = verts[p], verts[q]
        if max(x1, x2) < 500 or min(x1, x2) > 780 or max(y1, y2) < 0 or min(y1, y2) > 180:
            continue
        b.append(f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"/>')
    b.append("</g>")
    inside = [(key, xy) for key, xy in verts.items() if 536 <= xy[0] <= 744 and 30 <= xy[1] <= 150]
    inside.sort(key=lambda t: (math.hypot(t[1][0] - cx, t[1][1] - cy), t[1][1], t[1][0]))
    for (i, j, k), (x, y) in sorted(inside[:12], key=lambda t: (t[1][1], t[1][0])):
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE if k == 0 else BANNER_GREEN}"/>')
    b.append(text(48, 60, "SCREENING & CALIBRATION PIPELINE", 11, MUTED, MONO_B, tracking=1.5))
    b.append(text(48, 100, "Alloy Discovery Simulator", 32, INK, SANS_B))
    b.append(text(48, 130, "Physics-based screening, validated against 1,214 known alloys", 14, MUTED))
    svg("banner.svg", w, h, "Alloy Discovery Simulator",
        "Screening and calibration pipeline. Physics-based screening, validated against 1,214 known alloys.", b)


# ---------------------------------------------------------------- figure 1: the six steps
def funnel():
    w, h = 760, 120
    steps = ["Sample", "Screen", "Shortlist", "Simulate", "Rank", "Compare"]
    b = [card(w, h)]
    pad, gap, nh = 28, 30, 44
    nw = (w - 2 * pad - gap * (len(steps) - 1)) / len(steps)
    y = (h - nh) / 2
    for i, s in enumerate(steps):
        x = pad + i * (nw + gap)
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{nw:.1f}" height="{nh}" rx="6" fill="{GRID}" stroke="{BLUE}" stroke-width="1.5"/>')
        b.append(text(x + nw / 2, y + nh / 2 + 4.8, s, 13.5, INK, SANS_B, anchor="middle"))
        if i < len(steps) - 1:
            x1, x2, ym = x + nw + 5, x + nw + gap - 5, h / 2
            b.append(f'<path d="M{x1:.1f} {ym}H{x2 - 5:.1f}" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round"/>')
            b.append(f'<path d="M{x2:.1f} {ym}l-7 -4v8z" fill="{MUTED}"/>')
    svg("funnel.svg", w, h, "What the simulator does, in six steps",
        "Sample, then screen, then shortlist, then simulate, then rank, then compare.", b)


# ---------------------------------------------------------------- figure 2: yield, model vs calibrated vs handbook
# (name, composition, raw model, calibrated, handbook low, handbook high) — MPa, annealed; docs/RESULTS.md
YIELD = [
    ("5083 / 5182", "Al-5Mg", 73, 143, 130, 145),
    ("6061", "Al-1Mg-0.6Si", 15, 55, 55, 55),
    ("7075", "Al-Zn-Mg-Cu", 44, 99, 103, 103),
    ("Cartridge brass", "Cu-30Zn", 164, 117, 75, 110),
    ("Tin bronze", "Cu-12Sn", 964, 172, 150, 190),
    ("Aluminium bronze", "Cu-7Al", 263, 188, 210, 230),
    ("Silicon bronze", "Cu-3Si-1Mn", 42, 105, 145, 145),
]


def yield_validation():
    w, h = 720, 280
    left, right, top, base = 62, 20, 98, 222           # the plot box (room above it for the bar that runs off the scale)
    ymax = 300.0
    Y = lambda v: base - (base - top) * v / ymax       # noqa: E731
    b = [card(w, h)]
    b.append(text(20, 30, "Model vs Handbook Yield Strength", 14, INK, SANS_B))
    # legend, centered at the top of the plot
    items = [("Raw Model", AMBER), ("Calibrated", BLUE), ("Handbook", GREEN)]
    widths = [12 + 6 + advance(n, SANS, 11.5) for n, _ in items]
    lx = left + ((w - right - left) - (sum(widths) + 22 * (len(items) - 1))) / 2
    for (n, col), wd in zip(items, widths):
        b.append(f'<rect x="{lx:.1f}" y="48" width="12" height="12" rx="2.5" fill="{col}"/>')
        b.append(text(lx + 18, 58, n, 11.5, INK))
        lx += wd + 22
    # grid and axis
    for v in (0, 100, 200, 300):
        b.append(f'<path d="M{left} {Y(v):.1f}H{w - right}" stroke="{BORDER if v == 0 else GRID}" stroke-width="1"/>')
        b.append(text(left - 8, Y(v) + 3.8, f"{v}", 10.5, MUTED, anchor="end"))
    b.append(text(18, (top + base) / 2, "Yield Strength (MPa)", 10.5, MUTED, anchor="middle", rotate=-90))
    band = (w - right - left) / len(YIELD)
    bw, sg = 18, 2                                      # bar width, the gap between touching bars
    for i, (name, comp, raw, cal, lo, hi) in enumerate(YIELD):
        x0 = left + band * i + (band - (3 * bw + 2 * sg)) / 2
        hb = (lo + hi) / 2
        for k, (v, col) in enumerate(((raw, AMBER), (cal, BLUE), (hb, GREEN))):
            x = x0 + k * (bw + sg)
            if v > ymax:                                # off the scale: run past the top line, cut the bar, write the value
                yt = top - 12
                b.append(column(x, yt, base, bw, col))
                b.append(f'<path d="M{x - 2} {top + 9}l{bw + 4} -7" stroke="{CARD}" stroke-width="3.5"/>')
                b.append(text(x + bw / 2, yt - 5, f"{v:,}", 10.5, INK, SANS_B, anchor="middle"))
            else:
                b.append(column(x, Y(v), base, bw, col))
        if hi > lo:                                     # the published range, as a line on the handbook bar
            xm = x0 + 2 * (bw + sg) + bw / 2
            b.append(f'<path d="M{xm:.1f} {Y(hi):.1f}V{Y(lo):.1f}M{xm - 4:.1f} {Y(hi):.1f}h8M{xm - 4:.1f} {Y(lo):.1f}h8" stroke="{INK}" stroke-width="1.5" stroke-linecap="round" fill="none"/>')
        xc = left + band * i + band / 2
        b.append(text(xc, base + 16, name, 10.5, INK, anchor="middle"))
        b.append(text(xc, base + 30, comp, 10, MUTED, anchor="middle"))
    svg("yield_validation.svg", w, h, "Model vs handbook yield strength for seven classic alloys",
        "Grouped bars, yield strength in MPa, raw model / calibrated / handbook. "
        + "; ".join(f"{n} ({c}): {r}, {k}, {lo if lo == hi else f'{lo} to {hi}'}" for n, c, r, k, lo, hi in YIELD)
        + ". Tin bronze's raw value, 964, is off the 0 to 300 scale.", b)


# ---------------------------------------------------------------- figure 3: zinc
def zinc_fix():
    w, h = 540, 180
    left, right, top, base = 46, 150, 62, 142
    ymax = 100.0
    Y = lambda v: base - (base - top) * v / ymax       # noqa: E731
    b = [card(w, h)]
    b.append(text(20, 28, "Zinc Stiffness Correction", 14, INK, SANS_B))
    b.append(text(20, 44, "Young's modulus of pure zinc (GPa)", 10.5, MUTED))
    for v in (0, 50, 100):
        b.append(f'<path d="M{left} {Y(v):.1f}H{w - right}" stroke="{BORDER if v == 0 else GRID}" stroke-width="1"/>')
        b.append(text(left - 8, Y(v) + 3.8, f"{v}", 10.5, MUTED, anchor="end"))
    bars = [("First run", 3), ("Cell shape fixed", 59), ("With the × 1.45 reading", 86)]
    band = (w - right - left) / len(bars)
    for i, (label, v) in enumerate(bars):
        xc = left + band * i + band / 2
        b.append(column(xc - 12, Y(v), base, 24, BLUE))
        b.append(text(xc, Y(v) - 6, f"{v}", 11.5, INK, SANS_B, anchor="middle"))
        b.append(text(xc, base + 16, label, 10.5, INK, anchor="middle"))
    ym = Y(85)                                         # the measured value: a dashed benchmark line
    b.append(f'<path d="M{left} {ym:.1f}H{w - right + 8}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 4" stroke-linecap="round"/>')
    b.append(text(w - right + 16, ym + 4, "Measured: 85 GPa", 11.5, INK))
    svg("zinc_fix.svg", w, h, "Zinc stiffness correction",
        "Young's modulus of pure zinc in GPa: 3 in the first run, 59 once the cell shape was fixed, 86 with the 1.45 reading; measured 85.", b)


if __name__ == "__main__":
    banner(); funnel(); yield_validation(); zinc_fix()
