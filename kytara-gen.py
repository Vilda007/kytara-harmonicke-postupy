#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generátor: Harmonické postupy na kytaru — 12 tónin -> multipage HTML (pro PDF)."""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postupy-vsechny-toniny.html')
X = '✕'; O = '○'

# hmatová schémata: (shape low->high 6 prvků, base_fret) ; 'x'=netrhaná, 'o'/'0' = prázdná
def S(*s, base=1): return (s, base)

K = []  # (symbol, [7x (jmeno, tvar, base)], capo_tip)
#  tónina   I        ii         iii        IV       V        vi         vii°
K.append(("C", [("C", S('x',3,2,0,1,0)), ("Dm", S('x','x',0,2,3,1)), ("Em", S(0,2,2,0,0,0)),
                ("F", S(1,3,3,2,1,1)), ("G", S(3,2,0,0,0,3)), ("Am", S('x',0,2,2,1,0)),
                ("Bdim", None)], None))
K.append(("G", [("G", S(3,2,0,0,0,3)), ("Am", S('x',0,2,2,1,0)), ("Bm", S('x',2,4,4,3,2, base=2)),
                ("C", S('x',3,2,0,1,0)), ("D", S('x','x',0,2,3,2)), ("Em", S(0,2,2,0,0,0)),
                ("F♯dim", None)], "capo 2 + tvary F-dur → G, Am, Bm, C, D, Em — všechny snadné."))
K.append(("D", [("D", S('x','x',0,2,3,2)), ("Em", S(0,2,2,0,0,0)), ("F♯m", S(2,4,4,2,2,2, base=2)),
                ("G", S(3,2,0,0,0,3)), ("A", S('x',0,2,2,2,0)), ("Bm", S('x',2,4,4,3,2, base=2)),
                ("C♯dim", None)], "capo 2 + tvary C-dur → D, Em, F♯m, G, A, Bm — snazší tvary."))
K.append(("A", [("A", S('x',0,2,2,2,0)), ("Bm", S('x',2,4,4,3,2, base=2)), ("C♯m", S('x',4,6,6,6,4, base=4)),
                ("D", S('x','x',0,2,3,2)), ("E", S(0,2,2,1,0,0)), ("F♯m", S(2,4,4,2,2,2, base=2)),
                ("G♯dim", None)], "capo 2 + tvary G-dur → A, Bm, C♯m, D, E, F♯m — snazší tvary."))
K.append(("E", [("E", S(0,2,2,1,0,0)), ("F♯m", S(2,4,4,2,2,2, base=2)), ("G♯m", S(4,6,6,4,4,4, base=4)),
                ("A", S('x',0,2,2,2,0)), ("B", S('x',2,4,4,3,2, base=2)), ("C♯m", S('x',4,6,6,6,4, base=4)),
                ("D♯dim", None)], "capo 2 + tvary D-dur → E, F♯m, G♯m, A, B, C♯m — méně barré."))
K.append(("B", [("B", S('x',2,4,4,3,2, base=2)), ("C♯m", S('x',4,6,6,6,4, base=4)), ("D♯m", S('x',6,8,8,7,6, base=6)),
                ("E", S(0,2,2,1,0,0)), ("F♯", S(2,4,4,3,2,2, base=2)), ("G♯m", S(4,6,6,4,4,4, base=4)),
                ("A♯dim", None)], "capo 2 + tvary A-dur → B, C♯m, D♯m, E, F♯, G♯m — snazší tvary."))
K.append(("F♯", [("F♯", S(2,4,4,3,2,2, base=2)), ("G♯m", S(4,6,6,4,4,4, base=4)), ("A♯m", S('x',1,3,3,2,1)),
                ("B", S('x',2,4,4,3,2, base=2)), ("C♯", S('x',4,6,6,6,4, base=4)), ("D♯m", S('x',6,8,8,7,6, base=6)),
                ("E♯dim", None)], "capo 2 + tvary E-dur → F♯, G♯m, A♯m, B, C♯, D♯m — snazší tvary."))
K.append(("D♭", [("D♭", S(9,11,11,10,9,9, base=9)), ("E♭m", S(6,8,8,6,6,6, base=6)), ("Fm", S(1,3,3,1,1,1)),
                ("G♭", S(2,4,4,3,2,2, base=2)), ("A♭", S(4,6,6,5,4,4, base=4)), ("B♭m", S('x',1,3,3,2,1)),
                ("Cdim", None)], "capo 1 + tvary C-dur → D♭, E♭m, Fm, G♭, A♭, B♭m — snazší tvary."))
