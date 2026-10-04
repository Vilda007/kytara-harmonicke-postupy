#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporter: Extracts chord and progression data from Python generators to JSON."""
import json
import os

def S(*s, base=1): return (s, base)

# we need to import the data. Since the generators execute logic on import,
# we'll extract the specific variables manually or by executing the script
# in a controlled environment.

def extract_data():
    # Temporary namespace to run generators
    ns = {'S': S, 'math': __import__('math'), 'os': os, '__file__': 'temp.py'}

    # Process DUR keys
    with open('kytara-gen.py', 'r', encoding='utf-8') as f:
        src_dur = f.read()
        # Split to avoid running the HTML generation part
        src_dur = src_dur.split('pages_html = [')[0]
        exec(src_dur, ns)

    # Process MOL keys
    with open('kytara-gen-moll.py', 'r', encoding='utf-8') as f:
        src_mol = f.read()
        src_mol = src_mol.split('pages_html = [')[0]
        exec(src_mol, ns)

    # Structure the data
    data = {
        "keys": [],
        "progressions": [],
        "blues": []
    }

    # Process DUR (K)
    for i, (sym, chords, tip) in enumerate(ns['K']):
        key_obj = {
            "symbol": sym,
            "type": "major",
            "position": i,
            "capoTip": tip,
            "chords": {}
        }
        # Mapping roles I, ii, iii, IV, V, vi, vii°
        roles = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
        for idx, (name, shape_data) in enumerate(chords):
            role = roles[idx]
            if shape_data:
                shape, base = shape_data
                key_obj["chords"][role] = {
                    "name": name,
                    "fingering": list(shape),
                    "baseFret": base
                }
            else:
                key_obj["chords"][role] = None
        data["keys"].append(key_obj)

    # Process MOL (M)
    # M entries are (symbol, [chords], V7_name, V7_shape, tip)
    for i, (sym, chords, v7n, v7s, tip) in enumerate(ns['M']):
        key_obj = {
            "symbol": sym,
            "type": "minor",
            "position": i,
            "capoTip": tip,
            "chords": {}
        }
        # Mapping roles i, ii°, III, iv, v, VI, VII
        roles = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
        for idx, (name, shape_data) in enumerate(chords):
            role = roles[idx]
            if shape_data:
                shape, base = shape_data
                key_obj["chords"][role] = {
                    "name": name,
                    "fingering": list(shape),
                    "baseFret": base
                }
            else:
                key_obj["chords"][role] = None

        # Add V7 as a special case for harmonic minor
        key_obj["chords"]["V7"] = {
            "name": v7n,
            "fingering": list(v7s),
            "baseFret": 1 # V7 shapes are usually written as absolute or normalized to 1
        }
        data["keys"].append(key_obj)

    # Progressions (ROMROWS)
    # ROMROWS = [((("I", 0), ...), "genre")]
    for row in ns['ROMROWS']:
        roms = row[:-1]
        genre = row[-1]
        data["progressions"].append({
            "sequence": [r[0] for r in roms],
            "genre": genre
        })

    # Blues (BLUEST)
    # BLUEST = [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4]
    data["blues"] = ns['BLUEST']

    return data

if __name__ == "__main__":
    res = extract_data()
    with open('chords.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(res['keys'])} keys to chords.json")
