#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Fixer: fills in correct diminished triad shapes.

Fixes:
- minor keys: ii° was null (web app showed N/A)
- major keys: vii° had a generic name "dim" and some broken fingerings
  (e.g. fret 0 mixed with frets 10-11)

Diminished triad = root, minor 3rd (+3), diminished 5th (+6).
Two movable shapes are used (frets are absolute, baseFret = lowest fret):
- A-string root:  x  r  r+1  r+2  r+1  x
- E-string root:  r  r+1  r+2  r  x  x   (r may be 0 = open)
"""
import json

# chord name -> (fingering, baseFret); every dim triad used as ii° in minor /
# vii° in major keys. Shapes verified note by note.
DIM = {
    "Bdim":  (["x", 2, 3, 4, 3, "x"], 2),   # B F B D
    "F♯dim": ([2, 3, 4, 2, "x", "x"], 2),  # F♯ C F♯ A
    "C♯dim": (["x", 4, 5, 6, 5, "x"], 4),  # C♯ G C♯ E
    "G♯dim": ([4, 5, 6, 4, "x", "x"], 4),  # G♯ D G♯ B
    "D♯dim": (["x", 6, 7, 8, 7, "x"], 6),  # D♯ A D♯ F♯
    "A♯dim": (["x", 1, 2, 3, 2, "x"], 1),  # A♯ E A♯ C♯
    "E♯dim": ([1, 2, 3, 1, "x", "x"], 1),  # E♯(F) B E♯ G♯
    "Cdim":  (["x", 3, 4, 5, 4, "x"], 3),  # C G♭ C E♭
    "Gdim":  ([3, 4, 5, 3, "x", "x"], 3),  # G D♭ G B♭
    "Ddim":  (["x", 5, 6, 7, 6, "x"], 5),  # D G♭ D F
    "Adim":  ([5, 6, 7, 5, "x", "x"], 5),  # A E♭ A C
    "Edim":  ([0, 1, 2, 0, "x", "x"], 1),  # E B♭ E G  (open position)
}

# semitone offset of each key root (C major = 0); sharp aliases cover minor
# key symbols upper-cased into the sharp spelling (c♯, g♯, ...)
MAJOR_ROOT = {"C": 0, "G": 7, "D": 2, "A": 9, "E": 4, "B": 11,
              "F♯": 6, "D♭": 1, "A♭": 8, "E♭": 3, "B♭": 10, "F": 5,
              "C♯": 1, "G♯": 8, "D♯": 3, "A♯": 10}

SHARP = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]


def dim_name(root_pc):
    """Diminished triad name built on the given pitch class."""
    return SHARP[root_pc % 12] + "dim"


# F♯ major / d♯ minor spell their diminished degree as E♯°, not F°
ENHARMONIC = {("F♯", "major"): "E♯dim", ("d♯", "minor"): "E♯dim"}


def apply_dim_fixes(data):
    """Fill in the ii°/vii° entry of every key in a chords.json data dict."""
    fixed = 0
    for key in data["keys"]:
        chords = key["chords"]
        if key["type"] == "major":
            # vii° = 11 semitones above the tonic
            name = dim_name(MAJOR_ROOT[key["symbol"]] + 11)
            role = "vii°"
        else:
            # ii° = 2 semitones above the tonic
            name = dim_name(MAJOR_ROOT[key["symbol"].upper()] + 2)
            role = "ii°"
        name = ENHARMONIC.get((key["symbol"], key["type"]), name)
        fingering, base = DIM[name]
        chords[role] = {"name": name, "fingering": fingering, "baseFret": base}
        fixed += 1
    return fixed


if __name__ == "__main__":
    with open("chords.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = apply_dim_fixes(data)

    with open("chords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Fixed {fixed} diminished chords.")