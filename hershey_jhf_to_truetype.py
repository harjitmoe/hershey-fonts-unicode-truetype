#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, glob, itertools, subprocess, re, pprint, ast
sys.path.append(os.path.abspath(os.path.join(__file__, os.pardir, "ecma35lib")))
from ecma35.data.graphdata import gsets

os.makedirs("obj", exist_ok=True)
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

individual_offsets_to_unicode = {
    ("occident", 239+3): ("Sans-Regular", 0x2113),
    ("occident", 240+3): ("Sans-Regular", 0x2202),
    ("occident", 241+3): ("Sans-Regular", 0x03F5),
    ("occident", 242+3): ("Sans-Regular", 0x03B8),
    ("occident", 243+3): ("Sans-Regular", 0x03D5),
    ("occident", 244+3): ("Sans-Regular", 0x03C2),
    ("occident", 261+6): ("Sans-Regular", 0x0027),
    ("occident", 830+9): ("Serif-Regular", 0xFB00),
    ("occident", 831+9): ("Serif-Regular", 0xFB01),
    ("occident", 832+9): ("Serif-Regular", 0xFB02),
    ("occident", 833+9): ("Serif-Regular", 0xFB03),
    ("occident", 834+9): ("Serif-Regular", 0xFB04),
    ("occident", 835+9): ("Serif-Regular", 0x0131),
    ("occident", 836+9): ("Serif-Regular", 0x03F5),
    ("occident", 837+9): ("Serif-Regular", 0x03B8),
    ("occident", 838+9): ("Serif-Regular", 0x03D5),
    ("occident", 942+12): ("Sans-Regular", 0x00A9),
    ("occident", 943+12): ("Sans-Regular", 0x00AE),
    ("occident", 952+12): ("Serif-Regular", 0x264E),
    ("occident", 1227+18): ("Serif-Regular", 0x044D),
    ("occident", 1446+24): ("GothicGerman-Regular", 0x0073),
    ("occident", 1447+24): ("GothicGerman-Regular", 0x00DF),
    ("occident", 1448+24): ("GothicGerman-Regular", 0xA729),
    ("symbolic", 88): ("Serif-Italic", 0xFB00),
    ("symbolic", 89): ("Serif-Italic", 0xFB01),
    ("symbolic", 90): ("Serif-Italic", 0xFB02),
    ("symbolic", 91): ("Serif-Italic", 0xFB03),
    ("symbolic", 92): ("Serif-Italic", 0xFB04),
    ("cyrillic", 67): ("Serif-Regular", 0x042D),
    ("mathlow", 77): ("Serif-Regular", 0x2202),
    ("mathupp", 77): ("Serif-Regular", 0x2202),
}

