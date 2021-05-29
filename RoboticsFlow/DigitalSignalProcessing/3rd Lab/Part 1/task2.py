import numpy as np
import matplotlib.pylab as plt
import math
import cmath
import librosa as lib
from numpy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram
import random
import gc
import sys

gc.collect()

figure_counter = 0

path = "../music.wav"
# path = "DSP21_Lab3_material/dsp21_lab3_material/music.wav"


# 1.1
def read_from_files(path):
    original, samplerate = lib.load(path, sr=44100)
    return samplerate, original


samplerate, original = read_from_files(path)

def window_signal(original, window, length):
    signal = []
    start = 0
    while start + length < len(original):
        temp = []
        for n in range(length):
            temp.append(original[start + n] * window[n])
        signal.append(temp)
        start += length
    return signal


N = 512
window = np.hanning(N)
window_signal = window_signal(original, window, N)


def hx(k, M):
    L = 2 * M
    return [np.sin((n + 1 / 2) * math.pi / L) * math.sqrt(2 / M) * np.cos(
            (2 * n + M + 1) * (2 * k + 1) * math.pi / (4 * M)) for n in range(L)]
    


def gk(hx, k, M): 
    L = 2 * M
    return [ hx[k][L - 1 - n] for n in range(L)] 


M = 32
hk_ = [ hx(k, M) for k in range(M)]
gk_ = [ gk(hk_, k, M) for k in range(M)] 

figure_counter += 1
plt.figure(figure_counter)
plt.plot(hk_[10])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(gk_[10])

filtered_signal = [ [ np.convolve(hk_[k], window_signal[i]) for k in range(M)] for i in range(len(window_signal))]
  
figure_counter += 1
plt.figure(figure_counter)
plt.title("windowed")
plt.plot(window_signal[10])

figure_counter += 1
plt.figure(figure_counter)
plt.title("filtered")
plt.plot(filtered_signal[10][10])
# plt.show()

def decimate(signal, factor):
    temp = []
    for i in range(len(signal)):
        if i % factor == 0:
            temp.append(signal[i])
    return temp

decimated_filtered_signal = [ [ decimate(filtered_signal[i][k], M) for k in range(M)]  for i in range(len(window_signal))] 

figure_counter += 1
plt.figure(figure_counter)
plt.title("decimated")
plt.stem(decimated_filtered_signal[10][10])
# plt.show()

T_g = np.load("T_g_i.npy")

L = 2 * M


def f(k):
    return ((2 * k - 1) * samplerate * math.pi / (L) - samplerate * math.pi / (L),
            (2 * k - 1) * samplerate * math.pi / (L) + samplerate * math.pi / (L))


R = 2 ** 16


def newTg(k, T_g):
    f_ = f(k)
    # print(f_, i, k)
    temp = []
    for i in range(len(T_g)):
        f_i = samplerate * 2 * math.pi * i / N
        if f_[0] <= f_i <= f_[1]:
            temp.append(T_g[i])
    return (R / min(temp))


Bk = [ [math.ceil(np.log2(newTg(k, T_g[i])) - 1) for k in range(1, M + 1)] for i in range(len(window_signal))]  

delta = []

print(len(decimated_filtered_signal), print(len(decimated_filtered_signal[0])))

for i in range(len(decimated_filtered_signal)):
    temp = []
    min_temp = []
    for k in range(M):
        range_ = max(decimated_filtered_signal[i][k]) - min(decimated_filtered_signal[i][k])
        temp.append(range_ / (math.pow(2, Bk[i][k])))
    delta.append(temp)


# def quantization(segment, delta, num, i, k):
#     def find_nearest(array, value):
#         array = np.asarray(array)
#         idx = (np.abs(array - value)).argmin()
#         return array[idx]
#
#     # print(segment)
#     # segment = list(segment)
#     temp = [abs(x) for x in segment]
#     min_value = (min(temp))
#     # min_value = segment[minimum]
#
#     num_of_levels = 2 ** num
#     levels = []
#
#     if min_value < 0:
#         range_ = num_of_levels // 2 - 1
#     else:
#         range_ = num_of_levels // 2
#
#     for p in range(range_):
#         levels.append(min_value - p * delta)
#
#     levels = levels[::-1]
#
#     for l in range(num_of_levels - range_):
#         levels.append(min_value + l * delta)
#
#     if i == 10 and k == 10:
#         print(levels)
#
#     for q in range(len(segment)):
#         segment[q] = find_nearest(levels, segment[q])
#
#     for n in range(len(segment)):
#         if segment[n] not in levels:
#             print("failed")
#
#     return segment

def quantization(x, Delta_s, b):
    newSig = []

    for i in range(len(x)):
        bool = 0
        for k in range(2 ** (b - 1)):
            if k * Delta_s <= abs(x[i]) <= (k + 1) * Delta_s:
                if x[i] > 0:
                    newSig.append((0.5 + k) * Delta_s)
                elif x[i] < 0:
                    newSig.append((-0.5 - k) * Delta_s)
                else:
                    newSig.append(0.0)
                bool = 1
                break
        if bool == 0:
            if x[i] >= 0:
                newSig.append((2 ** (b - 1) - 0.5) * Delta_s)
            else:
                newSig.append(-(2 ** (b - 1) - 0.5) * Delta_s)
    return newSig

print("Bk len is:", len(Bk), len(Bk[0]))
print("Bk len is:", len(decimated_filtered_signal), len(decimated_filtered_signal[0]))
print("Bk len is:", len(delta), len(delta[0]))


