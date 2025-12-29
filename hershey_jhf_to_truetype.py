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
    "greekc": ("Serif-Regular", "hershey-greek-alternate"),
    "cyrillic": ("Serif-Regular", "hershey-cyrillic"),
    "cyrilc_1": ("Serif-Regular", "hershey-cyrillic-alternate"),
    "music": ("Serif-Regular", "hershey-musical"),
    "timesrb": ("Serif-Bold", "ir006"),
    "rowmant": ("Serif-Bold", "ir006/smart-quotes-up-arrow"),
    "astrology": ("Serif-Bold", "hershey-astrological"),
    "timesi": ("Serif-Italic", "ir006"),
    "timesib": ("Serif-BoldItalic", "ir006"),
    "gothiceng": ("GothicEnglish-Regular", "ir006"),
    "gothgbt": ("GothicEnglish-Regular", "ir006/smart-quotes-up-arrow"),
    "gothicger": ("GothicGerman-Regular", "ir006"),
    "gothgrt": ("GothicGerman-Regular", "ir006/smart-quotes-up-arrow"),
    "gothicita": ("GothicItalian-Regular", "ir006"),
    "gothitt": ("GothicItalian-Regular", "ir006/smart-quotes-up-arrow"),
    "cursive": ("Cursive-Regular", "ir006/smartquotes-hybrid"),
    "scriptc": ("ScriptComplex-Regular", "ir006/smart-quotes-up-arrow"),
    "scripts": ("Cursive-Regular", "ir006/smart-quotes-up-arrow"),
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
        for a, c in itertools.batched(glyph_data[2:], 2):
            x = ((ord(a) - 33) * SCALEFACTOR) - viewbox_x1
            y = (50 - (ord(c) - 33 - 9)) * SCALEFACTOR
            if ord(a) < 33:
                path_data.append("M")
            else:
                path_data.extend((str(x), str(y)))
        width = viewbox_w * (1280 / 80) / SCALEFACTOR
        if charset is None or offset > 94:
            ucs = 0xF020 + offset
        elif offset == 0:
            ucs = 0x0020
        else:
            ucs = (gsets[charset][2][offset - 1] or (0xF000 + offset,))[0]
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
    glyphs = {}
    for fn in sorted(glob.glob(f"obj/{fontname}_*.svg")):
        with open(fn, "r", encoding="utf-8") as fd:
            b = fd.read()
        x, y, w, h = b.split("viewBox=\"", 1)[1].split("\"", 1)[0].split()
        ucs = fn.split("_", 2)[1]
        data = b.split("<path", 1)[1].split("d=\"", 1)[1].split("\"", 1)[0] if "<path" in b else ""
        glyphs[ucs] = f"<glyph unicode='&#x{ucs};' horiz-adv-x='{w}' d='{data}'/>"
    with open(f"obj/{fontname}.svg", "w", encoding="utf-8") as fd:
        print(f"<svg xmlns=\"http://www.w3.org/2000/svg\"><defs><font id=\"Hershey{fontname}\"><font-face units-per-em=\"{round(42*SCALEFACTOR)}\" descent=\"{round(-11*SCALEFACTOR)}\" cap-height=\"{round(24*SCALEFACTOR)}\" x-height=\"{round(11*SCALEFACTOR)}\" font-family=\"Hershey {familyname}\" font-weight=\"{weight}\" font-style=\"{style}\"/>", file=fd)
        for ucs, glyph in sorted(glyphs.items()):
            print(glyph, file=fd)
        print("</font></defs></svg>", file=fd)
    subprocess.call(["fontforge", "-lang=ff", "-c", "Open($1); Generate($2)", f"obj/{fontname}.svg", f"dist/{fontname}.ttf"])
