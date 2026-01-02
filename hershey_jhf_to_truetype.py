#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025, 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, glob, itertools, subprocess, re, pprint, ast, shutil, binascii
sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, "ecma35lib")))
from ecma35.data.graphdata import gsets

os.makedirs("obj", exist_ok=True)
os.makedirs("obj/glyph_id", exist_ok=True)
os.makedirs("dist", exist_ok=True)
fns = []

SCALEFACTOR = 1000 / 42.0

with open("glyph_id_to_unicode.txt", "r", encoding="utf-8") as fd:
    input_glyph_id_to_unicode = ast.literal_eval(fd.read())

names = {
    "futural": ("Sans-Regular", "ir006/smartquotes"),
    "rowmans": ("Sans-Regular", "ir006/smart-quotes-up-arrow"),
    "greek": ("Sans-Regular", "hershey-greek/smartquotes"),
    "greeks": ("Sans-Regular", "hershey-greek-alternate"),
    "mathlow": ("Sans-Regular", "hershey-mathematical/lowercase"),
    "mathupp": ("Sans-Regular", "hershey-mathematical/uppercase"),
    "meteorology": ("Sans-Regular", "hershey-meteorological"),
    "markers": ("Sans-Regular", "hershey-list-markers"),
    "futuram": ("Sans-Bold", "ir006/angle-brackets-for-braces"),
    "rowmand": ("Sans-Bold", "ir006/smart-quotes-up-arrow"),
    "timesr": ("Serif-Regular", "ir006"),
    "timesg": ("Serif-Regular", "hershey-greek"),
    "greekc": ("Serif-Regular", "hershey-greek-alternate/disunified-semicolon"),
    "cyrillic": ("Serif-Regular", "hershey-cyrillic"),
    "cyrilc_1": ("Serif-Regular", "hershey-cyrillic-alternate"),
    "music": ("Serif-Regular", "hershey-musical"),
    "astrology": ("Serif-Regular", "hershey-astrological"),
    "symbolic": ("Serif-Regular", "hershey-symbolic"),
    "timesrb": ("Serif-Bold", "ir006"),
    "rowmant": ("Serif-Bold", "ir006/smart-quotes-up-arrow"),
    "timesi": ("Serif-Italic", "ir006"),
    "timesib": ("Serif-BoldItalic", "ir006"),
    "gothiceng": ("GothicEnglish-Regular", "ir006"),
    "gothgbt": ("GothicEnglish-Regular", "ir006/smart-quotes-up-arrow"),
    "gothicger": ("GothicGerman-Regular", "ir006"),
    "gothgrt": ("GothicGerman-Regular", "ir006/smart-quotes-up-arrow"),
    "gothicita": ("GothicItalian-Regular", "ir006"),
    "gothitt": ("GothicItalian-Regular", "ir006/smart-quotes-up-arrow"),
    "cursive": ("Cursive-Regular", "ir006/smartquotes-hybrid"),
    "scripts": ("Cursive-Regular", "ir006/smart-quotes-up-arrow"),
    "scriptc": ("CursiveComplex-Regular", "ir006/smart-quotes-up-arrow"),
}

adjustments = {}

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

glyph_id_to_unicode_and_fontname = {}

