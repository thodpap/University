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
 

# segments
seg_size = 1440  # 30 ms
number_of_segments = 2 * len(output) // seg_size - 1
window = np.hamming(seg_size)
length = len(original)

noise = []
for i in range(seg_size):
    noise.append(output[i])#n[3][i] - original[i])

segments = []
for i in range(number_of_segments):
    temp = []
    for j in range(seg_size):
        if i == 0:
            temp.append(output[j] * window[j])
        else:
            temp.append(output[j + i * seg_size // 2] * window[j])
    segments.append(temp)

# print(len(segments) * len(segments[2]))
# welch in beam output

fft_num = seg_size

f, S_noise = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)


# print(len(S_noise))

def wiener(seg, noise_psd, figure_counter, num):
    # print(len(seg))
    f, psd = welch(seg, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
    # print(len(psd))
    Hw_seg = []
    for k in range(len(psd)):
        Hw_seg.append(1 - noise_psd[k] / psd[k])

    seg_filtered = []
    dft_seg = np.fft.fft(seg, n=fft_num)
    for i in range(len(psd)):
        seg_filtered.append(dft_seg[i] * Hw_seg[i])
    return np.fft.ifft(seg_filtered, n=fft_num)
    # wiener_time = np.fft.ifft(Hw_seg)
    # wiener_time = np.real(wiener_time)
    # return np.convolve(wiener_time, seg)


filtered_signal_int = []
# print(len(segments[2]))
num = 0
for i in range(number_of_segments):
    if i == 50:
        # figure_counter += 1
        num = num + 1
    else:
        num = 0
    filtered_signal_int.append(list(wiener(segments[i], S_noise, figure_counter, num)))


def fill_list(start, size, values):
    temp = []
    last = start + len(values)
    # print(start, last, size)
    for i in range(start):
        temp.append(0)
    for i in range(start, min(last, size)):
        temp.append(values[i - start])
    for i in range(min(last, size), size):
        temp.append(0)
    return temp


# print(fill_list(3, 6, 7, [1, 2, 3, 4]))

def sum_lists(segments):
    temp = []
    for j in range(len(segments[0])):
        sum = 0
        for i in range(len(segments)):
            sum += segments[i][j]
        temp.append(sum)
    return temp


def create_lists(segments, figure_counter):
    temp = []
    start = 0
    for i in range(len(segments)):
        temp.append(fill_list(start, length, segments[i]))
        start += seg_size // 2
        # if i == 100 or i==101  or i==105:
        #     plt.figure(i)
        #     plt.plot(temp[i])
    # print(temp[2])
    return sum_lists(temp)


filtered_output = create_lists(filtered_signal_int, figure_counter)
figure_counter += 1
plt.figure(figure_counter)
plt.plot(filtered_output)

# plt.show()

# print(len(filtered_signal_int[2]))
figure_counter += 1
plt.figure(figure_counter)
plt.plot(filtered_signal_int[0])
# filtered_signal_int = []
# for i in range(len(filtered_signal)):
#     temp = [int(i.real) for i in filtered_signal[i]]
#     filtered_signal_int.append(temp)


# print(len(filtered_signal_int) * len(filtered_signal_int[2]))


# filtered_signal = int(filtered_signal)
# for i in range(len(filtered_signal)):
#     filtered_signal_int.append(filtered_signal.astype(int))


# print(list(filtered_signal_int[2]))


# figure_counter += 1
# plt.figure(figure_counter)
# plt.plot(filtered_signal_int[2])
## over-lap add


def over_lap_add(segmentss, seg_size):
    signal = []
    for i in range(len(segmentss)):
        pass
        # if i == 0:
        #     for j in range(seg_size // 2):
        #         signal.append(segmentss[i][j])
        #     continue
        # else:

        # start = i*seg_size+seg_size//2
        # while True:
        #     for i in range(start):

        # for j in range(seg_size):
        #     if j < seg_size // 2:
        #         signal.append(segmentss[i][j] + segmentss[i - 1][j + seg_size // 2])
        #     else:
        #         break

        # elif i == 2:
        #     for j in range(seg_size):
        #         if j < seg_size // 2:
        #             signal.append(segmentss[i][j] + segmentss[i - 1][j + seg_size // 2] + segmentss[i-2][j+2*seg_size//2])
        #         else:
        #             break
        #
        # elif i == 3:
        #     for j in range(seg_size):
        #         if j < seg_size // 2:
        #             signal.append(segmentss[i][j] + segmentss[i - 1][j + seg_size // 2] + segmentss[i-2][j+2*seg_size//2] + segmentss[i-3][j+3*seg_size//2])
        #         else:
        #             break
        # else:
        #     for j in range(seg_size):
        #         if j < seg_size // 2:
        #             signal.append(segmentss[i][j] + segmentss[i - 1][j + seg_size // 2] + segmentss[i-2][j+2*seg_size//2] + segmentss[i-3][j+3*seg_size//2])# + segmentss[i-4][j+4*seg_size//2])
        #         else:
        #             break
    return signal


flat_filtered_signal = over_lap_add(filtered_signal_int, seg_size)

# print(flat_filtered_signal)

# figure_counter += 1
# plt.figure(figure_counter)
# plt.plot(flat_filtered_signal)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)

plt.show()


filtered_output = np.array(filtered_output)
flat_filtered_signal = np.array(flat_filtered_signal)
write("beam_former_wiener_ouput.wav", samplerate, filtered_output.astype(int))
