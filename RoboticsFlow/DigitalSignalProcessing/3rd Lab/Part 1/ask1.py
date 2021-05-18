import numpy as np
import matplotlib.pylab as plt
import math
import cmath
import librosa as lib
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write
from scipy.signal import spectrogram 
import random

figure_counter = 0

path = "../music.wav"
  
# 1.1
def read_from_files(path):
    original, samplerate = lib.load(path) 
    return samplerate, original

samplerate, original = read_from_files(path)
print(original)
 

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
		return 10 * np.log10(abs(fft(signal) ** 2)) + 90.302
 
	return [calculate_P(sig)[0:length//2] for sig in window_signal] 

def calculate_S_T_k(power_spectrum, length):
	def S_T_k(P, k):
		def D_k(k):
			if 2 < k < 63:
				return 2
			if 63 <= k < 127:
				return random.randint(2,3)
			if 127 <= k <= 250:
				return random.randint(2,5)
			return "There was an error"

		if 3 <= k <= 250:
			d_k = D_k(k)
			return P[k] > P[k + 1] and P[k] > P[k - 1] and P[k] > P[k + d_k] + 7 and P[k] > P[k - d_k]  + 7
		else:
			return 0
	
	return [ [S_T_k(P,k) for k in range(length // 2)] for P in power_spectrum] 

def calculate_P_TM(power_spectrum, S_T, length):
	P_TM = []
	for i, p in enumerate(power_spectrum):
		temp = []
		for k in range(length // 2):
			if S_T[i][k] == 1:
				temp.append( 10 * np.log10( 10 ** (0.1 * p[k - 1])) + 10 ** (0.1 * p[k]) + 10 ** (0.1 * p[k + 1]) )
			else:
				temp.append(0)
		P_TM.append(temp)
	return P_TM

N = 512
window = np.hamming(N)
window_signal = window_signal(original, window, N)
power_spectrum = power_spectrum(window_signal, N) 		
S_T = calculate_S_T_k(power_spectrum, N)
P_TM = calculate_P_TM(power_spectrum, S_T, N)


def b(f):
	return 13 * np.arctan(0.00076 * f) + 3.5 * np.arctan((f/7500) ** 2)

def D_b(i,j):
	return b(i) - b(j)

def SF(P_TM, i,j):
	D_b = D_b(i,j)

	if -3 <= D_b < -1:
		return 17 * D_b - 0.4 * P_TM[j] + 11
	if -1 <= D_b < 0:
		return (0.4 * P_TM[j] + 6) * D_b
	if 0 <= D_b < 1:
		return -17 * D_b
	if 1 <= D_b < 8:
		return (0.15 * P_TM[j] - 17) * D_b - 0.15 * P_TM[j]

	return "Error"
def T_TM(P_TM, i,j):
	return P_TM[j] - 0.275 * b(j) + SF(P_TM, i,j) - 6.025

def T_NM(P_TM, P_NM, i, j):
	return P_NM[j] - 0.175 * b(j) + SF(P_TM, i, j) - 2.025



def T_g(i, T_q, T_TM. T_NM, L):
	sum1, sum2 = 0,0
	for l in range(1,L+1):
		sum1 += 10 ** (0.1 * T_TM[i][l])
	for m in range(1, M + 1):
		sum2 += 10 ** (0.1 * T_NM[i][m])
		
	return 10 * np.log10( 10 ** (0.1 * T_q[i]) + sum1 + sum2)



figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title('Original audio')





plt.show()
