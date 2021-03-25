import numpy as np
import math 
import pylab  
from scipy.io.wavfile import read
from scipy.io.wavfile import write 
from scipy.signal import get_window
from scipy.signal import find_peaks

# Define our main variables
N = 1000
n = np.array(range(1,1001)) 
total_frequency = 8192 # Hz

frequencies_row 	= [0.5346, 0.5906, 0.6535, 0.7217]  
frequencies_column  = [0.9273, 1.0247, 1.1328]



##################################### 
# 			1.1						#
#####################################


# Let our signals be named d[n] = sin(v1*t) + sin(v2*t)
d = []
d.append(np.sin(0.7217 * n) + np.sin(1.0247 * n)) # append first d[0]
for row in frequencies_row:
	for column in frequencies_column:
		if row == 0.7217: # If we are in the last row skip it -> we don't need it
			continue
		d.append(np.sin(row * n) + np.sin(column * n))
d = np.array(d) 


##################################### 
# 			1.2						#
#####################################


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

# Caclulate the frequency 
array_n = np.arange(N)
freq = array_n * total_frequency/ N

X_2 = DFT(d[2])
X_7 = DFT(d[7])
# f/fs = k/N

pylab.figure(1)
pylab.subplot(121)
pylab.title('DFT of number 2')
pylab.plot(freq, abs(X_2))
pylab.subplot(122)
pylab.title('DFT of number 7')
pylab.plot(freq, abs(X_7))



##################################### 
# 			1.3						#
#####################################


# 06236122 = 03118040 + 03118082
# phone_number = [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9,0,0,0,5,4,2,7,8,2] # for testing
phone_number = [0,6,2,3,6,1,2,2]
phone_number_length = len(phone_number)
phone_number_array = []

for index, number in enumerate(phone_number):
	for d_i in d[number]:
		phone_number_array.append(d_i)
	if index != phone_number_length - 1: 
		for temp in range(100):
			phone_number_array.append(0) 

phone_number_array = np.array(phone_number_array)
write("tone_sequence.wav", total_frequency, phone_number_array)

window = get_window('hamming',N) 

# pylab.figure(2)
# pylab.plot(np.arange(N),window)

# pylab.figure(3)
# pylab.plot(np.arange(8700), phone_number_array)


##################################### 
# 			1.4						#
#####################################

# i ????????? TODO: Write the 1.4.i

# ii 
hamming_result = []
for index, number in enumerate(phone_number):
	for index2, d_i in enumerate(d[number]):
		hamming_result.append(d_i * window[index2]) 
	if index != phone_number_length - 1: 
		for temp in range(100):
			hamming_result.append(0)

pylab.figure(4)
pylab.plot(np.arange(len(hamming_result)), hamming_result)




##################################### 
# 			1.5 					#
#####################################


# caclulate ω 
# pair: (row, column)
frequency_peaks = []
constant = total_frequency/(2*math.pi)
frequency_peaks.append( (round(0.7217 * constant), 
						 round(1.0247 * constant)))

for row in frequencies_row: 
	for column in frequencies_column:
		if row == 0.7217:
			continue
		frequency_peaks.append( (
			round(row * constant), round(column * constant)
		) ) 

print('The frequency peaks are', frequency_peaks)


##################################### 
# 			1.6 					#
#####################################
 

def findPeaksInInterval(array ):
	t = np.fft.fft(array)
	peaks, _ = find_peaks(abs(t), threshold=max(abs(t)/10))
	return peaks

peaks_array = []
for i in range(phone_number_length):
	start,last = i*1000 + 100*i, (i+1)*1000 + 100*(i+1)
	
	peaks_array.append(list(findPeaksInInterval(hamming_result[start:last]) * total_frequency / (N+100) ) ) # * total_frequency / (N+100))

 
def mapToValues(frequency_peaks, new_peaks_array, samples): 
	def findClosestFrequency(frequency_peaks, frequency): 
		frequency_peaks = np.asarray(frequency_peaks)
		idx = (np.abs(frequency_peaks - frequency)).argmin()
		return_list = []
		for index,fre in enumerate(frequency_peaks):
			if fre == frequency_peaks[idx] :
				return_list.append(index)
		return return_list

	first_pair_frequency = [a for a,b in frequency_peaks]
	second_pair_frequency = [b for a,b in frequency_peaks]

	mapped_frequencies = []

	for i in range(samples):
		a = findClosestFrequency(first_pair_frequency, new_peaks_array[i][0])
		b = findClosestFrequency(second_pair_frequency, new_peaks_array[i][1])
		c = np.intersect1d(a,b)
		mapped_frequencies.append(c[0]) 
	return mapped_frequencies

mapped_frequencies = mapToValues(frequency_peaks, peaks_array, 8 ) 

def ttdecode(filename, peaks, N):  
	samplerate, data = read(filename)
	frequency_peaks = []  
	samples = 0
	start, last = 0, N
	size = len(data) 
	i = 0
	while True:
		if samples > 0:
			i = start + 1000
		while True:
			if i + 1 > size:
				i += 1
				break
			if abs(data[i]) <= 0.01 and abs(data[i+1]) <= 0.01:
				i += 1
			else:
				break 
		start = i+1
		last = start + 1000
		if start >= size:
			break
		if last >= size:
			last = size
 
		samples += 1 
		temp_peaks = findPeaksInInterval(data[start:last]) * samplerate / N
		# print('find peaks: ', temp_peaks* total_frequency / N)
		frequency_peaks.append( (temp_peaks[0], temp_peaks[1])) 
		# start += 1
	# print(peaks)
	return mapToValues(peaks, frequency_peaks, samples)  

# 	return vector


# ###################################
# # Caclulate the array of peaks # 
# pylab.figure(2)
# pylab.plot(np.arange(len(phone_number_array)),phone_number_array)
# pylab.show()
print(ttdecode("tone_sequence.wav", frequency_peaks, N))



##################################### 
# 			1.7 					#
#####################################

easySigArray = np.load("../easySig.npy")
hardSigArray = np.load("../hardSig.npy")

write("easySigInitial.wav", total_frequency, easySigArray)
write("hardSigInitial.wav", total_frequency, hardSigArray)

print(ttdecode("easySigInitial.wav", frequency_peaks, N))
print(ttdecode("hardSigInitial.wav", frequency_peaks, N))



pylab.show()
