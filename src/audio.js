/**
 * Simple Audio Engine for Guitar Chords
 * Uses Web Audio API to synthesize guitar-like tones.
 */

class AudioEngine {
    constructor() {
        this.ctx = null;
        this.activeOscillators = [];
    }

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }

        // Prohlížeče často pozastaví AudioContext. Musíme ho resume() při interakci uživatele.
        if (this.ctx.state === 'suspended') {
            this.ctx.resume().catch(err => console.error("AudioContext resume failed:", err));
        }
    }

    /**
     * Standard Tuning Frequencies (Hz)
     * E2, A2, D3, G3, B3, E4
     */
    static TUNING = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63];

    /**
     * Convert guitar fingering to frequencies
     * @param {Object} chord - Chord object with fingering and baseFret
     * @returns {Array|null} Array of frequencies or null for 'x'
     */
    getChordFrequencies(chord) {
        if (!chord || !chord.fingering) return null;
        const baseFretOffset = chord.baseFret - 1;
        return chord.fingering.map((fret, i) => {
            if (fret === 'x') return null;
            const fretVal = (fret === 'o' || fret === 0) ? 0 : parseInt(fret, 10);
            return AudioEngine.TUNING[i] * Math.pow(2, (fretVal + baseFretOffset) / 12);
        });
    }

    /**
     * Play a single chord with a strumming effect
     * @param {Array} frequencies - List of frequencies
     * @param {string} direction - 'down' or 'up'
     * @param {number} startTime - AudioContext time to start
     */
    playStrum(frequencies, direction = 'down', startTime = 0) {
        this.init();
        const strumDelay = 0.02; // 20ms offset between strings

        // Down: 6th string (index 0) -> 1st string (index 5)
        // Up: 1st string (index 5) -> 6th string (index 0)
        const indices = direction === 'down'
            ? [0, 1, 2, 3, 4, 5]
            : [5, 4, 3, 2, 1, 0];

        indices.forEach((idx, i) => {
            const freq = frequencies[idx];
            if (!freq) return;
            this.playNote(freq, startTime + (i * strumDelay));
        });
    }

    /**
     * Play a percussive mute sound
     * @param {number} startTime - AudioContext time to start
     */
    playMute(startTime = 0) {
        this.init();
        const now = startTime || this.ctx.currentTime;

        // White noise burst for the "slap"
        const bufferSize = this.ctx.sampleRate * 0.05;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1000, now);
        filter.frequency.exponentialRampToValueAtTime(100, now + 0.05);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        noise.start(now);
        noise.stop(now + 0.06);
    }

    playNote(freq, time) {
        this.init();
        if (this.ctx.state === 'suspended') this.ctx.resume().catch(() => {});
        const now = Math.max(time || 0, this.ctx.currentTime);

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now);

        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.1, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.onended = () => {
            const i = this.activeOscillators.indexOf(osc);
            if (i !== -1) this.activeOscillators.splice(i, 1);
        };

        osc.start(now);
        osc.stop(now + 0.9);

        this.activeOscillators.push(osc);
    }

    stopAll() {
        if (!this.ctx) return;
        this.activeOscillators.forEach(osc => {
            try { osc.stop(); } catch (e) {}
        });
        this.activeOscillators = [];
    }
}

export const audioEngine = new AudioEngine();
