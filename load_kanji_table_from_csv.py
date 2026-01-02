#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import csv, ast, pprint

with open("glyph_id_to_unicode.txt", "r", encoding="utf-8") as fd:
    input_glyph_id_to_unicode = ast.literal_eval(fd.read())

with open("kanji.csv", "r", encoding="utf-8") as fd:
    for glyph_id, _unused, ucs in csv.reader(fd):
        if ucs:
            input_glyph_id_to_unicode[(True, int(glyph_id, 10))] = (
                    f"U+{ord(ucs):04X}", "Serif-Regular")

with open("glyph_id_to_unicode.txt", "w", encoding="utf-8") as fd:
    fd.write(pprint.pformat(input_glyph_id_to_unicode, sort_dicts=True))


