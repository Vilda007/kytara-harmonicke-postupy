#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generátor: Harmonické postupy na kytaru — 12 MOLÝCH tónin -> multipage HTML (pro PDF)."""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postupy-vsechny-molove-toniny.html')
X = '✕'; O = '○'

def S(*s, base=1): return (s, base)

# Molové tóniny (pořadí dle pozic na kruhu kvint, k=0..11):
# (symbol, [i, ii°(card), III, iv, v, VI, VII], V7_name, V7_shape, capo_tip)
M = [
 ("a", [("Am", S('x',0,2,2,1,0)), ("Bdim", None), ("C", S('x',3,2,0,1,0)), ("Dm", S('x','x',0,2,3,1)),
        ("Em", S(0,2,2,0,0,0)), ("F", S(1,3,3,2,1,1)), ("G", S(3,2,0,0,0,3))],
  "E7", "020100", None),
 ("e", [("Em", S(0,2,2,0,0,0)), ("F♯dim", None), ("G", S(3,2,0,0,0,3)), ("Am", S('x',0,2,2,1,0)),
        ("Bm", S('x',2,4,4,3,2, base=2)), ("C", S('x',3,2,0,1,0)), ("D", S('x','x',0,2,3,2))],
  "B7", "x21202", "Vše otevřené krom Bm (barré 2) — jinak capo 2 + tvary a-moll (Am→Bm, Dm→Em, C→D, G→A, Em→F♯m, F→G)."),
 ("b", [("Bm", S('x',2,4,4,3,2, base=2)), ("C♯dim", None), ("D", S('x','x',0,2,3,2)), ("Em", S(0,2,2,0,0,0)),
        ("F♯m", S(2,4,4,2,2,2, base=2)), ("G", S(3,2,0,0,0,3)), ("A", S('x',0,2,2,2,0))],
  "F♯7", "242322", "capo 2 + tvary a-moll (Am→Bm, Dm→Em, Em→F♯m, F→G, C→D, G→A)."),
 ("f♯", [("F♯m", S(2,4,4,2,2,2, base=2)), ("G♯dim", None), ("A", S('x',0,2,2,2,0)), ("Bm", S('x',2,4,4,3,2, base=2)),
        ("C♯m", S('x',4,6,6,5,4, base=4)), ("D", S('x','x',0,2,3,2)), ("E", S(0,2,2,1,0,0))],
  "C♯7", "x46464", "capo 2 + tvary e-moll (Em→F♯m, G→A, A→B, Bm→C♯m, C→D, D→E)."),
 ("c♯", [("C♯m", S('x',4,6,6,5,4, base=4)), ("D♯dim", None), ("E", S(0,2,2,1,0,0)), ("F♯m", S(2,4,4,2,2,2, base=2)),
        ("G♯m", S(4,6,6,4,4,4, base=4)), ("A", S('x',0,2,2,2,0)), ("B", S('x',2,4,4,4,2, base=2))],
  "G♯7", "464544", "capo 4 + tvary a-moll (Am→C♯m, Dm→F♯m, Em→G♯m, F→A, G→B, C→E)."),
 ("g♯", [("G♯m", S(4,6,6,4,4,4, base=4)), ("A♯dim", None), ("B", S('x',2,4,4,4,2, base=2)), ("C♯m", S('x',4,6,6,5,4, base=4)),
        ("D♯m", S('x',6,8,8,7,6, base=6)), ("E", S(0,2,2,1,0,0)), ("F♯", S(2,4,4,3,2,2, base=2))],
  "D♯7", "x68686", "capo 4 + tvary e-moll (Em→G♯m, G→B, A→C♯, Bm→D♯m, C→E, D→F♯)."),
 ("d♯", [("D♯m", S('x',6,8,8,7,6, base=6)), ("E♯dim", None), ("F♯", S(2,4,4,3,2,2, base=2)), ("G♯m", S(4,6,6,4,4,4, base=4)),
        ("A♯m", S('x',1,3,3,2,1)), ("B", S('x',2,4,4,4,2, base=2)), ("C♯", S('x',4,6,6,6,4, base=4))],
  "A♯7", "x13131", "capo 6 + tvary a-moll (Am→D♯m, Dm→G♯m, Em→A♯m, F→B, G→C♯, C→F♯)."),
 ("b♭", [("B♭m", S('x',1,3,3,2,1)), ("Cdim", None), ("D♭", S('x',4,6,6,6,4, base=4)), ("E♭m", S('x',6,8,8,7,6, base=6)),
        ("Fm", S(1,3,3,1,1,1)), ("G♭", S(2,4,4,3,2,2, base=2)), ("A♭", S(4,6,6,5,4,4, base=4))],
  "F7", "131211", "capo 1 + tvary a-moll (Am→B♭m, Dm→E♭m, Em→Fm, F→G♭, G→A♭, C→D♭)."),
 ("f", [("Fm", S(1,3,3,1,1,1)), ("Gdim", None), ("A♭", S(4,6,6,5,4,4, base=4)), ("B♭m", S('x',1,3,3,2,1)),
        ("Cm", S('x',3,5,5,4,3, base=3)), ("D♭", S('x',4,6,6,6,4, base=4)), ("E♭", S('x',6,8,8,8,6, base=6))],
  "C7", "x32310", "capo 1 + tvary e-moll (Em→Fm, G→A♭, A→B♭, Bm→Cm, C→D♭, D→E♭)."),
 ("c", [("Cm", S('x',3,5,5,4,3, base=3)), ("Ddim", None), ("E♭", S('x',6,8,8,8,6, base=6)), ("Fm", S(1,3,3,1,1,1)),
        ("Gm", S(3,5,5,3,3,3, base=3)), ("A♭", S(4,6,6,5,4,4, base=4)), ("B♭", S('x',1,3,3,3,1))],
  "G7", "320001", "capo 3 + tvary a-moll (Am→Cm, Dm→Fm, Em→Gm, F→A♭, G→B♭, C→E♭)."),
 ("g", [("Gm", S(3,5,5,3,3,3, base=3)), ("Adim", None), ("B♭", S('x',1,3,3,3,1)), ("Cm", S('x',3,5,5,4,3, base=3)),
        ("Dm", S('x','x',0,2,3,1)), ("E♭", S('x',6,8,8,8,6, base=6)), ("F", S(1,3,3,2,1,1))],
  "D7", "xx0212", "capo 3 + tvary e-moll (Em→Gm, G→B♭, A→C, Bm→Dm, C→E♭, D→F)."),
 ("d", [("Dm", S('x','x',0,2,3,1)), ("Edim", None), ("F", S(1,3,3,2,1,1)), ("Gm", S(3,5,5,3,3,3, base=3)),
        ("Am", S('x',0,2,2,1,0)), ("B♭", S('x',1,3,3,3,1)), ("C", S('x',3,2,0,1,0))],
  "A7", "x02020", "Bez capo — Dm/F/G/Am/B♭/C = převážně otevřené tvary; jinak capo 5 + tvary a-moll (Am→Dm)."),
]

