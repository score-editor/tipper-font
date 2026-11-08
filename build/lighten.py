# Run with: fontforge -lang=py -script lighten.py <bravura.otf> <glyphs.json> <out dir> <name> <weight-delta> [extra codepoints...]
import fontforge, json, sys, os
src, glyphs_json, out, name, delta = sys.argv[1:6]
extra = [int(x, 16) for x in sys.argv[6:]]
want = {int(g["codepoint"][2:], 16) for g in json.load(open(glyphs_json))} | set(extra)
f = fontforge.open(src)
keep = set()
for g in f.glyphs():
    if g.unicode in want or g.glyphname in (".notdef", "space"):
        keep.add(g.glyphname)
missing = sorted(hex(cp) for cp in want if not any(g.unicode == cp for g in f.glyphs()))
print("keeping", len(keep), "glyphs; missing from Bravura:", missing)
# Drop everything else: the font is the two apps' subset and no more.
f.selection.none()
for n in keep:
    f.selection.select(("more",), n)
f.selection.invert()
f.clear()
# Thin every kept outline, by how the glyph is built: a solid head loses little (it would only
# shrink), a hollow head a little more, and every stroked glyph — flags, rests, clefs, digits,
# dynamics, marks — the most, since its strokes are what read as heavy. Font units: 1000 to the em,
# 250 to the staff space.
solid, hollow, dynamics, marks, digits, stroked = [float(x) for x in delta.split(",")]
SOLID = {0xE0A4, 0xE1E7, 0xE043, 0xE210, 0xE220, 0xE221, 0xE222, 0xE22A, 0xE4A2, 0xE4A4, 0xECB7}
HOLLOW = {0xE0A2, 0xE0A3}
# The italic dynamics are hairline letters already: thinned as far as the rest they break.
DYNAMICS = set(range(0xE520, 0xE53F))
# Accents and marcatos are two strokes meeting at a point; thinned as far as a flag they are threads.
MARKS = {0xE4A0, 0xE4A6, 0xE4AC, 0xE4AD, 0xE4AE, 0xE4B0, 0xE4B2, 0xE4C0, 0xEB8C}
DIGITS = set(range(0xE080, 0xE08E)) | set(range(0xE880, 0xE88A))
def group(cp):
    return (solid if cp in SOLID else hollow if cp in HOLLOW else dynamics if cp in DYNAMICS
            else marks if cp in MARKS else digits if cp in DIGITS else stroked)
groups = {}
for n in keep:
    if n in (".notdef", "space"):
        continue
    groups.setdefault(group(f[n].unicode), []).append(n)
for amount, names in groups.items():
    if not names or amount == 0:
        continue
    f.selection.none()
    for n in names:
        f.selection.select(("more",), n)
    f.changeWeight(amount, "auto", 0, 0, "auto")
    print("thinned", len(names), "glyphs by", amount)
# Identity: a derivative of Bravura under the OFL, which reserves the name "Bravura".
f.familyname = name
f.fontname = name
f.fullname = name
f.weight = "Light"
f.version = "0.1"
f.sfntRevision = 0.1          # the head table's revision agrees with the name table's
f.os2_vendor = "DSCR"         # DrumScore, not Bravura's SMTG
f.copyright = ("Derived from Bravura, Copyright (c) 2017 Steinberg Media Technologies GmbH, "
               "under the SIL Open Font License 1.1. Outlines thinned and the font subset for "
               "Drum Score Editor and Staves, 2026. 'Bravura' is a Reserved Font Name and this is not it.")
f.sfnt_names = tuple(n for n in f.sfnt_names if n[1] not in ("Family", "Fullname", "PostScriptName",
    "SubFamily", "Preferred Family", "Preferred Styles", "UniqueID", "Version", "Copyright", "Trademark",
    "Designer", "Descriptor", "Vendor URL", "Designer URL", "License", "License URL", "Manufacturer",
    "Compatible Full"))
f.appendSFNTName("English (US)", "License", "This Font Software is licensed under the SIL Open Font License, Version 1.1.")
f.appendSFNTName("English (US)", "License URL", "https://openfontlicense.org")
f.appendSFNTName("English (US)", "Descriptor", "A lighter cut of Bravura's drum notation subset for Drum Score Editor and Staves.")
f.appendSFNTName("English (US)", "Designer", "Alan White (lightening and subset); Daniel Spreadbury, Steinberg (Bravura)")
f.appendSFNTName("English (US)", "Manufacturer", "DrumScore")
f.appendSFNTName("English (US)", "Vendor URL", "https://drumscore.scot")
f.appendSFNTName("English (US)", "UniqueID", name + " 0.1; DrumScore; 2026")
os.makedirs(os.path.join(out, name), exist_ok=True)
path = os.path.join(out, name, name + ".otf")
f.generate(path, flags=("opentype",))
print("wrote", path)
