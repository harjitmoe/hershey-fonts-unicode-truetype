#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, glob, subprocess, base64

with open("kanji.html", "w", encoding="utf-8") as f:
    print("<!DOCTYPE html><table>", file=f)
    for i in sorted(glob.glob("./obj/glyph_id/1*.svg")):
        kanji_id = int(os.path.splitext(os.path.basename(i))[0][1:], 10)
        if kanji_id >= 6000:
            continue
        print(kanji_id)
        png = os.path.splitext(i)[0] + ".png"
        exit_status = subprocess.call(["convert", i, "-crop", "642x642+0+667", "-flip", "-resize", "64x64", png])
        assert not exit_status
        with open(png, "rb") as in_file:
            b = in_file.read()
        print(f"<tr><td>{kanji_id}<td><img src=\"data:image/png;base64,{base64.b64encode(b).decode('utf-8')}\"/><td>", file=f)