MAJ = [("C", "Am"), ("G", "Em"), ("D", "Bm"), ("A", "F♯m"), ("E", "C♯m"), ("B", "G♯m"),
       ("F♯/G♭", "D♯m/E♭m"), ("D♭/C♯", "B♭m"), ("A♭/G♯", "Fm"), ("E♭", "Cm"), ("B♭", "Gm"), ("F", "Dm")]

CX, CY = 350.0, 570.0
R_RING, R_CHIP, R_MINOR_CHIP, R_INNER = 255.0, 218.0, 96.0, 132.0

def pt(k, r):
    th = math.radians(-90 + 30*k)
    return CX + r*math.cos(th), CY + r*math.sin(th)

def chip(x, y, w, h, label, fill, stroke='var(--line)', sw=1, fs=14):
    return (f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="{h/2}" '
            f'class="chip" style="fill:{fill};stroke:{stroke};stroke-width:{sw}"/>' +
            f'<text x="{x:.1f}" y="{y+fs*0.36:.1f}" text-anchor="middle" class="label" font-size="{fs}" fill="var(--fg)">{label}</text>')

def circle_svg(ki):
    kI, kV, kIV = ki, (ki+1) % 12, (ki-1) % 12
    out = [f'<path d="M {pt(kV,118)[0]:.1f} {pt(kV,118)[1]:.1f} A 118 118 0 0 0 {pt(kI,118)[0]:.1f} {pt(kI,118)[1]:.1f}" class="hedge" marker-end="url(#arr)"/>']
    kv_t, ki_t = -90+30*kV, -90+30*kI
    ti = ki_t if ki_t <= kv_t else ki_t - 360
    tm = (kv_t + ti)/2
    lx = CX + 158*math.cos(math.radians(tm)); ly = CY + 158*math.sin(math.radians(tm))
    out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="10" fill="var(--dom)">dominantový tah (v→i)</text>')
    for k in range(12):
        x, y = pt(k, R_CHIP)
        fill, stroke, sw = 'var(--neutral)', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--vinbg)', 'var(--vin)', 2          # III dur sourozenec
        out.append(chip(x, y, 46 if len(MAJ[k][0]) == 1 else 62, 26, MAJ[k][0], fill, stroke, sw, 14 if len(MAJ[k][0]) == 1 else 10.5))
    for k in range(12):
        x, y = pt(k, R_MINOR_CHIP)
        fill, stroke, sw = '#ecf0f4', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--tonicbg)', 'var(--tonic)', 2      # i tónika
        elif k == kV: fill, stroke, sw = 'var(--dombg)', 'var(--dom)', 2        # v
        elif k == kIV: fill, stroke, sw = 'var(--subbg)', 'var(--sub)', 2       # iv
        lab = MAJ[k][1]
        w = 34 if len(lab) <= 3 else 46
        out.append(chip(x, y, w, 20, lab, fill, stroke, sw, 9.5 if len(lab) <= 3 else 8.5))
    out.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RING:.0f}" fill="none" stroke="#d7d3c8" stroke-width="1"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="{R_INNER:.0f}" fill="none" stroke="#d7d3c8" stroke-width="1" stroke-dasharray="4 4" opacity="0.7"/>')
    return ''.join(out)

