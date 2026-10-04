#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generátor KNIHY: Harmonie na kytaru — teorie (3 str.) + 12 dur + 12 mol tónin -> multipage HTML."""
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'harmonic-prog-guitar-book.html')
X = '✕'; O = '○'
CX, CY = 350.0, 570.0

MAJ = [("C", "Am"), ("G", "Em"), ("D", "Bm"), ("A", "F♯m"), ("E", "C♯m"), ("B", "G♯m"),
       ("F♯/G♭", "D♯m/E♭m"), ("D♭/C♯", "B♭m"), ("A♭/G♯", "Fm"), ("E♭", "Cm"), ("B♭", "Gm"), ("F", "Dm")]

def pt(k, r):
    th = math.radians(-90 + 30*k)
    return CX + r*math.cos(th), CY + r*math.sin(th)

def chip(x, y, w, h, label, fill='var(--neutral)', stroke='var(--line)', sw=1, fs=14):
    return (f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="{h/2}" '
            f'class="chip" style="fill:{fill};stroke:{stroke};stroke-width:{sw}"/>' +
            f'<text x="{x:.1f}" y="{y+fs*0.36:.1f}" text-anchor="middle" class="label" font-size="{fs}" fill="var(--fg)">{label}</text>')

def txt(x, y, s, fs=12, w=400, fill='var(--fg)', anchor='start', bold=False):
    return (f'<text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" text-anchor="{anchor}"'
            + (' font-weight="700"' if bold else '') + f'>{s}</text>')

def panel(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="panel"/>'

def ptitle(x, y, s):
    return txt(x, y, s, 16, 700, 'var(--fg)', 'start', True)

def circle_dur(ki=0):
    """Kruh kvint, dur mód: I zeleně, V červeně (k+1), IV okrově (k-1), vi modře (vnitřní k)."""
    kI, kV, kIV = ki, (ki+1) % 12, (ki-1) % 12
    out = [f'<path d="M {pt(kV,238)[0]:.1f} {pt(kV,238)[1]:.1f} A 238 238 0 0 0 {pt(kI,238)[0]:.1f} {pt(kI,238)[1]:.1f}" class="hedge" marker-end="url(#arr)"/>']
    tm = None
    kv_t, ki_t = -90+30*kV, -90+30*kI
    if kI == 0 and kV == 1: tm = -75
    else:
        ti = ki_t if ki_t <= kv_t else ki_t - 360
        tm = (kv_t + ti)/2
    if tm is not None:
        ax = CX + 282*math.cos(math.radians(tm)); ay = CY + 282*math.sin(math.radians(tm))
        out.append(f'<text x="{ax:.1f}" y="{ay:.1f}" text-anchor="middle" font-size="10" fill="var(--dom)">dominantový tah (V→I)</text>')
    for k in range(12):
        x, y = pt(k, 218)
        fill, stroke, sw = 'var(--neutral)', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--tonicbg)', 'var(--tonic)', 2
        elif k == kV: fill, stroke, sw = 'var(--dombg)', 'var(--dom)', 2
        elif k == kIV: fill, stroke, sw = 'var(--subbg)', 'var(--sub)', 2
        out.append(chip(x, y, 46 if len(MAJ[k][0]) == 1 else 62, 26, MAJ[k][0], fill, stroke, sw, 14 if len(MAJ[k][0]) == 1 else 10.5))
    for k in range(12):
        x, y = pt(k, 96)
        fill, stroke, sw = '#ecf0f4', 'var(--line)', 1
        if k == kI: fill, stroke, sw = 'var(--vinbg)', 'var(--vin)', 2
        lab = MAJ[k][1]
        w = 34 if len(lab) <= 3 else 46
        out.append(chip(x, y, w, 20, lab, fill, stroke, sw, 9.5 if len(lab) <= 3 else 8.5))
    out.append(f'<circle cx="{CX}" cy="{CY}" r="255" fill="none" stroke="#d7d3c8" stroke-width="1"/>')
    out.append(f'<circle cx="{CX}" cy="{CY}" r="132" fill="none" stroke="#d7d3c8" stroke-width="1" stroke-dasharray="4 4" opacity="0.7"/>')
    return ''.join(out)

