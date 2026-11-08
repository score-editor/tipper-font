import json, re, sys, pathlib
S = pathlib.Path(sys.argv[1])
names = json.load(open(S / "downloads/glyphnames.json"))
by_name = {n: int(v["codepoint"][2:], 16) for n, v in names.items()}
by_cp = {cp: n for n, cp in by_name.items()}
wanted = {}
def add(cp, why):
    wanted.setdefault(cp, set()).add(why)
for f, why in [("java-glyphs.txt", "java name"), ("swift-glyphs.txt", "swift name")]:
    for line in open(S / f):
        n = line.strip()
        if n in by_name:
            add(by_name[n], why)
for line in open(S / "java-codepoints.txt"):
    add(int(line.strip(), 16), "java codepoint")
# Swift and StavesKit codepoints, written \u{E...}
for root in ["/Users/alanwhite/git/drumscore-core-swift/Sources", "/Users/alanwhite/git/staves-apple/StavesKit/Sources", "/Users/alanwhite/git/staves-apple/Staves"]:
    for p in pathlib.Path(root).rglob("*.swift"):
        for m in re.findall(r"\\u\{(E[0-9A-Fa-f]{3})\}|0x(E[0-9A-F]{3})", p.read_text()):
            cp = m[0] or m[1]
            add(int(cp, 16), "swift codepoint")
# the Java engravers also name glyphs through the metadata's required list
for n in ["repeatDots", "tremolo1", "tremolo2", "tremolo3", "buzzRoll", "arrowheadOpenDown"]:
    add(by_name[n], "metadata")
unknown = [hex(cp) for cp in wanted if cp not in by_cp]
out = sorted((cp, by_cp.get(cp, "?"), sorted(w)) for cp, w in wanted.items())
json.dump([{"codepoint": f"U+{cp:04X}", "name": n, "from": w} for cp, n, w in out], open(S / "glyphs.json", "w"), indent=1)
print("glyphs wanted:", len(out), "| not in SMuFL:", unknown)
ranges = {}
for cp, n, w in out:
    ranges.setdefault(n.rstrip("0123456789").rstrip("UpDownAboveBelowLeftRight") , 0)
print(", ".join(f"{n} {cp:04X}" for cp, n, w in out))