def chordbox(x, y, name, shape, base, numeral):
    g = ['<g>']
    if base == 1:
        g.append(f'<line x1="{x}" y1="{y+10}" x2="{x+80}" y2="{y+10}" stroke="var(--fg)" stroke-width="2.6"/>')
    else:
        g.append(f'<text x="{x-8}" y="{y+22}" font-size="9.5" fill="var(--muted)" text-anchor="end">{base}</text>')
    for i in range(6):
        g.append(f'<line x1="{x+i*16}" y1="{y+10}" x2="{x+i*16}" y2="{y+90}" stroke="var(--line)" stroke-width="1"/>')
    for r in range(5):
        g.append(f'<line x1="{x}" y1="{y+10+r*20}" x2="{x+80}" y2="{y+10+r*20}" stroke="#b6b2a6" stroke-width="0.8"/>')
    for i, f in enumerate(shape):
        sx = x + i*16
        if f == 'x': g.append(f'<text x="{sx}" y="{y-2}" font-size="10" fill="#8a8074" text-anchor="middle">{X}</text>')
        elif f in ('o', 0): g.append(f'<text x="{sx}" y="{y-2}" font-size="10" fill="var(--line)" text-anchor="middle">{O}</text>')
    nb = sum(1 for f in shape if (f == base) or (base == 1 and f == 1))
    if nb >= 2:
        x1 = x if isinstance(shape[0], (int, float)) else x + 14
        g.append(f'<rect x="{x1-1}" y="{y+13}" width="{x+80-x1+2}" height="14" rx="7" fill="var(--fg)" opacity="0.45"/>')
    for i, f in enumerate(shape):
        if not isinstance(f, (int, float)) or f in (0,): continue
        r = f - base
        g.append(f'<circle cx="{x+i*16}" cy="{y+10+r*20+10}" r="6.5" fill="var(--fg)"/>')
    g.append(f'<text x="{x+40}" y="{y+112}" text-anchor="middle" class="ch" font-size="15">{name}</text>')
    g.append(f'<text x="{x+40}" y="{y+127}" text-anchor="middle" font-size="9.5" fill="var(--muted)">{numeral}</text>')
    g.append('</g>')
    return ''.join(g)

