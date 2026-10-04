# Guitar Chord Progression Charts / Harmonické postupy na kytaru

**EN (default)** — Harmonic (chord progression) cheat sheets for **12 major keys** and **12 minor keys**, plus a full 28-page book with music theory from zero. Built around the circle of fifths: every page shows the key highlighted on the circle (I = green, V = red, IV = orange, vi = blue; arrow = the V→I dominant move), the diatonic chords with guitar fingering, proven progressions transposed into that key (I–IV–V, pop four-chord, doo-wop, ii–V–I, 12-bar blues), and barre shapes with the starting fret marked.

### Downloads
- **Book EN** (default): [`harmonic-prog-guitar-book-en.pdf`](harmonic-prog-guitar-book-en.pdf) — 28 pages A4: cover + 3 pages of theory (semitones, chord building; function & circle of fifths incl. minor roles; practice: reading diagrams, barre, capo, transposition) + all 24 keys.
- Single-page cheat sheets: 12 major keys [`harmonic-prog-guitar-all-keys.pdf`](harmonic-prog-guitar-all-keys.pdf) · 12 minor keys [`harmonic-prog-guitar-all-minor-keys.pdf`](harmonic-prog-guitar-all-minor-keys.pdf)
- Poster & preview: [`harmonic-prog-guitar.png`](harmonic-prog-guitar.png) · `diagram.html` (single-page C major poster)

### How it works
Each page: circle of fifths with the key highlighted → rule of thumb *V is one step right, IV one step left, vi sits under the tonic in the inner ring*; diatonic chords with fingering (barre start fret shown, vii° with a practical substitute V7); classic progressions + blues rewritten in that key; barre shapes (E, A, Em, Am) and the "easiest path" tip (capo + friendly keys).

Everything is **generated** — the Python generators hold the data tables and emit the HTML; PDFs are rendered headlessly. Edit a table, rerun, done.

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
| `harmonic-prog-guitar-all-keys.pdf` | 12 dur tónin (A4) |
| `harmonic-prog-guitar-all-minor-keys.pdf` | 12 molových tónin (A4) |
| `harmonic-prog-guitar.png` | preview C-dur |
| `kytara-gen.py` / `kytara-gen-moll.py` | generátor DUR / MOL sady |
| `kytara-gen-book.py` / `kytara-gen-book-en.py` | generátor knihy CZ / EN |

License: see `LICENSE`. Made by Klepeto 🦞 (agent) for Vilém Kužel.