def cover_page():
    p = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    p.append(txt(120, 220, 'Harmonie na kytaru', 46, 800))
    p.append(txt(120, 275, 'Hudební teorie a akordové postupy pro kytaristy', 20, 400, 'var(--muted)'))
    p.append(txt(120, 310, 'Kruh kvint · funkce akordů · 12 dur + 12 mol tónin · hmatová schémata · barré a capo', 14, 400, 'var(--muted)'))
    p.append(panel(120, 350, 1260, 480))
    items = [
        ('1', 'Tóny, polotóny a stavba akordu', 'chromatická řada · dur a mol stupnice · terciích (s. 2)'),
        ('2', 'Funkce akordů a kruh kvint', 'I/IV/V/vi · kadence · proč kruh funguje (s. 3)'),
        ('3', 'Praxe na hmatníku', 'jak číst schémata · barré · capo · transpozice · molové triky (s. 4)'),
        ('4', 'Dur tóniny', 'C · G · D · A · E · B · F♯ · D♭ · A♭ · E♭ · B♭ · F (s. 5–16)'),
        ('5', 'Molové tóniny', 'a · e · b · f♯ · c♯ · g♯ · d♯ · b♭ · f · c · g · d-moll (s. 17–28)'),
    ]
    yy = 400
    for n, t, d in items:
        p.append(f'<rect x="150" y="{yy-22}" width="34" height="34" rx="8" class="chip" style="fill:var(--tonicbg);stroke:var(--tonic)"/>')
        p.append(f'<text x="167" y="{yy}" text-anchor="middle" class="label" font-size="15" fill="var(--tonic)">{n}</text>')
        p.append(txt(210, yy, t, 17, 600, 'var(--fg)', 'start', True))
        p.append(txt(560, yy, d, 13, 400, 'var(--muted)'))
        yy += 62
    p.append(txt(120, 900, 'Repozitář a editace: github.com/Vilda007/kytara-harmonicke-postupy — generátory kytara-gen.py (dur), kytara-gen-moll.py (mol), kytara-gen-book.py (kniha).', 11, 400, 'var(--muted)'))
    p.append(txt(120, 925, 'Licence MIT (LICENSE). Diagramy optimální pro tisk A4; barvy = funkční role akordů (zelená tónika, okr subdominanta, červená dominanta, modrá mol).', 11, 400, 'var(--muted)'))
    p.append('</svg></div>')
    return ''.join(p)