def card(x, y, title, sub, line3):
    return (f'<rect x="{x}" y="{y}" width="84" height="104" rx="8" fill="#f4f2ec" stroke="#b6b2a6" stroke-dasharray="4 4"/>'
            f'<text x="{x+42}" y="{y+24}" text-anchor="middle" class="ch" font-size="13">{title}</text>'
            f'<text x="{x+42}" y="{y+40}" text-anchor="middle" font-size="9" fill="var(--muted)">{sub}</text>'
            f'<text x="{x+42}" y="{y+62}" text-anchor="middle" font-size="9.5" fill="var(--fg)">{line3}</text>')

BARR = [("E-dur tvar", (0,2,2,1,0,0), 1, "F=1 · G=3 · A=5 · B=7 · C=8 · D=10", "tónika na 6. struně"),
        ("A-dur tvar", ('x',0,2,2,2,0), 1, "B=2 · C=3 · D=5 · E=7 · F=8", "tónika na 5. struně"),
        ("Em-mol tvar", (0,2,2,0,0,0), 1, "F♯m=2 · Gm=3 · Am=5 · Bm=7 · Dm=10", "tónika na 6. struně"),
        ("Am-mol tvar", ('x',0,2,2,1,0), 1, "Bm=2 · Cm=3 · Dm=5 · Em=7 · Fm=8", "tónika na 5. struně")]
ROOTS = {"E-dur tvar": (0, 0), "A-dur tvar": (1, 0), "Em-mol tvar": (0, 0), "Am-mol tvar": (1, 0)}

def barrbox(x, y, title, shape, base, ex1, ex2, root):
    g = ['<g>']
    for i in range(6):
        g.append(f'<line x1="{x+i*16}" y1="{y}" x2="{x+i*16}" y2="{y+68}" stroke="var(--line)" stroke-width="1" opacity="0.45"/>')
    for r in range(4):
        g.append(f'<line x1="{x}" y1="{y+r*20}" x2="{x+80}" y2="{y+r*20}" stroke="#b6b2a6" stroke-width="0.7" opacity="0.6"/>')
    for i, f in enumerate(shape):
        sx = x + i*16
        if f == 'x': g.append(f'<text x="{sx}" y="{y-4}" font-size="9" fill="#8a8074" text-anchor="middle">{X}</text>')
        elif f in ('o', 0): g.append(f'<text x="{sx}" y="{y-4}" font-size="9" fill="var(--line)" text-anchor="middle">{O}</text>')
    nb = sum(1 for f in shape if isinstance(f, (int, float)) and f == base)
    if nb >= 3:
        x1 = x if isinstance(shape[0], (int, float)) else x + 14
        g.append(f'<rect x="{x1}" y="{y-1}" width="{x+80-x1}" height="12" rx="6" fill="var(--fg)" opacity="0.45"/>')
    for i, f in enumerate(shape):
        if not isinstance(f, (int, float)) or f in (0,): continue
        r = f - base
        g.append(f'<circle cx="{x+i*16}" cy="{y+r*20+10}" r="6" fill="var(--fg)"/>')
    si, sf = root
    g.append(f'<circle cx="{x+si*16}" cy="{y+sf*20+10}" r="4.6" fill="none" stroke="var(--tonic)" stroke-width="2.2"/>')
    g.append(f'<text x="{x+40}" y="{y+88}" text-anchor="middle" class="ch" font-size="12.5">{title}</text>')
    g.append(f'<text x="{x+40}" y="{y+102}" text-anchor="middle" font-size="8.5" fill="var(--muted)">{ex1}</text>')
    g.append(f'<text x="{x+40}" y="{y+115}" text-anchor="middle" font-size="8.5" fill="var(--muted)">{ex2}</text>')
    g.append('</g>')
    return ''.join(g)

