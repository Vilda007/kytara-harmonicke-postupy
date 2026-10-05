import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { audioEngine } from './audio';

const I18N = {
    en: {
        title: "Guitar Chord Progressions",
        subtitle: "Interactive Harmony Guide",
        currentKey: "Current Key",
        diatonicChords: "Diatonic Chords",
        provenProgressions: "Proven Progressions",
        // Chord roles
        "I": "Tonic", "i": "Tonic",
        "IV": "Subdominant", "iv": "Subdominant",
        "V": "Dominant", "v": "Dominant", "V7": "Dominant",
        "vi": "Relative Minor", "VI": "Subdominant",
        "ii": "Supertonic", "iii": "Mediant", "vii°": "Leading Tone",
        "II": "Supertonic", "III": "Mediant", "VII": "Leading Tone", "ii°": "Supertonic",
        // Other
        easyPath: "Easy path: ",
        capoNote: "Capo = clamp: shifts easy shapes up by N frets.",
        funcHint: "Function: "
    },
    cs: {
        title: "Harmonické postupy na kytaru",
        subtitle: "Interaktivní průvodce harmonií",
        currentKey: "Aktuální tónina",
        diatonicChords: "Diatonické akordy",
        provenProgressions: "Osvědčené postupy",
        // Chord roles
        "I": "tónika", "i": "tónika",
        "IV": "subdominanta", "iv": "subdominanta",
        "V": "dominanta", "v": "dominanta", "V7": "dominanta",
        "vi": "rel. mol", "VI": "subdominanta",
        "ii": "subdom.", "iii": "mezikrok", "vii°": "vedlejší",
        "II": "subdom.", "III": "mezikrok", "VII": "vedlejší", "ii°": "subdom.",
        // Other
        easyPath: "Nejsnazší cesta: ",
        capoNote: "Capo = strunný pásek: posune snadné tvary o N polotónů nahoru.",
        funcHint: "Funkce: "
    }
};

const MAJOR_KEYS = ["C", "G", "D", "A", "E", "B", "F♯", "D♭", "A♭", "E♭", "B♭", "F"];
const MINOR_KEYS = ["a", "e", "b", "f♯", "c♯", "g♯", "d♯", "b♭", "f", "c", "g", "d"];

const COLOR_MAP = {
    'I': 'var(--tonic)', 'i': 'var(--tonic)',
    'IV': 'var(--sub)', 'iv': 'var(--sub)',
    'V': 'var(--dom)', 'v': 'var(--dom)', 'V7': 'var(--dom)',
    'vi': 'var(--vin)', 'VI': 'var(--sub)',
    'ii': 'var(--muted)', 'iii': 'var(--muted)', 'vii°': 'var(--muted)',
    'II': 'var(--muted)', 'III': 'var(--vin)', 'VII': 'var(--muted)', 'ii°': 'var(--muted)'
};

