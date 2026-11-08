#!/bin/zsh
# Rebuild Tipper from Bravura. Needs: fontforge (brew install fontforge) and a venv with fonttools.
#   build/build.sh <Bravura.otf> <bravura_metadata.json> <glyphnames.json>
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
BRAVURA=${1:?Bravura.otf}; META=${2:?bravura_metadata.json}; NAMES=${3:?glyphnames.json}
OUT="$HERE/../dist"
# Thinning, in font units (1000 to the em, 250 to a staff space), by how a glyph is built:
#   solid heads and dots, hollow heads, italic dynamics, accents and marcatos, digits, everything stroked.
fontforge -lang=py -script "$HERE/lighten.py" "$BRAVURA" "$HERE/glyphs.json" "$OUT" Tipper "-12,-16,-8,-14,-20,-24" ECA3 ECA5 ECA7 ECB7
python3 "$HERE/metadata.py" "$OUT/Tipper/Tipper.otf" "$META" "$NAMES" Tipper "$OUT/Tipper/tipper_metadata.json"
