#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025, 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, glob, itertools, subprocess, re, ast, shutil, binascii

os.makedirs("obj", exist_ok=True)
os.makedirs("dist", exist_ok=True)
fns = []

VERSION = "1.0.2"

SCALEFACTOR = 1000 / 42.0

with open("glyph_id_to_unicode.txt", "r", encoding="utf-8") as fd:
    input_glyph_id_to_unicode = ast.literal_eval(fd.read())

ascii_space_glyph_id = {
    "futural": 699,
    "rowmans": 699,
    "greek": 699,
    "greeks": 699,
    "mathlow": 699,
    "mathupp": 699,
    "meteorology": 699,
    "markers": 699,
    "futuram": 2699,
    "rowmand": 2699,
    "timesr": 2199,
    "timesg": 2199,
    "greekc": 2199,
    "cyrillic": 2199,
    "cyrilc_1": 2199,
    "music": 2199,
    "astrology": 2199,
    "symbolic": 2199,
    "timesrb": 3199,
    "rowmant": 3199,
    "timesi": 2749,
    "cursive": 2749,
    "scripts": 2749,
    "scriptc": 2749,
    "timesib": 3249,
    "gothiceng": 3699,
    "gothgbt": 3699,
    "gothicger": 3699,
    "gothgrt": 3699,
    "gothicita": 3699,
    "gothitt": 3699,
}

def differentiate_latin_greek_cyrillic(glyph_id):
    if 1 <= glyph_id <= 26:
        return "L"
    if 27 <= glyph_id <= 50:
        return "G"
    if 501 <= glyph_id <= 526:
        return "L"
    if 527 <= glyph_id <= 550:
        return "G"
    if 551 <= glyph_id <= 576:
        return "L"
    if 601 <= glyph_id <= 626:
        return "L"
    if 627 <= glyph_id <= 650:
        return "G"
    if 651 <= glyph_id <= 678:
        return "L"
    if 684 <= glyph_id <= 687:
        return "G"
    if 1001 <= glyph_id <= 1026:
        return "L"
    if 1027 <= glyph_id <= 1050:
        return "G"
    if 1051 <= glyph_id <= 1126:
        return "L"
    if 1127 <= glyph_id <= 1150:
        return "G"
    if 1151 <= glyph_id <= 1182:
        return "L"
    if 1184 <= glyph_id <= 1187:
        return "G"
    if 1191 <= glyph_id <= 1196:
        return "L"
    if 2001 <= glyph_id <= 2026:
        return "L"
    if 2027 <= glyph_id <= 2050:
        return "G"
    if 2051 <= glyph_id <= 2076:
        return "L"
    if 2101 <= glyph_id <= 2126:
        return "L"
    if 2127 <= glyph_id <= 2150:
        return "G"
    if 2151 <= glyph_id <= 2182:
        return "L"
    if 2184 <= glyph_id <= 2187:
        return "G"
    if 2190 <= glyph_id <= 2196:
        return "L"
    if 2501 <= glyph_id <= 2676:
        return "L"
    if 2801 <= glyph_id <= 2932:
        return "C"
    if 3001 <= glyph_id <= 3176:
        return "L"
    if 3301 <= glyph_id <= 3626:
        return "L"
    if 3801 <= glyph_id <= 3926:
        return "L"
    return None

latin_greek_or_cyrillic = {
    "cyrillic": "C",
    "cyrilc_1": "C",
    "greek": "G",
    "greekc": "G",
    "greeks": "G",
    "timesg": "G"}

id_to_glyph = {}
glyph_to_id = {}
erroneous_glyph_ids = set()

for fn in [*glob.glob("complete-hershey-data/*.jhf"), *glob.glob("hershey-fonts/hershey-fonts/*.jhf")]:
    basename = os.path.splitext(os.path.basename(fn))[0]
    is_japanese = basename in ("japanese", "oriental")
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    while b:
        glyph_id, b = int(b[:5].lstrip(), 10), b[5:]
        number_pairs, b = int(b[:3].lstrip(), 10), b[3:]
        glyph_data, b = b[:(number_pairs*2)], b[(number_pairs*2):]
        if glyph_id != 12345:
            result = id_to_glyph.setdefault((is_japanese, glyph_id), glyph_data)
            if result != glyph_data:
                erroneous_glyph_ids.add((is_japanese, glyph_id))
            else:
                glyph_to_id.setdefault(glyph_data, set()).add((is_japanese, glyph_id))

fontnames = set()