const ChordDiagram = ({ chord, numeral, lang }) => {
    if (!chord) return <div className="w-24 h-32 flex items-center justify-center text-xs text-gray-400 border border-dashed border-gray-300 rounded">N/A</div>;

    const { fingering, baseFret, name } = chord;
    // tolerate numeric strings ('3', '0') in the data
    const frets = fingering.map(f => typeof f === 'string' && f !== 'x' ? parseInt(f, 10) : f);
    const stringSpacing = 16;
    const fretSpacing = 20;

    return (
        <div className="flex flex-col items-center gap-2">
            <svg width="110" height="140" viewBox="-10 -10 120 150">
                {/* Fretboard Grid */}
                {Array.from({length: 6}).map((_, i) => (
                    <line key={`s${i}`} x1={20 + i * stringSpacing} y1={10} x2={20 + i * stringSpacing} y2={90} className="string-line" />
                ))}
                {Array.from({length: 5}).map((_, i) => (
                    <line key={`f${i}`} x1={20} y1={10 + i * fretSpacing} x2={20 + 5 * stringSpacing} y2={10 + i * fretSpacing} className="fret-line" />
                ))}

                {/* Nut / Base Fret */}
                {baseFret === 1 ? (
                    <line x1={20} y1={10} x2={20 + 5 * stringSpacing} y2={10} stroke="var(--fg)" strokeWidth="2.6" />
                ) : (
                    <text x={12} y={22} fontSize="12" fontWeight="700" fill="var(--fg)" textAnchor="end">{baseFret}</text>
                )}

                {/* Muted/Open markers - enlarged and bolder */}
                {frets.map((f, i) => {
                    const sx = 20 + i * stringSpacing;
                    if (f === 'x') return <text key={`x${i}`} x={sx} y={8} fontSize="12" fontWeight="700" fill="#8a8074" textAnchor="middle">✕</text>;
                    if (f === 'o' || f === 0) return <text key={`o${i}`} x={sx} y={8} fontSize="12" fontWeight="700" fill="var(--line)" textAnchor="middle">○</text>;
                    return null;
                })}

                {/* Barre highlight */}
                {frets.filter(f => f === baseFret && typeof f === 'number').length >= 2 && (
                    <rect
                        x={frets[0] === baseFret ? 19 : 33}
                        y={13}
                        width={frets[0] === baseFret ? 82 : 68}
                        height="14"
                        rx="7"
                        className="barre-rect"
                    />
                )}

                {/* Dots - ensured visibility on highest string */}
                {frets.map((f, i) => {
                    if (typeof f !== 'number' || f === 0) return null;
                    const r = f - baseFret;
                    return <circle key={`d${i}`} cx={20 + i * stringSpacing} cy={10 + r * fretSpacing + 10} r="6.5" className="chord-dot" />;
                })}

                <text x={50} y={112} textAnchor="middle" className="font-bold" fontSize="15">{name}</text>
                <text x={50} y={127} textAnchor="middle" fontSize="9.5" fill="var(--muted)">{numeral}</text>
            </svg>
        </div>
    );
};

