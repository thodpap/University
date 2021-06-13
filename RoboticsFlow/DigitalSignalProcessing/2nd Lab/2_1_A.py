import numpy as np
import matplotlib.pylab as plt
import math
import cmath
import librosa as lib
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram 

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
 
def read_from_files(path, endpath):
    n = []
    for i in range(7):
        data, y = lib.load(path + str(i) + endpath, sr=None)
        n.append(data)

    original, samplerate = lib.load("Material/MicArraySimulatedSignals/source.wav", sr=None)
    return samplerate, n, original


samplerate, n, original = read_from_files(path, endpath)


def time_delays():
    tn = []
    for i in range(7):
        tn.append(((-(i - (N - 1) / 2) * d * math.cos(theta_signal)) / c) * samplerate)
    return np.array(tn)


tn = time_delays()
my_len = len(n[0])  # length of all signals
 
def calculate_output(n, tn):
    def calculate_dfts(n):
        dfts = []
        for i in range(7):
            dfts.append(list(fft(n[i])))
        return np.array(dfts)

    def calculate_idfts(dfts, dft_len):
        idfts = []
        for i in range(7):
            temp = []
            for k in range(dft_len):
                temp.append(dfts[i][k] * np.exp(-1j * 2 * math.pi * k * tn[N - 1 - i] / dft_len))  # m = tn[i]

            idfts.append(np.fft.ifft(temp))
        return idfts

    def find_output(idfts):
        output = []
        for i in range(len(idfts[0])):
            sum = 0.0
            for j in range(7):
                sum += idfts[j][i]

            output.append((1 / 7) * sum)
        return output

    dfts = calculate_dfts(n)
    dft_len = len(dfts[0])
    idfts = calculate_idfts(dfts, dft_len)

    return find_output(idfts)


output = np.array(calculate_output(n, tn)) 

write("sim_ds.wav", samplerate, output.astype(n[3].dtype))

def SNR(original, output):
    def signal_energy(signal):
        energy = 0.0
        for n in range(len(signal)):
            energy += math.pow(abs(signal[n]), 2)

        return energy

    noise = output - original
    SNR = 10 * np.log10(signal_energy(original) / signal_energy(noise))
    return SNR


SNR = SNR(original, output)
print("SNR: ", SNR)



###################################################
# Plots                                           #
###################################################
 

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(original)), original)
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("source signal")
# plt.savefig("Figures/2_1/A/original.png")
 
figure_counter += 1
plt.figure(figure_counter)
plt.specgram(original, Fs=samplerate)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of source signal")
# plt.savefig("Figures/2_1/A/original_spec.png")

figure_counter += 1
plt.figure(figure_counter)
fft_source = fft(list(original))
plt.plot(np.arange(len(fft_source)), np.real(fft_source))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of source signal")
# plt.savefig("Figures/2_1/A/fft_source.png")

# b)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(n[3])), list(n[3]))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("n[3] signal")
# plt.savefig("Figures/2_1/A/n_3.png")
 
figure_counter += 1
plt.figure(figure_counter)
plt.specgram(n[3], Fs=samplerate)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of n[3] signal")
# plt.savefig("Figures/2_1/A/n_3_spec.png")

figure_counter += 1
plt.figure(figure_counter)
fft3 = fft(list(n[3]))
plt.plot(np.arange(len(fft3)), np.real(fft3))
plt.xlabel("discrete time")
# plt.savefig("Figures/2_1/A/fft3.png")

# c)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(output)), output)
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("output signal") 
# plt.savefig("Figures/2_1/A/output.png")

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(output, Fs=samplerate)
plt.ylim([0, 23800])
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of output signal")
# plt.savefig("Figures/2_1/A/output_spec.png")

figure_counter += 1
plt.figure(figure_counter)
fft_output = fft(list(output))
plt.plot(np.arange(len(fft_output)), np.real(fft_output))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of output signal")
plt.ylabel("amplitude") 
# plt.savefig("Figures/2_1/A/fft_output.png")

plt.show()
