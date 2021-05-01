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
noise = output - original
def absolute(a):
    if a > 0:
        return a
    else:
        return (-1) * a
def signal_energy(signal):
    energy = 0.0
    print(signal)
    for n in range(len(signal)):
        energy += math.pow(signal[n], 2)
         
    return energy / len(signal)
# output = output.astype(n[3].dtype)


SNR = 20 * np.log10( signal_energy(output) / signal_energy(noise)) 
print(SNR)
 
plt.show()
