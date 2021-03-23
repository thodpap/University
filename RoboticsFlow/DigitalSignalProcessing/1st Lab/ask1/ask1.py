import numpy as np
import math 
import pylab  
from scipy.io.wavfile import read
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
print(frequency_peaks)

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

# pylab.figure(2)
# pylab.plot(np.arange(N),window)

# pylab.figure(3)
# pylab.plot(np.arange(8700), phone_number_array)


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
	# for _ in range(500):
	# 	tmp_arr.append(0)
	fft_with_hamming.append(np.fft.fft(tmp_arr)) 

peaks_array = []

for i in range(8): 
	print(max(abs(fft_with_hamming[i]))/20)
	peaks, _ = find_peaks(abs(fft_with_hamming[i]), threshold=max(abs(fft_with_hamming[i]))/10) 
	peaks_array.append(list(peaks)) 

# f = k/N * fs
new_peaks_array = []
for peak in peaks_array:
	new_peaks_array.append(np.array(peak)* total_frequency / (N+100))


##############################
# Debug #

for i in range(8):
	print(new_peaks_array[i], phone_number[i], frequency_peaks[phone_number[i]])

#pylab.show()
def mapToValues(frequency_peaks):

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

	for i in range(8):
		a = findClosestFrequency(first_pair_frequency, new_peaks_array[i][0])
		b = findClosestFrequency(second_pair_frequency, new_peaks_array[i][1])
		c = np.intersect1d(a,b)
		mapped_frequencies.append(c[0])
	print(mapped_frequencies)
	return mapped_frequencies

mapToValues(frequency_peaks)
# print(mapped_frequencies)

 

# print(findClosestFrequency(frequency_peaks,peaks_array[0]))

# # frequency will be a tuple
# def fromFrequencyToNumber(frequency_peaks, frequency):
# 	return frequency_peaks.index(frequency) 


# pylab.show()
# def ttdecode(filename, peaks ): 
# 	samplerate, data = read(filename)
# 	print(samplerate,data, data[664])

# 	vector = [] 

# 	N = 1000
# 	window = get_window('hamming',N)
# 	value_around_zero_amplitude = 10
# 	start = 0
# 	last = 1000
# 	while True: 
# 		if start >= len(data) - 1000:
# 			break
# 		if last > len(data):
# 			last = len(data)
# 			start = len(data) - 1000


# 		array = data[start:last] 
# 		array = array * window
# 		array = np.fft.fft(array)

# 		# array = np.square(array)
# 		peaks_note, _ = find_peaks(array, threshold=25)

# 		if len(peaks_note) == 4: # even if we add the smaller window its okay ?? 
# 			vector.append(peaks_note)
# 			start += 1050
# 			last  += 1050
# 		else: 
# 			num = vector[-1] # Previous number -> remove the max of the previous freq
# 			for peak in peaks_note:
# 				pass


# 	# pylab.figure(7)
# 	# pylab.stem(np.arange(0,10850), data)
# 	# pylab.show()
	

# 	return vector


# ###################################
# # Caclulate the array of peaks # 

# print(ttdecode('number.wav', frequency_peaks))


###########################################
# 1.7 #

# easySigArray = np.load("../easySig.npy")
# hardSigArray = np.load("../hardSig.npy")

# write("easySigInitial.wav", total_frequency, easySigArray)
# write("hardSigInitial.wav", total_frequency, hardSigArray)

# print(ttdecode("easySigInitial.wav", peaks_array))
# print(ttdecode("hardSigInitial.wav", peaks_array))



# pylab.show()
