#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Fixer: corrects V7 (dominant seventh) entries in chords.json.

Problems fixed:
- fingerings were stored as one-character strings ('3', '0', ...), which the
  web app's ChordDiagram skips (it checks typeof f === 'number'), so every
  V7 diagram rendered an empty fretboard
- baseFret was hard-coded to 1, pushing dots off the grid for high shapes
  (e.g. C♯7 x-4-6-4-6-4)
- E♭ major had the wrong chord entirely (A7 instead of B♭7)
- names used '#' instead of the '♯' used everywhere else
"""
import json


def parse_v7(shape):
    """'x21202' / ['x','2',...] -> ['x', 2, 1, 2, 0, 2]."""
    if isinstance(shape, str):
        shape = list(shape)
    out = []
    for ch in shape:
        s = str(ch).strip().lower()
        if s == "x":
            out.append("x")
        elif s == "o":
            out.append(0)
        else:
            out.append(int(s))
    return out


def v7_base_fret(fingering):
    """1 for shapes with open strings, else the lowest pressed fret."""
    frets = [f for f in fingering if isinstance(f, int) and f > 0]
    return min(frets) if frets and 0 not in fingering else 1


# Correct V7 for the 12 major keys (name, shape). The dominant of E♭ is B♭7 —
# the data previously carried A7 here.
V7_MAJOR = {
    "C":  ("G7", "320003"),
    "G":  ("D7", "xx0212"),
    "D":  ("A7", "x02020"),
    "A":  ("E7", "020100"),
    "E":  ("B7", "x21202"),
    "B":  ("F♯7", "242322"),
    "F♯": ("C♯7", "x46464"),
    "D♭": ("G♯7", "464544"),
    "A♭": ("E♭7", "x68686"),
    "E♭": ("B♭7", "x13131"),
    "B♭": ("F7", "131211"),
    "F":  ("C7", "x32310"),
}


def apply_v7_fixes(data):
    """Normalize/add the V7 entry of every key in a chords.json data dict."""
    fixed = 0
    for key in data["keys"]:
        chords = key["chords"]
        if key["type"] == "major":
            name, shape = V7_MAJOR[key["symbol"]]
        else:
            v7 = chords.get("V7")
            if not v7:
                continue
            name = v7["name"].replace("#", "♯")
            shape = v7["fingering"]
        name = name.replace("#", "♯")
        fingering = parse_v7(shape)
        chords["V7"] = {"name": name, "fingering": fingering,
                        "baseFret": v7_base_fret(fingering)}
        fixed += 1
    return fixed


if __name__ == "__main__":
    with open("chords.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = apply_v7_fixes(data)

    with open("chords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Fixed {fixed} V7 chords.")