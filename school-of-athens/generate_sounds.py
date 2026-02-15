#!/usr/bin/env python3
"""Generate UI sound effects for School of Athens."""
import wave
import struct
import math
import os

SAMPLE_RATE = 44100
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "audio")


def generate_sine(frequency, duration, volume=0.3):
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        samples.append(volume * math.sin(2 * math.pi * frequency * t))
    return samples


def apply_envelope(samples, attack=0.01, decay=0.05, sustain_level=0.7, release=0.1):
    n = len(samples)
    attack_samples = int(SAMPLE_RATE * attack)
    decay_samples = int(SAMPLE_RATE * decay)
    release_samples = int(SAMPLE_RATE * release)
    sustain_samples = max(0, n - attack_samples - decay_samples - release_samples)

    envelope = []
    for i in range(n):
        if i < attack_samples:
            env = i / max(attack_samples, 1)
        elif i < attack_samples + decay_samples:
            pos = (i - attack_samples) / max(decay_samples, 1)
            env = 1.0 - (1.0 - sustain_level) * pos
        elif i < attack_samples + decay_samples + sustain_samples:
            env = sustain_level
        else:
            pos = (i - attack_samples - decay_samples - sustain_samples) / max(release_samples, 1)
            env = sustain_level * (1.0 - pos)
        envelope.append(env)

    return [s * e for s, e in zip(samples, envelope)]


def generate_harmonic_tone(frequency, duration, volume=0.3, harmonics=None):
    if harmonics is None:
        harmonics = [(1.0, 1.0), (2.0, 0.3), (3.0, 0.1)]

    num_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * num_samples

    for mult, amp in harmonics:
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            samples[i] += volume * amp * math.sin(2 * math.pi * frequency * mult * t)

    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak > 0:
        samples = [s / peak * volume for s in samples]

    return samples


def mix_samples(*sample_lists):
    max_len = max(len(s) for s in sample_lists)
    mixed = [0.0] * max_len
    for samples in sample_lists:
        for i, s in enumerate(samples):
            mixed[i] += s
    peak = max(abs(s) for s in mixed) if mixed else 1.0
    if peak > 1.0:
        mixed = [s / peak for s in mixed]
    return mixed


def add_delay(samples, offset_seconds):
    pad = [0.0] * int(SAMPLE_RATE * offset_seconds)
    return pad + samples


def save_wav(filename, samples):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        for s in samples:
            s = max(-1.0, min(1.0, s))
            w.writeframes(struct.pack('<h', int(s * 32767)))
    print(f"  Generated {filepath}")


def generate_message_sent():
    """Ascending tri-tone chord — bright, confident swoosh."""
    vol = 0.18
    duration = 0.12

    tone1 = generate_harmonic_tone(1047, duration, vol, [(1.0, 1.0), (2.0, 0.25), (3.0, 0.08)])
    tone1 = apply_envelope(tone1, attack=0.005, decay=0.03, sustain_level=0.6, release=0.06)

    tone2 = generate_harmonic_tone(1319, duration, vol, [(1.0, 1.0), (2.0, 0.2), (3.0, 0.06)])
    tone2 = apply_envelope(tone2, attack=0.005, decay=0.03, sustain_level=0.5, release=0.06)
    tone2 = add_delay(tone2, 0.04)

    tone3 = generate_harmonic_tone(1568, duration * 0.9, vol * 0.85, [(1.0, 1.0), (2.0, 0.15)])
    tone3 = apply_envelope(tone3, attack=0.005, decay=0.02, sustain_level=0.4, release=0.08)
    tone3 = add_delay(tone3, 0.08)

    return mix_samples(tone1, tone2, tone3)


def generate_message_received():
    """Soft dual-tone notification — warm, gentle, descending."""
    vol = 0.15
    duration = 0.15

    tone1 = generate_harmonic_tone(784, duration, vol, [(1.0, 1.0), (2.0, 0.3), (3.0, 0.1), (4.0, 0.03)])
    tone1 = apply_envelope(tone1, attack=0.008, decay=0.04, sustain_level=0.5, release=0.08)

    tone2 = generate_harmonic_tone(659, duration * 1.2, vol * 0.9, [(1.0, 1.0), (2.0, 0.2), (3.0, 0.05)])
    tone2 = apply_envelope(tone2, attack=0.008, decay=0.04, sustain_level=0.4, release=0.12)
    tone2 = add_delay(tone2, 0.06)

    echo = generate_harmonic_tone(784, duration * 0.8, vol * 0.2, [(1.0, 1.0), (2.0, 0.15)])
    echo = apply_envelope(echo, attack=0.005, decay=0.02, sustain_level=0.2, release=0.1)
    echo = add_delay(echo, 0.18)

    return mix_samples(tone1, tone2, echo)


def generate_button_tap():
    """Short percussive click with subtle resonance."""
    vol = 0.12
    click = generate_sine(3500, 0.008, vol * 1.5)
    click = apply_envelope(click, attack=0.001, decay=0.003, sustain_level=0.2, release=0.004)

    ring = generate_harmonic_tone(1200, 0.04, vol * 0.6, [(1.0, 1.0), (2.5, 0.15)])
    ring = apply_envelope(ring, attack=0.002, decay=0.01, sustain_level=0.3, release=0.025)
    ring = add_delay(ring, 0.003)

    return mix_samples(click, ring)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating sound effects...")
    print("  message_sent.wav...")
    save_wav("message_sent.wav", generate_message_sent())
    print("  message_received.wav...")
    save_wav("message_received.wav", generate_message_received())
    print("  button_tap.wav...")
    save_wav("button_tap.wav", generate_button_tap())
    print("Done!")


if __name__ == "__main__":
    main()