K.append(("A♭", [("A♭", S(4,6,6,5,4,4, base=4)), ("B♭m", S('x',1,3,3,2,1)), ("Cm", S('x',3,5,5,4,3, base=3)),
                ("D♭", S(9,11,11,10,9,9, base=9)), ("E♭", S('x',6,8,8,8,6, base=6)), ("Fm", S(1,3,3,1,1,1)),
                ("Gdim", None)], "capo 1 + tvary G-dur → A♭, B♭m, Cm, D♭, E♭, Fm — snazší tvary."))
K.append(("E♭", [("E♭", S('x',6,8,8,8,6, base=6)), ("Fm", S(1,3,3,1,1,1)), ("Gm", S(3,5,5,3,3,3, base=3)),
                ("A♭", S('x',4,6,6,6,4, base=4)), ("B♭", S('x',1,3,3,3,1)), ("Cm", S('x',3,5,5,4,3, base=3)),
                ("Ddim", None)], "capo 3 + tvary C-dur → E♭, Fm, Gm, A♭, B♭, Cm — snazší tvary."))
K.append(("B♭", [("B♭", S('x',1,3,3,3,1)), ("Cm", S('x',3,5,5,4,3, base=3)), ("Dm", S('x','x',0,2,3,1)),
                ("E♭", S('x',6,8,8,8,6, base=6)), ("F", S(1,3,3,2,1,1)), ("Gm", S(3,5,5,3,3,3, base=3)),
                ("Adim", None)], "capo 1 + tvary A-dur → B♭, Cm, Dm, E♭, F, Gm — snazší tvary."))
K.append(("F", [("F", S(1,3,3,2,1,1)), ("Gm", S(3,5,5,3,3,3, base=3)), ("Am", S('x',0,2,2,1,0)),
                ("B♭", S('x',1,3,3,3,1)), ("C", S('x',3,2,0,1,0)), ("Dm", S('x','x',0,2,3,1)),
                ("Edim", None)], "F/Gm/B♭ barré + Am/C/D otevřené; jinak capo 5 + tvary C-dur → F, Gm, Am, B♭, C, Dm."))

ALT7 = {"C": ("B7", "x21202"), "G": ("F♯7", "242322"), "D": ("C♯7", "x46464"), "A": ("G♯7", "464544"),
        "E": ("D♯7", "x68686"), "B": ("A♯7", "x13131"), "F♯": ("E♯7 = F7", "131211"),
        "D♭": ("C7", "x32310"), "A♭": ("G7", "320001"), "E♭": ("D7", "xx0212"),
        "B♭": ("A7", "x02020"), "F": ("E7", "020100")}

MAJ = [("C", "Am"), ("G", "Em"), ("D", "Bm"), ("A", "F♯m"), ("E", "C♯m"), ("B", "G♯m"),
       ("F♯/G♭", "D♯m/E♭m"), ("D♭/C♯", "B♭m"), ("A♭/G♯", "Fm"), ("E♭", "Cm"), ("B♭", "Gm"), ("F", "Dm")]

POS = {  # pozice k=0..11 na kruhu (θ = -90 + 30k), cx,cy, rMaj,rMin
}
def pt(k, r, cx=350.0, cy=570.0):
    th = math.radians(-90 + 30*k)
    return cx + r*math.cos(th), cy + r*math.sin(th)

C, PAGE_W, PAGE_H = 350.0, 570.0, 0  # (unused PAGE_H)
CX, CY = 350.0, 570.0
R_RING, R_CHIP, R_MINOR_CHIP = 255.0, 218.0, 96.0
R_INNER = 132.0

def chip(x, y, w, h, label, fill, stroke='var(--line)', sw=1, fs=14, tcol='var(--fg)'):
    return (f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="{h/2}" '
            f'class="chip" style="fill:{fill};stroke:{stroke};stroke-width:{sw}"/>' +
            f'<text x="{x:.1f}" y="{y+fs*0.36:.1f}" text-anchor="middle" class="label" font-size="{fs}" fill="{tcol}">{label}</text>')