quantized_signal = [ [ quantization(decimated_filtered_signal[i][k], delta[i][k], Bk[i][k]) 
                        for k in range(len(decimated_filtered_signal[i]))] 

                        for i in range(len(decimated_filtered_signal))] 

figure_counter += 1
plt.figure(figure_counter)
plt.stem(quantized_signal[10][10])
# plt.show()
# print(delta[10][10])



def test_quantization(segment, delta, num, i, k):
    def find_nearest(array, value):
        array = np.array(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    # print(segment)
    # segment = list(segment)
    # delta = (max(segment) - min(segment))/(2**num)
    # temp = [abs(x) for x in segment]
    min_value = 0
    # min_value = segment[minimum]

    num_of_levels = 2 ** num
    levels = [min_value]

    # if min_value < 0:
    #     range_ = num_of_levels // 2 - 1
    # else:
    #     range_ = num_of_levels // 2 + 1

    for p in range(num_of_levels//2 - 1):
        levels.append(min_value - p * delta)

    # levels = levels[::-1]

    for j in range(num_of_levels//2 - 1):
        levels.append(min_value + j * delta)

    if i == 10 and k == 10:
        print(levels)

    for q in range(len(segment)):
        segment[q] = find_nearest(levels, segment[q])
        # print(segment[i])

    for n in range(len(segment)):
        if segment[n] not in levels:
            print("failed")

    return segment


test_Bk = 8
original = list(original)
# test_delta = (max(original) - min(original))/(2**test_Bk)
test_quantized = []
for i in range(len(decimated_filtered_signal)):
    temp = []
    test_delta = (max(window_signal[i]) - min(window_signal[i]))/(2**test_Bk)
    # print(len(decimated_filtered_signal[i]), i)
    for k in range(len(decimated_filtered_signal[i])):
        if i == 10 and k == 10:
            print(test_delta)
        temp.append(test_quantization(decimated_filtered_signal[i][k], test_delta, test_Bk, i, k))

    test_quantized.append(temp)

figure_counter += 1
plt.figure(figure_counter)
plt.stem(test_quantized[10][10])


interpolated = []

# for q in quantized_signal:
#     temp = []
#     for k in q:
#         temp2 = np.zeros(M * len(k) + 1)
#         for i, l in enumerate(k):
#             temp[M * i] = l
#         temp.append(list(temp2))
    # interpolated.append(temp)

for q in quantized_signal:
    temp2 = []
    for k in q:
        temp = []
        for l in k:
            temp.append(l)
            for m in range(M-1):
                temp.append(0)

        temp2.append(temp)

    interpolated.append(temp2)


# for i in range(len(quantized_signal)):
#     temp = []
#     for k in range(len(quantized_signal[i])):
#         temp2 = []
#         for l in range(len(quantized_signal[i][k])):
#             temp2.append(quantized_signal[i][k][l])
#             for m in range(M-1):
#                 temp2.append(0)
#
#         temp.append(temp2)
#
#     interpolated.append(temp)

print(len(interpolated[0]), len(interpolated[0][0]))

figure_counter += 1
plt.figure(figure_counter)
plt.plot(interpolated[10][10])

# plt.show()



last_filtered_signal = [ [ np.convolve(interpolated[i][k], gk_[k]) for k in range(len(interpolated[i]))] 
                             for i in range(len(interpolated))] 

# segment_again = []
# for i in range(len(window_signal)):
#     temp = []
#     for j in range(len(interpolated[i][0])):
#         for k in range(M):
#             temp.append(interpolated[i][k][j])
#
#     segment_again.append(temp)

print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", len(interpolated), len(interpolated[0]), len(interpolated[0][0]))

#
# def fill_list(start, size, values):
#     temp = []
#     last = start + len(values)
#
#     for i in range(start):
#         temp.append(0)
#     for i in range(start, min(last, size)):
#         temp.append(values[i - start])
#     for i in range(min(last, size), size):
#         temp.append(0)
#     return temp


figure_counter += 1
plt.figure(figure_counter)
plt.plot(last_filtered_signal[10][10])

# plt.show()

# size = len(interpolated[0])
print("GEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE: ", len(last_filtered_signal), len(last_filtered_signal[0]), last_filtered_signal[0][M-1][600])
print("GEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE: ", len(last_filtered_signal), len(last_filtered_signal[0]), len(last_filtered_signal[1][5]))
summer = []



for l in last_filtered_signal:
    temp = np.zeros(639)
    for k in l: 
        for n, c in enumerate(k):
            temp[n] += c

    temp = list(temp)
    summer.append(temp) 

figure_counter += 1
plt.figure(figure_counter)
plt.plot(summer[10], label="summer")
plt.plot(window_signal[10], label="original")
plt.legend()


figure_counter += 1
plt.figure(figure_counter)
plt.plot(summer[50], label="summer")
plt.plot(window_signal[50], label="original")
plt.legend()


def overlap(my_list, length, tot_length, seg_length):
    start = 0
    temp = np.zeros(tot_length)

    for l in my_list:
        if start >= tot_length - seg_length:
            return temp
        for i in range(length):
            if start + i > tot_length:
                break
            temp[start+i] += l[i]

        start += seg_length
    return temp
 

sum_overlap_add = overlap(summer, len(summer[0]), len(original), N)


figure_counter += 1
plt.figure(figure_counter)
plt.plot(sum_overlap_add)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)

 
sum_overlap_add = np.array(sum_overlap_add)
write("output.wav", samplerate, np.array(sum_overlap_add / np.max(np.abs(sum_overlap_add))* 65535, dtype = np.int16)) 


print(len(original), sys.getsizeof(original[0]))
print(len(sum_overlap_add), sys.getsizeof(sum_overlap_add[0]))
plt.show()