for fn in [*glob.glob("hershey-fonts/hershey-fonts/*.jhf"), *glob.glob("complete-hershey-data/*.jhf")]:
    basename = os.path.splitext(os.path.basename(fn))[0]
    is_japanese = basename in ("japanese", "oriental")
    lgc = latin_greek_or_cyrillic.get(basename, "L")
    _fontname, charset = names.get(basename, (basename.title() + "-Regular", None))
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    offset = 0
    _last_glyph_id = -1
    while b:
        fontname = _fontname
        glyph_id, b = int(b[:5].lstrip(), 10), b[5:]
        number_pairs, b = int(b[:3].lstrip(), 10), b[3:]
        glyph_data, b = b[:(number_pairs*2)], b[(number_pairs*2):]
        if (glyph_id == 12345 or (is_japanese, glyph_id) in erroneous_glyph_ids):
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
            if offset == 0 and glyph_data == "JZ":
                glyph_id = 3199
            elif possibilities:
                glyph_id = min(possibilities)[1]
            else:
                glyph_id = 12345
        effective_glyph_id = glyph_id if glyph_id != 12345 else (
                20000 + (binascii.crc32(glyph_data.encode("utf-8")) & 0xFFFF))
        path_data = ["M"]
        additional_scale, additional_margin, additional_elevation = adjustments.get(glyph_id, (1, 0, 0))
        def apply_scale(n, margin_factor, elevation_factor):
            return ((n * additional_scale) + (additional_margin * margin_factor) +
                    (additional_elevation * elevation_factor)) * SCALEFACTOR
        viewbox_x1 = apply_scale(ord(glyph_data[0]) - 33, 0, 0)
        viewbox_x2 = apply_scale(ord(glyph_data[1]) - 33, 2, 0)
        viewbox_w = viewbox_x2 - viewbox_x1
        for a, c in itertools.islice(itertools.pairwise(glyph_data[2:]), 0, None, 2):
            x = apply_scale(ord(a) - 33, 1, 0) - viewbox_x1
            y = apply_scale(50 - (ord(c) - 33 - 9), 0, 1)
            if ord(a) < 33:
                path_data.append("M")
            else:
                path_data.extend((str(x), str(y)))
        if value := input_glyph_id_to_unicode.get((is_japanese, effective_glyph_id), None):
            ucs = int(value[0].removeprefix("U+"), 16)
            fontnames.add(value[1])
            if ucs > 0x0020:
                fontname = value[1]
        elif charset is None:
            ucs = 0xF000 + offset
        elif gsets[charset][0] > 94:
            ucs = (gsets[charset][2][offset] or (0xF000 + offset,))[0]
        elif offset > 94:
            ucs = 0xF020 + offset
        elif offset == 0:
            ucs = 0x0020
        elif gsets[charset][2][offset - 1] is None:
            ucs = 0xF020 + offset
        elif gsets[charset][2][offset - 1][-1] in (0xF879, 0xF87F):
            ucs = 0xF020 + offset
        else:
            ucs = gsets[charset][2][offset - 1][0]
        fontnames.add(fontname)
        if not (0xF000 <= ucs <= 0xF8FF):
            glyph_id_to_unicode_and_fontname.setdefault((is_japanese, effective_glyph_id), set()
                    ).add((f"U+{ucs:04X}", fontname))
        if offset == 0 or path_data != ["M"]:
            glyph_id_to_unicode_and_fontname.setdefault((is_japanese, effective_glyph_id), set())
            filenames = [f"obj/glyph_id/{is_japanese:01d}{effective_glyph_id:05d}.svg"]
            fn = f"obj/{fontname}_{ucs:04X}_{is_japanese:01d}{effective_glyph_id:05d}.svg"
            filenames.append(fn)
            fns.append(fn)
            for fn in filenames:
                with open(fn, "w", encoding="utf-8") as fd:
                    print(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 {-30*SCALEFACTOR} {viewbox_w} {80*SCALEFACTOR}'>", file=fd)
                    if path_data != ["M"]:
                        path_string = " ".join(path_data)
                        for i in path_string.split(" M "):
                            print(f"<path d='M {i.removeprefix('M').lstrip()}' stroke='black' fill='none' stroke-width='{2*SCALEFACTOR}' stroke-linejoin='round' stroke-linecap='round'/>", file=fd)
                    print("</svg>", file=fd)
        offset += 1
        _last_glyph_id = glyph_id

for i, j in [*glyph_id_to_unicode_and_fontname.items()]:
    if (not j) and i in id_to_glyph:
        reverse = glyph_to_id[id_to_glyph[i]]
        for k in reverse:
            if glyph_id_to_unicode_and_fontname[k] is not j:
                j.update(glyph_id_to_unicode_and_fontname[k])

with open("dist/glyph_id_to_unicode.txt", "w", encoding="utf-8") as fd:
    fd.write(pprint.pformat(glyph_id_to_unicode_and_fontname))

subprocess.call(["inkscape", "--actions", "select-all;object-stroke-to-path;path-union", "-l", "--export-overwrite", *fns])

with open("hershey-fonts/hershey-fonts.notes", "r", encoding="utf-8") as fd:
    b = fd.read()

copying_notice = b.split("-" * 78, 2)[1].strip()

camel_case_break = re.compile(r"([a-z])([A-Z])")
fonts = {i for i, j in names.values()}

no_output = set()
for fontname in fontnames:
    if "Mini" in fontname or "Giant" in fontname:
        continue
    if not glob.glob(f"obj/{fontname}_*.svg"):
        no_output.add(fontname)
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

truetype_filenames = []
for fontname in fontnames:
    if fontname in no_output:
        continue
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
        ucs = fn.split("_", 2)[1]
        data = b.split("<path", 1)[1].split(" d=\"", 1)[1].split("\"", 1)[0] if "<path" in b else ""
        glyph = f"<glyph unicode='&#x{ucs};' horiz-adv-x='{w}' d='{data}'/>"
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
""", f"obj/{fontname}.svg", fn, friendlyname, copying_notice, friendlyvariant, repr(SCALEFACTOR)])

subprocess.call(["fontforge", "-quiet", "-lang=py", "-c", """
all_fonts = [open(i) for i in argv[2:]]
all_fonts[0].generateTtc(argv[1], all_fonts[1:], ttcflags=('merge',), layer='Fore')
""", "dist/Hershey.ttc", *sorted(truetype_filenames)])