def circle_svg(ki):
    """Kruh kvint s hightlightem tóniny ki (I=tónika, V=(ki+1)%12, IV=(ki+11)%12, vi=vnitřní ki)."""
    kI, kV, kIV = ki, (ki+1) % 12, (ki-1) % 12
    out = [f'<path d="M {pt(kV,238)[0]:.1f} {pt(kV,238)[1]:.1f} A 238 238 0 0 0 {pt(kI,238)[0]:.1f} {pt(kI,238)[1]:.1f}" class="hedge" marker-end="url(#arr)"/>']
    tm = None
    kv_t, ki_t = -90+30*kV, -90+30*kI
    ti = ki_t if ki_t <= kv_t else ki_t - 360
    tm = (kv_t + ti)/2
    if tm is not None:
        lx, ly = pt(kI, 0)[0], pt(kI, 0)[1]
        ax = lx + 282*math.cos(math.radians(tm)); ay = ly + 282*math.sin(math.radians(tm))
        out.append(f'<text x="{ax:.1f}" y="{ay:.1f}" text-anchor="middle" font-size="10" fill="var(--dom)">dominantový tah (V→I)</text>')
    for k in range(12):
        x, y = pt(k, R_CHIP); mx, my = pt(k, 60)
        fill, stroke, sw = 'var(--neutral)', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--tonicbg)', 'var(--tonic)', 2
        elif k == kV: fill, stroke, sw = 'var(--dombg)', 'var(--dom)', 2
        elif k == kIV: fill, stroke, sw = 'var(--subbg)', 'var(--sub)', 2
        out.append(chip(x, y, 46 if len(MAJ[k]) == 1 else 62, 26, MAJ[k][0], fill, stroke, sw, 14 if len(MAJ[k]) == 1 else 10.5))
    for k in range(12):
        x, y = pt(k, R_MINOR_CHIP)
        fill, stroke, sw = '#ecf0f4', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--vinbg)', 'var(--vin)', 2
        lab = MAJ[k][1]
        w = 34 if len(lab) <= 3 else 46
        out.append(chip(x, y, w, 20, lab, fill, stroke, sw, 9.5 if len(lab) <= 3 else 8.5))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.0f" fill="none" stroke="#d7d3c8" stroke-width="1"/>' % (CX, CY, R_RING))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.0f" fill="none" stroke="#d7d3c8" stroke-width="1" stroke-dasharray="4 4" opacity="0.7"/>' % (CX, CY, R_INNER))
    return ''.join(out)

def chordbox(x, y, name, shape, base, numeral, fun):
    lines = ['<g>']
    if base == 1:  # matice
        lines.append(f'<line x1="{x}" y1="{y+10}" x2="{x+80}" y2="{y+10}" stroke="var(--fg)" stroke-width="2.6"/>')
    else:
        lines.append(f'<text x="{x-8}" y="{y+22}" font-size="9.5" fill="var(--muted)" text-anchor="end">{base}</text>')
    for i in range(6):
        lines.append(f'<line x1="{x+i*16}" y1="{y+10}" x2="{x+i*16}" y2="{y+90}" stroke="var(--line)" stroke-width="1"/>')
    for r in range(5):
        lines.append(f'<line x1="{x}" y1="{y+10+r*20}" x2="{x+80}" y2="{y+10+r*20}" stroke="#b6b2a6" stroke-width="0.8"/>')
    # značky nad oknem
    for i, f in enumerate(shape):
        sx = x + i*16
        if f == 'x': lines.append(f'<text x="{sx}" y="{y-2}" font-size="10" fill="#8a8074" text-anchor="middle">{X}</text>')
        elif f in ('o', 0): lines.append(f'<text x="{sx}" y="{y-2}" font-size="10" fill="var(--line)" text-anchor="middle">{O}</text>')
    # barre pokud ≥3 struny na base
    nb = sum(1 for f in shape if (f == base) or (base == 1 and f == 1))
    if nb >= 2:
        x1 = x + 0 if shape[0] != 'x' and isinstance(shape[0], (int, float)) else x + 14
        x2 = x + 80
        lines.append(f'<rect x="{x1-1}" y="{y+13}" width="{x2-x1+2}" height="14" rx="7" fill="var(--fg)" opacity="0.45"/>')
    for i, f in enumerate(shape):
        if f == 'x' or f in ('o', 0) or f == 'o': continue
        if not isinstance(f, int) and not isinstance(f, float): continue
        r = f - base
        cxp, cyp = x + i*16, y + 10 + r*20 + 10
        lines.append(f'<circle cx="{cxp}" cy="{cyp}" r="6.5" fill="var(--fg)"/>')
    lines.append(f'<text x="{x+40}" y="{y+112}" text-anchor="middle" class="ch" font-size="15">{name}</text>')
    lines.append(f'<text x="{x+40}" y="{y+127}" text-anchor="middle" font-size="9.5" fill="var(--muted)">{numeral}</text>')
    lines.append('</g>')
    return ''.join(lines)

