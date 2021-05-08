import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import welch


N = 7
d = 0.08  # meter
figure_counter = 0
theta_signal = math.pi / 4
samplerate, n_3 = read("Material/MicArraySimulatedSignals/sensor_3.wav")
_, original = read("Material/MicArraySimulatedSignals/source.wav")
print(samplerate)
samplerate = 48000
fft_ = np.fft.fft(original)
freqs = np.fft.fftfreq(len(fft_))
# figure_counter += 1
# plt.figure((figure_counter))
# plt.plot(samplerate*freqs, fft_)

# 1)
start = int(0.47 * samplerate)
end = int(0.50 * samplerate)
n_3 = n_3[start:(end + 1)]
original = original[start:(end + 1)]

noise = []
for i in range(len(n_3)):
    noise.append(n_3[i] - original[i])

f1, Sn_3 = welch(n_3, detrend=False, return_onesided=False, fs=48000)
print("f1: ", list(f1))
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
    nsd.append(math.pow(1 - Hw_PSD[i], 2))

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

# fft_num = len(Hw)+len(n_3) # correct convolution in frequency domain
fft_num = 2*len(n_3) #correct convolution in frequency domain
dft_n_3 = np.fft.fft(n_3, n=fft_num)
plt.figure(100)
plt.plot(dft_n_3)
# fft_num = len(dft_n_3)
# print(fft_num)
f1_, Sn_3_ = welch(n_3, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
# print("f1_: ", len(f1_))
f2_, S_noise_ = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)


Hw = []
for i in range(fft_num):
    Hw.append(1-S_noise_[i]/Sn_3_[i])

plt.figure(101)
plt.plot(Hw)
# dft_n_3 = np.fft.fft(n_3, n=fft_num)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(dft_n_3)


# f_total = np.linspace(0, max(freqs), fft_num, endpoint=True)
# print("xxxx: ", f_total)
# Hw = np.interp(f_total, freqs, Hw_PSD)


figure_counter += 1
plt.figure(figure_counter)
plt.semilogy(Hw)


# Hw = list(Hw)
# output_wiener = dft_n_3 * Hw
print("lengths: ", len(dft_n_3), len(Hw))
output_wiener = []
Hw_time = np.fft.ifft(Hw)
# output_wiener = np.convolve(Hw_time, n_3)
for i in range(len(Hw)):
    # if 100 <= i <= 500:
    #     print(i, Hw[i], dft_n_3[i], dft_n_3[i]*Hw[i])
    output_wiener.append(dft_n_3[i]*Hw[i])

freqs = np.fft.fftfreq(len(output_wiener))
figure_counter += 1
plt.figure(figure_counter)
plt.plot(freqs*samplerate, output_wiener)
plt.title("dft of output wiener")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(dft_n_3)
plt.title("dft of  n_3")

output_wiener_time = np.fft.ifft(output_wiener, n=fft_num)
# output_wiener_time = output_wiener
print("aaaaaaaaaaaaaaaaaaa: ", len(output_wiener_time))
output_wiener_time = output_wiener_time.astype(int)
# print("output_wiener_time: ", list(output_wiener_time))
# print(list(n_3))

f, S_output = welch(output_wiener_time, detrend=False, return_onesided=False, fs=48000)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(S_original, label="source signal")
plt.plot(Sn_3, label="microphone 3")
plt.plot(S_noise, label="noise")
plt.plot(S_output, label="wiener filer output")
plt.legend()


## 4)

output_wiener_time = np.array(output_wiener_time)
# output_wiener_time = output_wiener_time.astype(int)
output_noise = []

space = np.arange(len(original))
output_wiener_time = np.interp(space, np.arange(len(output_wiener_time)), output_wiener_time)
print("lengths: ", len(output_wiener_time), len(original))
for i in range(len(output_wiener_time)):
    output_noise.append(output_wiener_time[i] - original[i])

# bool_ = []
# for i in range(len(n_3)):
#     if n_3[i]==output_wiener_time[i]:
#         bool_.append(True)
#     else:
#         bool_.append(False)

# print(bool_)
# print(list(output_noise))
# print(list(noise))

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output_wiener_time)
plt.title("22")

def signal_energy(signal):
    energy = 0.0
    for n in range(len(signal)):
        energy += math.pow(signal[n], 2)
    return energy/(len(signal))
# output = output.astype(n[3].dtype)

SNR_output = 10*math.log10(signal_energy(original)/signal_energy(output_noise))
SNR_input = 10*math.log10(signal_energy(original)/signal_energy(noise))

#-----------------------------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pylab as plt
import math
import cmath
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram
import wavfile

import warnings

warnings.filterwarnings('ignore')

N = 7
d = 0.08  # meter
c = 340  # m/s
# figure_counter = 0

theta_signal = math.pi / 4
theta_noise = 3 * math.pi / 4

path = "Material/MicArraySimulatedSignals/sensor_"
endpath = ".wav"

n = []
for i in range(7):
    Fs, data = read(path + str(i) + endpath)
    n.append(data[start:(end+1)])

samplerate, original = read("Material/MicArraySimulatedSignals/source.wav")
original = original[start:(end+1)]
# data *= 100
# original *= 100

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

output = []
idfts = []
for i in range(7):
    temp = []
    for k in range(dft_len):
        temp.append(dfts[i][k] * np.exp(-1j * 2 * math.pi * k * tn[N - 1 - i] / dft_len))  # m = tn[i]

    idfts.append(np.fft.ifft(temp))

for i in range(len(idfts[0])):
    sum = 0.0
    for j in range(7):
        sum += idfts[j][i]

    output.append((1 / 7) * sum)

output = np.array(output)
output = output.astype(int)
# output = list(output)

def signal_energy(signal):
    energy = 0.0
    for n in range(len(signal)):
        energy += math.pow(signal[n], 2)
    return energy/(len(signal))

diff = output - original
SNR_beam = 10*math.log10(signal_energy(original)/signal_energy(diff))

#-----------------------------------------------------------------------------------------------------------------------


print("SNR_beam: ", SNR_beam)
print("SNR_input: ", SNR_input)
print("SNR_wiener_output: ", SNR_output)


write("wiener_ouput.wav", samplerate, output_wiener_time.astype(n[3].dtype))
# print(list(output_wiener_time))
# print(list(n_3))

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output_wiener_time)
plt.title("output_wiener")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title("original")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)
plt.title("beam_output")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n_3)
plt.title("input")

plt.show()