no_output = {"Occident-Regular", "Oriental-Regular"}

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
    "gothgrt": {0x23: 0xFE5F, 0x2D: 0x2212, 0x5F: 0x02CD, 0x73: 0x017F, 0x7F: 0x00B0},
    "gothitt": {0x23: 0xFE5F, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "gothiceng": {0x7F: 0x2588},
    "gothicger": {0x73: 0x017F, 0x7F: 0x2588},
    "gothicita": {0x7F: 0x2588},
    "futural": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x60: 0x02BB, 0x7F: 0x2588},
    "futuram": {0x7F: 0x2588},
    "greek": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x60: 0x02BB, 0x7F: 0x2588},
    "greekc": {0x23: 0xFE5F, 0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "greeks": {0x23: 0xFE5F, 0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "markers": {0x49: 0xFE61, 0x69: 0xFE61},
    "mathlow": {0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x72: 0x27EE, 0x73: 0x27EF, 0x74: 0x2772, 0x75: 0x2773, 0x7F: 0x007E},
    "mathupp": {0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x2C: 0x201A, 0x2E: 0x2024, 0x72: 0x27EE, 0x73: 0x27EF, 0x74: 0x2772, 0x75: 0x2773, 0x7B: 0x005D, 0x7D: 0x007B, 0x7F: 0x007E},
    "meteorology": {0x24: 0x25B4, 0x2A: 0x2217, 0x3F: 0x2753, 0x5F: 0xF05F, 0x7F: 0x007E},
    "music": {0x7F: 0x2588},
    "rowmand": {0x23: 0xFE5F, 0x26: 0x1F674, 0x28: 0x2768, 0x29: 0x2769, 0x2D: 0x2212, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "rowmans": {0x2C: 0x201A, 0x2E: 0x2024, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "rowmant": {0x23: 0xFE5F, 0x28: 0x2768, 0x29: 0x2769, 0x2D: 0x2212, 0x4A: 0xF04A, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "scriptc": {0x7F: 0x00B0},
    "scripts": {0x21: 0x2757, 0x22: 0x2033, 0x24: 0x1F4B2, 0x26: 0x1F675, 0x28: 0x2768, 0x29: 0x2769, 0x2C: 0x201A, 0x2E: 0x2024, 0x30: 0x1D7CE, 0x31: 0x1D7CF, 0x32: 0x1D7D0, 0x33: 0x1D7D1, 0x34: 0x1D7D2, 0x35: 0x1D7D3, 0x36: 0x1D7D4, 0x37: 0x1D7D5, 0x38: 0x1D7D6, 0x39: 0x1D7D7, 0x3A: 0xF03A, 0x3B: 0xF03B, 0x3F: 0x2753, 0x5F: 0x02CD, 0x7F: 0x00B0},
    "symbolic": {0x34: 0x27EE, 0x35: 0x27EF, 0x4F: 0xFE61, 0x71: 0x2774, 0x72: 0x2775, 0x75: 0x23B7, 0x7F: 0x007E},
    "timesg": {0x22: 0x2033, 0x28: 0x2768, 0x29: 0x2769, 0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x7F: 0x2588},
    "timesi": {0x7F: 0x2588},
    "timesib": {0x7F: 0x2588},
    "timesb": {0x7F: 0x2588},
    "timesr": {0x2A: 0x2217, 0x3A: 0xFE55, 0x3B: 0xFE54, 0x7F: 0x2588},
}

adjustments = {
    2403: (37 / 74.0, 0, 7.5),
    2404: (37 / 74.0, 0, 7.5),
    2405: (37 / 74.0, 0, 7.5),
    2406: (37 / 74.0, 0, 7.5),
    2407: (37 / 74.0, 0, 7.5),
    2408: (37 / 74.0, 0, 7.5),
    2409: (42 / 74.0, 0, 6.5),
    2410: (42 / 74.0, 0, 6.5),
    2411: (36.5 / 74.0, 0, 4),
    2412: (37 / 74.0, 0, 7.5),
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

glyph_id_to_unicode_and_fontname = {}

for fn in [*glob.glob("hershey-fonts/hershey-fonts/*.jhf"), *glob.glob("complete-hershey-data/*.jhf")]:
    basename = os.path.splitext(os.path.basename(fn))[0]
    is_japanese = basename in ("japanese", "oriental")
    lgc = latin_greek_or_cyrillic.get(basename, "L")
    fontname, charset = names.get(basename, (basename.title() + "-Regular", None))
    fontnames.add(fontname)
    with open(fn, "r", encoding="utf-8") as fd:
        b = fd.read().rstrip("\x1A").replace("\n", "")
    offset = 0
    _fontname = fontname
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
        if glyph_id != 12345 and (
                value := input_glyph_id_to_unicode.get((is_japanese, glyph_id), None)):
            ucs = int(value[0].removeprefix("U+"), 16)
            if ucs > 0x0020:
                fontname = value[1]
        elif override := individual_offsets_to_unicode.get((basename, offset), None):
            fontname, ucs = override
        elif (offset + 0x20) in overrides.setdefault(basename, {}):
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
        if not (0xF000 <= ucs <= 0xF8FF):
            glyph_id_to_unicode_and_fontname.setdefault((is_japanese, glyph_id), set()).add(
                (f"U+{ucs:04X}", fontname))
        if offset == 0 or path_data != ["M"]:
            fn = f"obj/{fontname}_{ucs:04X}_{basename}_{glyph_id:05d}.svg"
            with open(fn, "w", encoding="utf-8") as fd:
                print(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 {-30*SCALEFACTOR} {viewbox_w} {80*SCALEFACTOR}'>", file=fd)
                if path_data != ["M"]:
                    print(f"<path d='{' '.join(path_data)}' stroke='black' fill='none' stroke-width='{2*SCALEFACTOR}' stroke-linejoin='round' stroke-linecap='round'/>", file=fd)
                print("</svg>", file=fd)
            fns.append(fn)
        offset += 1
        _last_glyph_id = glyph_id

with open("dist/glyph_id_to_unicode.txt", "w", encoding="utf-8") as fd:
    fd.write(pprint.pformat(glyph_id_to_unicode_and_fontname))

subprocess.call(["inkscape", "--actions", "select-all;object-stroke-to-path", "-l", "--export-overwrite", *fns])

with open("hershey-fonts/hershey-fonts.notes", "r", encoding="utf-8") as fd:
    b = fd.read()

copying_notice = b.split("-" * 78, 2)[1].strip()

camel_case_break = re.compile(r"([a-z])([A-Z])")
fonts = {i for i, j in names.values()}

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
    print()
    print(fontname)
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
""", f"obj/{fontname}.svg", f"dist/Hershey{fontname}.ttf", friendlyname, copying_notice, friendlyvariant, repr(SCALEFACTOR)])
