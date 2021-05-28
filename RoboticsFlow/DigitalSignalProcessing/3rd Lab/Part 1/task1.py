import numpy as np
import matplotlib.pylab as plt
import math
import cmath
import librosa as lib
from numpy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram
import random

figure_counter = 0

path = "../music.wav"
path = "DSP21_Lab3_material/dsp21_lab3_material/music.wav"


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



def power_spectrum(window_signal, length):
    def calculate_P(signal):
        return 10 * np.log10(abs(fft(signal, n=len(signal))) ** 2) + 90.302

    return [calculate_P(sig)[0:(length // 2)+1] for sig in window_signal]


def calculate_S_T_k(power_spectrum, length):
    def S_T_k(P, k):
        def D_k(k):
            if 2 < k < 63:
                return [2]
            d_k = []
            if 63 <= k < 127:
                for i in range(2, 4):
                    d_k.append(i)
            if 127 <= k <= 250:
                for i in range(2, 7):
                    d_k.append(i)
            return d_k
            # return "There was an error"

        if 3 <= k <= 250:
            d_k = D_k(k)
            # if d_k == 2: # and len(d_k) == 1:
            #     print("aaaaa: ", d_k)
            #     return (P[k] > P[k + 1] and P[k] > P[k - 1] and (P[k] > P[k + d_k] + 7) and (P[k] > P[k - d_k] + 7))
            # else:
            res = []
            bool = True
            for i in range(len(d_k)):
                if not(P[k] > P[k + 1] and P[k] > P[k - 1] and P[k] > (P[k + d_k[i]] + 7) and P[k] > (P[k - d_k[i]] + 7)):
                    bool = False
            return bool
        else:
            return 0

    return [[S_T_k(P, k) for k in range(length // 2 - 6)] for P in power_spectrum]


def calculate_P_TM(power_spectrum, S_T, length):
    P_TM = []
    for i, p in enumerate(power_spectrum):
        temp = []
        for k in range(length // 2 - 6):
            if S_T[i][k] != 0:
                temp.append(10 * np.log10(math.pow(10, (0.1 * p[k - 1])) + math.pow(10, (0.1 * p[k])) + math.pow(10, (0.1 * p[k + 1]))))
            else:
                temp.append(0)
        P_TM.append(temp)
    return P_TM


N = 512
window = np.hanning(N)
window_signal = window_signal(original, window, N)
# figure_counter += 1
# plt.figure(figure_counter)
# plt.plot(window_signal[10])
# plt.plot(original[10*512:10*512+513])
power_spectrum = power_spectrum(window_signal, N)

# print(power_spectrum[10])
# figure_counter += 1
# plt.figure(figure_counter)
# plt.stem(power_spectrum[10])

S_T = calculate_S_T_k(power_spectrum, N)

# for i in S_T:
#     temp = []
#     for k in i:
#         if isinstance(k, list):
#             for j in k:
#                 temp.append(j)
#         else:
#             temp.append(k)
#     S_T_new.append(temp)

# print(len(S_T_new))

# print(S_T[10])
P_TM = calculate_P_TM(power_spectrum, S_T, N)
# print((P_TM[10]))

P_NM = np.load("DSP21_Lab3_material/dsp21_lab3_material/P_NM.npy")
P_NMc = np.load("DSP21_Lab3_material/dsp21_lab3_material/P_NMc.npy")
P_TMc = np.load("DSP21_Lab3_material/dsp21_lab3_material/P_TMc.npy")


# print(list(P_TMc))
P_TMc = np.transpose(P_TMc)
P_NMc = np.transpose(P_NMc)
# P_TMc = P_TMc[::-1]

print("aaaaaaaaaaaaaaa ", len(P_TMc[10]), len(P_NMc[10]))

# print(list(P_TMc[50]))
# print(P_TM[50])
figure_counter += 1
plt.figure(figure_counter)
plt.stem((P_TMc[10]))
plt.stem(P_TM[10])

# def is_equal(list1, list2, k):
#     bool = True
#     # print(len(list1))
#     # print(len(list2))
#     for i in range(len(list1)):
#         if list1[i] != list2[i]:
#             bool = False
#     return bool
#
# bool = False
# for i in range(len(P_TM)):
#     for j in range(len(P_TM)):
#         if is_equal(P_TM[i], P_TMc[j], i):
#                 bool = True
#                 print(i, j)
#
#
# print(bool)


figure_counter += 1
plt.figure(figure_counter)
plt.stem((P_TM[10]), label="original")


def b(i):
    cons = i*samplerate / N
    return 13 * np.arctan(0.00076 * cons) + 3.5 * np.arctan((cons / 7500) ** 2)


def D_b(i, j):
    return b(i) - b(j)


def SF(P_xM, i, j):
    def D_b(i, j):
        return b(i) - b(j)
    D_b = D_b(i, j)

    if -3 <= D_b < -1:
        return 17 * D_b - 0.4 * P_xM[j] + 11
    if -1 <= D_b < 0:
        return (0.4 * P_xM[j] + 6) * D_b
    if 0 <= D_b < 1:
        return -17 * D_b
    if 1 <= D_b < 8:
        return (0.15 * P_xM[j] - 17) * D_b - 0.15 * P_xM[j]

    return "Error"



def T_TM(P_TM, i, j):
    return P_TM[j] - 0.275 * b(j) + SF(P_TM, i, j) - 6.025

def T_NM(P_NM, i, j):
    return P_NM[j] - 0.175 * b(j) + SF(P_NM, i, j) - 2.025

def T_q(i):
    cons = i * samplerate/N
    return 3.64*((cons/1000)**(-0.8)) - 6.5 * np.exp(-0.6*(((cons/1000) - 3.3)**2)) + (10**(-3)) * (cons/1000)**4


T_TM_ = []
T_NM_ = []

counter = 0

for k in range(len(P_TM)):

    temp_t = []
    double_temp_t = []
    for i in range(256):
            temp_t = []
            for j in range(256):
                if P_TMc[k][j] == 0: #-------------------------------------------------------
                    temp_t.append(0)
                    continue
                if b(i) < b(j) - 3 or b(i) > b(j) + 8:
                    temp_t.append(0)
                    continue #----------------------------------------------------
                if k == 10:
                    counter += 1
                temp_t.append(T_TM(P_TMc[k], i, j))
            # print(temp_t)
            # input("press any key to continue")
            # temp_t.append(temp_t)
            # temp_t = np.array(temp_t)
            # temp_t = np.transpose(temp_t)
            # temp_t = list(temp_t)
            # print(temp_t)
            double_temp_t.append(temp_t)
    T_TM_.append(double_temp_t)

    double_temp_n = []
    for i in range(256):
            temp_n = []
            for j in range(256):
                if P_NMc[k][j] == 0: #----------------------------------------------------
                    temp_n.append(0)
                    continue
                if b(i) < b(j) - 3 or b(i) > b(j) + 8:
                    temp_n.append(0)
                    continue #-------------------------------------------------------
                temp_n.append(T_NM(P_NMc[k], i, j))
            # temp_n = np.array(temp_n)
            # temp_n = np.transpose(temp_n)
            # temp_n = list(temp_n)
            double_temp_n.append(temp_n)
    T_NM_.append(double_temp_n)
    print(k)

# print(T_TM_)
# print(T_NM_)

print(counter)
print(len(T_TM_))

# figure_counter += 1
# plt.figure(figure_counter)
# plt.plot(T_TM_[10])
#
# figure_counter += 1
# plt.figure(figure_counter)
# plt.plot(T_NM_[10])
# T_TM_ = np.array(T_TM_)
# print(T_TM_.size)

# T_NM_ = np.array(T_NM_)
# print(T_NM_.size)

def T_g(i, T_TM, T_NM, P_TMc, P_NMc):
    sum1, sum2 = 0, 0
    for l in range(len(T_TM[i])):
        if P_TMc[l] != 0:
            sum1 += 10 ** (0.1 * T_TM[i][l])

    for m in range(len(T_NM[i])):
        if P_NMc[m] != 0:
            sum2 += 10 ** (0.1 * T_NM[i][m])

    return 10 * np.log10(10 ** (0.1 * T_q(i)) + sum1 + sum2)

T_g_ = []
for k in range(len(P_TMc)-1):
    temp = []
    for i in range(1, len(P_TMc[k])):
        # try:
        temp.append(T_g(i, T_TM_[k], T_NM_[k], P_TMc[k], P_NMc[k]))
        # except:
        #     print("List index out of range, i = ", k)
    T_g_.append(temp)

np.save("T_g_i.npy", T_g_)

print(T_g_[10])
figure_counter += 1
plt.figure(figure_counter)
plt.plot(T_g_[10])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(window_signal[10])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(T_g_[30])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(window_signal[30])

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title('Original audio')

plt.show()