def notecard(x, y, dimname, altname, altshape):
    return (f'<rect x="{x-6}" y="{y}" width="92" height="104" rx="8" fill="#f4f2ec" stroke="#b6b2a6" stroke-dasharray="4 4"/>'
            f'<text x="{x+40}" y="{y+24}" text-anchor="middle" class="ch" font-size="13">{dimname}</text>'
            f'<text x="{x+40}" y="{y+40}" text-anchor="middle" font-size="9" fill="var(--muted)">vii° · vynechat</text>'
            f'<text x="{x+40}" y="{y+60}" text-anchor="middle" font-size="9.5" fill="var(--fg)">tah nahradí:</text>'
            f'<text x="{x+40}" y="{y+76}" text-anchor="middle" class="ch" font-size="13">{altname}</text>'
            f'<text x="{x+40}" y="{y+92}" text-anchor="middle" font-size="9.5" fill="var(--muted)">{altshape}</text>')

BARR = [("E-dur tvar", S(0,2,2,1,0,0), 1, "F=1 · G=3 · A=5 · B=7 · C=8 · D=10", "tónika na 6. struně"),
        ("A-dur tvar", S('x',0,2,2,2,0), 1, "B=2 · C=3 · D=5 · E=7 · F=8", "tónika na 5. struně"),
        ("Em-mol tvar", S(0,2,2,0,0,0), 1, "F♯m=2 · Gm=3 · Am=5 · Bm=7 · Dm=10", "tónika na 6. struně"),
        ("Am-mol tvar", S('x',0,2,2,1,0), 1, "Bm=2 · Cm=3 · Dm=5 · Em=7 · Fm=8", "tónika na 5. struně")]

def barrbox(x, y, title, shape, base, ex1, ex2, root):
    """barré tvar: root = (string_index, fret_or_0) pro zelený kroužek"""
    g = [f'<g>']
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

FUN = [("I", "tónika", 'var(--tonic)', 'var(--tonicbg)'), ("ii", "subdom.", 'var(--muted)', '#f4f2ec'),
       ("iii", "mezikrok", 'var(--muted)', '#f4f2ec'), ("IV", "subdom.", 'var(--sub)', 'var(--subbg)'),
       ("V", "dominanta", 'var(--dom)', 'var(--dombg)'), ("vi", "rel. mol", 'var(--vin)', 'var(--vinbg)'),
       ("vii°", "vedlejší", 'var(--muted)', '#f4f2ec')]

ROMROWS = [(("I", 0), ("IV", 3), ("V", 4), "základ rocku a folku"),
           (("I", 0), ("V", 4), ("vi", 5), ("IV", 3), 'popová „čtyřka“'),
           (("vi", 5), ("IV", 3), ("I", 0), ("V", 4), "tutéž čtyřka, ale domov v molu"),
           (("I", 0), ("vi", 5), ("IV", 3), ("V", 4), "doo-wop 50. let"),
           (("ii", 1), ("V", 4), ("I", 0), "jazzový obrat")]
BLUEST = [("I", 0), ("I", 0), ("I", 0), ("I", 0), ("IV", 3), ("IV", 3),
          ("I", 0), ("I", 0), ("V", 4), ("IV", 3), ("I", 0), ("V", 4)]

FUNC_COLOR = {"I": 'var(--tonic)', "ii": 'var(--muted)', "iii": 'var(--muted)', "IV": 'var(--sub)',
              "V": 'var(--dom)', "vi": 'var(--vin)', "vii°": 'var(--muted)'}

def row_svg(y, roms, chords, genre, x0=702):
    out = [f'<text x="{x0}" y="{y}" class="roman" font-size="17">']
    for idx, (rn, ci) in enumerate(roms):
        col = FUNC_COLOR[rn]
        if idx: out.append(' <tspan fill="var(--line)"> – </tspan>')
        out.append(f'<tspan fill="{col}">{rn}</tspan>')
    out.append('</text>')
    out.append(f'<text x="{x0+300}" y="{y}" font-size="16.5" font-weight="600">' +
               ' – '.join(chords[ci] for _, ci in roms) + '</text>')
    out.append(f'<text x="1458" y="{y}" text-anchor="end" font-size="10.5" fill="var(--muted)">{genre}</text>')
    return ''.join(out)

