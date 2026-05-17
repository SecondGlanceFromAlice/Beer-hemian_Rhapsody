from beerhemian import sine_wave
import numpy as np

def test_sine_wave():
    audio = sine_wave(hz=1, seconds=1, SAMPLE_RATE=1000)

    t = np.linspace(0, 1, 1000, endpoint=False)
    expected = np.sin(2 * np.pi * 1 * t).astype(np.float32)

    np.testing.assert_array_almost_equal(audio, expected)


