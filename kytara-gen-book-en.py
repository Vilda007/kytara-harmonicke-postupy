#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EN book — node-anchored: reads CZ book HTML, rewrites every Czech text node per rule list, verifies 0 Czech leftovers."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'harmonic-prog-guitar-book.html')
OUT = os.path.join(BASE, 'harmonic-prog-guitar-book-en.html')

# ---------- 1) jednoduché fráze (aplikují se na celý soubor, regex-safe přes re.escape) ----------
PHRASES = [
 # — run-4 doplněné chybějící EN fráze (footer, cover TOC, teorie str. 4, molové capo boxy, proven box) —
 ('Praxe na hmatníku — schémata, barré, capo a přenášení postupů',
  'Fretboard practice — diagrams, barre, capo and transposing progressions'),
 ('Praxe na hmatníku', 'Fretboard practice'),
 ('Přenášet postup do libovolné tóniny — krok za krokem',
  'Transposing a progression into any key — step by step'),
 ('Osvědčené postupy', 'Proven progressions'),
 ('a · e · b · f♯ · c♯ · g♯ · d♯ · b♭ · f · c · g · d-moll (s. 17–28)',
  'a · e · b · f♯ · c♯ · g♯ · d♯ · b♭ · f · c · g · d (p. 17–28)'),
 ('Repozitář a editace: github.com/Vilda007/kytara-harmonicke-postupy — generátory kytara-gen.py (dur), kytara-gen-moll.py (mol), kytara-gen-book.py (kniha).',
  'Repo and edits: github.com/Vilda007/kytara-harmonicke-postupy — generators kytara-gen.py (major), kytara-gen-moll.py (minor), kytara-gen-book.py (book), kytara-gen-book-en.py (EN book).'),
 ('Licence MIT (LICENSE). Diagramy optimální pro tisk A4; barvy = funkční role akordů (zelená tónika, okr subdominanta, červená dominanta, modrá mol).',
  'MIT licence (LICENSE). Diagrams optimized for A4 print; colors = chord functions (green tonic, ochre subdominant, red dominant, blue minor).'),
 ('CAPO = strunný pásek: zkrátí všechny struny na pražci N → tvary snadné tóniny hrají o N polotónů výš.',
  'CAPO = the clamp: it shortens all strings at fret N → easy-key shapes play N semitones up.'),
 ('Snadné dur tvary: C · G · D · A · E — snadné mol tvary: a-moll · e-moll. Vše ostatní = tytéž tvary + capo.',
  'Easy major shapes: C · G · D · A · E — easy minor shapes: Am · Em. Everything else = the same shapes + a capo.'),
 ('Výběr: nejbližší snadná tónina = menší počet pražců barré (např. b♭-moll: capo 1 + tvary a-moll).',
  'Choosing: the nearest easy key = fewer barre frets (e.g. B♭ minor: capo 1 + A-minor shapes).'),
 ('Capo = strunný pásek: posune tvary snadné tóniny',
  'Capo = the clamp: it shifts the easy-key shapes'),
 ('o N pražců nahoru — vznikne tónina této stránky.',
  "up by N frets — you land in this page's key."),
 ('F/Gm/B♭ barré + Am/C/D otevřené; jinak capo 5 + tvary',
  'F/Gm/B♭ barre, Am/C/D open; otherwise capo 5 + shapes'),
 ('v mol dominanta', 'v minor dominant'),
 ('mosty, barvy, obraty', 'bridges, colors, turnarounds'),
 ('funkce: <tspan', 'Functions: <tspan'),
 ('Em-mol', 'Em minor'),
 ('Am-mol', 'Am minor'),
 ('Značení: ○ = prázdná struna, ✕ = netrhaná, tečka = prst; číslo vlevo = pražec, od nějž schéma začíná (barré).',
  "Notation: ○ = open string, ✕ = don't pluck, dot = a fingertip; the left number = the fret where a barre shape starts."),
 ('Tóny, polotóny a stavba akordu', 'Tones, semitones & chord building'),
 ('chromatická řada · dur a mol stupnice · terciích (s. 2)', 'the chromatic scale · major & minor scales · stacked thirds (p. 2)'),
 ('I/IV/V/vi · kadence · proč kruh funguje (s. 3)', 'I/IV/V/vi · cadences · why the circle works (p. 3)'),
 ('jak číst schémata · barré · capo · transpozice · molové triky (s. 4)', 'reading diagrams · barre & capo · transposing · minor tricks (p. 4)'),
 ('(s. 5–16)', '(p. 5–16)'),
 ('Kruh kvint · funkce akordů · 12 dur + 12 mol tónin · hmatová schémata · barré a capo',
  'Circle of fifths · chord functions · 12 major + 12 minor keys · chord diagrams · barre & capo'),
 ('Kruh kvint · funkce akordů molu · osvědčené postupy · transpozice barré tvary',
  'Circle of fifths · minor-key chord functions · proven progressions · barre transposition'),
 ('Kruh kvint · funkce akordů · osvědčené postupy · transpozice barré tvary',
  'Circle of fifths · chord functions · proven progressions · barre transposition'),
 ('Harmonie na kytaru — kniha (teorie + 24 tónin)', 'Guitar Harmony — the book (theory + 24 keys)'),
 ('Harmonie na kytaru', 'Guitar Harmony'),
 ('Hudební teorie a akordové postupy pro kytaristy', 'Music theory and chord progressions for guitarists'),
 ('Molové triky: ii° → nahraď iv · v → V7 (harmonický mol, ostrá septima) · andaluská sestupná i–VII–VI–V = molový stíh od domova dolů.',
  'Minor-key tricks: ii° → replace with iv · v → V7 (harmonic minor, raised 7th) · the Andalusian cadence i–VII–VI–V = a minor descent from home.'),
 ('Blues (12 taktů): dur I: I×4–IV×2–I×2–V–IV–I–V · mol i: i×4–iv×2–i×2–V7–iv–i–V7 (V7 = ostrá septima).',
  'Blues (12 bars): major: I×4–IV×2–I×2–V–IV–I–V · minor: i×4–iv×2–i×2–V7–iv–i–V7 (V7 = the raised 7th).'),
 ('Všechny postupy hraj pomalu, metronom 60; akordy měň na doby. Barvy v diagramu = funkční role → najdou se tvým okem rychle.',
  'Play the progressions slowly at 60 BPM and change chords on the beat. Colours in the diagrams = chord functions → your eyes find them fast.'),
 ('Příklad: čtyřka I–V–vi–IV v E-dur (tónika C → E = posun o 4 polotóny): E – B – C♯m – A; snadno: capo 4 + tvary C-dur.',
  'Example: the four-chord I–V–vi–IV in E major (C → E = shifted 4 semitones): E – B – C♯m – A; the easy route: capo 4 + C-major shapes.'),
 ('Dur stupnice = vzorec celý–celý–půl–celý–celý–celý–půl (od C: bílý klávesy). Oktáva = 12 polotónů = stejný tón výše.',
  'The major scale = whole–whole–half–whole–whole–whole–half (from C: the white piano keys). An octave = 12 semitones = the same tone up.'),
 ('Tónina = tytéž tóny přeložené kamkoliv (vzorec zachováš): G-dur = F♯ jako jediný posun, D-dur = F♯+C♯ atd.',
  'A key = the same tones transposed anywhere (the pattern holds): G major = one sharp (F♯) only, D major = F♯+C♯, etc.'),
 ('Polotón na kytře = jeden pražec; celý tón = dva pražce. Zápis ♯/♭ = znamínko polotónu up/down.',
  'On the guitar a semitone = one fret; a whole step = two frets. The ♯/♭ signs shift a tone by a half step.'),
 ('a-moll = RELATIVNÍ MOL C-dur: tytéž sedm tónů, ale tonika = A. Molový vzorec: celý–půl–celý–celý–půl–celý–celý.',
  'A minor = the RELATIVE MINOR of C major: the same seven tones, but tonic = A. The minor pattern: whole–half–whole–whole–half–whole–whole.'),
 ('Zvukově: dur = otevřené/výrazné, mol = temnější; rozdíl není v tónech, ale v tom, kam se vrací domů.',
  'In sound: major = bright/open, minor = darker; the difference is not the tones but where the song calls home.'),
 ('Rovněž poznámka k pojmenování: česká tradice říká místo B = H (a B♭ = B). Diagramy v repu drží mezinárodní (B, B♭) — čti je takto.',
  'A note on names: Czech tradition says H where we say B natural (B♭ = their B). The repo diagrams keep international names (B, B♭).'),
 ('Chromatická řada (12 tónů) a dur stupnice', 'The chromatic scale (12 tones) and the major scale'),
 ('dur = sedmi kroků, T = celý tón, S = polotón', 'major scale = 7 steps, W = whole step, H = half step'),
 ('Dur vs. mol — stejné tóny, jiný domov', 'Major vs. minor — same tones, different home'),
 ('Stavba akordu: tři tóny po terciích', 'Chord construction: three tones stacked in thirds'),
 ('dur: velká tercie + malá (4+3 polotónů)', 'major: a major third + a minor one (4+3 semitones)'),
 ('mol: malá tercie + velká (3+4)', 'minor: a minor third + a major one (3+4)'),
 ('dim: malá + malá (3+3) — napjatý, dvojitě zm.', 'dim: two minor thirds (3+3) — tense, doubly flat'),
 ('Septima = přidej další tercií (C7 = C·E·G·B♭) — na kytře běžné v blues (C7). Název akordu = jeho nejnižší tón (tonika triády).',
  'A seventh = add one more third (C7 = C·E·G·B♭) — very common in blues. A chord is named after its lowest tone (its root).'),
 ('Funkce akordů a kruh kvint', 'Chord functions & the circle'),
 ('Funkce = role akordů v tónině', 'Functions = chord roles inside a key'),
 ('domov, klid — píseň na něm stojí', 'home, rest — the song rests on it'),
 ('odjezd ven — otevírá, svěží nádech', 'moving away — opens up, a fresh breath'),
 ('napětí — táhne zpět k tónice (V→I)', 'tension — pulls back to the tonic (V→I)'),
 ('druhý domov — zbarví píseň do molu', 'a second home — colours the song minor'),
 ('vedlejší role', 'a side role'),
 ('Kadence — typické tahy (v C-dur)', 'Cadences — typical pulls (in C major)'),
 ('pevné dokončení', 'the firm resolution'),
 ('plagalické „Amen“', 'the plagal "Amen"'),
 ('Molové role (v a-moll)', 'Minor roles (in A minor)'),
 ('domov (Am)', 'the home (Am)'),
 ('subdominanta (Dm, F)', 'the subdominant (Dm, F)'),
 ('měkká: Em — přelévá se, netlačí', 'soft: Em — it glides, no push'),
 ('V7 ostrá dominanta', 'V7, the sharp dominant'),
 ('III sourozenec', 'III, the major sibling'),
 ('dur „úniková“ stránka (C)', 'the "escape door" (C)'),
 ('HARMONICKÉ MOL = zvednutá septima (7. stupeň; a-moll: G→G♯) — dominanta z v (Em) na V7 (E7)',
  'HARMONIC MINOR = a raised 7th (the 7th degree; A minor: G→G♯) — the dominant rises from v (Em) to V7 (E7)'),
 ('a tah v→i pak slyšíš jako dur V→I. ii° (Bdim) na kytře vynech — prakticky ho zastoupí iv (Dm).',
  'and the v→i pull then sounds like a major V→I. Skip ii° (Bdim) on guitar — iv (Dm) fills in fine.'),
 ('Proč kruh funguje: sousedé po směru = kvinta (7 polotónů), doleva kvarta (5).',
  'Why the circle works: clockwise = a fifth (7), counterclockwise = a fourth (5).'),
 ('Každý krok doprava přidá jednu ♯, doleva odečte jednu ♭.', 'Each clockwise step adds one ♯, counterclockwise drops one ♭.'),
 ('Křížky: F♯ C♯ G♯ D♯ A♯ E♯ B♯ · bémoly: B♭ E♭ A♭ D♭ G♭ C♭ F♭.', 'Sharps: F♯ C♯ G♯ D♯ A♯ E♯ B♯ · flats: B♭ E♭ A♭ D♭ G♭ C♭ F♭.'),
 ('Kvintový kruh = „mapa vztahů“: V = chci domů, IV = rozhlédnout se, vi = smutek, III = útěk.',
  'Circle of fifths = a map of relations: V = home, IV = look around, vi = sadness, III = escape.'),
 ('Příklad C-dur: V (G) = soused doprava, IV (F) doleva,', 'The C major example: V (G) = the clockwise neighbour, IV (F) on the left,'),
 ('vi (Am) uvnitř pod tóninou — celý kruh platí stejně pro každou tóninu.', 'vi (Am) inside the ring — the whole circle works identically for every key.'),
 ('Tvá tónina = pozice na kruhu: V(dominanta) je soused doprava, IV(subdominanta) doleva,',
  'Your key = a position on the circle: V (dominant) = the clockwise neighbour, IV (subdominant) on the left,'),
 ('Tvá molová tónina = chip uvnitř: v(dominanta) = soused po směru doprava, iv(subdom.) doleva,',
  'Your minor key = the inner chip: v (dominant) = the clockwise neighbour, iv (subdominant) on the left,'),
 ('dur sourozenec (III) sedí nad tóninou ve vnějším kruhu. ', 'the major sibling (III) sits above the tonic in the outer ring; '),
 ('Transpozice na kytaře: barré tvar = jeden úchop, libovolná tónina', 'Transposing on the guitar: one barre shape, any key'),
 ('Transpozice barré tvary', 'Barre transposition'),
 ('Jak se to čte: Barré = prst přes všechny struny', 'How to read it: a barre = one finger across all strings,'),
 ('na zvoleném pražci — tvar stejný, mění se jen pozice.', 'at the chosen fret — the shape stays, only the position changes.'),
 ('Zelený kroužek = kde „sedí tónika“ (název akordu).', "The green ring marks where the tonic sits (the chord's name)."),
 ('Postupy platí v KAŽDÉ tónině — posouváš dle kruhu kvint:', 'Progressions work in ANY key — you shift them along the circle of fifths:'),
 ('Postupy platí v KAŽDÉ molové tónině — posouváš dle kruhu:', 'Progressions work in EVERY minor key — you shift them along the circle:'),
 ('např. C–G–Am–F → G-dur: G–D–Em–C (posun o 7 pražců).', 'e.g. C–G–Am–F → G major: G–D–Em–C (a 7-fret shift).'),
 ('např. a–F–C–G (Am–F–C–G) → e-moll: Em–C–G–D.', 'e.g. a–F–C–G (Am–F–C–G) → E minor: Em–C–G–D.'),
 ('např. popová čtyřka I–V–vi–IV', 'e.g. the pop four-chord I–V–vi–IV'),
 ('tvá cílová tónina (kdekoliv na kruhu)', 'your target key (anywhere on the circle)'),
 ('V = doprava, IV = doleva, vi = chip uvnitř pod tóninou', 'V = clockwise, IV = counterclockwise, vi = the inner chip below the tonic'),
 ('stejné romány, nová jména', 'the same romans, new names'),
 ('otevřené tvary snadné tóniny + capo, jinak barré', 'easy-key open shapes + a capo, or a barre'),
 ('Vyber postup', 'Pick a progression'),
 ('Najdi tóniku na kruhu kvint', 'Find the tonic on the circle'),
 ('Přečti sousedství', 'Read the neighbourhood'),
 ('Přepiš akordy', 'Rewrite the chords'),
 ('Zvol tvary / capo', 'Pick shapes or a capo'),
 ('E7 = E-G♯-B-D: G♯ = zvednutá septima', 'E7 = E-G♯-B-D: G♯ = the raised 7th'),
 ('Ukazováčková barré = prst přes všechny struny → jeden tvar kdekoli na hmatníku.',
  'A barre = one finger across all strings → one shape anywhere on the neck.'),
 ('Čeští kytaristi říkají „h“ místo „b“ — v diagramu zůstává mezinárodní (B, B♭).',
  'The diagrams keep international names (B, B♭); Czech players often say H for B natural.'),
 ('Tóny na kytře: každý pražec = polotón. Otevřené struny: E(6.) A(5.) D(4.) G(3.) B(2.) e(1.)',
  'Notes on the guitar: every fret = a semitone. Open strings: E(6th) A(5th) D(4th) G(3rd) B(2nd) e(1st).'),
 ('Akord = 3–5 strun najednou; dušená struna (✕) jen ztlumí — nevadí, když zvučí zbývající.',
  'A chord = 3–5 strings at once; a muted string (✕) just stays dead — the rest ringing is fine.'),
 ('tloušťka nahoře = pražec 0 (matka)', 'the thick top line = fret 0 (the nut)'),
 ('✕ = netrhat, ○ = prázdná struna', "✕ = don't pluck, ○ = open string"),
 ('tečka = prst; pořadí sloupců = struny', 'a dot = a fingertip; the columns = strings'),
 ('E A D G B e  (zleva = nejnižší → nejvyšší)', 'E A D G B e  (left = lowest → highest)'),
 ('u barré: číslo vlevo = pražec startu', 'on barres: the left number = the starting fret'),
 ('Funkce: <tspan', 'Functions: <tspan'),
 ('III dur sourozenec', 'III the major sibling'),
 ('Vztahy platí v každé dur tónině — mění se tóny, ne role akordů.', 'The relations hold in every major key — the notes change, not the roles.'),
 ('— mění se tóny, ne role akordů.', '— the notes change, not the roles.'),
 ('Jak číst hmatová schémata', 'How to read the chord diagrams'),
 ('Barré tvary a capo', 'Barre shapes and the capo'),
 ('Blues, 12 taktů:', 'Blues, 12 bars:'),
 ('Blues v molu, 12 taktů:', 'Blues in minor, 12 bars:'),
 ('základ rocku a folku', 'the staple of rock and folk'),
 ('popová „čtyřka“', 'the pop "four-chord"'),
 ('tutéž čtyřka, ale domov v molu', 'the same four chords, but home in the minor'),
 ('doo-wop 50. let', 'do-wop, the 1950s'),
 ('harmonický tah (ostrá septima)', 'the harmonic pull (raised 7th)'),
 ('popová čtyřka, domov v molu', 'the pop four-chord, home in the minor'),
 ('měkčí modalní varianta', 'the softer modal variant'),
 ('andaluská sestupná', 'the Andalusian cadence'),
 ('rotace čtyřky', 'the four-chord rotation'),
 ('tah nahradí:', 'pull substitute:'),
 ('vii° · vynechat', 'vii° · skip it'),
 ('ii° · vynech', 'ii° · skip it'),
 ('místo něj iv: ', 'take iv instead: '),
 ('V7 tah (harmonický mol)', 'the V7 pull (harmonic minor)'),
 ('tvar: ', 'shape: '),
 ('E-dur tvar', 'E major shape'),
 ('A-dur tvar', 'A major shape'),
 ('Em-mol tvar', 'Em minor shape'),
 ('Am-mol tvar', 'Am minor shape'),
 ('tónika na 6. struně', 'tonic on string 6'),
 ('tónika na 5. struně', 'tonic on string 5'),
 ('rel. mol', 'rel. minor'),
 ('rel. dur', 'rel. major'),
 ('III · rel. dur', 'III · rel. major'),
 ('v · mol dom.', 'v · minor dom.'),
 ('mol dom.', 'minor dom.'),
 ('mezikrok', 'linking'),
 ('I · tónika', 'I · tonic'),
 ('i · tónika', 'i · tonic'),
 ('I tónika', 'I tonic'),
 ('i tónika', 'i tonic'),
 ('V · dominanta', 'V · dominant'),
 ('v dominanta', 'v dominant'),
 ('V dominanta', 'V dominant'),
 ('relativní mol', 'relative minor'),
 ('subdominanta', 'subdominant'),
 ('dominanta', 'dominant'),
 ('vedlejší', 'side'),
 ('tónika', 'tonic'),
 ('— snazší tvary.', '— easier shapes.'),
 ('— všechny snadné.', '— all easy.'),
 ('— méně barré.', '— fewer barres.'),
 ('Vše otevřené krom Bm', 'All open shapes except Bm'),
 ('(barré 2) — jinak capo 2 + tvary a-moll', '(barre at fret 2) — otherwise capo 2 + A-minor shapes'),
 ('Bez capo — Dm/F/G/Am/B♭/C = převážně otevřené tvary; jinak capo 5 + tvary a-moll (Am→Dm).',
  'No capo — Dm/F/G/Am/B♭/C mostly open shapes; otherwise capo 5 + A-minor shapes (Am→Dm).'),
 ('C-dur → F, Gm, Am, B♭, C, Dm.', 'C major → F, Gm, Am, B♭, C, Dm.'),
 ('dominantový tah (V→I)', 'the dominant pull (V→I)'),
 ('dominantový tah (v→i)', 'the dominant pull (v→i)'),
 ('jazzový obrat', 'a jazz turnaround'),
 ('celý', 'whole'),
 ('půl', 'half'),
 ('Dur tóniny', 'Major keys'),
 ('Molové tóniny', 'Minor keys'),
]
PHRASES = [p for p in PHRASES if len(p) == 2 and p[0] != p[1]]  # filtruj duplicitní no-opy
_seen = set()
PHRASES = [p for p in PHRASES if p[0] not in _seen and not _seen.add(p[0])]  # dedup CZ strany (1. výskyt vyhrává)
PHRASES = sorted(PHRASES, key=lambda kv: -len(kv[0]))  # nejdelší první

