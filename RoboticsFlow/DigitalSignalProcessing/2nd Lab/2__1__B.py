import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import welch


N = 7
d = 0.08  # meter
figure_counter = 0
theta_signal = math.pi / 4
_, n_3 = read("Material/MicArraySimulatedSignals/sensor_3.wav", mmap=True)
_, original = read("Material/MicArraySimulatedSignals/source.wav")
samplerate = 48000

# 1)
start = int(0.47 * samplerate)
end = int(0.50 * samplerate)
n_3 = n_3[start:(end + 1)]
original = original[start:(end + 1)]

noise = []
for i in range(len(n_3)):
    noise.append(n_3[i] - original[i])

f1, Sn_3 = welch(n_3, detrend=False, return_onesided=False, fs=48000)
f2, S_noise = welch(noise, detrend=False, return_onesided=False, fs=48000)
f3, S_original = welch(original, detrend=False, return_onesided=False, fs=48000)

print(len(S_noise), len(S_original), len(Sn_3))

figure_counter += 1
plt.figure(figure_counter)
plt.title("S_noise")
plt.plot(S_noise)

figure_counter += 1
plt.figure(figure_counter)
plt.title("Sn_3")
plt.plot(Sn_3)

figure_counter += 1
plt.figure(figure_counter)
plt.title("S_original")
plt.plot(S_original)

Hw = []
for i in range(len(S_noise)):
    Hw.append(1 - S_noise[i] / Sn_3[i])
    # Hw.append(S_original[i]/Sn_3)

freqs = []
Hw_PSD = []
for i in range(len(f1)):
    if 0 <= f1[i] <= 8000:
        freqs.append(f1[i])
        Hw_PSD.append(Hw[i])
    else:
        break

figure_counter += 1
fig = plt.figure(figure_counter)
ax = fig.add_subplot(111)
# plt.yscale('log')
plt.semilogy(freqs, Hw_PSD)
plt.title("Wiener filter PSD")
plt.xlabel("Hertz")
plt.ylabel("Wiener filter PSD amplitude")

# 2)


nsd = []
for i in range(len(freqs)):
    # print(abs(1-Hw_PSD[i])**2)
    nsd.append((abs(1 - Hw_PSD[i])) ** 2)

# print(Hw, Hw_PSD)

figure_counter += 1
fig = plt.figure(figure_counter)
ax = fig.add_subplot(111)
# plt.yscale('log')
plt.semilogy(freqs, nsd)
plt.title("speech distortion PSD")
plt.xlabel("Hertz")
plt.ylabel("speech distortion PSD amplitude")

# 3)

noise = []
for i in range(len(original)):
    noise.append(n_3[i] - original[i])

fft_num = len(Hw)+len(n_3)
f1_, Sn_3_ = welch(n_3, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
f2_, S_noise_ = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
dft_n_3 = np.fft.fft(n_3, n=fft_num)


f_total = np.linspace(0, max(f1_), len(dft_n_3), endpoint=True)
print(f_total)
Hw = np.interp(f_total, f1, Hw)
Hw = list(Hw)
output_wiener = dft_n_3 * Hw
output = np.fft.ifft(output_wiener)

f, S_output = welch(output, detrend=False, return_onesided=False, fs=48000)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(S_original, label="source signal")
plt.plot(Sn_3, label="microphone 3")
plt.plot(S_noise, label="noise")
plt.plot(S_output, label="wiener filer output")
plt.legend()

plt.show()