def theory1():
    """Tóny, polotóny, stupnice dur/mol + triady."""
    p = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    p.append(txt(120, 52, 'Tóny, polotóny a stavba akordu', 24, 800))
    # Panel 1: chromatická řada
    p.append(panel(60, 80, 1404, 300))
    p.append(ptitle(90, 118, 'Chromatická řada (12 tónů) a dur stupnice'))
    p.append(txt(1330, 118, 'dur = sedmi kroků, T = celý tón, S = polotón', 11.5, 400, 'var(--muted)', 'end'))
    tones = ['C', 'C♯/D♭', 'D', 'D♯/E♭', 'E', 'F', 'F♯/G♭', 'G', 'G♯/A♭', 'A', 'A♯/B♭', 'B']
    white = {0, 2, 4, 5, 7, 9, 11}
    for i, t in enumerate(tones):
        x = 92 + i*112
        f = 'var(--tonicbg)' if i in white else '#f4f2ec'
        st = 'var(--tonic)' if i in white else 'var(--line)'
        sw = 2 if i in white else 1
        w = 88 if len(t) <= 2 else 92
        p.append(chip(x, 190, w, 40, t, f, st, sw, 14 if len(t) == 1 else 10.5))
    seq = ['T', 'T', 'S', 'T', 'T', 'T', 'S']
    idxw = sorted(white)
    for j in range(7):
        a = idxw[j]; b = idxw[j+1] if j < 6 else 12
        x = 92 + (a if j < 6 else 11)*112 + 56
        lbl = seq[j] if j < 6 else 'S'
        p.append(f'<text x="{x:.0f}" y="252" text-anchor="middle" font-size="15" font-weight="700" fill="{("var(--dom)" if lbl == "S" else "var(--muted)")}">{lbl}</text>')
        p.append(txt(x, 274, 'celý' if lbl == 'T' else 'půl', 9, 400, 'var(--muted)', 'middle'))
    p.append(txt(92, 320, 'Dur stupnice = vzorec celý–celý–půl–celý–celý–celý–půl (od C: bílý klávesy). Oktáva = 12 polotónů = stejný tón výše.', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 342, 'Tónina = tytéž tóny přeložené kamkoliv (vzorec zachováš): G-dur = F♯ jako jediný posun, D-dur = F♯+C♯ atd.', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 364, 'Polotón na kytře = jeden pražec; celý tón = dva pražce. Zápis ♯/♭ = znamínko polotónu up/down.', 11.5, 400, 'var(--muted)'))
    # Panel 2: dur vs mol
    p.append(panel(60, 400, 1404, 300))
    p.append(ptitle(90, 438, 'Dur vs. mol — stejné tóny, jiný domov'))
    crow = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    arow = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    p.append(txt(92, 480, 'C-dur', 13, 700, 'var(--fg)', 'start', True))
    for i, t in enumerate(crow):
        f = 'var(--tonicbg)' if i == 0 else '#f4f2ec'
        p.append(chip(180 + i*112, 474, 64, 34, t, f, 'var(--line)', 2 if i == 0 else 1, 14))
    p.append(txt(92, 540, 'a-moll', 13, 700, 'var(--fg)', 'start', True))
    mpat = ['T', 'S', 'T', 'T', 'S', 'T', 'T']
    for i, t in enumerate(arow):
        f = 'var(--vinbg)' if i == 0 else '#f4f2ec'
        p.append(chip(180 + i*112, 534, 64, 34, t, f, ('var(--vin)' if i == 0 else 'var(--line)'), 2 if i == 0 else 1, 14))
        if i < 6:
            p.append(f'<text x="{180 + i*112 + 88}" y="560" text-anchor="middle" font-size="11" font-weight="700" fill="var(--muted)">{mpat[i+1]}</text>')
    p.append(txt(92, 606, 'a-moll = RELATIVNÍ MOL C-dur: tytéž sedm tónů, ale tonika = A. Molový vzorec: celý–půl–celý–celý–půl–celý–celý.', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 628, 'Zvukově: dur = otevřené/výrazné, mol = temnější; rozdíl není v tónech, ale v tom, kam se vrací domů.', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 678, 'Rovněž poznámka k pojmenování: česká tradice říká místo B = H (a B♭ = B). Diagramy v repu drží mezinárodní (B, B♭) — čti je takto.', 11, 400, '#b04a2f'))
    # Panel 3: triády
    p.append(panel(60, 720, 1404, 310))
    p.append(ptitle(90, 758, 'Stavba akordu: tři tóny po terciích'))
    tri = [('C = C·E·G', 'dur: velká tercie + malá (4+3 polotónů)', 'var(--tonic)', [('C', 0), ('E', 1), ('G', 2)]),
           ('Am = A·C·E', 'mol: malá tercie + velká (3+4)', 'var(--vin)', [('A', 0), ('C', 1), ('E', 2)]),
           ('Bdim = B·D·F', 'dim: malá + malá (3+3) — napjatý, dvojitě zm.', 'var(--muted)', [('B', 0), ('D', 1), ('F', 2)])]
    for i, (name, desc, col, notes) in enumerate(tri):
        x = 150 + i*380
        for j, (nn, lv) in enumerate(notes):
            y = 880 - lv*56
            p.append(f'<circle cx="{x}" cy="{y}" r="17" style="fill:{col};opacity:0.15"/>')
            p.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" class="label" font-size="13" fill="{col}">{nn}</text>')
            if lv < 2:
                p.append(f'<line x1="{x}" y1="{y-37}" x2="{x}" y2="{y-19}" stroke="var(--line)" stroke-width="1.4"/>')
                p.append(txt(x+9, y-24, '3', 9.5, 400, 'var(--muted)'))
        p.append(txt(x + 44, 822, name, 16, 600))
        p.append(txt(x + 44, 842, desc, 10.5, 400, 'var(--muted)'))
    p.append(txt(92, 1000, 'Septima = přidej další tercii (C7 = C·E·G·B♭) — na kytře běžné v blues (C7). Název akordu = jeho nejnižší tón (tonika triády).', 11.5, 400, 'var(--muted)'))
    p.append('</svg></div>')
    return ''.join(p)

