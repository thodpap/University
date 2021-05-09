import numpy as np
import matplotlib.pylab as plt
import math
import cmath
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram 
import librosa as lib  

N = 7
d = 0.04  # meter
c = 340  # m/s

figure_counter = 0

theta_signal = math.pi / 4
# theta_noise = 3 * math.pi / 4

path = "Material/MicArraySimulatedSignals/sensor_"
endpath = ".wav" 

def read_from_files(path, endpath):
    n = []
    for i in range(7):
        data, y = lib.load(path + str(i) + endpath, sr=None)
        n.append(data)
    print(n)
    original, samplerate = lib.load("Material/MicArraySimulatedSignals/source.wav", sr=None)
    return samplerate, n, original


samplerate, n, original = read_from_files(path, endpath) 
 
def time_delays():
    tn = []
    for i in range(7):
        tn.append((-(i - (N - 1) / 2) * d * math.cos(theta_signal) / c) * samplerate)
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
original = np.array(original)

write("beam_former_ouput.wav", samplerate, output.astype(n[3].dtype))
  
output = np.array(output)
original = np.array(original) 

# write("beam_former_ouput.wav", samplerate, output.astype(n_3.dtype))
 
#3)
def SSNR(original, signal):
    def calculate_ssnr(signal, noise, M):
        def signal_energy(signal):
            energy = 0.0
            for n in range(len(signal)):
                energy += math.pow(abs(signal[n]), 2)

            return energy 

        SSNR = [] 
        for i in range(M):
            cons = signal_energy(signal[i*L:(i*L+L)]) / signal_energy(noise[i*L:(i*L+L)]) 

            res = 10*np.log10(cons)
            if res >= 35:
                res = 35
            if res <= -20:
                continue

            SSNR.append(res)
        return SSNR

    L = 1440  
    noise = output - original 
    M = len(signal)//L
    SSNR = sum(calculate_ssnr(signal, noise, M)) / M 

    return SSNR

SSNR_n_3 = SSNR(original, n[3])
SSNR_output = SSNR(original, output) 
print("SSNR_n_3: ", SSNR_n_3 )
print("SSNR_output: ", SSNR_output) 
 


###################################################
# Plots                                           #
###################################################



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
fft_source = np.array(fft(original), dtype="complex_")
plt.plot(np.arange(len(fft_source)), np.real(fft_source))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of source signal") 
 

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
plt.plot(np.arange(len(fft3)), np.real(fft3))
plt.xlabel("discrete time")  

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(output)), np.real(output))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("output signal")

 
f_output, t_output, Sxx_output = spectrogram(output, fs=48000, return_onesided=False)
figure_counter += 1 
plt.figure(figure_counter)
plt.pcolormesh(t_output, f_output, Sxx_output)
plt.xlabel("discrete time")
plt.ylabel("frequencies")
plt.title("spectogram of output signal")

figure_counter += 1
plt.figure(figure_counter)
fft_output = fft(list(output))
plt.plot(np.arange(len(fft_output)), np.real(fft_output))
plt.xlabel("discrete time")
plt.ylabel("amplitude")
plt.title("fft of output signal")
plt.ylabel("amplitude")

plt.show()