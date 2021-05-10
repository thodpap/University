import numpy as np
import matplotlib.pylab as plt
import math
import cmath
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram, welch
import librosa as lib

import warnings

warnings.filterwarnings('ignore')

N = 7
d = 0.04  # meter
c = 340  # m/s
figure_counter = 0

theta_signal = math.pi / 4
# theta_noise = 3 * math.pi / 4

path = "Material/MicArrayRealSignals/sensor_"
endpath = ".wav"


def read_from_files(path, endpath):
    n = []
    for i in range(7):
        data, y = lib.load(path + str(i) + endpath, sr=None)
        n.append(data)

    original, samplerate = lib.load("Material/MicArrayRealSignals/source.wav", sr=None)
    return samplerate, n, original


samplerate, n, original = read_from_files(path, endpath)
samplerate = 48000

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

# segments
seg_size = 1440  # 30 ms
number_of_segments = 2 * len(output) // seg_size - 1
window = np.hamming(seg_size)
length = len(original)

segments = []
for i in range(number_of_segments):
    temp = []
    for j in range(seg_size):
        if i == 0:
            temp.append(output[j] * window[j])
        else:
            temp.append(output[j + i * seg_size // 2] * window[j])
    segments.append(temp)

# welch in beam output
# noise = output[0:seg_size]
fft_num = 2 * seg_size
noise = segments[0]

f, S_noise = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)


def calculate_wiener_output(seg, noise_psd, fft_num):
    seg_dft = np.fft.fft(seg, n=fft_num)
    f, psd = welch(seg, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)

    Hw = []
    for k in range(len(psd)):
        Hw.append(1 - noise_psd[k] / psd[k])

    output_wiener = []
    for i in range(len(Hw)):
        output_wiener.append(seg_dft[i] * Hw[i])

    freqs = np.fft.fftfreq(len(output_wiener))

    output_wiener_time = np.fft.ifft(output_wiener, n=fft_num)
    f, S_output = welch(output_wiener_time, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)

    return output_wiener_time, output_wiener, freqs, f, S_output

def fill_signal_int(segments, number_of_segments, S_noise, fft_num):
    filtered_signal_int = []
    num = 0
    for i in range(number_of_segments):
        output_wiener_time, output_wiener, freqs, f, S_output = calculate_wiener_output(segments[i], S_noise, fft_num)
        filtered_signal_int.append(output_wiener_time)
    return filtered_signal_int

fill_signal_int = fill_signal_int(segments, number_of_segments, S_noise, fft_num)

def fill_list(start, size, values):
    temp = []
    last = start + len(values)

    for i in range(start):
        temp.append(0)
    for i in range(start, min(last, size)):
        temp.append(values[i - start])
    for i in range(min(last, size), size):
        temp.append(0)
    return temp


def create_lists(segments, figure_counter):
    def sum_lists(segments):
        temp = []
        for j in range(len(segments[0])):
            sum = 0
            for i in range(len(segments)):
                sum += segments[i][j]
            temp.append(sum)
        return temp

    temp = []
    start = 0
    for i in range(len(segments)):
        temp.append(fill_list(start, length, segments[i]))
        start += seg_size // 2

    return sum_lists(temp)


filtered_output = create_lists(filtered_signal_int, figure_counter)
filtered_output = np.array(filtered_output) 

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n[3])
plt.title('n[3]')
plt.savefig("Figures/2_2/B/n[3].png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(filtered_output)
plt.title('Filtered_output')
plt.savefig("Figures/2_2/B/filtered_output.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title('original')
plt.savefig("Figures/2_2/B/original.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)
plt.title('output')
plt.savefig("Figures/2_2/B/output.png")

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(filtered_output, Fs=samplerate)
plt.title('filtered_output')
plt.ylim([0, 23800])
plt.savefig("Figures/2_2/B/filtered_output_spec.png")

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(n[3], Fs=samplerate)
plt.title('n[3]')
plt.ylim([0, 23800])
plt.savefig("Figures/2_2/B/n[3].spec.png")

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(original, Fs=samplerate)
plt.title('original')
plt.ylim([0, 23800])
plt.savefig("Figures/2_2/B/original_spec.png")

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(output, Fs=samplerate)
plt.title('output')
plt.ylim([0, 23800])
plt.savefig("Figures/2_2/B/output_spec.png")
  
write("beamformer_output.wav", samplerate, np.real(output).astype(float))
write("beamformer_weiner_output.wav", samplerate, np.real(filtered_output).astype(float))

# 3

L = 1440


def signal_power(signal):
    energy = 0.0
    for n in range(len(signal)):
        energy += math.pow(abs(signal[n]), 2)

    return energy / len(signal)


def SSNR(signal, noise_power):
    def calculate_ssnr(signal, noise_power, M):
        SSNR = []
        for i in range(M):
            cons = (signal_power(signal[i * L:i * L + L]) - noise_power) / noise_power
            if cons <= 0:
                continue
            res = 10 * np.log10(cons)
            if res >= 35:
                res = 35
            if res <= -20:
                continue
            SSNR.append(res)
        return SSNR

    L = 1440
    M = len(signal) // L
    SSNR = sum(calculate_ssnr(signal, noise_power, M)) / M

    return SSNR


noise_power_1 = signal_power(n[3][0:L])
SSNR_n_3 = SSNR(n[3], noise_power_1)
noise_power_2 = signal_power(segments[0])
SSNR_filtered_output = SSNR(filtered_output, noise_power_2)
noise_power_3 = signal_power(output[0:L])
SSNR_output = SSNR(output, noise_power_3)

print("SSNR_n_3: ", SSNR_n_3)
print("SSNR_output: ", SSNR_output)
print("SSNR_filtered_output: ", SSNR_filtered_output)

# 4

SSNRs_input = []
for n_i in n:
    noise_power_i = signal_power(n_i[0:L])
    SSNRs_input.append(SSNR(n_i, noise_power_i))

print("Average SSNR's: ", sum(SSNRs) / 7)

plt.show()
