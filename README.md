[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/MIT)

# Beer-hemian_Rhapsody

This package started as a student project "Beer-hemian Rhapsody: Ale-iance of density and sound" 
(pl: "Co w piwie piszczy? Fizykochemiczna analiza akustyczna piwa"). Our goal was to check if liquid in a glass affects 
the sound it makes (if you can't imagine it check out this [Youtube video](https://youtu.be/QdoTdG_VNV4?si=qiWBI7zX1te2O__g) by GlassDuo - Glass Harp)

Our functions include:

- **load_audio(file_path)**: Loads single audio file

- **load_all(directory)**: Load all audio files (.m4a, .wav, .mp3) from a given directory.

- **dominant_frequencies(recordings, start_ml=20, step_ml=10, min_freq=0, max_freq=3000)**: finds the dominant frequency in each given recording and returns Pandas Dataframe {beer name, frequencies, volume} and fft_data

- **plot_spectrum(fft_data, df, max_freq=3000)**: using fft_data plots sound spectrum of the sound file

- **plot_spectrum_multiple(fft_data, df, ax, max_freq=3000)**: analog to plot_spectrum, but produces single plot with all recordings

- **plot_with_curve(beer_name, volumes, frequencies)**: Designed to just prepare layout of the plot. plt.plot() is needed after executing the function

## Installation

To make sure every dependency is connected properly please use the following command:

``!pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ Beer-hemian``

Then, in your code, please use ``import beerhemian`` to import the library


## Our team

Special thanks to our team from SKNF Bozon AGH (Student Research Club Bozon, AGH university of Krakow):
- Alicja Jagielska
- Wiktoria Seweryn
- Krzysztof Kryk
- Szymon Książek
- Mikołaj Lewandowski
- Wiktor Sala
- Witold Rudziński



## Dependencies

Beer-hemian_Rhapsody dependencies are: 
[PyAv](https://pyav.org/docs/develop/#),
[numpy](https://numpy.org/),
[scipy](https://scipy.org/),
[pandas](https://pandas.pydata.org/),
[matplotlib](https://matplotlib.org/),
[IPython](https://ipython.org/)
