"""Generates assets/header.svg: blocky voxel header (original art, no game assets).

python tools/voxel.py  ->  writes assets/header.svg
"""
import random

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "<": ["...#", "..#.", ".#..", "#...", ".#..", "..#.", "...#"],
    ">": ["#...", ".#..", "..#.", "...#", "..#.", ".#..", "#..."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    "-": ["...", "...", "...", "###", "...", "...", "..."],
    " ": ["..", "..", "..", "..", "..", "..", ".."],
}


def glyph(c, bold):
    g = FONT[c]
    if not bold or c == " ":
        return g
    # bold = glyph OR glyph shifted one pixel right
    return ["".join("#" if (row + ".")[i] == "#" or ("." + row)[i] == "#" else "." for i in range(len(row) + 1)) for row in g]


def text_width(s, px, bold=False):
    return sum((len(glyph(c, bold)[0]) + 1) * px for c in s) - px


def pixel_text(s, x, y, px, front, side, depth, cls="", stagger=0.0, bold=False):
    """Chunky extruded pixel letters. Each letter is its own <g> so it can drop in."""
    out = []
    for i, ch in enumerate(s):
        g = glyph(ch, bold)
        w = len(g[0])
        if ch != " ":
            back, face = [], []
            for r, row in enumerate(g):
                for c, v in enumerate(row):
                    if v == "#":
                        X, Y = x + c * px, y + r * px
                        back.append(f'<rect x="{X + depth}" y="{Y + depth}" width="{px}" height="{px}"/>')
                        face.append(f'<rect x="{X}" y="{Y}" width="{px}" height="{px}"/>')
            style = f' style="animation-delay:{0.3 + i * stagger:.2f}s"' if stagger else ""
            out.append(
                f'<g class="{cls}"{style}><g fill="{side}">{"".join(back)}</g>'
                f'<g fill="{front}" stroke="{side}" stroke-width="1" stroke-opacity=".25">{"".join(face)}</g></g>'
            )
        x += (w + 1) * px
    return "".join(out)


# ---- isometric voxels -------------------------------------------------------
A, B, C = 15, 7.5, 15  # half-width, half-height of top rhombus, block height


def iso(ox, oy, X, Y, Z):
    return ox + (X - Y) * A, oy + (X + Y) * B - Z * C


def shade(hex_, f):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def island(ox, oy):
    rnd = random.Random(7)
    vox = {}
    N = 8
    for x in range(N):
        for y in range(N):
            edge = min(x, y, N - 1 - x, N - 1 - y)
            depth = 2 + edge + rnd.randint(0, 1)  # tapers underneath
            for z in range(-depth, 0):
                vox[(x, y, z)] = "#b9784a" if z > -3 else "#8a8f98"
            if (x, y) in {(5, 5), (6, 5), (5, 6), (6, 6), (6, 4)}:
                vox[(x, y, -1)] = "#3d9be9"  # pond
            else:
                vox[(x, y, 0)] = "#5cc24a" if (x + y) % 3 else "#52b443"
    # tree
    for z in range(1, 4):
        vox[(2, 2, z)] = "#8a5a35"
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for z in (4, 5):
                vox[(2 + dx, 2 + dy, z)] = "#2f9e44" if (dx + dy + z) % 2 else "#37b24d"
    vox[(2, 2, 6)] = "#37b24d"
    # the terminal block (breakinggood lives here)
    vox[(5, 2, 1)] = "#2b2f36"
    vox[(5, 2, 2)] = "#2b2f36"
    # flowers
    vox[(1, 6, 1)] = "#ffd43b"
    vox[(6, 1, 1)] = "#ff6b9a"

    faces = []
    for (x, y, z) in sorted(vox, key=lambda v: (v[0] + v[1] + v[2], v[2])):
        col = vox[(x, y, z)]
        pts = lambda *cs: " ".join("%.1f,%.1f" % iso(ox, oy, *c) for c in cs)
        if (x, y, z + 1) not in vox:
            faces.append(f'<polygon points="{pts((x,y,z+1),(x+1,y,z+1),(x+1,y+1,z+1),(x,y+1,z+1))}" fill="{shade(col,1.08)}"/>')
        if (x, y + 1, z) not in vox:
            faces.append(f'<polygon points="{pts((x,y+1,z),(x+1,y+1,z),(x+1,y+1,z+1),(x,y+1,z+1))}" fill="{shade(col,.82)}"/>')
        if (x + 1, y, z) not in vox:
            faces.append(f'<polygon points="{pts((x+1,y,z),(x+1,y+1,z),(x+1,y+1,z+1),(x+1,y,z+1))}" fill="{shade(col,.64)}"/>')
    # glowing screen on the terminal block's front-left face
    sx, sy = iso(ox, oy, 5, 3, 2.75)
    faces.append(
        f'<g transform="translate({sx:.1f} {sy:.1f}) skewY(26.57)">'
        f'<rect x="3" y="0" width="24" height="20" fill="#0e1a12"/>'
        f'<rect x="6" y="5" width="3" height="3" fill="#69db7c"/><rect x="9" y="8" width="3" height="3" fill="#69db7c"/>'
        f'<rect x="6" y="11" width="3" height="3" fill="#69db7c"/>'
        f'<rect class="blink" x="14" y="12" width="8" height="3" fill="#69db7c"/></g>'
    )
    return "".join(faces)