TAGS = ["tónika", "vedlejší", "rel. dur", "subdom.", "mol dom.", "subdom.", "vedlejší"]
NUMS = ["i · tónika", "III · rel. dur", "iv · subdom.", "v · mol dom.", "VI · subdom.", "VII · vedlejší"]
RCOL = {"i": 'var(--tonic)', "ii°": 'var(--muted)', "III": 'var(--vin)', "iv": 'var(--sub)',
        "v": 'var(--dom)', "V": 'var(--dom)', "VI": 'var(--sub)', "VII": 'var(--muted)'}
ROWS = [((("i", 0), ("VI", 5), ("III", 2), ("VII", 6)), "popová čtyřka, domov v molu"),
        ((("i", 0), ("iv", 3), ("V", 'C')), "harmonický tah (ostrá septima)"),
        ((("i", 0), ("VII", 6), ("VI", 5), ("V", 'M')), "andaluská sestupná"),
        ((("i", 0), ("VII", 6), ("VI", 5), ("v", 4)), "měkčí modalní varianta"),
        ((("i", 0), ("III", 2), ("VII", 6), ("VI", 5)), "rotace čtyřky")]
BLUESM = [0, 0, 0, 0, 3, 3, 0, 0, 'C', 3, 0, 'C']  # takt 9 = V7 (obrat), takt 12 = v (dech) — viz blues forma v molu; BLUEST v duru je [0,0,0,0,3,3,0,0,4,3,0,4]

def row_svg(y, roms, real, genre, x0=712):
    out = [f'<text x="{x0}" y="{y}" class="roman" font-size="16.5">']
    for idx, (rn, _) in enumerate(roms):
        if idx: out.append(' <tspan fill="var(--line)"> – </tspan>')
        out.append(f'<tspan fill="{RCOL[rn]}">{rn}</tspan>')
    out.append('</text>')
    out.append(f'<text x="{x0+296}" y="{y}" font-size="16" font-weight="600">{real}</text>')
    out.append(f'<text x="1458" y="{y}" text-anchor="end" font-size="10.5" fill="var(--muted)">{genre}</text>')
    return ''.join(out)