# ---------- 2) regexy pro per-key konstrukty ----------
REGEXES = [
 (r'Harmonické postupy v ([A-Ga-g][#♯]?[b♭]?)-dur\b', lambda m: 'Chord progressions in ' + m.group(1) + ' major'),
 (r'Harmonické postupy v ([A-Ga-g][#♯]?[b♭]?)-moll\b', lambda m: 'Chord progressions in ' + m.group(1).capitalize() + ' minor'),
 (r'Diatonické akordy tóniny ([A-Ga-g][#♯]?[b♭]?)-dur\b', lambda m: 'Diatonic chords in ' + m.group(1) + ' major'),
 (r'Diatonické akordy tóniny ([A-Ga-g][#♯]?[b♭]?)-moll\b', lambda m: 'Diatonic chords in ' + m.group(1).capitalize() + ' minor'),  # fix: [#žd]? → [#♯]? (ostřené molové tóniny)
 (r'Nej\w+ cesta — tónina ([A-Ga-g][#♯]?[b♭]?)-moll:', lambda m: 'The easiest way — the key of ' + m.group(1).capitalize() + ' minor:'),
 (r'Nej\w+ cesta — tónina ([A-Ga-g][#♯]?[b♭]?)-dur:', lambda m: 'The easiest way — the key of ' + m.group(1) + ' major:'),
 (r'Nej\w+ cesta — tónina ([A-Ga-g][#♯]?[b♭]?):', lambda m: 'The easiest way — the key of ' + m.group(1) + ':'),
 (r'\(v ([A-Ga-g][#♯]?[b♭]?)-dur\)', lambda m: '(in ' + m.group(1) + ' major)'),
 (r'\(v ([A-Ga-g][#♯]?[b♭]?)-moll\)', lambda m: '(in ' + m.group(1).capitalize() + ' minor)'),
 (r'Tónina ([^ <]+)-dur je vyznačena barvami', lambda m: 'the key of ' + m.group(1) + ' is highlighted'),
 (r'Tónina ([^ <]+)-moll je vyznačena barvami', lambda m: 'the key of ' + m.group(1).capitalize() + ' minor is highlighted'),
 (r'vi \((?:the )?(?:relativní mol|relative minor)\)[^<]*', 'vi (the relative minor) sits in the inner ring below the tonic; the highlighted key is marked by colour.'),
 (r'dur sourozenec \(III\) [^<]*', 'the major sibling (III) sits above the tonic in the outer ring; the highlighted minor key is marked by colour.'),
 (r'capo (\d+) \+ tvary ([A-Ga-g][#♯]?[b♭]?)-dur\b', lambda m: 'capo ' + m.group(1) + ' + ' + m.group(2) + ' major shapes'),
 (r'capo (\d+) \+ tvary ([A-Ga-g][#♯]?[b♭]?)-moll\b', lambda m: 'capo ' + m.group(1) + ' + ' + m.group(2).capitalize() + ' minor shapes'),
 (r'— tvary platí [^<]*', '— the shapes hold in every key; the key = the fret where the tonic sits'),
 (r'Značení: [^<]*', "Notation: ○ = open string, ✕ = don't pluck, dot = a fingertip; the left number = the fret where a barre shape starts."),
 # generic backstop — spouští se PO všech specifických pravidlech na zbytek X-dur / X-moll tokenů
 (r'\b([A-Ga-g][#♯]?[b♭]?)-dur\b', lambda m: m.group(1) + ' major'),
 (r'\b([A-Ga-g][#♯]?[b♭]?)-moll\b', lambda m: m.group(1).capitalize() + ' minor'),
]

