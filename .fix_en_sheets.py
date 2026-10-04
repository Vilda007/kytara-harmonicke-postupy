# -*- coding: utf-8 -*-
"""Jednorázová oprava EN listů: vymění chybné chordbox diagramy za opravené (z čerstvých CZ)
a přeloží 'tvar' -> 'shape'. EN chordboxy se od CZ liší jen textem popisku (numeral)."""
import re, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def git_read(fn):
    return subprocess.run(['git', 'show', 'HEAD:' + fn], capture_output=True).stdout.decode('utf-8')

def groups(s):
    return re.findall(r'<g>.*?</g>', s)

NUM = re.compile(r'(font-size="9\.5" fill="var\(--muted\)">)([^<]*)(</text>)')

for cz_fn, en_fn in [('postupy-vsechny-toniny.html', 'postupy-vsechny-toniny-en.html'),
                     ('postupy-vsechny-molove-toniny.html', 'postupy-vsechny-molove-toniny-en.html')]:
    old_cz, new_cz, old_en = git_read(cz_fn), open(cz_fn, encoding='utf-8').read(), git_read(en_fn)
    gc, gn, ge = groups(old_cz), groups(new_cz), groups(old_en)
    assert len(gc) == len(gn) == len(ge), f"{cz_fn}: {len(gc)}/{len(gn)}/{len(ge)}"
    n_fix = 0
    for i in range(len(gc)):
        if gc[i] == gn[i]:
            continue  # tato skupina se nezměnila
        # ověř: old_cz vs old_en se liší jen v numeralu
        a, b = NUM.sub(r'\1@NUM@\3', gc[i]), NUM.sub(r'\1@NUM@\3', ge[i])
        assert a == b, f"{cz_fn} grupa {i}: EN/CZ se liší víc než v popisku!"
        # nový EN = nový CZ s EN popiskem
        en_num = NUM.search(ge[i]).group(2)
        new_en = NUM.sub(lambda m: m.group(1) + en_num + m.group(3), gn[i], count=1)
        old_en = old_en.replace(ge[i], new_en, 1)
        n_fix += 1
    old_en = old_en.replace('Em minor tvar', 'Em minor shape').replace('Am minor tvar', 'Am minor shape')
    open(en_fn, 'w', encoding='utf-8').write(old_en)
    print(f"{en_fn}: vyměněno {n_fix} diagramů, tvar->shape, {len(old_en)} bytes")