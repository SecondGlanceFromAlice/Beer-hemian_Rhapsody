import av
import numpy as np
import os
import glob
from scipy import fft
import pandas as pd
import matplotlib.pyplot as plt

def load_audio(file_path):
    ''' There is a space for future description of the function '''
    container = av.open(file_path)
    audio_stream = next(s for s in container.streams if s.type == "audio")
    sr = audio_stream.sample_rate
    channels = audio_stream.channels  

    frames = []
    for frame in container.decode(audio_stream):
        frames.append(frame.to_ndarray())

    container.close()

    audio = np.concatenate(frames, axis=1)[0]  
    
    if channels == 2:
        audio = audio[::2] 

    audio = audio.astype(np.float32)
    if audio.max() > 1.0:
        audio = audio / np.iinfo(np.int16).max

    return audio, sr

def load_all(directory):
    
    """Load all audio files (.m4a, .wav, .mp3) from a given directory."""
    files = []
    for ext in ("*.m4a", "*.wav", "*.mp3"):
        files.extend(glob.glob(os.path.join(directory, ext)))
        
    files = sorted(files)

    if not files:
        print(f"No audio files found in: {directory}")
        return []

    recordings = []
    for file_path in files:
        y, sr = load_audio(file_path)
        filename = os.path.basename(file_path)
        recordings.append((filename, y, sr))
        print(f"Loaded: {filename} | {sr} Hz | {len(y)/sr:.2f}s")

    return recordings
def dominant_frequencies(recordings, start_ml=20, step_ml=10, min_freq=0, max_freq=3000):
    ''' There is a space for future description of the function '''
    frequencies = []
    volume = []
    beer_names = []
    fft_data = []
    ml = start_ml

    for filename, y, sr in recordings:
        fft_result = np.abs(fft.rfft(y))
        freqs = fft.rfftfreq(len(y), 1 / sr)

        valid_indices = np.where((freqs > min_freq) & (freqs < max_freq))[0]
        best_index_in_valid = np.argmax(fft_result[valid_indices])
        actual_best_index = valid_indices[best_index_in_valid]
        dominant_freq = freqs[actual_best_index]

        frequencies.append(dominant_freq)
        volume.append(ml)
        beer_names.append(filename.split('-')[0])
        fft_data.append((filename, freqs, fft_result))
        ml += step_ml

    return pd.DataFrame({'Beer': beer_names, 'frequencies': frequencies, 'volume': volume}), fft_data


def plot_spectrum(fft_data, df, max_freq=3000):
    ''' There is a space for future description of the function '''
    beer_names = df['Beer'].unique()

    for beer in beer_names:
        plt.figure(figsize=(10, 5))
        beer_df = df[df['Beer'] == beer]
        beer_fft = [(filename, freqs, fft_result) for (filename, freqs, fft_result) in fft_data if filename.split('-')[0] == beer]

        for (filename, freqs, fft_result), (_, row) in zip(beer_fft, beer_df.iterrows()):
            plot_mask = freqs < max_freq
            plt.plot(freqs[plot_mask], fft_result[plot_mask], alpha=0.7, label=f"{row['volume']}ml")


        plt.title(f"Frequency Spectrum - {beer}")
        plt.xlabel("Częstotliwość [Hz]")
        plt.ylabel("Amplituda")
        plt.legend(loc='upper right', fontsize='small')
        plt.show()