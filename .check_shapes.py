# -*- coding: utf-8 -*-
"""Ověří, že hmat v tabulce skutečně odpovídá názvu akordu (podle pitch classes)."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHROM = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
OPEN = [4, 9, 2, 7, 11, 4]  # E A D G B e (6. -> 1.)
PC = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11,
      'Db':1,'Eb':3,'Gb':6,'Ab':8,'Bb':10,'Cb':11,'Fb':4,'E#':5,'B#':0}

def name2pc(nm):
    m = nm.replace('♯', '#').replace('♭', 'b')
    q = 'maj'
    if m.endswith('dim'): q = 'dim'; m = m[:-3]
    elif m.endswith('m7'): q = 'm7'; m = m[:-2]
    elif m.endswith('m'): q = 'min'; m = m[:-1]
    elif m.endswith('7'): q = '7'; m = m[:-1]
    return PC[m], q

TRIADS = {'maj': (0, 4, 7), 'min': (0, 3, 7), 'dim': (0, 3, 6), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10)}

def shape_notes(shape):
    return [(OPEN[i] + int(f)) % 12 for i, f in enumerate(shape) if f not in ('x', 'o')]

def check(name, shape, ctx):
    try:
        pc, q = name2pc(name)
    except KeyError:
        print(f"  SKIP [{ctx}] {name} (nerozpoznaný název)")
        return
    want = set((pc + iv) % 12 for iv in TRIADS[q])
    got = set(shape_notes(shape))
    if not got <= want:
        extra = got - want
        print(f"  MISMATCH [{ctx}] {name}: hmat = {sorted(CHROM[p] for p in got)}, "
              f"akord = {sorted(CHROM[p] for p in want)}; cizí tóny: {sorted(CHROM[p] for p in extra)}")

def S(*s, base=1): return (s, base)

def load_src(path):
    src = open(path, encoding='utf-8').read()
    for marker in ('pages_html = [', 'pages_html =', 'html = CSS'):
        idx = src.find(marker)
        if idx > 0:
            return src[:idx]
    return src

def ns_for(path):
    return {'S': S, 'math': __import__('math'), 'os': os, '__file__': path}

print("== DUR sada (kytara-gen.py) ==")
ns = {}
exec(load_src('kytara-gen.py'), ns_for('kytara-gen.py'), ns)
for sym, chords, tip in ns['K']:
    for i, (nm, sh) in enumerate(chords):
        if sh is None: continue
        check(nm, sh[0], f"{sym}-dur #{i}")
for key, (nm, sh) in ns['ALT7'].items():
    shape = tuple(int(c) if c.isdigit() else ('x' if c == 'x' else 0) for c in sh)
    check(nm, shape, f"ALT7[{key}]")

print("== MOL sada (kytara-gen-moll.py) ==")
ns = {}
exec(load_src('kytara-gen-moll.py'), ns_for('kytara-gen-moll.py'), ns)
for sym, chords, v7n, v7s, tip in ns['M']:
    for i, (nm, sh) in enumerate(chords):
        if sh is None: continue
        check(nm, sh[0], f"{sym}-moll #{i}")
    shape = tuple(int(c) if c.isdigit() else ('x' if c == 'x' else 0) for c in v7s)
    check(v7n, shape, f"{sym}-moll V7")
print("hotovo")