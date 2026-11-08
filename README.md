# Tipper

A lighter cut of Bravura for Drum Score Editor and Staves: the 92 SMuFL glyphs the two apps draw
(plus the four tempo-note glyphs DSE's New Score window shows), with every outline thinned and the
engraving defaults the apps read set lighter.

Derived from Bravura (Copyright © 2017 Steinberg Media Technologies GmbH) under the SIL Open Font
License 1.1, which reserves the name "Bravura" — so this is not called that, and `dist/Tipper/OFL.txt`
travels with it.

## What is lighter, and by how much

Outlines, in font units (1000 to the em, 250 to a staff space), thinned per kind of glyph with
FontForge's change-weight:

| Kind | Glyphs | Thinned by |
|---|---|---|
| solid heads and dots | black notehead, augmentation dot, repeat dots, tremolo strokes, buzz, staccato, tenuto | 12 |
| hollow heads | whole, half | 16 |
| italic dynamics | p … fff, sf, sfz | 8 (their hairlines break beyond this) |
| accents and marcatos | > ^ and their staccato forms, fermata, open arrowhead | 14 (they turn to threads beyond this) |
| digits | time signatures, tuplet numbers | 20 |
| everything stroked | flags, rests, clefs, grace note, common time | 24 |

Engraving defaults in `tipper_metadata.json` (Bravura's in brackets): beam 0.45 (0.5), stem 0.095
(0.12), staff line 0.10 (0.13), leger line 0.13 (0.16), thin barline 0.13 (0.16), thick barline
0.45 (0.5), tie and slur midpoint 0.18 (0.22), tuplet bracket 0.12 (0.16), hairpin 0.13 (0.16).
Every other SMuFL font keeps the beam at half a space, so the beam moves least; a thinner one reads
as a different style rather than a lighter one.

Glyph boxes are measured from the thinned outlines; the notehead stem anchors follow the new edges;
every other anchor is Bravura's.

## Measured

On `feature-test.ds` rendered by DSE's `create-pdf` at 2400 px tall: 20% fewer dark pixels and 13%
less total ink than Bravura (`preview/`).

## Installing

- **Drum Score Editor**: Settings ▸ Music Font ▸ add a font, choosing `dist/Tipper/Tipper.otf` and
  `tipper_metadata.json`; or copy the `dist/Tipper` folder to `~/.DrumScoreEditor/fonts/Tipper/`.
  Then set the score's music font to Tipper.
- **Staves**: draws only its bundled Bravura today (`StavesKit/MusicFace`). Offering Tipper needs the
  kit to load the font the score names — a small follow-up.

## Rebuilding

`build/build.sh <Bravura.otf> <bravura_metadata.json> <glyphnames.json>` — needs FontForge
(`brew install fontforge`) and fontTools (`pip install fonttools`). `build/glyphs.json` is the
inventory, made by `build/inventory.py` from the two cores' sources; `build/sheet.py` draws the
before/after glyph sheets.
