import numpy as np
import math 
import pylab  
from scipy.io.wavfile import write 
from scipy.signal import get_window
from scipy.signal import find_peaks

N = 1000
n = np.array(range(1,1001))
total_frequency = 8192 # Hz

frequencies_row 	= [0.5346, 0.5906, 0.6535, 0.7217]
frequencies_column  = [0.9273, 1.0247, 1.1328]


# Let our signals be named d[n]
d = []
d.append(np.sin(0.7217 * n) + np.sin(1.0247 * n)) # d[0]
for row in frequencies_row:
	for column in frequencies_column:
		if row == 0.7217:
			continue
		d.append(np.sin(row * n) + np.sin(column * n))
d = np.array(d)

# Caclulates the DFT of a signal x

# We added the dft function from
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
def DFT(x):  

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X

X_2 = DFT(d[2])
X_7 = DFT(d[7])
# f/fs = k/N
# Caclulate the frequency 
array_n = np.arange(N)
freq = array_n * total_frequency/ N

pylab.figure(1)
pylab.subplot(121)
pylab.plot(freq, abs(X_2))
pylab.subplot(122)
pylab.plot(freq, abs(X_7))

# pylab.show()
# 06236122 = 03118040 + 03118082
phone_number = [0,6,2,3,6,1,2,2]
phone_number_array = []

for index, number in enumerate(phone_number):
	for d_i in d[number]:
		phone_number_array.append(d_i)
	if index != 7: 
		for temp in range(100):
			phone_number_array.append(0) 

phone_number_array = np.array(phone_number_array)
write("number.wav", total_frequency, phone_number_array)

window = get_window('hamming',N)

pylab.figure(2)
pylab.plot(np.arange(N),window)

pylab.figure(3)
pylab.plot(np.arange(8700), phone_number_array)


#############################################################
hamming_result = []
for index, number in enumerate(phone_number):
	for index2, d_i in enumerate(d[number]):
		hamming_result.append(d_i * window[index2]) 
	if index != 7: 
		for temp in range(100):
			hamming_result.append(0)

pylab.figure(4)
pylab.plot(np.arange(8700), hamming_result)



###################################################
# FFT #

fft_with_hamming = []

for i in range(8):
	start,last = i*1000 + 100*i, (i+1)*1000 + 100*(i+1)
	tmp_arr = hamming_result[start:last]
	fft_with_hamming.append(np.fft.fft(tmp_arr))

pylab.figure(5)
pylab.plot(np.arange(1100), fft_with_hamming[0])

peaks_array = []

for i in range(8): 
	peaks_array.append(find_peaks(fft_with_hamming[i]))


print(np.array(peaks_array))










pylab.show()
