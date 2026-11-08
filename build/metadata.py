# venv python metadata.py <font.otf> <bravura_metadata.json> <glyphnames.json> <name> <out json> <lighten factor>
import json, sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
font_path, bravura_json, names_json, name, out = sys.argv[1:6]
font = TTFont(font_path)
names = json.load(open(names_json))
by_cp = {int(v["codepoint"][2:], 16): n for n, v in names.items()}
bravura = json.load(open(bravura_json))
SP = font["head"].unitsPerEm / 4.0  # one staff space
cmap = font.getBestCmap()
glyphset = font.getGlyphSet()
boxes = {}
for cp, gname in sorted(cmap.items()):
    smufl = by_cp.get(cp)
    if not smufl:
        continue
    pen = BoundsPen(glyphset)
    glyphset[gname].draw(pen)
    if pen.bounds is None:
        continue
    x0, y0, x1, y1 = pen.bounds
    boxes[smufl] = {"bBoxNE": [round(x1 / SP, 4), round(y1 / SP, 4)], "bBoxSW": [round(x0 / SP, 4), round(y0 / SP, 4)]}
# Anchors: Bravura's, for the glyphs kept; a stem anchor follows the notehead's new edge.
anchors = {}
for smufl, a in bravura["glyphsWithAnchors"].items():
    if smufl not in boxes:
        continue
    kept = dict(a)
    box = boxes[smufl]
    for key in ("stemUpSE", "stemDownNW", "stemUpNW", "stemDownSW"):
        if key in kept:
            x, y = kept[key]
            kept[key] = [box["bBoxNE"][0] if key.endswith("SE") or key.endswith("NE") else box["bBoxSW"][0], y]
    anchors[smufl] = kept
# Engraving defaults: the strokes the apps draw themselves, set lighter one by one — stems, staff
# and leger lines, barlines, ties and brackets most; beams least, since every SMuFL font keeps a
# beam at half a space and a thinner one reads as a different style rather than a lighter one.
defaults = dict(bravura["engravingDefaults"])
defaults.update({
    "beamThickness": 0.45, "stemThickness": 0.095, "staffLineThickness": 0.1,
    "legerLineThickness": 0.13, "thinBarlineThickness": 0.13, "thickBarlineThickness": 0.45,
    "hairpinThickness": 0.13, "tupletBracketThickness": 0.12, "bracketThickness": 0.45,
    "subBracketThickness": 0.13, "slurMidpointThickness": 0.18, "tieMidpointThickness": 0.18,
    "slurEndpointThickness": 0.08, "tieEndpointThickness": 0.08, "repeatEndingLineThickness": 0.13,
    "dashedBarlineThickness": 0.13, "octaveLineThickness": 0.13, "arrowShaftThickness": 0.13,
    "textEnclosureThickness": 0.13, "lyricLineThickness": 0.13, "pedalLineThickness": 0.13,
})
meta = {
    "fontName": name, "fontVersion": 0.1,
    "engravingDefaults": defaults,
    "glyphBBoxes": boxes,
    "glyphsWithAnchors": anchors,
}
json.dump(meta, open(out, "w"), indent=2)
print("glyph boxes", len(boxes), "anchors", len(anchors))
for g in ("noteheadBlack", "flag8thUp", "restQuarter", "dynamicForte", "gClef"):
    b = bravura["glyphBBoxes"].get(g); n = boxes.get(g)
    print(f"  {g:14s} Bravura {b['bBoxSW']}..{b['bBoxNE']}  ->  {n['bBoxSW']}..{n['bBoxNE']}")
print("  stemUpSE noteheadBlack:", bravura["glyphsWithAnchors"]["noteheadBlack"]["stemUpSE"], "->", anchors["noteheadBlack"]["stemUpSE"])