def page(sym, chords, v7n, v7s, tip, ki, is_first):
    nm = [c[0] for c in chords]
    parts = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--dom)"/></marker></defs>')
    parts.append(f'<text x="120" y="46" class="title" font-size="24">Harmonické postupy v {sym}-moll</text>')
    parts.append('<text x="120" y="66" class="subtitle" font-size="12.5">Kruh kvint · funkce akordů molu · osvědčené postupy · transpozice barré tvary</text>')

    parts.append(circle_svg(ki))
    parts.append(f'<text x="350" y="852" text-anchor="middle" font-size="10.5" fill="var(--muted)">Tvá molová tónina = chip uvnitř: v(dominanta) = soused po směru doprava, iv(subdom.) doleva,</text>')
    parts.append(f'<text x="350" y="868" text-anchor="middle" font-size="10.5" fill="var(--muted)">dur sourozenec (III) sedí nad tóninou ve vnějším kruhu. Tónina {sym}-moll je vyznačena barvami.</text>')

    parts.append('<rect x="688" y="88" width="782" height="404" rx="10" class="panel"/>')
    parts.append(f'<text x="712" y="122" class="ptitle" font-size="16">Diatonické akordy tóniny {sym}-moll</text>')
    parts.append('<text x="1458" y="122" text-anchor="end" font-size="9" fill="var(--muted)">funkce: <tspan fill="var(--tonic)" font-weight="700">i</tspan> · <tspan fill="var(--sub)" font-weight="700">iv/VI</tspan> · <tspan fill="var(--dom)" font-weight="700">v</tspan> · <tspan fill="var(--vin)" font-weight="700">III</tspan></text>')
    ROM7 = ["i", "ii°", "III", "iv", "v", "VI", "VII"]
    FILL7 = ['var(--tonicbg)', '#f4f2ec', 'var(--vinbg)', 'var(--subbg)', 'var(--dombg)', 'var(--subbg)', '#f4f2ec']
    for i in range(7):
        x = 712 + i*104
        parts.append(f'<rect x="{x}" y="140" width="96" height="40" rx="9" class="chip" style="fill:{FILL7[i]}"/>')
        parts.append(f'<text x="{x+48}" y="160" text-anchor="middle" class="label" font-size="12">{ROM7[i]} · {nm[i]}</text>')
        parts.append(f'<text x="{x+48}" y="173" text-anchor="middle" font-size="9" fill="var(--muted)">{TAGS[i]}</text>')
    for i in range(8):
        x = 702 + i*94
        y = 196
        if i == 0: parts.append(chordbox(x, y, nm[0], chords[0][1][0], 1, NUMS[0]))
        elif i == 1: parts.append(card(x, y, nm[1], "ii° · vynech", f"místo něj iv: {nm[3]}"))
        elif i == 2: parts.append(chordbox(x, y, nm[2], chords[2][1][0], chords[2][1][1], NUMS[1]))
        elif i == 3: parts.append(chordbox(x, y, nm[3], chords[3][1][0], chords[3][1][1], NUMS[2]))
        elif i == 4: parts.append(chordbox(x, y, nm[4], chords[4][1][0], chords[4][1][1], NUMS[3]))
        elif i == 5: parts.append(chordbox(x, y, nm[5], chords[5][1][0], chords[5][1][1], NUMS[4]))
        elif i == 6: parts.append(chordbox(x, y, nm[6], chords[6][1][0], chords[6][1][1], NUMS[5]))
        else: parts.append(card(x, y, v7n, "V7 tah (harmonický mol)", f"tvar: {v7s}"))
    parts.append('<text x="712" y="472" font-size="10.5" fill="var(--muted)">Značení: ○ = prázdná struna, ✕ = netrhaná, tečka = prst; číslo vlevo = pražec, od nějž schéma začíná (barré).</text>')

    parts.append('<rect x="688" y="512" width="782" height="356" rx="10" class="panel"/>')
    parts.append(f'<text x="712" y="546" class="ptitle" font-size="16">Osvědčené postupy <tspan font-weight="400" fill="var(--muted)" font-size="12">(v {sym}-moll)</tspan></text>')
    for j, (roms, genre) in enumerate(ROWS):
        real = ' – '.join(nm[ci] if isinstance(ci, int) else (v7n if ci == 'C' else v7n[:-1]) for _, ci in roms)
        parts.append(row_svg(592 + j*38, roms, real, genre))
    parts.append('<text x="712" y="790" class="label" font-size="12.5">Blues v molu, 12 taktů:</text>')
    for bi, cell in enumerate(BLUESM):
        bx = 912 + bi*44 + (6 if bi >= 4 else 0) + (6 if bi >= 8 else 0)
        cn = (nm[cell] + '7') if isinstance(cell, int) else v7n  # 0→i7, 3→iv7, 4→v7; 'C'/'M'→V7
        parts.append(f'<rect x="{bx}" y="776" width="40" height="24" rx="5" class="cell"/>')
        parts.append(f'<text x="{bx+20}" y="792" text-anchor="middle" font-size="10" fill="var(--fg)">{cn}</text>')

    parts.append('<rect x="42" y="880" width="1428" height="168" rx="10" class="panel"/>')
    if is_first:
        parts.append('<text x="66" y="912" class="ptitle" font-size="15">Transpozice na kytaře: barré tvar = jeden úchop, libovolná tónina</text>')
    else:
        parts.append('<text x="66" y="912" class="ptitle" font-size="15">Transpozice barré tvary <tspan fill="var(--muted)" font-size="11" font-weight="400">— tvary platí v každé tónině; tónina = pražec, na němž sedí tónika</tspan></text>')
    bx0 = 66
    for (t, sh, _bs, e1, e2) in BARR:
        parts.append(barrbox(bx0, 928, t, sh, 1, e1, e2, ROOTS[t]))
        bx0 += 232
    xcol = 1000
    if is_first:
        genlines = ["Jak se to čte: Barré = prst přes všechny struny", "na zvoleném pražci — tvar stejný, mění se jen pozice.", 'Zelený kroužek = kde „sedí tónika“ (název akordu).', "Postupy platí v KAŽDÉ molové tónině — posouváš dle kruhu:", "např. a–F–C–G (Am–F–C–G) → e-moll: Em–C–G–D."]
        for li, ln in enumerate(genlines):
            fw = '700' if li == 0 else '400'
            parts.append(f'<text x="{xcol}" y={934+li*15} font-size="10.5" fill="var(--fg)" font-weight="{fw}">{ln}</text>')
    else:
        parts.append(f'<text x="{xcol}" y="930" font-size="10.5" font-weight="700" fill="var(--tonic)">Nejsnazší cesta — tónina {sym}-moll:</text>')
        half = tip.find(' (')
        if 0 < half <= 56:
            parts.append(f'<text x="{xcol}" y="948" font-size="10.5" fill="var(--fg)">{tip[:half]}</text>')
            parts.append(f'<text x="{xcol}" y="963" font-size="10.5" fill="var(--fg)">{tip[(half+1):]}</text>')
        else:
            parts.append(f'<text x="{xcol}" y="948" font-size="10.5" fill="var(--fg)">{tip}</text>')
        parts.append('<text x="1000" y="984" font-size="10.5" fill="var(--muted)">Capo (kapodastr): posune tvary snadné tóniny')
        parts.append('<text x="1000" y="999" font-size="10.5" fill="var(--muted)">o N pražců nahoru — vznikne tónina této stránky.</text>')
    parts.append('<text x="1000" y="1014" font-size="10.5" fill="var(--muted)">Funkce: <tspan fill="var(--tonic)" font-weight="700">i tónika</tspan> · <tspan fill="var(--sub)" font-weight="700">iv/VI subdominanta</tspan> · <tspan fill="var(--dom)" font-weight="700">v dominanta</tspan></text>')
    parts.append('<text x="1000" y="1029" font-size="10.5" fill="var(--muted)"><tspan fill="var(--vin)" font-weight="700">III dur sourozenec</tspan> — mění se tóny, ne role akordů.</text>')
    parts.append('</svg></div>')
    return ''.join(parts)

