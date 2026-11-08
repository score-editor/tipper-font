# Tipper

A lighter cut of Bravura for drum notation: the 92 SMuFL glyphs that Drum Score Editor and Staves
draw (plus the four tempo-note glyphs Drum Score Editor's New Score window shows), every outline
thinned and the engraving defaults the apps read set lighter.

**Scope.** Tipper is a deliberate subset. Noteheads, flags, rests, clefs, time-signature digits,
tuplet numbers, dynamics, articulations, tremolo and buzz strokes, grace notes and repeat dots are
there; the rest of the SMuFL set is not. A general notation program such as Dorico or MuseScore will
show missing glyphs if asked to use it. `build/glyphs.json` lists exactly what it holds.

**Licence.** Tipper is derived from Bravura (Copyright © 2017 Steinberg Media Technologies GmbH,
designed by Daniel Spreadbury) under the [SIL Open Font License 1.1](LICENSE), and is released under
the same licence. "Bravura" is Steinberg's Reserved Font Name and "Tipper" is ours, so a modified
copy must be called something else. [FONTLOG.txt](FONTLOG.txt) records what changed.

## Download

Take the latest `Tipper-<version>.zip` from the
[Releases](https://github.com/score-editor/tipper-font/releases) page. It holds `Tipper.otf`,
`tipper_metadata.json` (the SMuFL metadata) and `OFL.txt`. The same files are in `dist/Tipper/`.

## Installing

- **Drum Score Editor**: Settings ▸ Music Font ▸ add a font, choosing `Tipper.otf` and
  `tipper_metadata.json`; or copy the `Tipper` folder to `~/.DrumScoreEditor/fonts/Tipper/`.
  Then set the score's music font to Tipper.
- **Staves**: draws only its bundled Bravura today. Offering Tipper there is a planned follow-up.
- **Other SMuFL applications**: install `Tipper.otf` as a system font, then put
  `tipper_metadata.json` where the SMuFL specification says a font's metadata lives:
  `~/Library/Application Support/SMuFL/Fonts/Tipper/` on macOS,
  `%CommonProgramFiles%\SMuFL\Fonts\Tipper\` on Windows, `~/.local/share/SMuFL/Fonts/Tipper/` on
  Linux. Remember the scope note above.

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

On a test score rendered by Drum Score Editor at 2400 px tall: 20% fewer dark pixels and 13% less
total ink than Bravura. Before and after renders and glyph sheets are in `preview/`.

## Rebuilding

`build/build.sh <Bravura.otf> <bravura_metadata.json> <glyphnames.json>` needs FontForge
(`brew install fontforge`) and fontTools (`pip install fonttools`). Bravura and its metadata come
from [Steinberg's Bravura repository](https://github.com/steinbergmedia/bravura); `glyphnames.json`
from the [SMuFL repository](https://github.com/w3c/smufl). `build/glyphs.json` is the inventory,
made by `build/inventory.py` from the two apps' sources; `build/sheet.py` draws the before/after
glyph sheets.
