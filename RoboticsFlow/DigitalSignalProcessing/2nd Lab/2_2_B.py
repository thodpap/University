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

write("4.wav", samplerate, output.astype(n[3].dtype))

# segments
seg_size = 1440  # 30 ms
number_of_segments = 2 * len(output) // seg_size - 1
window = np.hamming(seg_size)
length = len(original)

noise = output[0:seg_size]

def get_segments(signal, window, number_of_segments, seg_size):
    segments = []
    start = 0

    while start + seg_size < len(signal):
        temp = []
        for i in range(seg_size):
            temp.append(signal[start + i] * window[i])
        start += seg_size // 2
        segments.append(temp)
    return segments

segments = get_segments(output, window, number_of_segments, seg_size)

 
# welch in beam output

fft_num = 2 * seg_size 
f, S_noise = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num) 

def calculate_wiener_output(seg, noise_psd, fft_num):
    seg_dft = np.fft.fft(seg, n=fft_num)
    f, psd = welch(seg, detrend=False, return_onesided=False, fs=48000, nfft=fft_num) 

    output_wiener = []  
    for i in range(len(seg_dft)): 
        output_wiener.append(seg_dft[i]* (1 - noise_psd[i] / psd[i]))   
    freqs = np.fft.fftfreq(len(output_wiener))  

    output_wiener_time = np.fft.ifft(output_wiener, n=fft_num)    
    f, S_output = welch(output_wiener_time, detrend=False, return_onesided=False, fs=48000, nfft=fft_num) 

    return output_wiener_time, output_wiener, freqs, f, S_output 
 

filtered_signal_int = [] 
num = 0
for i in range(number_of_segments):  
    output_wiener_time, output_wiener, freqs, f, S_output = calculate_wiener_output(segments[i], S_noise, fft_num)
    filtered_signal_int.append(output_wiener_time)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(filtered_signal_int[1])

def get_original(segments):
    sums = np.zeros(len(original))
    start = 0
    count = 0
    while start + seg_size < len(original):
        for i, s in enumerate(segments[count]):
            if start + i >= len(original):
                break

            sums[start + i] += s

        start += seg_size // 2
        count += 1
    return sums 

filtered_output = get_original(filtered_signal_int)  

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n[3]) 
plt.title('n[3]')


figure_counter += 1
plt.figure(figure_counter)
plt.plot(filtered_output) 
plt.title('Filtered_output')

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title('original')

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)
plt.title('output')

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(filtered_output, Fs=samplerate) 
plt.title('filtered_output')
plt.ylim([0,23800])

figure_counter += 1
plt.figure(figure_counter)
plt.specgram(original, Fs=samplerate)
plt.title('original')
plt.ylim([0,23800])



output = np.array(output)
filtered_output = np.array(filtered_output)

write("4.wav", samplerate, output.astype(n[3].dtype)) 
write("5.wav", samplerate, filtered_output.astype(n[3].dtype))



# 3 

def SSNR(signal):
    def signal_power(signal):
        energy = 0.0
        for n in range(len(signal)):
            energy += math.pow(abs(signal[n]), 2)

        return energy/len(signal)

    def calculate_ssnr(signal, noise_power, M): 
        SSNR = [] 
        for i in range(M):
            cons = (signal_power(signal[i*L:i*L+L])-noise_power)/noise_power
            if cons <= 0:
                continue
            res = 10*np.log10(cons)
            if res >= 35:
                res = 35
            if res <= -20:
                continue
            SSNR.append(res)
        return SSNR

    L = 1440  
    noise_power = signal_power(signal[0:L])
    M = len(signal)//L
    SSNR = sum(calculate_ssnr(signal, noise_power, M)) / M 

    return SSNR

SSNR_n_3 = SSNR(n[3])
SSNR_filtered_output = SSNR(filtered_output) 
SSNR_output = SSNR(output)

print("SSNR_n_3: ", SSNR_n_3 )
print("SSNR_output: ", SSNR_output)  
print("SSNR_filtered_output: ", SSNR_filtered_output)

# 4

SSNRs = [] 
for n_i in n:
    SSNRs.append(SSNR(n_i)) 

print("Average SSNR's: ", sum(SSNRs)/7)

plt.show()