def theory2():
    """Funkce akordů, kadence, kruh kvint, molové role."""
    p = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    p.append('<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="var(--dom)"/></marker></defs>')
    p.append(txt(120, 52, 'Funkce akordů a kruh kvint', 24, 800))
    p.append(circle_dur(0))
    p.append(txt(350, 852, 'Příklad C-dur: V (G) = soused doprava, IV (F) doleva,', 10.5, 400, 'var(--muted)', 'middle'))
    p.append(txt(350, 868, 'vi (Am) uvnitř pod tóninou — celý kruh platí stejně pro každou tóninu.', 10.5, 400, 'var(--muted)', 'middle'))
    # pravé panely
    p.append(panel(688, 88, 782, 320))
    p.append(ptitle(712, 122, 'Funkce = role akordů v tónině'))
    # tabulka funkcí
    for yy, (lab, role, desc, col) in enumerate([('I', 'tónika', 'domov, klid — píseň na něm stojí', 'var(--tonic)'),
                                                 ('IV', 'subdominanta', 'odjezd ven — otevírá, svěží nádech', 'var(--sub)'),
                                                 ('V', 'dominanta', 'napětí — táhne zpět k tónice (V→I)', 'var(--dom)'),
                                                 ('vi', 'relativní mol', 'druhý domov — zbarví píseň do molu', 'var(--vin)'),
                                                 ('ii·iii·vii°', 'vedlejší role', 'mosty, barvy, obraty', 'var(--muted)')]):
        y = 158 + yy*48
        p.append(chip(752, y-5, 104, 30, lab, 'var(--neutral)', 'var(--line)', 1, 12.5))
        p.append(txt(836, y+3, role, 12.5, 400, 'var(--fg)', 'start', True))
        p.append(txt(970, y+3, desc, 12.5, 400, 'var(--muted)'))
    # kadence
    p.append(panel(688, 428, 782, 200))
    p.append(ptitle(712, 462, 'Kadence — typické tahy (v C-dur)'))
    for yy, (roms, real, g, col) in enumerate([('V → I', 'G → C', 'pevné dokončení', 'var(--dom)'),
                                               ('IV → I', 'F → C', 'plagalické „Amen“', 'var(--sub)'),
                                               ('ii – V – I', 'Dm – G → C', 'jazzový obrat', 'var(--muted)')]):
        y = 502 + yy*40
        p.append(f'<text x="712" y="{y}" font-size="14.5" font-weight="700" fill="{col}">{roms}</text>')
        p.append(txt(930, y, real, 14.5, 600))
        p.append(txt(1458, y, g, 11, 400, 'var(--muted)', 'end'))
    # molové role
    p.append(panel(688, 648, 782, 320))
    p.append(ptitle(712, 682, 'Molové role (v a-moll)'))
    for yy, (rn, desc, col) in enumerate([('i tónika', 'domov (Am)', 'var(--tonic)'),
                                          ('iv + VI', 'subdominanta (Dm, F)', 'var(--sub)'),
                                          ('v mol dominanta', 'měkká: Em — přelévá se, netlačí', 'var(--dom)'),
                                          ('V7 ostrá dominanta', 'E7 = E-G♯-B-D: G♯ = zvednutá septima', 'var(--dom)'),
                                          ('III sourozenec', 'dur „úniková“ stránka (C)', 'var(--vin)')]):
        y = 718 + yy*44
        p.append(txt(712, y, rn, 13.5, 400, col, 'start', True))
        p.append(txt(1000, y, desc, 12.5, 400, 'var(--muted)'))
    p.append(txt(712, 942, 'HARMONICKÉ MOL = zvednutá septima (7. stupeň; a-moll: G→G♯) — dominanta z v (Em) na V7 (E7)', 12, 400, 'var(--fg)', 'start', True))
    p.append(txt(712, 960, 'a tah v→i pak slyšíš jako dur V→I. ii° (Bdim) na kytře vynech — prakticky ho zastoupí iv (Dm).', 12, 400, 'var(--muted)'))
    # proč kruh
    p.append(txt(92, 898, 'Proč kruh funguje: sousedé po směru = kvinta (7 polotónů), doleva kvarta (5).', 12.5, 400, 'var(--fg)', 'start', True))
    p.append(txt(92, 920, 'Každý krok doprava přidá jednu ♯, doleva odečte jednu ♭.', 12, 400, 'var(--muted)'))
    p.append(txt(92, 940, 'Křížky: F♯ C♯ G♯ D♯ A♯ E♯ B♯ · bémoly: B♭ E♭ A♭ D♭ G♭ C♭ F♭.', 12, 400, 'var(--muted)'))
    p.append(txt(92, 960, 'Kvintový kruh = „mapa vztahů“: V = chci domů, IV = rozhlédnout se, vi = smutek, III = útěk.', 12, 400, 'var(--muted)'))
    p.append('</svg></div>')
    return ''.join(p)