src = open(SRC, encoding='utf-8').read()
out = src

# fráze (nejdelší první)
missing = []
for cz, en in PHRASES:
    if cz in out:
        out = out.replace(cz, en)
    else:
        missing.append(cz)

# regexy
for pat, repl in REGEXES:
    out = re.sub(pat, repl, out)

# ---------- 3) brány kvality ----------
diac = [f.strip() for f in re.findall(r'[^<>]*[áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][^<>]*', out) if f.strip()]
words = re.findall(r"\b(dur|moll|tón\w*|postup\w*|kruh\w*|kyt\w*|pražc\w*|strun\w*|vynech\w*|místo|každ\w*|vznik\w*|tvary?|celý|půl|jinak|tečka|domov|jednu|zvolené?|jména|romány|obrat|sestupná|na němž|pod tónikou|tónikou|vynechát)\b", out)
dupes = set()

seen = []
for d in diac:
    if d not in seen: seen.append(d)
seenw = []
for d in words:
    if d not in seenw: seenw.append(d)

if missing:
    print('=== UNMATCHED PHRASES (%d) ===' % len(missing))
    for cz in missing[:25]:
        print('  MISS:', repr(cz[:100]))
if seen:
    print('=== LEFTOVER DIACRITICS (%d unique) ===' % len(seen))
    for d in seen[:30]:
        print('  CZ?:', repr(d[:110]))
if seenw:
    print('=== LEFTOVER CZ WORDS (%d unique) ===' % len(seenw))
    for d in seenw[:30]:
        print('  WORD:', repr(d))

open(OUT, 'w', encoding='utf-8').write(out)
print('WROTE', OUT, len(out), 'bytes; missing=%d diac=%d words=%d' % (len(missing), len(diac), len(words)))