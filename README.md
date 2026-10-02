# Harmonické postupy na kytaru

Diagramy harmonických (akordových) postupů pro **12 dur tónin** — C, G, D, A, E, B, F♯, D♭, A♭, E♭, B♭, F (pořadí dle kruhu kvint).

Doplňková sada **molových tónin** (a, e, b, f♯, c♯, g♯, d♯, b♭, f, c, g, d-moll) = stejná šablona, ale molové role: zvýrazněny **i** (zelená), **v** (červená), **iv** (okr) a **III dur sourozenec** (modrá na vnějším kruhu); dvě karty — **ii°** (vynechat, místo něj iv) a **V7 tah harmonického molu** (např. v a-moll E7 s ostrým G♯).

**Kniha** (`harmonic-prog-guitar-book.pdf`, 28 stránek) = obálka s obsahem + 3 stránky hudební teorie (strojnice: tóny a polotóny, stavba akordu · funkce a kruh kvint včetně molových rolí · praxe na hmatníku: čtení schémat, barré, capo, transpozice krok za krokem, molové triky) + obě sady (dur s. 5–16, mol s. 17–28). Čísla stránek na každé straně mimo obálku.

**Anglické vydání** (EN): `harmonic-prog-guitar-book-en.pdf` (28 stránek A4) — totéž v angličtině (obálka + teorie + 24 tónin, terminologie major/minor keys); generátor `kytara-gen-book-en.py` čte CZ knihu a přepisuje textové uzly do EN.

Každá strana (A4) obsahuje:
- **Kruh kvint** se zvýrazněnou tóninou — I = zelená, V = červená, IV = okr, vi = modrá; šipka = dominantový tah (V→I). Pravidlo: *V je soused doprava, IV doleva, vi ve vnitřním kruhu pod tónikou.*
- **Diatonické akordy** dané tóniny s hmatovými schématy — u barré je uveden **počáteční pražec**; vii° zvlášť s praktickou náhradou (dominantový septimový akord).
- **Osvědčené postupy** (I–IV–V, popová čtyřka, doo-wop, ii–V–I) + **blues 12 taktů** — vše přepsané do dané tóniny.
- **Barré tvary** (E-dur, A-dur, Em-mol, Am-mol) a tip **„Nejsnazší cesta"** (capo + tvary snadné tóniny).

## Soubory

| Soubor | Popis |
| --- | --- |
| `postupy-vsechny-toniny.html` | 12stránkový A4 dokument DUR — zdroj (otevři v prohlížeči / vytiskni) |
| `harmonic-prog-guitar-all-keys.pdf` | hotový PDF export DUR (A4, 12 stránek) |
| `postupy-vsechny-molove-toniny.html` | 12stránkový A4 dokument MOL — zdroj |
| `harmonic-prog-guitar-all-minor-keys.pdf` | hotový PDF export MOL (A4, 12 stránek) |
| `harmonic-prog-guitar-book.html` | KNIHA — obálka + teorie + obě sady (28 stránek, zdroj) |
| `harmonic-prog-guitar-book.pdf` | hotová kniha — jedno PDF (28 stránek A4) |
| `harmonic-prog-guitar.png` | PNG úvodní stránky (C-dur) |
| `diagram.html` | jednostránkový poster (C-dur) |
| `kytara-gen.py` | generátor DUR sady — datová tabulka tónin → HTML |
| `kytara-gen-moll.py` | generátor MOL sady — datová tabulka molů → HTML |
| `kytara-gen-book.py` | generátor KNIHY — čte obě sady a přidává obálku + teorii |
| `harmonic-prog-guitar-book-en.html` | EN KNIHA — zdroj (28 stránek; generuje `kytara-gen-book-en.py`) |
| `harmonic-prog-guitar-book-en.pdf` | hotová EN kniha — jedno PDF (28 stránek A4) |
| `kytara-gen-book-en.py` | generátor EN knihy — čte CZ knihu, přepisuje texty do EN |

## Jak upravit

1. **Přímo na GitHubu** (editace v prohlížeči): tlačítko **Edit (✏️)** u souboru → změň → commit.
2. **Lokálně přes generátor** — uprav datovou tabulku v `kytara-gen.py` (DUR), `kytara-gen-moll.py` (MOL) nebo teorii v `kytara-gen-book.py` a přegeneruj:
   - `python3 kytara-gen.py` → přegeneruje `postupy-vsechny-toniny.html` vedle skriptu
   - PDF: `chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=harmonic-prog-guitar-all-keys.pdf file://$PWD/postupy-vsechny-toniny.html`
   - PNG úvodní strany: `chromium --headless --no-sandbox --disable-gpu --force-device-scale-factor=2 --screenshot=harmonic-prog-guitar.png --window-size=1540,1195 file://$PWD/diagram.html`
3. Commit / pull request — merge do `main`.

Pozn.: číslo u barré tvaru = pražec, od nějž schéma začíná; ○ = prázdná struna, ✕ = netrhaná.

## Licence

MIT — viz LICENSE.
