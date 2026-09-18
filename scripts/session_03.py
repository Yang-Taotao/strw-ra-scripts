# %%
# you can run this in interactive python mode

# lib
import numpy as np
import matplotlib.pyplot as plt
import itertools

import scienceplots

# cfg
plt.style.use(["science", "no-latex", "notebook"])

# %%
# local var
filename_raw = "../data/session_03_data_raw"
filename_fft = "../data/session_03_data_fft"

fig_path = "../fig/session_03.pdf"

f_raw = np.fromfile(open(filename_raw), dtype=np.complex64)
f_fft = np.fromfile(open(filename_fft), dtype=np.complex64)

sample_rate = 1e6
tgt_sample_freq = 2.84e9
size = len(f_raw)

# cast to real and imag
f_raw_r, f_raw_i = f_raw.real, f_raw.imag
f_fft_r, f_fft_i = f_fft.real, f_fft.imag

# %%
# time and freq
# time
t = np.linspace(0, size, size, dtype=np.float64)
t *= 1 / sample_rate

f_fft_manual = f_fft_r**2 + f_fft_i**2

# freq
freq_fft = np.linspace(0, tgt_sample_freq, len(f_fft))

freq_fft_r = np.fft.fftfreq(len(f_fft_r), 1e-7)
freq_fft_i = np.fft.fftfreq(len(f_fft_i), 1e-7)
freq_fft_manual = np.fft.fftfreq(len(f_fft_manual), 1e-7)

# %%
# plt

n = int(0.25 * len(t))


def common_plot() -> None:
    """simple plotter"""
    fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(12, 21))

    color_cycle = itertools.cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

    ax1.plot(t[0:n], f_raw_r[0:n], color=next(color_cycle))
    ax1.set_xlabel("t (s)")
    ax1.set_ylabel("amp_real (raw)")
    ax1.set_title("data_real vs t")

    ax2.plot(t[0:n], f_raw_i[0:n], color=next(color_cycle))
    ax2.set_xlabel("t (s)")
    ax2.set_ylabel("amp_imag (raw)")
    ax2.set_title("data_imag vs t")

    ax3.plot(freq_fft, f_fft_r, color=next(color_cycle))
    ax3.set_xlabel("freq_fft")
    ax3.set_ylabel("amp_real (fft)")
    ax3.set_title("data_fft_real vs freq")

    ax4.plot(freq_fft, f_fft_i, color=next(color_cycle))
    ax4.set_xlabel("freq_fft")
    ax4.set_ylabel("amp_imag (fft)")
    ax4.set_title("data_fft_imag vs freq")

    ax5.plot(freq_fft_r, f_fft_r, color=next(color_cycle))
    ax5.set_xlabel("freq_fft_real")
    ax5.set_ylabel("amp_imag (fft)")
    ax5.set_title("data_fft_real vs freq_fft_real")

    ax6.plot(freq_fft_i, f_fft_i, color=next(color_cycle))
    ax6.set_xlabel("freq_fft_imag")
    ax6.set_ylabel("amp_imag (fft)")
    ax6.set_title("data_fft_imag vs freq_fft_imag")

    ax7.plot(freq_fft_manual, f_fft_manual, color=next(color_cycle))
    ax7.set_xlabel("freq_fft_manual")
    ax7.set_ylabel("amp_manual (fft)")
    ax7.set_title("data_fft_manual vs freq_fft_manual")

    plt.tight_layout()
    plt.show()
    plt.savefig(fig_path, dpi=300, format="pdf")
    plt.close(fig)


common_plot()
