"""
Radio Astronomy Session 03 Scripts
- Use `./env.yml` for `conda` managed env replication
- Run with `python ./scripts/session_03.py`, see detail in `./README.md`
- See below for local directory assignment
"""

# imports
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401

# plt cfg
plt.style.use(["science"])

# path assignment
DIR_SCRIPTS = Path(__file__).resolve().parent
DIR_BASE = DIR_SCRIPTS.parent
DIR_DATA = DIR_BASE / "data"
DIR_FIG = DIR_BASE / "fig"

PATH_RAW = DIR_DATA / "session_03_data_raw"
PATH_FFT = DIR_DATA / "session_03_data_fft"
PATH_INT = DIR_DATA / "session_03_data_fft_int"

PATH_FIG = DIR_FIG / "session_03.pdf"
PATH_FIG_SPECTRUM = DIR_FIG / "session_03_spectrum.pdf"
PATH_FIG_WATERFALL = DIR_FIG / "session_03_waterfall.pdf"

# local const
SAMP_RATE = 1e7  # 10 MHz
CENTRAL_FREQ = 1.42e9  # 1.42 GHz
TGT_SAMP_FREQ = 2.84e9  # 2.84 GHz
SAMP_SPACING = 1 / SAMP_RATE
FFT_SIZE = 2048  # N
ERR = 1e-32

# data loader


def load_spectrum(path):
    """read bin data from path and return freq, amp"""

    # read data_fft_int from bin
    data = np.fromfile(path, dtype=np.float32)
    # reshape
    # data.shape should now be (fft_size, xxx)
    data = data.reshape(-1, FFT_SIZE)
    # average into (fft_size, )
    amp = np.nanmean(data, axis=0)

    # center around central freq at Hz
    base = np.fft.fftfreq(FFT_SIZE, d=SAMP_SPACING)
    freq = CENTRAL_FREQ + np.fft.fftshift(base)

    return freq, amp


def load_waterfall(path):
    """read bin data from path and return freq, time, and gain"""

    # read data_fft from bin
    data = np.fromfile(path, dtype=np.complex64)
    # reshape
    data = data.reshape(-1, FFT_SIZE)

    # get complex to mag**2
    gain = np.abs(data) ** 2
    # cast to db at log10 with small ERR for numerical stability
    gain = 10 * np.log10(gain + ERR)

    # convert to s
    time = np.arange(len(data)) * FFT_SIZE * SAMP_SPACING

    # center around central freq at Hz
    base = np.fft.fftfreq(FFT_SIZE, d=SAMP_SPACING)
    freq = CENTRAL_FREQ + np.fft.fftshift(base)

    return freq, time, gain


# plt - main


def plot_spectrum(freq, amp, path) -> None:
    """spectrum plot"""
    # fig
    fig, ax = plt.subplots()
    ax.plot(freq, amp)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")

    fig.tight_layout()
    fig.savefig(path, dpi=300, format="pdf")
    plt.close(fig)


def plot_waterfall(freq, time, gain, path) -> None:
    """waterfall plot"""
    # local repo
    extent = (float(time[0]), float(time[-1]), float(freq[0]), float(freq[-1]))
    vmin, vmax = np.percentile(gain, [5, 99.99])

    # fig
    fig, ax = plt.subplots()
    im = ax.imshow(
        gain.T,
        origin="lower",
        aspect="auto",
        extent=extent,
        cmap="inferno",
        vmin=vmin,
        vmax=vmax,
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Freqency (Hz)")
    fig.colorbar(im, ax=ax, label="Relative Gain (dB)")

    fig.tight_layout()
    fig.savefig(path, dpi=300, format="pdf")
    plt.close(fig)


def main():
    """wrapper for main call"""

    print("SESSION03")
    print("=" * 88)
    print(f"         PROCESSING {PATH_INT}")
    arg_tmp = load_spectrum(PATH_INT)
    plot_spectrum(*arg_tmp, PATH_FIG_SPECTRUM)
    print(f"         PLOT SAVED {PATH_FIG_SPECTRUM}")
    print(f"         PROCESSING {PATH_FFT}")
    arg_tmp = load_waterfall(PATH_FFT)
    plot_waterfall(*arg_tmp, PATH_FIG_WATERFALL)
    print(f"         PLOT SAVED {PATH_FIG_WATERFALL}")
    print("=" * 88)


if __name__ == "__main__":
    main()
