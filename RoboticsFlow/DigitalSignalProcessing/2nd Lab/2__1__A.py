import numpy as np
import matplotlib.pylab as plt
import math
import librosa
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
figure_counter = 0

theta_signal = math.pi / 4
theta_noise = 3 * math.pi / 4

path = "Material/MicArraySimulatedSignals/sensor_"
endpath = ".wav"

n = []
for i in range(7):
    Fs, data, bits = wavfile.read(path + str(i) + endpath)
    n.append(data) 

samplerate, original, bits = wavfile.read("Material/MicArraySimulatedSignals/source.wav")
 
 
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
    sum  = 0.0
    for j in range(7):
        sum += idfts[j][i]

    output.append( (1 / 7) * sum)

print("00: ", output[5000])
output = np.array(output)
original = np.array(original)

diff = output - original
 
write("beam_former_ouput.wav", samplerate, diff.astype(n[3].dtype))

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
plt.plot(np.arange(len(n[3])), list(n[3]))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("n[3] signal")

f3, t3, Sxx3 = spectrogram(n[3], fs=48000)
figure_counter += 1
plt.figure(figure_counter)
plt.pcolormesh(t3, f3, Sxx3)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of n[3] signal")

figure_counter += 1
plt.figure(figure_counter)
fft3 = fft(list(n[3]))
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
output = output.astype(n[3].dtype)
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

# 3)

# def signaltonoise(a, axis=0, ddof=0):
#     a = np.asanyarray(a)
#     m = a.mean(axis)
#     sd = a.std(axis=axis, ddof=ddof)
#     return np.where(sd == 0, 0, m/sd)
#
#
# SNR_n3 = signaltonoise(n_3)
# SNR_bfoutput = signaltonoise(output)
#
# print(SNR_bfoutput)
# print(SNR_n3)

noise1 = []
noise2 = []

output = output.astype(n[3].dtype)
print(output)

for i in range(len(original)):
    noise1.append(n[3][i] - original[i])
    noise2.append(output[i] - original[i])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(noise2)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)


# def energy(x):
#     temp1 = []
#     for j in range(len(x)):
#         if x[j]*x[j] <= 0:
#             temporary = (-1)*x[j]*x[j]
#         else:
#             temporary = x[j]*x[j]
#         temp1.append(temporary)
#     return sum(temp1)/len(x)


def energy(x):
    print(np.sum(np.abs(x) ** 2) * (1/len(x)))
    return np.sum(np.abs(x) ** 2) * (1/len(x))

def SNR(s1,s2):
    return 10*np.log10(energy(s1)/energy(s2))

SNR_output = SNR(output, noise2)
SNR_n_3 = SNR(n[3],noise1)
print(SNR_output)
print(SNR_n_3)

# SNR_n3 = energy(n_3)/energy(noise1)
# SNR_output = energy(output)/energy(noise2)
#
# print("SNR n_3: ", SNR_n3)
# print("SNR output: ", SNR_output)

plt.show()
