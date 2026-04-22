import av
import numpy as np
import os
import glob
from scipy import fft
import pandas as pd
import matplotlib.pyplot as plt

def load_audio(file_path):
    container = av.open(file_path)
    audio_stream = next(s for s in container.streams if s.type == "audio")
    sr = audio_stream.sample_rate
    channels = audio_stream.channels  # <-- pobierz liczbę kanałów

    frames = []
    for frame in container.decode(audio_stream):
        frames.append(frame.to_ndarray())

    container.close()

    audio = np.concatenate(frames, axis=1)[0]  # shape: (1, N) -> (N,)
    
    # Przeplatane stereo: [L, R, L, R, ...] -> weź tylko lewy kanał
    if channels == 2:
        audio = audio[::2]  # co druga próbka = lewy kanał

    audio = audio.astype(np.float32)
    if audio.max() > 1.0:
        audio = audio / np.iinfo(np.int16).max

    return audio, sr

def load_all(directory):
    """Load all audio files (.m4a, .wav, .mp3) from a given directory."""
    files = []
    # Szukamy różnych formatów w podanym folderze
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
    frequencies = []
    volume = []
    beer_names = []  # Nowa lista na nazwy piw
    ml = start_ml

    for filename, y, sr in recordings:  # no axes needed
        fft_result = np.abs(fft.rfft(y))
        freqs = fft.rfftfreq(len(y), 1 / sr)
        # --- ZMIANA: Tworzymy "okno" od 800 Hz do 3000 Hz ---
        # Znak & oznacza "i jednocześnie"
        valid_indices = np.where((freqs > min_freq) & (freqs < max_freq))[0]
        
        # Szukamy najgłośniejszego piku tylko w tym bezpiecznym przedziale
        best_index_in_valid = np.argmax(fft_result[valid_indices])
        actual_best_index = valid_indices[best_index_in_valid]
        
        dominant_freq = freqs[actual_best_index]

        # dominant_freq = freqs[np.argmax(fft_result)]
        frequencies.append(dominant_freq)
        volume.append(ml)

        # Wyciąganie nazwy piwa z nazwy pliku 
        # (dzieli np. "Kasztelan-20.m4a" na ["Kasztelan", "20.m4a"] i bierze pierwszy element)
        beer_name = filename.split('-')[0]
        beer_names.append(beer_name)

        ml += step_ml

    data = {'Beer': beer_names,'frequencies': frequencies, 'volume': volume}
    df = pd.DataFrame(data)

    return df

# Jeśli nadal potrzebujesz DataFrame z wynikami, ale chcesz też wykres:
def dominant_frequencies_with_plot(recordings, start_ml=20, step_ml=10, min_freq=0, max_freq=3000):
    frequencies = []
    volume = []
    beer_names = []
    ml = start_ml

    # Tworzymy figurę przed pętlą
    plt.figure(figsize=(10, 5))

    for filename, y, sr in recordings:
        # FFT
        fft_result = np.abs(fft.rfft(y))
        freqs = fft.rfftfreq(len(y), 1 / sr)
        
        print(f"Sample rate: {sr}, długość y: {len(y)}, shape: {y.shape}")

        # Logika szukania dominanty (z Twojego kodu)
        valid_indices = np.where((freqs > min_freq) & (freqs < max_freq))[0]
        best_index_in_valid = np.argmax(fft_result[valid_indices])
        actual_best_index = valid_indices[best_index_in_valid]
        dominant_freq = freqs[actual_best_index]

        # RYSOWANIE: Dodajemy linię dla tego konkretnego nagrania
        # Ograniczamy zakres x do max_freq, żeby wykres nie był "pusty" na końcu
        plot_mask = freqs < max_freq 
        plt.plot(freqs[plot_mask], fft_result[plot_mask], alpha=0.7, label=f"{ml}ml - {filename}")
        
        # Zbieranie danych do DF
        frequencies.append(dominant_freq)
        volume.append(ml)
        beer_name = filename.split('-')[0]
        beer_names.append(beer_name)
        ml += step_ml

    plt.title("Analiza Spektralna - Amplituda od Częstotliwości")
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda")
    plt.legend(loc='upper right', fontsize='small')
    plt.show()

    return pd.DataFrame({'Beer': beer_names, 'frequencies': frequencies, 'volume': volume})