CSS = '''<!doctype html><meta charset="utf-8"/><title>Harmonické postupy na kytaru — 12 molových tónin</title>
<style>
@page { size: A4 landscape; margin: 0; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: var(--bg); }
:root { --bg: #faf9f5; --fg: #172033; --muted: #5b6475; --line: #64748b; --neutral: #e8e4d8;
  --tonic: #2f6b4f; --sub: #8a6d3b; --dom: #b04a2f; --vin: #5b6478;
  --tonicbg: #d8ecdf; --subbg: #f0e6d2; --dombg: #f3ded5; --vinbg: #e2e6ea; }
body { font: 13px/1.35 "DejaVu Sans", system-ui, sans-serif; color: var(--fg); }
.page { width: 297mm; height: 210mm; page-break-after: always; background: var(--bg); }
.page:last-child { page-break-after: auto; }
svg { width: 100%; height: 100%; display: block; }
.chip { stroke: var(--line); stroke-width: 1; }
.cell { fill: #f4f2ec; stroke: var(--line); stroke-width: 0.8; }
.panel { fill: #ffffff; stroke: #d7d3c8; stroke-width: 1; }
.hedge { stroke: var(--dom); stroke-width: 2; fill: none; }
.roman { font-weight: 700; }
.label { font-weight: 700; fill: var(--fg); }
</style>'''

pages_html = [page(sym, ch, v7n, v7s, tip or "", ki, ki == 0) for ki, (sym, ch, v7n, v7s, tip) in enumerate(M)]
html = CSS + ''.join(pages_html)
open(OUT, 'w', encoding='utf-8').write(html)
print('WROTE', OUT, len(html), 'bytes,', len(M), 'pages')