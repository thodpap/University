import numpy as np
import matplotlib.pylab as plt
import math
import cmath
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram

import warnings

warnings.filterwarnings('ignore')

N = 7
d = 0.04  # meter
c = 340  # m/s
figure_counter = 0

theta_signal = math.pi / 4
# theta_noise = 3 * math.pi / 4

samplerate, n_0 = read("Material/MicArrayRealSignals/sensor_0.wav")
_, n_1 = read("Material/MicArrayRealSignals/sensor_1.wav")
_, n_2 = read("Material/MicArrayRealSignals/sensor_2.wav")
_, n_3 = read("Material/MicArrayRealSignals/sensor_3.wav")
_, n_4 = read("Material/MicArrayRealSignals/sensor_4.wav")
_, n_5 = read("Material/MicArrayRealSignals/sensor_5.wav")
_, n_6 = read("Material/MicArrayRealSignals/sensor_6.wav")
_, original = read("Material/MicArrayRealSignals/source.wav")
print(original[5000])

n = [list(n_0), list(n_1), list(n_2), list(n_3), list(n_4), list(n_5), list(n_6)]

## calculate τn
# samplerate = 48000
tn = []
for i in range(7):
    tn.append(((-(i - (N - 1) / 2) * d * math.cos(theta_signal)) / c) * samplerate)

my_len = len(n[0])  # length of all signals

# DFT OF SIGNALS

dfts = []

for i in range(7):
    dfts.append(fft(n[i]))

print("dft[3]: ", dfts[3])

dft_len = len(dfts[0])

# shifted

new_dfts = []

for i in range(7):
    temp = []
    for k in range(dft_len):
        temp.append(dfts[i][k] * np.exp(-1j * 2 * math.pi * k * tn[N - 1 - i] / dft_len))  # m = tn[i]
    new_dfts.append(temp)

idfts = []
for i in range(7):
    idfts.append(np.fft.ifft(new_dfts[i]))

print("gsfgfgdg: ", idfts[2][5001])

print("idft: ", idfts[0])

output = []
for i in range(len(idfts[0])):
    output.append(
        (1 / 7) * (idfts[0][i] + idfts[1][i] + idfts[2][i] + idfts[3][i] + idfts[4][i] + idfts[5][i] + idfts[6][i]))
print("00: ", output[5000])
output = np.array(output)
original = np.array(original)
diff = []
for i in range(len(output)):
    diff.append(output[i] - original[i])

diff = np.array(diff)

# diff = np.real(diff)
print(diff)
print(diff.astype(n_3.dtype))
write("beam_former_ouput.wav", samplerate, output.astype(n_3.dtype))

## B


# a)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(original)), original)
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("source signal")

f, t, Sxx = spectrogram(original, fs=48000)
figure_counter += 1
plt.figure(figure_counter)
plt.pcolormesh(t, f, Sxx)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of source signal")

figure_counter += 1
plt.figure(figure_counter)
fft_source = fft(list(original))
plt.plot(np.arange(len(fft_source)), fft_source)
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of source signal")

# b)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(n_3)), list(n_3))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("n_3 signal")

f3, t3, Sxx3 = spectrogram(n_3, fs=48000)
figure_counter += 1
plt.figure(figure_counter)
plt.pcolormesh(t3, f3, Sxx3)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of n_3 signal")

figure_counter += 1
plt.figure(figure_counter)
fft3 = fft(list(n_3))
plt.plot(np.arange(len(fft3)), fft3)
plt.xlabel("discrete time")

# c)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(output)), list(output))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("output signal")

output = np.array(output)
output = output.astype(n_3.dtype)
f_output, t_output, Sxx_output = spectrogram(output, fs=48000)
figure_counter += 1
print("foutput: ", f_output)
plt.figure(figure_counter)
plt.pcolormesh(t_output, f_output, Sxx_output)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of output signal")

figure_counter += 1
plt.figure(figure_counter)
fft_output = fft(list(output))
plt.plot(np.arange(len(fft_output)), fft_output)
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of output signal")
plt.ylabel("amplitude")


#3)

## SNR
def signal_energy(signal):
    energy = 0.0
    # print(signal)
    for n in range(len(signal)):
        energy += math.pow((signal[n]), 2)

    return energy / len(signal)


L = 1440

noise_power = signal_energy(n_3[0:L])

# n_3 = n_3[72000:122000]
M = len(n_3)//L

SSNR = []
counter = 0
for i in range(M):
    cons = (signal_energy(n_3[i*L:i*L+L])-noise_power)/noise_power
    if cons <= 0:
        # print(i)
        counter += 1
        continue
    res = 10*np.log10(cons)
    if res >= 35:
        res = 35
    if res <= -20:
        continue
    SSNR.append(res)

print("counter: ", counter)
print("sdfdf: ", noise_power)
print("n_3: ", sum(SSNR)/M)

#-----------------------------------------------------------------------------------------------------------------------

noise_power = signal_energy(output[0:L])

# output = output[72000:122000]
M = len(output)//L


SSNR = []
counter = 0
for i in range(M):
    cons = (signal_energy(output[L*i:L*i+L]) - noise_power)/noise_power
    if cons <= 0:
        # print(i)
        counter += 1
        continue
    res = 10*np.log10(cons)
    if res >= 35:
        res = 35
    if res <= -10:
        continue
    SSNR.append(res)

print("counter: ", counter)
print("sdfdf: ", noise_power)
print("output: ", sum(SSNR)/M)

plt.show()