const CircleOfFifths = ({ activeKey, onKeyChange }) => {
    const centerX = 300, centerY = 300;
    const R_RING = 280, R_CHIP = 240, R_MINOR = 130;

    const getPos = (k, r) => {
        const th = (Math.PI / 180) * (-90 + 30 * k);
        return [centerX + r * Math.cos(th), centerY + r * Math.sin(th)];
    };

    return (
        <div className="flex justify-center items-center p-4 bg-white rounded-2xl shadow-sm">
            <svg className="w-full h-auto max-w-[600px]" viewBox="0 0 600 600">
                <circle cx={centerX} cy={centerY} r={R_RING} fill="none" stroke="#d7d3c8" strokeWidth="1" />
                <circle cx={centerX} cy={centerY} r={R_MINOR} fill="none" stroke="#d7d3c8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7" />

                {MAJOR_KEYS.map((s, i) => {
                    const [x, y] = getPos(i, R_CHIP);
                    const isActive = activeKey.symbol === s;
                    return (
                        <g key={`maj-${i}`} onClick={() => onKeyChange({symbol: s, type: 'major', position: i})} style={{cursor: 'pointer'}}>
                            <rect x={x-30} y={y-18} width="60" height="36" rx="18"
                                  fill={isActive ? 'var(--tonicbg)' : 'var(--neutral)'}
                                  stroke={isActive ? 'var(--tonic)' : 'var(--line)'}
                                  strokeWidth={isActive ? 2 : 1} />
                            <text x={x} y={y+6} textAnchor="middle" className="font-bold" fontSize="18" fill="var(--fg)">{s}</text>
                        </g>
                    );
                })}

                {MINOR_KEYS.map((s, i) => {
                    const [x, y] = getPos(i, R_MINOR);
                    const isActive = activeKey.symbol === s;
                    return (
                        <g key={`min-${i}`} onClick={() => onKeyChange({symbol: s, type: 'minor', position: i})} style={{cursor: 'pointer'}}>
                            <rect x={x-24} y={y-14} width="48" height="28" rx="14"
                                  fill={isActive ? 'var(--vinbg)' : '#ecf0f4'}
                                  stroke={isActive ? 'var(--vin)' : 'var(--line)'}
                                  strokeWidth={isActive ? 2 : 1} />
                            <text x={x} y={y+6} textAnchor="middle" className="font-bold" fontSize="14" fill="var(--fg)">{s}</text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
};

const App = () => {
    const [data, setData] = useState(null);
    const [lang, setLang] = useState('en');
    const [activeKey, setActiveKey] = useState({ symbol: 'C', type: 'major', position: 0 });
    const [playbackState, setPlaybackState] = useState({
        isPlaying: false,
        isMuted: false,
        bpmOverride: null,
        currentChordIndex: -1,
        currentProgIndex: -1
    });

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const urlLang = params.get('lang') || 'en';
        setLang(urlLang === 'cs' ? 'cs' : 'en');

        fetch('chords.json')
            .then(r => r.json())
            .then(jsonData => {
                setData(jsonData);
                const urlKey = params.get('key');
                const urlType = params.get('type');
                if (urlKey && urlType) {
                    const found = jsonData.keys.find(k => k.symbol === urlKey && k.type === urlType);
                    if (found) {
                        setActiveKey({
                            symbol: found.symbol,
                            type: found.type,
                            position: found.position
                        });
                    }
                }
            });
    }, []);

    useEffect(() => {
        if (playbackState.isPlaying) {
            return () => audioEngine.stopAll();
        }
    }, [playbackState.isPlaying]);

    if (!data) return <div className="flex items-center justify-center h-screen">Loading harmony...</div>;

    const t = I18N[lang];
    const currentKeyData = data.keys.find(k => k.symbol === activeKey.symbol);

    const handleStop = () => {
        audioEngine.stopAll();
        setPlaybackState({
            isPlaying: false,
            isMuted: false,
            bpmOverride: null,
            currentChordIndex: -1,
            currentProgIndex: -1
        });
    };

    const handleToggleMute = () => {
        setPlaybackState(prev => ({ ...prev, isMuted: !prev.isMuted }));
    };

    const handleBpmChange = (e) => {
        setPlaybackState(prev => ({ ...prev, bpmOverride: parseInt(e.target.value, 10) }));
    };

    const handlePlayChord = (chord) => {
        if (!chord) return;

        // Ensure AudioContext is resumed on user interaction
        audioEngine.init();

        // Stop any current progression to avoid overlap
        audioEngine.stopAll();
        setPlaybackState({
            isPlaying: false,
            isMuted: false,
            bpmOverride: null,
            currentChordIndex: -1,
            currentProgIndex: -1
        });

        const freqs = audioEngine.getChordFrequencies(chord);
        // Play as a standard downstrum for single chord clicks
        audioEngine.playStrum(freqs, 'down', audioEngine.ctx.currentTime);
    };

    const handlePlayProgression = async (progIndex, prog) => {
        if (playbackState.isPlaying && playbackState.currentProgIndex === progIndex) {
            handleStop();
            return;
        }

        handleStop();

        // Ensure AudioContext is resumed on user interaction
        audioEngine.init();

        setPlaybackState(prev => ({
            ...prev,
            isPlaying: true,
            currentChordIndex: 0,
            currentProgIndex: progIndex
        }));

        const rhythmKey = prog.rhythm || 'pop';
        const rhythmData = data.rhythms[rhythmKey] || data.rhythms['pop'];
        const baseBpm = rhythmData.bpm || 120;
        const currentBpm = playbackState.bpmOverride || baseBpm;
        const pattern = rhythmData.pattern || ["D"];

        const sequence = prog.sequence;
        let currentStep = 0;
        let currentChordIdx = 0;

        const playNextStep = () => {
            // IMPORTANT: We must check if we are still playing.
            // Since this is a closure, we can't check playbackState directly from the state hook
            // but we can check the currentProgIndex from the playbackState if we had a ref.
            // As a fix for this architecture, we'll check a global or use a ref.
            // For now, let's use a simple check against a variable we can access.

            if (!playbackState.isPlaying) return;

            const stepType = pattern[currentStep % pattern.length];
            const chord = currentKeyData.chords[sequence[currentChordIdx]];
            const freqs = audioEngine.getChordFrequencies(chord);

            if (!playbackState.isMuted) {
                if (stepType === 'D') {
                    audioEngine.playStrum(freqs, 'down', audioEngine.ctx.currentTime);
                } else if (stepType === 'U') {
                    audioEngine.playStrum(freqs, 'up', audioEngine.ctx.currentTime);
                } else if (stepType === 'M') {
                    audioEngine.playMute(audioEngine.ctx.currentTime);
                }
            }

            currentStep++;
            if (currentStep % 4 === 0) {
                currentChordIdx++;
                if (currentChordIdx >= sequence.length) {
                    currentChordIdx = 0;
                }
                setPlaybackState(prev => ({ ...prev, currentChordIndex: currentChordIdx }));
            }

            const activeBpm = playbackState.bpmOverride || baseBpm;
            const currentDuration = 60 / activeBpm / 2;

            setTimeout(playNextStep, currentDuration * 1000);
        };

        playNextStep();
    };

    return (
        <div className="max-w-3xl mx-auto p-8 flex flex-col gap-12">
            <header className="flex flex-col items-center text-center mb-4 gap-4">
                <div className="flex gap-2 bg-white p-1 rounded-full shadow-sm border border-gray-200">
                    <button onClick={() => setLang('en')} className={`px-4 py-1 rounded-full text-xs font-bold transition-all ${lang === 'en' ? 'bg-amber-500 text-white shadow-inner' : 'text-gray-500 hover:text-gray-700'}`}>EN</button>
                    <button onClick={() => setLang('cs')} className={`px-4 py-1 rounded-full text-xs font-bold transition-all ${lang === 'cs' ? 'bg-amber-500 text-white shadow-inner' : 'text-gray-500 hover:text-gray-700'}`}>CZ</button>
                </div>
                <h1 className="text-4xl font-extrabold mb-2">{t.title}</h1>
                <p className="text-gray-500">{t.subtitle}</p>
            </header>

            <div className="flex flex-col gap-12">
                <section className="bg-white p-6 rounded-2xl shadow-sm flex flex-col items-center gap-6">
                    <CircleOfFifths activeKey={activeKey} onKeyChange={setActiveKey} />
                    <div className="text-center max-w-md">
                        <h2 className="text-xl font-bold mb-2">{t.currentKey}: {activeKey.symbol} {activeKey.type === 'major' ? (lang === 'en' ? 'Major' : 'dur') : (lang === 'en' ? 'Minor' : 'mol')}</h2>
                        <p className="text-sm text-gray-500">{currentKeyData?.capoTip && typeof currentKeyData.capoTip === 'object' ? currentKeyData.capoTip[lang] : (currentKeyData?.capoTip || "Select a key on the circle to explore.")}</p>
                    </div>
                </section>

                <section className="bg-white p-6 rounded-2xl shadow-sm">
                    <h3 className="text-lg font-bold mb-6 border-b pb-2">{t.diatonicChords}</h3>
                    <div className="grid grid-cols-3 sm:grid-cols-4 gap-4 items-start">
                        {Object.entries(currentKeyData?.chords || {}).map(([role, chord]) => (
                            <div key={role} className="flex flex-col items-center">
                                <div className="px-3 py-1 rounded-full text-xs font-bold mb-2 h-8 flex items-center justify-center text-center cursor-pointer hover:brightness-90 transition-all"
                                     onClick={(e) => {
                                         e.stopPropagation();
                                         handlePlayChord(chord);
                                     }}
                                     style={{backgroundColor: 'var(--neutral)', color: COLOR_MAP[role] || 'var(--fg)'}}>
                                    {role} {t[role] ? `· ${t[role]}` : ''}
                                </div>
                                <ChordDiagram chord={chord} numeral={role} lang={lang} />
                            </div>
                        ))}
                    </div>
                </section>

                <section className="bg-white p-6 rounded-2xl shadow-sm">
                    <div className="flex items-center justify-between mb-6 border-b pb-2">
                        <h3 className="text-lg font-bold">{t.provenProgressions}</h3>

                        {playbackState.isPlaying && (
                            <div className="flex items-center gap-4 bg-gray-50 p-2 rounded-full px-4 border border-gray-200">
                                <button
                                    onClick={handleToggleMute}
                                    className={`px-3 py-1 rounded-full text-xs font-bold transition-all ${playbackState.isMuted ? 'bg-red-100 text-red-600' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-100'}`}
                                >
                                    {playbackState.isMuted ? (lang === 'en' ? 'Unmute' : 'Zapnout zvuk') : (lang === 'en' ? 'Mute' : 'Ztlumit')}
                                </button>
                                <button
                                    onClick={handleStop}
                                    className="px-3 py-1 rounded-full text-xs font-bold bg-gray-800 text-white hover:bg-black transition-all"
                                >
                                    {lang === 'en' ? 'Stop' : 'Stop'}
                                </button>
                                <div className="flex items-center gap-2 ml-2 border-l pl-4">
                                    <span className="text-[10px] font-bold text-gray-400 uppercase">BPM</span>
                                    <input
                                        type="range"
                                        min="40"
                                        max="220"
                                        value={playbackState.bpmOverride || 120}
                                        onChange={handleBpmChange}
                                        className="w-24 h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-amber-500"
                                    />
                                    <span className="text-xs font-mono font-bold text-gray-600 w-8">{playbackState.bpmOverride || 120}</span>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className="space-y-6">
                        {(activeKey.type === 'minor' ? (data.minorProgressions || data.progressions) : data.progressions).map((prog, i) => (
                            <div
                                key={i}
                                onClick={() => handlePlayProgression(i, prog)}
                                className={`flex items-center justify-between p-3 rounded-lg transition-all cursor-pointer ${playbackState.currentProgIndex === i ? 'bg-amber-50 ring-1 ring-amber-200' : 'hover:bg-gray-50'}`}
                            >
                                <div className="flex items-center gap-3">
                                    <div className="flex gap-2">
                                        {prog.sequence.map((role, idx) => {
                                            const chord = currentKeyData?.chords[role];
                                            const isActive = playbackState.currentProgIndex === i && playbackState.currentChordIndex === idx;
                                            return (
                                                <span
                                                    key={idx}
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handlePlayChord(chord);
                                                    }}
                                                    className={`px-2 py-1 rounded font-bold text-sm transition-all cursor-pointer hover:brightness-90 ${isActive ? 'bg-amber-400 text-white scale-110 shadow-sm' : 'bg-gray-100'}`}
                                                      style={{color: isActive ? 'white' : (COLOR_MAP[role] || 'var(--fg)')}}>
                                                    {chord ? chord.name : role}
                                                </span>
                                            );
                                        })}
                                    </div>
                                    <span className="text-gray-400 text-sm">—</span>
                                    <span className="text-sm font-medium">{typeof prog.genre === 'object' ? prog.genre[lang] : prog.genre}</span>
                                </div>
                                {playbackState.currentProgIndex === i && (
                                    <div className="text-amber-600 animate-pulse text-xs font-bold">
                                        {lang === 'en' ? 'Playing...' : 'Hrají...'}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
};

const root = createRoot(document.getElementById('root'));
root.render(<App />);