def page(sym, chords, tip, ki, capo_note, is_first):
    parts = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--dom)"/></marker></defs>')
    parts.append(f'<text x="120" y="46" class="title" font-size="24">Harmonické postupy v {sym}-dur</text>')
    parts.append('<text x="120" y="66" class="subtitle" font-size="12.5">Kruh kvint · funkce akordů · osvědčené postupy · transpozice barré tvary</text>')

    # kruh kvint
    parts.append(circle_svg(ki))
    parts.append(f'<text x="350" y="852" text-anchor="middle" font-size="10.5" fill="var(--muted)">Tvá tónina = pozice na kruhu: V(dominanta) je soused doprava, IV(subdominanta) doleva,</text>')
    parts.append(f'<text x="350" y="868" text-anchor="middle" font-size="10.5" fill="var(--muted)">vi (relativní mol) najdeš ve vnitřním kruhu pod tónikou. Tónina {sym} je vyznačena barvami.</text>')

    # Panel A
    parts.append('<rect x="688" y="88" width="782" height="404" rx="10" class="panel"/>')
    parts.append(f'<text x="712" y="122" class="ptitle" font-size="16">Diatonické akordy tóniny {sym}-dur</text>')
    for i, (rn, fn, rcol, rfill) in enumerate(FUN):
        x = 702 + i*106
        nm = chords[i][0] if i < 6 else chords[6][0]
        parts.append(f'<rect x="{x}" y="140" width="98" height="40" rx="9" class="chip" fill="{rfill}"/>')
        parts.append(f'<text x="{x+49}" y="160" text-anchor="middle" class="label" font-size="12.5">{rn} · {nm}</text>')
        parts.append(f'<text x="{x+49}" y="173" text-anchor="middle" font-size="9" fill="var(--muted)">{fn}</text>')
    for i in range(7):
        x = 702 + i*106 + 8
        y = 196
        if i < 6:
            sh, bs = chords[i][1][0], chords[i][1][1]
            nm = chords[i][0]
            parts.append(chordbox(x, y, nm, sh, bs, f'{["I","ii","iii","IV","V","vi"][i]} · {FUN[i][1]}', FUN[i][1]))
        else:
            dn, en = ALT7[sym]
            parts.append(notecard(x, y, chords[6][0], dn, en))
    parts.append(f'<text x="712" y="472" font-size="10.5" fill="var(--muted)">Značení: {O} = prázdná struna, {X} = netrhaná, tečka = prst; číslo vlevo = pražec, od nějž schéma začíná (barré).</text>')

    # Panel B
    parts.append('<rect x="688" y="512" width="782" height="356" rx="10" class="panel"/>')
    parts.append('<text x="712" y="546" class="ptitle" font-size="16">Osvědčené postupy <tspan font-weight="400" fill="var(--muted)" font-size="12">(v {}-dur)</tspan></text>'.format(sym))
    for j, row in enumerate(ROMROWS):
        roms, genre = row[:-1], row[-1]
        parts.append(row_svg(596 + j*38, roms, [c[0] for c in chords], genre))
    parts.append('<text x="712" y="790" class="label" font-size="12.5">Blues, 12 taktů:</text>')
    for bi, (rn, ci) in enumerate(BLUEST):
        bx = 866 + bi*46 + (6 if bi >= 4 else 0) + (6 if bi >= 8 else 0)
        nm = chords[ci][0] + '7'
        parts.append(f'<rect x="{bx}" y="776" width="40" height="24" rx="5" class="cell"/>')
        parts.append(f'<text x="{bx+20}" y="792" text-anchor="middle" font-size="10" fill="var(--fg)">{nm}</text>')

    # patní pás
    parts.append('<rect x="42" y="880" width="1428" height="168" rx="10" class="panel"/>')
    if is_first:
        parts.append('<text x="66" y="912" class="ptitle" font-size="15">Transpozice na kytaře: barré tvar = jeden úchop, libovolná tónina</text>')
    else:
        parts.append(f'<text x="66" y="912" class="ptitle" font-size="15">Transpozice barré tvary <tspan fill="var(--muted)" font-size="11" font-weight="400">— tvary platí v každé tónině; tónina = pražec, na němž sedí tónika</tspan></text>')
    bx0 = 66
    for (t, sh, bs, e1, e2) in BARR:
        parts.append(barrbox(bx0, 928, t, sh[0], 1, e1, e2, ROOTS[t]))
        bx0 += 232
    xcol = 1000
    if is_first:
        gen = ["<text x='"+str(xcol)+"' y='930' font-size='10.5' fill='var(--fg)' font-weight='700'>Jak se to čte:</text>",
               "<text>…</text>"]
        genlines = ["Jak se to čte: Barré = prst přes všechny struny", "na zvoleném pražci — tvar stejný, mění se jen pozice.", 'Zelený kroužek = kde „sedí tónika“ (název akordu).', "Postupy platí v KAŽDÉ tónině — posouváš dle kruhu kvint:", "např. C–G–Am–F → G-dur: G–D–Em–C (posun o 7 pražců)."]
        for li, ln in enumerate(genlines):
            fw = '700' if li == 0 else '400'
            col = 'var(--fg)' if li else 'var(--fg)'
            parts.append(f'<text x="{xcol}" y={934+li*15} font-size="10.5" fill="var(--fg)" font-weight="{fw}">{ln}</text>')
    else:
        parts.append(f'<text x="{xcol}" y="930" font-size="10.5" font-weight="700" fill="var(--tonic)">Nejsnazší cesta — tónina {sym}:</text>')
        # zalomit capo tip na 2 řádky
        half = tip.find(' → ')
        if 0 < half <= 52:
            parts.append(f'<text x="{xcol}" y="948" font-size="10.5" fill="var(--fg)">{tip[:half]}</text>')
            parts.append(f'<text x="{xcol}" y="963" font-size="10.5" fill="var(--fg)">{tip[half+3:]}</text>')
        else:
            words = tip.split()
            l1 = words; l2 = []
            while sum(len(w)+1 for w in l2) < 30 and l1: l2.insert(0, l1.pop())
            parts.append(f'<text x="{xcol}" y="948" font-size="10.5" fill="var(--fg)">{" ".join(l1)}</text>')
            parts.append(f'<text x="{xcol}" y="963" font-size="10.5" fill="var(--fg)">{" ".join(l2)}</text>')
        parts.append(f'<text x="{xcol}" y="984" font-size="10.5" fill="var(--muted)">Capo = strunný pásek: posune tvary snadné tóniny</text>')
        parts.append(f'<text x="{xcol}" y="999" font-size="10.5" fill="var(--muted)">o N pražců nahoru — vznikne tónina této stránky.</text>')
    parts.append(f'<text x="{xcol}" y="1014" font-size="10.5" fill="var(--muted)">Funkce: <tspan fill="var(--tonic)" font-weight="700">I tónika</tspan> · <tspan fill="var(--sub)" font-weight="700">IV subdominanta</tspan> · <tspan fill="var(--dom)" font-weight="700">V dominanta</tspan> · <tspan fill="var(--vin)" font-weight="700">vi rel. mol</tspan></text>')
    parts.append(f'<text x="{xcol}" y="1029" font-size="10.5" fill="var(--muted)">Vztahy platí v každé dur tónině — mění se tóny, ne role akordů.</text>')
    parts.append('</svg></div>')
    return ''.join(parts)

