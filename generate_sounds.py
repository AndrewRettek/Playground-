#!/usr/bin/env python3
"""Generate simple UI sound effects for the phone chat app."""
import wave
import struct
import math
import os

SAMPLE_RATE = 44100
OUTPUT_DIR = "game/audio"

def generate_tone(frequency, duration, volume=0.3, fade_out=True):
    """Generate a sine wave tone."""
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Sine wave
        val = volume * math.sin(2 * math.pi * frequency * t)
        # Fade out
        if fade_out:
            fade = 1.0 - (i / num_samples)
            val *= fade
        samples.append(val)
    return samples

def generate_blip(freq1, freq2, duration=0.08, gap=0.02, volume=0.25):
    """Generate a two-tone blip sound."""
    samples = generate_tone(freq1, duration, volume)
    # Small gap
    gap_samples = int(SAMPLE_RATE * gap)
    samples.extend([0.0] * gap_samples)
    # Second tone
    samples.extend(generate_tone(freq2, duration * 0.8, volume * 0.8))
    return samples

def save_wav(filename, samples):
    """Save samples as a WAV file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with wave.open(filepath, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        for s in samples:
            s = max(-1.0, min(1.0, s))
            w.writeframes(struct.pack('<h', int(s * 32767)))
    print(f"  Generated {filepath}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Message sent - bright ascending two-tone blip
    print("Generating message_sent.wav...")
    samples = generate_blip(880, 1320, duration=0.06, gap=0.015, volume=0.2)
    save_wav("message_sent.wav", samples)

    # Message received - softer descending two-tone
    print("Generating message_received.wav...")
    samples = generate_blip(1100, 780, duration=0.07, gap=0.02, volume=0.18)
    save_wav("message_received.wav", samples)

    # Button tap - very short click
    print("Generating button_tap.wav...")
    samples = generate_tone(600, 0.03, volume=0.15, fade_out=True)
    save_wav("button_tap.wav", samples)

    print("Done!")

if __name__ == "__main__":
    main()
