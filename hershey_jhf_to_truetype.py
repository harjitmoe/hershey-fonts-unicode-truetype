#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, glob, itertools, subprocess, re
sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, "ecma35lib")))
from ecma35.data.graphdata import gsets

os.makedirs("obj", exist_ok=True)
os.makedirs("dist", exist_ok=True)
fns = []

SCALEFACTOR = 1000 / 42.0

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
    "japanese": ("Serif-Regular", "hershey-japanese"),
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

gsets["hershey-japanese"] = (192, 1, (
                          (0xFF0E,), (0xFF0C,), (0x30FC,),
    (0x65E5,), (0x5186,), (0x5E74,), (0x5927,), (0x56FD,),
    (0x4EBA,), (0x6771,), (0x4E2D,), (0x672C,), (0x4EAC,),
    (0x51FA,), (0x6642,), (0x4E0A,), (0x8005,), (0x5341,),
    (0x4E00,), (0x4E8C,), (0x4E09,), (0x56DB,), (0x4E94,),
    (0x516D,), (0x4E03,), (0x5165,), (0x4E5D,), (0xFF0E,),
    (0xFF0E,), (0xFF0E,), (0xFF0E,), (0xFF0E,), (0xFF0E,),
    (0x3042,), (0x3044,), (0x3046,), (0x3048,), (0x304A,),
    (0x304B,), (0x304D,), (0x304F,), (0x3051,), (0x3053,),
    (0x3055,), (0x3057,), (0x3059,), (0x305B,), (0x305D,),
    (0x305F,), (0x3061,), (0x3064,), (0x3066,), (0x3068,),
    (0x306A,), (0x306B,), (0x306C,), (0x306D,), (0x306E,),
    (0x306F,), (0x3072,), (0x3075,), (0x3078,), (0x307B,),
    (0x307E,), (0x307F,), (0x3080,), (0x3081,), (0x3082,),
    (0x3084,), (0x3044,), (0x3086,), (0x3048,), (0x3088,),
    (0x3089,), (0x308A,), (0x308B,), (0x308C,), (0x308D,),
    (0x308F,), (0x3090,), (0x3046,), (0x3091,), (0x3092,),
    (0x3093,), (0xFF0E,), (0xFF0E,), (0xFF0E,), (0xFF0E,),
    (0x304C,), (0x304E,), (0x3050,), (0x3052,), (0x3054,),
    (0x3056,), (0x3058,), (0x305A,), (0x305C,), (0x305E,),
    (0x3060,), (0x3062,), (0x3065,), (0x3067,), (0x3069,),
    (0x3070,), (0x3073,), (0x3076,), (0x3079,), (0x307C,),
    (0x3071,), (0x3074,), (0x3077,), (0x307A,), (0x307D,),
    (0x30A2,), (0x30A4,), (0x30A6,), (0x30A8,), (0x30AA,),
    (0x30AB,), (0x30AD,), (0x30AF,), (0x30B1,), (0x30B3,),
    (0x30B5,), (0x30B7,), (0x30B9,), (0x30BB,), (0x30BD,),
    (0x30BF,), (0x30C1,), (0x30C4,), (0x30C6,), (0x30C8,),
    (0x30CA,), (0x30CB,), (0x30CC,), (0x30CD,), (0x30CE,),
    (0x30CF,), (0x30D2,), (0x30D5,), (0x30D8,), (0x30DB,),
    (0x30DE,), (0x30DF,), (0x30E0,), (0x30E1,), (0x30E2,),
    (0x30E4,), (0x30A4,), (0x30E6,), (0x30A8,), (0x30E8,),
    (0x30E9,), (0x30EA,), (0x30EB,), (0x30EC,), (0x30ED,),
    (0x30EF,), (0x30F0,), (0x30A6,), (0x30F1,), (0x30F2,),
    (0x30F3,), (0xFF0E,), (0xFF0E,), (0xFF0E,), (0xFF0E,),
    (0x30AC,), (0x30AE,), (0x30B0,), (0x30B2,), (0x30B4,),
    (0x30B6,), (0x30B8,), (0x30BA,), (0x30BC,), (0x30BE,),
    (0x30C0,), (0x30C2,), (0x30C5,), (0x30C7,), (0x30C9,),
    (0x30D0,), (0x30D3,), (0x30D6,), (0x30D9,), (0x30DC,),
    (0x30D1,), (0x30D4,), (0x30D7,), (0x30DA,), (0x30DD,)))

