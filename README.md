# Guitar Chord Progression Charts / Harmonické postupy na kytaru

**EN (default)** — Harmonic (chord progression) cheat sheets for **12 major keys** and **12 minor keys**, plus a full 28-page book with music theory from zero. Built around the circle of fifths: every page shows the key highlighted on the circle (I = green, V = red, IV = orange, vi = blue; arrow = the V→I dominant move), the diatonic chords with guitar fingering, proven progressions transposed into that key (I–IV–V, pop four-chord, doo-wop, ii–V–I, 12-bar blues), and barre shapes with the starting fret marked.

### Downloads
- **Book EN** (default): [`harmonic-prog-guitar-book-en.pdf`](harmonic-prog-guitar-book-en.pdf) — 28 pages A4: cover + 3 pages of theory (semitones, chord building; function & circle of fifths incl. minor roles; practice: reading diagrams, barre, capo, transposition) + all 24 keys.
- Standalone sheets EN: 12 major keys [`harmonic-prog-guitar-all-keys-en.pdf`](harmonic-prog-guitar-all-keys-en.pdf) ([HTML](postupy-vsechny-toniny-en.html)) · 12 minor keys [`harmonic-prog-guitar-all-minor-keys-en.pdf`](harmonic-prog-guitar-all-minor-keys-en.pdf) ([HTML](postupy-vsechny-molove-toniny-en.html))
- Live page: <https://vilda007.github.io/kytara-harmonicke-postupy/>
- **Improvements & fixes welcome** — open an issue or PR: <https://github.com/Vilda007/kytara-harmonicke-postupy>
- Poster & preview: [`harmonic-prog-guitar.png`](harmonic-prog-guitar.png) · `diagram.html` (single-page C major poster)

### How it works
Each page: circle of fifths with the key highlighted → rule of thumb *V is one step right, IV one step left, vi sits under the tonic in the inner ring*; diatonic chords with fingering (barre start fret shown, vii° with a practical substitute V7); classic progressions + blues rewritten in that key; barre shapes (E, A, Em, Am) and the "easiest path" tip (capo + friendly keys).

Everything is **generated** — the Python generators hold the data tables and emit the HTML; PDFs are rendered headlessly. Edit a table, rerun, done.

### Interactive web app
The live page is a React app. Source lives in `src/app.jsx`; the built artifacts (`app.v1.js`, `app.v1.css`) are committed so GitHub Pages needs no CI:

```bash
npm install
npm run build   # esbuild bundle + Tailwind CSS -> app.v1.js, app.v1.css
```

Web data (`chords.json`, 24 keys + rhythm patterns) exports from the generators via `python3 export_data.py`.

---

## Česky

Diagramy harmonických (akordových) postupů pro **12 dur tónin** — C, G, D, A, E, B, F♯, D♭, A♭, E♭, B♭, F (pořadí dle kruhu kvint) — a doplňková sada **12 molových tónin** (stejná šablona, molové role: **i** zelená, **v** červená, **iv** okr, **III dur** modrá; karty **ii°** a **V7** harmonického molu).

**Kniha** (`harmonic-prog-guitar-book.pdf`, 28 str.) = obálka s obsahem + 3 str. teorie (tóny a polotóny, stavba akordu · funkce a kruh kvint včetně molových rolí · praxe: čtení schémat, barré, capo, transpozice) + obě sady. Anglické vydání: `harmonic-prog-guitar-book-en.pdf`.

Každá strana: kruh kvint se zvýrazněnou tóninou (šipka = dominantový tah V→I), diatonické akordy s hmaty (barré = počáteční pražec, vii° s náhradou), osvědčené postupy přepsané do tóniny, barré tvary + tip „Nejsnazší cesta" (capo).

### Soubory
| Soubor | Popis |
| --- | --- |
| `harmonic-prog-guitar-book-en.pdf` | **kniha EN — výchozí** (28 str., A4) |
| `harmonic-prog-guitar-book.pdf` | kniha CZ (28 str., A4) |
| `harmonic-prog-guitar-all-keys-en.pdf` / `-all-keys.pdf` | 12 dur tónin EN / CZ (A4) |
| `harmonic-prog-guitar-all-minor-keys-en.pdf` / `-all-minor-keys.pdf` | 12 molových tónin EN / CZ (A4) |
| `postupy-vsechny-toniny.html` (+ `-en`) | HTML zdroj DUR (CZ / EN) |
| `postupy-vsechny-molove-toniny.html` (+ `-en`) | HTML zdroj MOL (CZ / EN) |
| `harmonic-prog-guitar.png` | preview C-dur |
| `kytara-gen.py` / `kytara-gen-moll.py` | generátor DUR / MOL sady |
| `kytara-gen-book.py` / `kytara-gen-book-en.py` | generátor knihy CZ / EN |
| `gen-en-sheets.py` | EN listy z čerstvých CZ (sdílí překlady s EN knihou; gate = 0 CZ znaků) |
| `export_data.py` → `chords.json` | data pro interaktivní web (24 tónin + rytmické patterny) |
| `src/app.jsx` → `app.v1.js` + `app.v1.css` | interaktivní web (React, build: `npm install && npm run build`) |

**Chyby & vylepšení** — otevři issue nebo pošli PR: <https://github.com/Vilda007/kytara-harmonicke-postupy>

License: see `LICENSE`. Made by Klepeto 🦞 (agent) for Vilém Kužel.

### Regenerate

```bash
python3 kytara-gen.py && python3 kytara-gen-moll.py
python3 kytara-gen-book.py && python3 kytara-gen-book-en.py
python3 gen-en-sheets.py   # EN listy — VŽDY po CZ generátorech (čtou čerstvé CZ HTML)
python3 export_data.py     # chords.json pro web
npm run build      # app.v1.js + app.v1.css
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-book.pdf --no-pdf-header-footer harmonic-prog-guitar-book.html
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-book-en.pdf --no-pdf-header-footer harmonic-prog-guitar-book-en.html
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-all-keys.pdf --no-pdf-header-footer postupy-vsechny-toniny.html
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-all-keys-en.pdf --no-pdf-header-footer postupy-vsechny-toniny-en.html
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-all-minor-keys.pdf --no-pdf-header-footer postupy-vsechny-molove-toniny.html
chromium --headless --disable-gpu --no-sandbox --print-to-pdf=harmonic-prog-guitar-all-minor-keys-en.pdf --no-pdf-header-footer postupy-vsechny-molove-toniny-en.html
```

English | [Čeština](#česky)