def theory3():
    """Praxe: hmatník, schémata, barré, capo, transpozice."""
    p = ['<div class="page"><svg viewBox="0 0 1500 1062" xmlns="http://www.w3.org/2000/svg">']
    p.append(txt(120, 52, 'Praxe na hmatníku — schémata, barré, capo a přenášení postupů', 24, 800))
    # P1: jak číst schéma
    p.append(panel(60, 80, 700, 420))
    p.append(ptitle(90, 118, 'Jak číst hmatová schémata'))
    # anatomie: jedno schéma C s popisky
    bx, by = 150, 160
    for i in range(6):
        p.append(f'<line x1="{bx+i*16}" y1="{by+10}" x2="{bx+i*16}" y2="{by+90}" stroke="var(--line)" stroke-width="1"/>')
    for r in range(5):
        p.append(f'<line x1="{bx}" y1="{by+10+r*20}" x2="{bx+80}" y2="{by+10+r*20}" stroke="#b6b2a6" stroke-width="0.8"/>')
    p.append(f'<line x1="{bx}" y1="{by+10}" x2="{bx+80}" y2="{by+10}" stroke="var(--fg)" stroke-width="2.6"/>')
    p.append(f'<text x="{bx}" y="{by-2}" font-size="10" fill="#8a8074" text-anchor="middle">✕</text><text x="{bx+48}" y="{by-2}" font-size="10" fill="var(--line)" text-anchor="middle">○</text><text x="{bx+64}" y="{by-2}" font-size="10" fill="var(--line)" text-anchor="middle">○</text>')
    p.append(f'<circle cx="{bx+16}" cy="{by+70}" r="6.5" fill="var(--fg)"/><circle cx="{bx+32}" cy="{by+50}" r="6.5" fill="var(--fg)"/><circle cx="{bx+64}" cy="{by+30}" r="6.5" fill="var(--fg)"/>')
    p.append(txt(bx+40, by+120, 'C', 16, 600, 'var(--fg)', 'middle', True))
    p.append(txt(330, by+24, 'tloušťka nahoře = pražec 0 (matka)', 11.5, 400, 'var(--muted)'))
    p.append(txt(330, by+48, '✕ = netrhat, ○ = prázdná struna', 11.5, 400, 'var(--muted)'))
    p.append(txt(330, by+72, 'tečka = prst; pořadí sloupců = struny', 11.5, 400, 'var(--muted)'))
    p.append(txt(330, by+96, 'E A D G B e  (zleva = nejnižší → nejvyšší)', 11.5, 400, 'var(--fg)', 'start', True))
    p.append(txt(330, by+132, 'u barré: číslo vlevo = pražec startu', 11.5, 400, 'var(--dom)'))
    p.append(txt(92, 352, 'Tóny na kytře: každý pražec = polotón. Otevřené struny: E(6.) A(5.) D(4.) G(3.) B(2.) e(1.)', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 376, 'Akord = 3–5 strun najednou; dušená struna (✕) jen ztlumí — nevadí, když zvučí zbývající.', 11.5, 400, 'var(--muted)'))
    p.append(txt(92, 400, 'Čeští kytaristi říkají „h“ místo „b“ — v diagramu zůstává mezinárodní (B, B♭).', 11, 400, '#b04a2f'))
    p.append(txt(92, 430, 'Ukazováčková barré = prst přes všechny struny → jeden tvar kdekoli na hmatníku.', 11.5, 400, 'var(--muted)'))
    # P2: barré + capo
    p.append(panel(780, 80, 684, 420))
    p.append(ptitle(806, 118, 'Barré tvary a capo'))
    for i, (t, sh, e1, e2) in enumerate([("E-dur", (0,2,2,1,0,0), "F=1·G=3·A=5·B=7·C=8·D=10", "tónika na 6. struně"),
                                          ("A-dur", ('x',0,2,2,2,0), "B=2·C=3·D=5·E=7·F=8", "tónika na 5. struně"),
                                          ("Em-mol", (0,2,2,0,0,0), "F♯m=2·Gm=3·Am=5·Bm=7", "tónika na 6. struně"),
                                          ("Am-mol", ('x',0,2,2,1,0), "Bm=2·Cm=3·Dm=5·Em=7", "tónika na 5. struně")]):
        cx = 856 + (i % 2)*300; cy = 150 + (i//2)*170
        for s in range(6):
            p.append(f'<line x1="{cx+s*14}" y1="{cy}" x2="{cx+s*14}" y2="{cy+56}" stroke="var(--line)" stroke-width="1" opacity="0.45"/>')
        for r in range(4):
            p.append(f'<line x1="{cx}" y1="{cy+r*18}" x2="{cx+70}" y2="{cy+r*18}" stroke="#b6b2a6" stroke-width="0.7" opacity="0.6"/>')
        for s, f in enumerate(sh):
            sx = cx + s*14
            if f == 'x': p.append(f'<text x="{sx}" y="{cy-3}" font-size="8.5" fill="#8a8074" text-anchor="middle">✕</text>')
            elif f in ('o', 0): p.append(f'<text x="{sx}" y="{cy-3}" font-size="8.5" fill="var(--line)" text-anchor="middle">○</text>')
            else: p.append(f'<circle cx="{sx}" cy="{cy+(f-1)*18+9}" r="5" fill="var(--fg)"/>')
        si, sf = [(0,0),(1,0),(0,0),(1,0)][i]
        p.append(f'<circle cx="{cx+si*14}" cy="{cy+sf*18+9}" r="4.4" fill="none" stroke="var(--tonic)" stroke-width="2"/>')
        p.append(txt(cx+35, cy+76, t, 12, 600, 'var(--fg)', 'middle', True))
        p.append(txt(cx+86, cy+76, e1, 8.5, 400, 'var(--muted)', 'start'))
        p.append(txt(cx+86, cy+92, e2, 8.5, 400, 'var(--muted)', 'start'))
    p.append(txt(806, 447, 'CAPO = strunný pásek: zkrátí všechny struny na pražci N → tvary snadné tóniny hrají o N polotónů výš.', 12, 400, 'var(--fg)', 'start', True))
    p.append(txt(806, 466, 'Snadné dur tvary: C · G · D · A · E — snadné mol tvary: a-moll · e-moll. Vše ostatní = tytéž tvary + capo.', 12, 400, 'var(--muted)'))
    p.append(txt(806, 484, 'Výběr: nejbližší snadná tónina = menší počet pražců barré (např. b♭-moll: capo 1 + tvary a-moll).', 12, 400, 'var(--muted)'))
    # P3: transpozice krok za krokem
    p.append(panel(60, 540, 1404, 500))
    p.append(ptitle(90, 578, 'Přenášet postup do libovolné tóniny — krok za krokem'))
    steps = [
        ('1', 'Vyber postup', 'např. popová čtyřka I–V–vi–IV'),
        ('2', 'Najdi tóniku na kruhu kvint', 'tvá cílová tónina (kdekoliv na kruhu)'),
        ('3', 'Přečti sousedství', 'V = doprava, IV = doleva, vi = chip uvnitř pod tóninou'),
        ('4', 'Přepiš akordy', 'stejné romány, nová jména'),
        ('5', 'Zvol tvary / capo', 'otevřené tvary snadné tóniny + capo, jinak barré'),
    ]
    for i, (n, t, d) in enumerate(steps):
        y = 618 + i*52
        p.append(f'<rect x="120" y="{y-20}" width="34" height="34" rx="8" class="chip" style="fill:var(--tonicbg);stroke:var(--tonic)"/>')
        p.append(f'<text x="137" y="{y+2}" text-anchor="middle" class="label" font-size="14" fill="var(--tonic)">{n}</text>')
        p.append(txt(178, y, t, 14, 600, 'var(--fg)', 'start', True))
        p.append(txt(420, y, d, 12.5, 400, 'var(--muted)'))
    p.append(txt(92, 892, 'Příklad: čtyřka I–V–vi–IV v E-dur (tónika C → E = posun o 4 polotóny): E – B – C♯m – A; snadno: capo 4 + tvary C-dur.', 12.5, 400, 'var(--fg)', 'start', True))
    p.append(txt(92, 920, 'Molové triky: ii° → nahraď iv · v → V7 (harmonický mol, ostrá septima) · andaluská sestupná i–VII–VI–V = molový stíh od domova dolů.', 12.5, 400, 'var(--muted)'))
    p.append(txt(92, 948, 'Blues (12 taktů): dur I: I×4–IV×2–I×2–V–IV–I–V · mol i: i×4–iv×2–i×2–V7–iv–i–V7 (V7 = ostrá septima).', 12.5, 400, 'var(--muted)'))
    p.append(txt(92, 976, 'Všechny postupy hraj pomalu, metronom 60; akordy měň na doby. Barvy v diagramu = funkční role → najdou se tvým okem rychle.', 12, 400, 'var(--muted)'))
    p.append('</svg></div>')
    return ''.join(p)

def read_pages(fn):
    src = open(os.path.join(BASE, fn), encoding='utf-8').read()
    parts = src.split('<div class="page">')
    return ['<div class="page">' + p for p in parts[1:]]

CSS = '''<!doctype html><meta charset="utf-8"/><title>Harmonie na kytaru — kniha (teorie + 24 tónin)</title>
<style>
@page { size: A4 landscape; margin: 0; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: var(--bg); }
:root { --bg: #faf9f5; --fg: #172033; --muted: #5b6475; --line: #64748b; --neutral: #e8e4d8;
  --tonic: #2f6b4f; --sub: #8a6d3b; --dom: #b04a2f; --vin: #5b6478;
  --tonicbg: #d8ecdf; --subbg: #f0e6d2; --dombg: #f3ded5; --vinbg: #e2e6ea; }
body { font: 13px/1.35 "DejaVu Sans", system-ui, sans-serif; color: var(--fg); }
.page { width: 297mm; height: 210mm; page-break-after: always; background: var(--bg); position: relative; }
.page:last-child { page-break-after: auto; }
svg { width: 100%; height: 100%; display: block; }
.chip { stroke: var(--line); stroke-width: 1; }
.cell { fill: #f4f2ec; stroke: var(--line); stroke-width: 0.8; }
.panel { fill: #ffffff; stroke: #d7d3c8; stroke-width: 1; }
.hedge { stroke: var(--dom); stroke-width: 2; fill: none; }
.roman { font-weight: 700; }
.label { font-weight: 700; fill: var(--fg); }
.pgno { position: absolute; bottom: 6px; right: 14px; font-size: 9.5px; color: #8a8074; }
</style>'''

dur = read_pages('postupy-vsechny-toniny.html')
mol = read_pages('postupy-vsechny-molove-toniny.html')
pages = [cover_page(), theory1(), theory2(), theory3()] + dur + mol
out_pages = []
for i, pg in enumerate(pages):
    n = '' if i == 0 else f'<span class="pgno">s. {i+1}</span>'
    out_pages.append(pg.replace('<div class="page">', '<div class="page">' + n, 1))
html = CSS + ''.join(out_pages)
open(OUT, 'w', encoding='utf-8').write(html)
print('WROTE', OUT, len(html), 'bytes,', len(pages), 'pages (4 + dur', len(dur), '+ mol', len(mol), ')')