for fn in [*glob.glob("hershey-fonts/hershey-fonts/*.jhf"), *glob.glob("complete-hershey-data/*.jhf")]:
    basename = os.path.splitext(os.path.basename(fn))[0]
    is_japanese = basename in ("japanese", "oriental")
    lgc = latin_greek_or_cyrillic.get(basename, "L")
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    _last_glyph_id = -1
    while b:
        glyph_id, b = int(b[:5].lstrip(), 10), b[5:]
        number_pairs, b = int(b[:3].lstrip(), 10), b[3:]
        glyph_data, b = b[:(number_pairs*2)], b[(number_pairs*2):]
        if glyph_id == 12345 or (is_japanese, glyph_id) in erroneous_glyph_ids:
            possibilities = glyph_to_id.get(glyph_data, set())
            if len(possibilities) > 1:
                if candidate := {i for i in possibilities if i[0] == is_japanese}:
                    possibilities = candidate
            if len(possibilities) > 1:
                if candidate := {i for i in possibilities if differentiate_latin_greek_cyrillic(i[1]) == lgc}:
                    possibilities = candidate
            if len(possibilities) > 1:
                if candidate := {i for i in possibilities if i[1] == (_last_glyph_id + 1)}:
                    possibilities = candidate
            if glyph_data == "JZ" and basename in ascii_space_glyph_id:
                glyph_id = ascii_space_glyph_id[basename]
            elif possibilities:
                glyph_id = min(possibilities)[1]
            else:
                glyph_id = 20000 + (binascii.crc32(glyph_data.encode("utf-8")) & 0xFFFF)
        path_data = []
        viewbox_x1 = (ord(glyph_data[0]) - 33) * SCALEFACTOR
        viewbox_x2 = (ord(glyph_data[1]) - 33) * SCALEFACTOR
        viewbox_w = viewbox_x2 - viewbox_x1
        if glyph_data[2:]:
            subpath = []
            for a, c in itertools.islice(itertools.pairwise(glyph_data[2:]), 0, None, 2):
                x = (ord(a) - 33) * SCALEFACTOR - viewbox_x1
                y = (50 - (ord(c) - 33 - 9)) * SCALEFACTOR
                if ord(a) < 33:
                    path_data.append(subpath)
                    subpath = []
                else:
                    subpath.extend((str(x), str(y)))
            path_data.append(subpath)
        elif (is_japanese, glyph_id) not in input_glyph_id_to_unicode:
            continue
        value = input_glyph_id_to_unicode[is_japanese, glyph_id]
        ucs = int(value[0].removeprefix("U+"), 16)
        fontname = value[1]
        fontnames.add(fontname)
        fn = f"obj/{fontname}_{ucs:04X}_{is_japanese:01d}{glyph_id:05d}.svg"
        fns.append(fn)
        with open(fn, "w", encoding="utf-8") as fd:
            print(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 {-30*SCALEFACTOR} {viewbox_w} {80*SCALEFACTOR}'>", file=fd)
            for subpath in path_data:
                print(f"<path d='M {' '.join(subpath)}' stroke='black' fill='none' stroke-width='{2*SCALEFACTOR}' stroke-linejoin='round' stroke-linecap='round'/>", file=fd)
            print("</svg>", file=fd)
        _last_glyph_id = glyph_id

subprocess.call(["inkscape", "--actions", "select-all;object-stroke-to-path;path-union", "-l", "--export-overwrite", *fns])

for fontname in fontnames:
    if "Mini" in fontname or "Giant" in fontname:
        continue
    familyname, variant = fontname.rsplit("-", 1)
    for ucs in range(0x20, 0x7F):
        if not glob.glob(f"obj/{fontname}_{ucs:04X}_*.svg"):
            if "Gothic" in fontname and (
                    others := glob.glob(f"obj/GothicEnglish-{variant}_{ucs:04X}_*.svg")):
                other = min(others)
                shutil.copy(other, f"obj/{fontname}_{os.path.basename(other).split('_', 1)[1]}")
            elif others := glob.glob(f"obj/Serif-{variant}_{ucs:04X}_*.svg"):
                other = min(others)
                shutil.copy(other, f"obj/{fontname}_{os.path.basename(other).split('_', 1)[1]}")
            elif others := glob.glob(f"obj/Sans-{variant}_{ucs:04X}_*.svg"):
                other = min(others)
                shutil.copy(other, f"obj/{fontname}_{os.path.basename(other).split('_', 1)[1]}")

with open("hershey-fonts/hershey-fonts.notes", "r", encoding="utf-8") as fd:
    b = fd.read()

copying_notice = f"""\
Generated with `hershey_jhf_to_truetype.py` from JHF (James Hurt Format) sources:

Glyph-ID-mapped font data: https://media.unpythonic.net/emergent-files/software/hershey/tex-hershey.zip
ASCII-mapped font data: https://media.unpythonic.net/emergent-files/software/hershey/hershey.zip
Python sources: https://github.com/harjitmoe/hershey-jhf-to-truetype/blob/main/hershey_jhf_to_truetype.py
Unicode mappings: https://github.com/harjitmoe/hershey-jhf-to-truetype/blob/main/glyph_id_to_unicode.txt

---

Terms for the JHF-format Hershey font data:

{b.split("-" * 78, 2)[1].strip().replace(chr(0x09), '  ')}
"""
camel_case_break = re.compile(r"([a-z])([A-Z])")

ucs_to_glyph_name = {}
with open("agl-aglfn/aglfn.txt", "r", encoding="utf-8") as fd:
    for line in fd:
        if not line.startswith("#"):
            ucs, glyph_name = line.split(";", 2)[:2]
            ucs_to_glyph_name[ucs] = glyph_name

truetype_filenames = []
for fontname in fontnames:
    familyname, variant = fontname.rsplit("-", 1)
    familyname = camel_case_break.sub(lambda m: f"{m.group(1)} {m.group(2)}", familyname)
    style = "italic" if variant in ("Italic", "BoldItalic") else "regular"
    weight = {
        "Regular": 400,
        "Italic": 400,
        "Bold": 700,
        "BoldItalic": 700,
    }[variant]
    friendlyvariant = camel_case_break.sub(lambda m: f"{m.group(1)} {m.group(2)}", variant)
    friendlyname = "Hershey " + familyname + (f" {friendlyvariant}" if variant != "Regular" else "")
    glyphs = {}
    for fn in sorted(glob.glob(f"obj/{fontname}_*.svg")):
        with open(fn, "r", encoding="utf-8") as fd:
            b = fd.read()
        x, y, w, h = b.split("viewBox=\"", 1)[1].split("\"", 1)[0].split()
        _, ucs, glyph_id = os.path.splitext(fn)[0].split("_", 2)
        glyph_name = ucs_to_glyph_name.get(ucs, (f"uni{ucs}" if len(ucs) == 4 else f"u{ucs}")
                ) + "." + ("occident" if glyph_id[0] == "0" else "japanese") + "." + glyph_id[1:]
        data = b.split("<path", 1)[1].split(" d=\"", 1)[1].split("\"", 1)[0] if "<path" in b else ""
        glyph = f"<glyph glyph-name='{glyph_name}' unicode='&#x{ucs};' horiz-adv-x='{w}' d='{data}'/>"
        if glyphs.get(ucs, glyph) != glyph:
            print(fn)
        glyphs[ucs] = glyph
    with open(f"obj/{fontname}.svg", "w", encoding="utf-8") as fd:
        print(f"<svg xmlns=\"http://www.w3.org/2000/svg\"><defs><font id=\"Hershey{fontname}\"><font-face units-per-em=\"{round(42*SCALEFACTOR)}\" descent=\"{round(-11*SCALEFACTOR)}\" cap-height=\"{round(24*SCALEFACTOR)}\" x-height=\"{round(11*SCALEFACTOR)}\" font-family=\"Hershey {familyname}\" font-weight=\"{weight}\" font-style=\"{style}\"/>", file=fd)
        for ucs, glyph in sorted(glyphs.items()):
            print(glyph, file=fd)
        print("</font></defs></svg>", file=fd)
    print()
    print(fontname)
    fn = f"obj/Hershey{fontname}.ttf"
    truetype_filenames.append(fn)
    # Note that `UseTypoMetrics` seemingly cannot be set from FontForge's native script language
    subprocess.call(["fontforge", "-quiet", "-lang=py", "-c", """
f = open(argv[1])
f.fullname = argv[3]
f.copyright = argv[4]
f.version = argv[6]
f.appendSFNTName(0x409, 2, argv[5])
f.os2_use_typo_metrics = True
f.layers['Fore'].is_quadratic = True
f.selection.all()
f.addExtrema()
f.correctDirection()
f.canonicalStart()
f.canonicalContours()
f.autoHint()
f.autoInstr()
f.generate(argv[2])
""", f"obj/{fontname}.svg", fn, friendlyname, copying_notice, friendlyvariant, VERSION])

subprocess.call(["fontforge", "-quiet", "-lang=py", "-c", """
all_fonts = [open(i) for i in argv[2:]]
all_fonts[0].generateTtc(argv[1], all_fonts[1:], ttcflags=('merge',), layer='Fore')
""", "dist/Hershey.ttc", *sorted(truetype_filenames)])