overrides = {
    "astrology": {0x7F: 0x007E},
    "cursive": {0x2A: 0x2217, 0x2F: 0x2215, 0x60: 0x02BB, 0x7F: 0x2588},
    "cyrilc_1": {0x23: 0xFE5F, 0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "cyrillic": {0x22: 0x2033, 0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x45: 0x0418, 0x7F: 0x007E},
    "gothgbt": {0x23: 0xFE5F, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "gothgrt": {0x23: 0xFE5F, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "gothitt": {0x23: 0xFE5F, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "gothiceng": {0x7F: 0x2588},
    "gothicger": {0x7F: 0x2588},
    "gothicita": {0x7F: 0x2588},
    "futural": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x60: 0x02BB, 0x7F: 0x2588},
    "futuram": {0x7F: 0x2588},
    "greek": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x60: 0x02BB, 0x7F: 0x2588},
    "greekc": {0x23: 0xFE5F, 0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "greeks": {0x23: 0xFE5F, 0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "markers": {0x49: 0xF049, 0x69: 0xF069},
    "mathlow": {0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x7F: 0x007E},
    "mathupp": {0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x2C: 0x201A, 0x2E: 0x2024, 0x7B: 0x005D, 0x7D: 0x007B, 0x7F: 0x007E},
    "meteorology": {0x24: 0x25B4, 0x2A: 0x2217, 0x3F: 0x2753, 0x5F: 0xF05F, 0x7F: 0x007E},
    "music": {0x7F: 0x2588},
    "rowmand": {0x23: 0xFE5F, 0x26: 0x1F674, 0x28: 0x2768, 0x29: 0x2769, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "rowmans": {0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "rowmant": {0x23: 0xFE5F, 0x28: 0x2768, 0x29: 0x2769, 0x2D: 0x2212, 0x4A: 0xF04A, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "scriptc": {0x7F: 0x00B0},
    "scripts": {0x21: 0x2757, 0x22: 0x201D, 0x24: 0x1F4B2, 0x26: 0x1F675, 0x28: 0x2768, 0x29: 0x2769, 0x2C: 0x201A, 0x2E: 0x2024, 0x30: 0x1D7CE, 0x31: 0x1D7CF, 0x32: 0x1D7D0, 0x33: 0x1D7D1, 0x34: 0x1D7D2, 0x35: 0x1D7D3, 0x36: 0x1D7D4, 0x37: 0x1D7D5, 0x38: 0x1D7D6, 0x39: 0x1D7D7, 0x3A: 0xF03A, 0x3B: 0xF03B, 0x3F: 0x2753, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "symbolic": {0x4F: 0xF04F, 0x7F: 0x007E},
    "timesg": {0x22: 0x2033, 0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x7F: 0x2588},
    "timesi": {0x7F: 0x2588},
    "timesib": {0x7F: 0x2588},
    "timesb": {0x7F: 0x2588},
    "timesr": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x7F: 0x2588},
}

fontnames = set()

for fn in glob.glob("hershey-fonts/hershey-fonts/*.jhf"):
    basename = os.path.splitext(os.path.basename(fn))[0]
    fontname, charset = names.get(basename, (basename.title() + "-Regular", None))
    fontnames.add(fontname)
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    offset = 0
    while b:
        glyph_id, b = int(b[:5].lstrip(), 10), b[5:]
        number_pairs, b = int(b[:3].lstrip(), 10), b[3:]
        glyph_data, b = b[:(number_pairs*2)], b[(number_pairs*2):]
        path_data = ["M"]
        viewbox_x1 = (ord(glyph_data[0]) - 33) * SCALEFACTOR
        viewbox_x2 = (ord(glyph_data[1]) - 33) * SCALEFACTOR
        viewbox_w = viewbox_x2 - viewbox_x1
        for a, c in itertools.islice(itertools.pairwise(glyph_data[2:]), 0, None, 2):
            x = ((ord(a) - 33) * SCALEFACTOR) - viewbox_x1
            y = (50 - (ord(c) - 33 - 9)) * SCALEFACTOR
            if ord(a) < 33:
                path_data.append("M")
            else:
                path_data.extend((str(x), str(y)))
        width = viewbox_w * (1280 / 80) / SCALEFACTOR
        if (offset + 0x20) in overrides.setdefault(basename, {}):
            ucs = overrides[basename][offset + 0x20]
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
        if offset == 0 or path_data != ["M"]:
            fn = f"obj/{fontname}_{ucs:04X}_{basename}_{glyph_id:05d}.svg"
            with open(fn, "w", encoding="utf-8") as fd:
                print(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 {-30*SCALEFACTOR} {viewbox_w} {80*SCALEFACTOR}' width='{width}px' height='1280px'>", file=fd)
                if path_data != ["M"]:
                    print(f"<path d='{' '.join(path_data)}' stroke='black' fill='none' stroke-width='{2*SCALEFACTOR}' stroke-linejoin='round' stroke-linecap='round'/>", file=fd)
                print("</svg>", file=fd)
            fns.append(fn)
        offset += 1

subprocess.call(["inkscape", "--actions", "select-all;object-stroke-to-path", "-l", "--export-overwrite", *fns])

with open("hershey-fonts/hershey-fonts.notes", "r", encoding="utf-8") as fd:
    b = fd.read()

copying_notice = b.split("-" * 78, 2)[1].strip()

camel_case_break = re.compile(r"([a-z])([A-Z])")
fonts = {i for i, j in names.values()}

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
        ucs = fn.split("_", 2)[1]
        data = b.split("<path", 1)[1].split("d=\"", 1)[1].split("\"", 1)[0] if "<path" in b else ""
        glyph = f"<glyph unicode='&#x{ucs};' horiz-adv-x='{w}' d='{data}'/>"
        if glyphs.get(ucs, glyph) != glyph:
            print(fn)
        glyphs[ucs] = glyph
    with open(f"obj/{fontname}.svg", "w", encoding="utf-8") as fd:
        print(f"<svg xmlns=\"http://www.w3.org/2000/svg\"><defs><font id=\"Hershey{fontname}\"><font-face units-per-em=\"{round(42*SCALEFACTOR)}\" descent=\"{round(-11*SCALEFACTOR)}\" cap-height=\"{round(24*SCALEFACTOR)}\" x-height=\"{round(11*SCALEFACTOR)}\" font-family=\"Hershey {familyname}\" font-weight=\"{weight}\" font-style=\"{style}\"/>", file=fd)
        for ucs, glyph in sorted(glyphs.items()):
            print(glyph, file=fd)
        print("</font></defs></svg>", file=fd)
    subprocess.call(["fontforge", "-quiet", "-lang=ff", "-c", "Open($1); SetFontNames('', '', $3, '', $4); SetTTFName(0x409, 2, $5); Generate($2)", f"obj/{fontname}.svg", f"dist/Hershey{fontname}.ttf", friendlyname, copying_notice, friendlyvariant])
