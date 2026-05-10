import numpy as np

def sine_wave(hz, seconds, SAMPLE_RATE = 44100):
    """A clean sine wave of given frequency and time"""
    duration = seconds
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), endpoint=False)
    audio = np.sin(2 * np.pi * hz * t).astype(np.float32)
    return audio