def cloud(x, y, s, dur, delay):
    rects = [(0, 1, 6, 2), (1, 0, 3, 1), (4, 0.5, 1.5, 1)]
    body = "".join(f'<rect x="{x + a * s}" y="{y + b * s}" width="{w * s}" height="{h * s}"/>' for a, b, w, h in rects)
    under = f'<rect x="{x}" y="{y + 3 * s - s * .5}" width="{6 * s}" height="{s * .5}" fill="#dceaf7"/>'
    return f'<g class="drift" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g fill="#ffffff">{body}</g>{under}</g>'


def hills(W, base, colours):
    rnd = random.Random(3)
    out = []
    for layer, col in enumerate(colours):
        x, step = 0, 24
        h = base - 40 + layer * 30
        while x < W:
            h = max(base - 90 + layer * 30, min(base - 10 + layer * 25, h + rnd.choice((-12, 0, 0, 12))))
            out.append(f'<rect x="{x}" y="{h}" width="{step + 1}" height="{500 - h}" fill="{col}"/>')
            out.append(f'<rect x="{x}" y="{h}" width="{step + 1}" height="4" fill="{shade(col,1.15)}"/>')
            x += step
    return "".join(out)


def header(W=1200, H=400):
    name = "EKLAVYA PANDEY"
    px = 8
    sub = "I BUILD TOOLS THAT MAKE THINGS RUN"
    cmd = "NPX BREAKINGGOOD <URL>"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="eklavya pandey - I build tools that make things run">',
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#4ea8ff"/><stop offset="1" stop-color="#bfe4ff"/></linearGradient>'
        f'<clipPath id="r"><rect width="{W}" height="{H}" rx="10"/></clipPath></defs>',
        "<style>"
        ".drop{opacity:0;animation:drop .5s cubic-bezier(.3,1.6,.5,1) forwards}"
        "@keyframes drop{from{opacity:0;transform:translateY(-60px)}to{opacity:1;transform:none}}"
        ".drift{animation:drift linear infinite}"
        f"@keyframes drift{{from{{transform:translateX(-260px)}}to{{transform:translateX({W + 40}px)}}}}"
        ".bob{animation:bob 4s ease-in-out infinite}"
        "@keyframes bob{50%{transform:translateY(-8px)}}"
        ".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        ".fade{opacity:0;animation:fade .6s ease forwards}@keyframes fade{to{opacity:1}}"
        "</style>",
        f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#sky)"/>',
        cloud(0, 40, 14, 70, 10), cloud(0, 90, 9, 95, 60), cloud(0, 25, 11, 80, 40), cloud(0, 140, 7, 110, 85),
        hills(W, 345, ["#8fd18a", "#5cb85c", "#3f9e4a"]),
        f'<g class="bob">{island(990, 120)}</g>',
        pixel_text(name, 56, 84, px, "#fffaf0", "#3b2a20", 6, "drop", 0.06, bold=True),
        f'<g class="fade" style="animation-delay:1.3s">',
        pixel_text(sub, 58, 190, 3.4, "#ffffff", "#1d3b5c", 3, bold=True),
        # command "sign"
        f'<rect x="56" y="244" width="{text_width(cmd, 3) + 36}" height="44" fill="#2b2f36" stroke="#1a1d22" stroke-width="4"/>',
        f'<rect x="60" y="248" width="{text_width(cmd, 3) + 28}" height="4" fill="#3a3f48"/>',
        pixel_text(cmd, 74, 256, 3, "#69db7c", "#0e1a12", 0),
        f'<rect class="blink" x="{74 + text_width(cmd, 3) + 6}" y="272" width="9" height="3" fill="#69db7c"/>',
        "</g></g>",
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="none" stroke="#1d3b5c" stroke-opacity=".35" stroke-width="2"/>',
        "</svg>",
    ]
    return "".join(parts)


if __name__ == "__main__":
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    (root / "assets" / "header.svg").write_text(header(), encoding="utf-8")
    print("wrote assets/header.svg")
