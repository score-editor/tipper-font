# venv python sheet.py <out.svg> <half: 0 heads/flags/rests, 1 dynamics/marks> <label:font.otf> [<label:font.otf> ...]
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
out = sys.argv[1]
half = int(sys.argv[2])
fonts = [(a.split(":", 1)[0], TTFont(a.split(":", 1)[1])) for a in sys.argv[3:]]
show = [0xE0A4, 0xE0A3, 0xE0A2, 0xE0A9, 0xE1E7, 0xE240, 0xE241, 0xE242, 0xE244, 0xE4E5, 0xE4E6, 0xE4E7, 0xE4E8,
        0xE069, 0xE050, 0xE084, 0xE08A, 0xE520, 0xE522, 0xE52F, 0xE536, 0xE4A0, 0xE4A2, 0xE4AC, 0xE4C0,
        0xE220, 0xE222, 0xE22A, 0xE560, 0xE883, 0xE043, 0xE1D7]
show = show[half * 16:(half + 1) * 16]
SP = 48  # pixels per staff space
cell_w, cell_h = 3.2 * SP, 7.5 * SP
cols = 8
rows = (len(show) + cols - 1) // cols
W = cols * cell_w; H = rows * cell_h * len(fonts)
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}"><rect width="100%" height="100%" fill="white"/>']
for fi, (label, font) in enumerate(fonts):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upem = font["head"].unitsPerEm; k = SP * 4 / upem
    for i, cp in enumerate(show):
        gname = cmap.get(cp)
        r, c = divmod(i, cols)
        x0 = c * cell_w + 0.6 * SP; y0 = (r * len(fonts) + fi) * cell_h + 4.5 * SP
        parts.append(f'<line x1="{c*cell_w:.0f}" y1="{y0:.1f}" x2="{(c+1)*cell_w:.0f}" y2="{y0:.1f}" stroke="#bbb" stroke-width="1"/>')
        parts.append(f'<text x="{c*cell_w+4:.0f}" y="{(r*len(fonts)+fi)*cell_h+14:.0f}" font-family="Helvetica" font-size="11" fill="#888">{label} {cp:04X}</text>')
        if not gname:
            continue
        pen = SVGPathPen(gs)
        gs[gname].draw(TransformPen(pen, (k, 0, 0, -k, x0, y0)))
        parts.append(f'<path d="{pen.getCommands()}" fill="black"/>')
parts.append("</svg>")
open(out, "w").write("".join(parts))
print("wrote", out, f"{W:.0f}x{H:.0f}")
