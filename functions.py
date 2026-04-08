import av
import numpy as np
import os
import glob
from scipy import fft
import pandas as pd

def load_audio(file_path):
    """Load audio from any format (m4a, wav, mp3, etc.) using PyAV."""
    container = av.open(file_path)
    audio_stream = next(s for s in container.streams if s.type == "audio")
    sr = audio_stream.sample_rate

    frames = []
    for frame in container.decode(audio_stream):
        frames.append(frame.to_ndarray())

    container.close()

    # Flatten, convert to float32, and mix down to mono if stereo
    audio = np.concatenate(frames, axis=1).mean(axis=0).astype(np.float32)

    # Normalize to -1.0 / +1.0 range (same as librosa)
    if audio.max() > 1.0:
        audio = audio / np.iinfo(np.int16).max

    return audio, sr

def load_all(directory, extension="*.m4a"):
    """Load all .m4a files from a given directory. Returns a list of (filename, y, sr) tuples."""
    files = sorted(glob.glob(os.path.join(directory, extension)))

    if not files:
        print(f"No .m4a files found in: {directory}")
        return []

    recordings = []
    for file_path in files:
        y, sr = load_audio(file_path)
        filename = os.path.basename(file_path)
        recordings.append((filename, y, sr))
        print(f"Loaded: {filename} | {sr} Hz | {len(y)/sr:.2f}s")

    return recordings

def dominant_frequencies(recordings, ml=20):
    frequencies = []
    volume = []
    ml = 20

    for filename, y, sr in recordings:  # no axes needed
        fft_result = np.abs(fft.rfft(y))
        freqs = fft.rfftfreq(len(y), 1 / sr)
        dominant_freq = freqs[np.argmax(fft_result)]
        frequencies.append(dominant_freq)
        volume.append(ml)
        ml += 20

    data = {'frequencies': frequencies, 'volume': volume}
    df = pd.DataFrame(data)

    return df


