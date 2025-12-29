#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, glob, itertools, subprocess

os.makedirs("obj", exist_ok=True)
os.makedirs("dist", exist_ok=True)
fns = []

SCALEFACTOR = 1000 / 80.0

for fn in glob.glob("hershey-fonts/*.jhf"):
    basename = os.path.splitext(os.path.basename(fn))[0]
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    byte = 32 if basename != "japanese" else 31
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
        fn = f"obj/{basename}_{byte:02X}_{glyph_id:05d}.svg"
        with open(fn, "w", encoding="utf-8") as fd:
            print(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 {-30*SCALEFACTOR} {viewbox_w} {80*SCALEFACTOR}' width='{width}px' height='1280px'>", file=fd)
            if path_data != ["M"]:
                print(f"<path d='{' '.join(path_data)}' stroke='black' fill='none' stroke-width='{2*SCALEFACTOR}' stroke-linejoin='round' stroke-linecap='round'/>", file=fd)
            print("</svg>", file=fd)
        fns.append(fn)
        byte += 1

subprocess.call(["inkscape", "--actions", "select-all;object-stroke-to-path", "-l", "--export-overwrite", *fns])

names = {
    "cyrilc_1": ("Cyrillic1-Regular", "Cyrillic 1"),
    "futural": ("Futura-Light", "Futura"),
    "futuram": ("Futura-Medium", "Futura"),
    "gothgbt": ("GothicEnglish-Triplex", "Gothic English"),
    "gothgrt": ("GothicGerman-Triplex", "Gothic German"),
    "gothiceng": ("GothicEnglish-Regular", "Gothic English"),
    "gothicger": ("GothicGerman-Regular", "Gothic German"),
    "gothicita": ("GothicItalian-Regular", "Gothic Italian"),
    "gothitt": ("GothicItalian-Triplex", "Gothic Italian"),
    "greekc": ("GreekComplex-Regular", "Greek Complex"),
    "greeks": ("GreekSimplex-Regular", "Greek Simplex"),
    "mathlow": ("MathLowercase-Regular", "Math Lowercase"),
    "mathupp": ("MathUppercase-Regular", "Math Uppercase"),
    "rowmand": ("RowMan-Duplex", "RowMan"),
    "rowmans": ("RowMan-Simplex", "RowMan"),
    "rowmant": ("RowManTriplex-Regular", "RowMan Triplex"),
    "scriptc": ("ScriptComplex-Regular", "Script Complex"),
    "scripts": ("ScriptSimplex-Regular", "Script Simplex"),
    "timesg": ("TimesGreek-Regular", "Times Greek"),
    "timesi": ("Times-Italic", "Times"),
    "timesib": ("Times-BoldItalic", "Times"),
    "timesr": ("Times-Regular", "Times"),
    "timesrb": ("Times-Bold", "Times"),
}

for fn in glob.glob("hershey-fonts/*.jhf"):
    basename = os.path.splitext(os.path.basename(fn))[0]
    fontname, familyname = names.get(basename, (basename.title() + "-Regular", basename.title()))
    variant = fontname.rsplit("-", 1)[1]
    style = "italic" if variant in ("Italic", "BoldItalic") else "regular"
    weight = {
        "Light": 300,
        "Simplex": 300,
        "Regular": 400,
        "Italic": 400,
        "Triplex": 400,
        "Medium": 500,
        "Duplex": 500,
        "Bold": 700,
        "BoldItalic": 700,
    }[variant]
    glyphs = []
    for fn in sorted(glob.glob(f"obj/{basename}_*.svg")):
        with open(fn, "r", encoding="utf-8") as fd:
            b = fd.read()
        x, y, w, h = b.split("viewBox=\"", 1)[1].split("\"", 1)[0].split()
        ucs = fn.rsplit("_", 2)[1]
        if ucs > "7E" or ucs < "20":
            print(basename)
            ucs = "F0" + ucs
        data = b.split("<path", 1)[1].split("d=\"", 1)[1].split("\"", 1)[0] if "<path" in b else ""
        glyphs.append(f"<glyph unicode='&#x{ucs};' horiz-adv-x='{w}' d='{data}'/>")
    with open(f"obj/{basename}.svg", "w", encoding="utf-8") as fd:
        print(f"<svg xmlns=\"http://www.w3.org/2000/svg\"><defs><font id=\"Hershey{fontname}\"><font-face units-per-em=\"{round(42*SCALEFACTOR)}\" descent=\"{round(-11*SCALEFACTOR)}\" cap-height=\"{round(24*SCALEFACTOR)}\" x-height=\"{round(11*SCALEFACTOR)}\" font-family=\"Hershey {familyname}\" font-weight=\"{weight}\" font-style=\"{style}\"/>", file=fd)
        for glyph in glyphs:
            print(glyph, file=fd)
        print("</font></defs></svg>", file=fd)
    subprocess.call(["fontforge", "-lang=ff", "-c", "Open($1); Generate($2)", f"obj/{basename}.svg", f"dist/{basename}.ttf"])
