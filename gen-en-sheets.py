#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the EN standalone sheets (postupy-vsechny-toniny-en.html, postupy-vsechny-molove-toniny-en.html)
from the freshly generated CZ sheets.

How it works: the committed EN sheets and their CZ twins share the same tag
skeleton and differ only in text segments. The CZ<->EN segment pairs are read
from the last committed version of both files (`git show HEAD:...`), then
applied as a replacement map onto the *fresh* CZ output of kytara-gen.py /
kytara-gen-moll.py. Because of that order, run the CZ generators first.

Run AFTER: python3 kytara-gen.py && python3 kytara-gen-moll.py
Run BEFORE: PDF rendering of the EN sheets.

Gate printed at the end:
- leftover Czech diacritics in the output (must be 0)
- a diff summary of changed text nodes vs the committed EN sheet (sanity check)
"""
import io, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))

TAG = re.compile(r'<[^>]+>')
DIAC = re.compile(r'[áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]')

def git_show(path):
    return subprocess.run(['git', '-C', BASE, 'show', 'HEAD:' + path],
                          capture_output=True, check=True).stdout.decode('utf-8')

def build_map(old_cz, old_en):
    """CZ text segment -> EN text segment, from the committed twin files."""
    sz, se = TAG.split(old_cz), TAG.split(old_en)
    if len(sz) != len(se):
        raise SystemExit(f'segment count mismatch: {len(sz)} vs {len(se)}')
    m = {}
    for a, b in zip(sz, se):
        if a != b and a.strip() and b.strip() and a not in m:
            m[a] = b
    return m

def translate(fn):
    cz_path = os.path.join(BASE, fn)
    en_path = cz_path.replace('.html', '-en.html')
    mp = build_map(git_show(fn), git_show(fn.replace('.html', '-en.html')))
    out = open(cz_path, encoding='utf-8').read()
    applied = 0
    for cz_seg in sorted(mp, key=len, reverse=True):
        if cz_seg in out:
            out = out.replace(cz_seg, mp[cz_seg])
            applied += 1
    # keep the committed EN title
    m = re.search(r'<title>[^<]*</title>', git_show(fn.replace('.html', '-en.html')))
    out = re.sub(r'<title>[^<]*</title>', m.group(0), out, count=1)
    open(en_path, 'w', encoding='utf-8').write(out)

    diac = DIAC.findall(TAG.sub(' ', out))
    head = git_show(fn.replace('.html', '-en.html'))
    ta = set(re.findall(r'>([^<>]{2,})<', head))
    tb = set(re.findall(r'>([^<>]{2,})<', out))
    print(f'{fn}: map={len(mp)} applied={applied} leftover-diacritics={len(diac)}')
    for d, c in {x: out.count(x) for x in set(diac)}.items():
        print(f'  DIAC {d!r} x{c}')
    for x in sorted(tb - ta)[:10]:
        print('  NEW:', x[:70])
    return len(diac)

if __name__ == '__main__':
    total = 0
    for fn in ('postupy-vsechny-toniny.html', 'postupy-vsechny-molove-toniny.html'):
        total += translate(fn)
    print('TOTAL LEFTOVER DIACRITICS:', total)
    sys.exit(1 if total else 0)