ROOTS = {"E-dur tvar": (0, 0), "A-dur tvar": (1, 0), "Em-mol tvar": (0, 0), "Am-mol tvar": (1, 0)}

CSS = '''<!doctype html><meta charset="utf-8"/><title>Harmonické postupy na kytaru — 12 tónin</title>
<style>
@page { size: A4 landscape; margin: 0; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: var(--bg); }
:root { --bg: #faf9f5; --fg: #172033; --muted: #5b6475; --line: #64748b; --neutral: #e8e4d8;
  --tonic: #2f6b4f; --sub: #8a6d3b; --dom: #b04a2f; --vin: #5b6478;
  --tonicbg: #d8ecdf; --subbg: #f0e6d2; --dombg: #f3ded5; --vinbg: #e2e6ea; --vinbg2: #dce4ec; }
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

pages_html = []
for idx, (sym, chords, tip) in enumerate(K):
    kpos = ["C", "G", "D", "A", "E", "B", "F♯", "D♭", "A♭", "E♭", "B♭", "F"].index(sym)
    pages_html.append(page(sym, chords, tip or "", kpos, None, idx == 0))

html = CSS + ''.join(pages_html)
open(OUT, 'w', encoding='utf-8').write(html)
print('WROTE', OUT, len(html), 'bytes,', len(K), 'pages')