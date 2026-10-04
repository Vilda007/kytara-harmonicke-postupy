#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Fixer: Fills in missing vii° chords and ensures data consistency."""
import json

def S(*s, base=1): return (s, base)

def get_dim_shape(root_pc):
    # Basic diminished triad: Root, m3, d5
    # This is a simplified mapping for vii° based on common guitar voicings
    # mapping root index (0=C) to a reasonable fingering
    # [Root, 3rd, 5th]
    voicings = {
        0: (('x', 1, 3, 2, 1, 'x'), 1), # Cdim
        1: (('x', 2, 4, 3, 2, 'x'), 2), # C#dim
        2: (('x', 3, 5, 4, 3, 'x'), 3), # Ddim
        3: (('x', 4, 6, 5, 4, 'x'), 4), # D#dim
        4: (('x', 5, 7, 6, 5, 'x'), 5), # Edim
        5: (('x', 6, 8, 7, 6, 'x'), 6), # Fdim
        6: (('x', 7, 9, 8, 7, 'x'), 7), # F#dim
        7: (('x', 8, 10, 9, 8, 'x'), 8), # Gdim
        8: (('x', 9, 11, 10, 9, 'x'), 9), # G#dim
        9: (('x', 10, 0, 11, 10, 'x'), 10), # Adim (simplified)
        10: (('x', 11, 1, 0, 11, 'x'), 11), # A#dim
        11: (('x', 0, 2, 1, 0, 'x'), 1), # Bdim
    }
    return voicings.get(root_pc, (('x', 1, 3, 2, 1, 'x'), 1))

if __name__ == "__main__":
    with open('chords.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Root pitch classes for keys
    # C G D A E B F# Db Ab Eb Bb F
    root_pcs = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]

    for i, key in enumerate(data["keys"]):
        if key["type"] == "major":
            # vii° is the 7th chord
            if not key["chords"].get("vii°"):
                root_pc = (root_pcs[i] + 11) % 12 # vii is 11 semitones above I
                shape, base = get_dim_shape(root_pc)
                key["chords"]["vii°"] = {
                    "name": "dim", # Simplified name for the diagram
                    "fingering": list(shape),
                    "baseFret": base
                }

    with open('chords.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Filled missing vii° chords in chords.json")
