import numpy as np
import math  
from scipy.io.wavfile import read, write
from scipy.signal import get_window
import matplotlib.pyplot as plt

# Define our main variables
figure_counter = 0
N = 1000
n = np.array(range(1,1001)) 
total_frequency = 8192 # Hz

frequencies_row 	= [0.5346, 0.5906, 0.6535, 0.7217]  
frequencies_column  = [0.9273, 1.0247, 1.1328]



##############################################################################
#																			 #
#		1.1 : Create 10 sounds of 1000 samples based on the table     	  	 #
#																			 #
##############################################################################  
#																			 #
#	 Let our signals be named d[n] = sin(v1*t) + sin(v2*t)					 #
#																			 #
##############################################################################

d = []
d.append(np.sin(0.7217 * n) + np.sin(1.0247 * n)) # append first d[0]
for row in frequencies_row:
	for column in frequencies_column:
		if row == 0.7217: 	# Skip the last row since we already added 0 in d[0]
			continue
		d.append(np.sin(row * n) + np.sin(column * n))
d = np.array(d) 

figure_counter += 1
plt.figure(figure_counter, figsize=(20,20)) 
plt.suptitle("The Number's Signals") 

for i in range(3):
	for j in range(3):
		string = 'd[' + str(i * 3 + j + 1) + ']'
		ax = plt.subplot2grid((4,3), (i,j))
		plt.title(string)
		plt.plot(np.arange(len(d[figure_counter])),d[figure_counter])


ax = plt.subplot2grid((4,3), (3,1))
plt.title('d[0]')
plt.plot(np.arange(len(d[0])),d[0])  
plt.savefig('diagrams/d[n].png')
plt.tight_layout() 


##############################################################################
#																			 #
#		1.2 : Calculate DFT of 2 and 7							     	  	 #
#																			 # 
#########################################################################################################
#																										#
#		Caclulates the DFT of a signal x 						    	  	 							#
#		We added the dft function from  									 							#
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html	#
#																										#
######################################################################################################### 

def DFT(x):   
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X


##############################################################################
#																			 #
#	  Calculates the respective DFT's and plot them			     	 		 #
#																			 #
############################################################################## 

freq = np.arange(N) * total_frequency/ N
dft_array = []
for i in range(10):
	dft_array.append(DFT(d[i]))

X_2 = dft_array[2]
X_7 = dft_array[7]


figure_counter += 1
plt.figure(figure_counter)
plt.suptitle('Dft of d[2] and d[7]')

plt.subplot(121)
plt.title('DFT(d[2])')
plt.plot(freq,abs(X_2))

plt.subplot(122)
plt.title('DFT(d[7])')
plt.plot(freq,abs(X_7))  
plt.savefig('diagrams/dft_2&7.png')

figure_counter +=1
plt.figure(figure_counter, figsize=(20,30))
plt.suptitle("All the DFT's")
for i in range(3):
	for j in range(3):
		ax = plt.subplot2grid( (4,3), (i,j) )
		plt.title('DFT of d[' + str(i*3+j + 1) + ']')
		plt.plot(freq, abs(dft_array[i*3+j + 1]))
 

ax = plt.subplot2grid((4,3), (3,1))
plt.title('DFT of d[0]')
plt.plot(freq,abs(dft_array[0]))
plt.tight_layout()  
plt.savefig('diagrams/all_dfts.png')



##############################################################################
#																			 #
#		1.3 : Write our .wav filename							     	  	 #
#																			 #
##############################################################################   
#																			 #
#	  Calculates the phone array, which consists of the the signal points 	 #
# 	  separated by 100 zero points 											 #
#																			 #																			 #
############################################################################## 
#																			 #
#			06236122 = 03118040 + 03118082 									 #
#																			 #																		 #
############################################################################## 

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

figure_counter += 1
plt.figure(figure_counter)
plt.title('Our phone number signal: [0,6,2,3,6,1,2,2]') 
plt.plot(np.arange(len(phone_number_array)), phone_number_array)
plt.savefig('diagrams/phone_number_array.png')

##############################################################################
#																			 #
#		1.4 : Trnasorm out signal using boxcar and hamming window 			 #
#																			 #
############################################################################## 



##############################################################################
#																			 #
#		1.4.i : Transform our signal with a square window - boxcar 			 #
#				Also, we insert 100 zeros between each number 				 #
#																			 #
############################################################################## 

square_window = get_window('boxcar', N)
square_result = []

for index, number in enumerate(phone_number):
	for index2, d_i in enumerate(d[number]):
		square_result.append(d_i * square_window[index2])

	if index != phone_number_length - 1:
		for _ in range(100):
			square_result.append(0)

print(square_window, d[0])
figure_counter += 1
plt.figure(figure_counter)
plt.title('Signal with a boxcar window')
plt.plot(np.arange(len(square_result)), square_result)
plt.savefig('boxcar_window_result.png')
 
##############################################################################
#																			 #
#		1.4.ii : Transform our signal with a Hamming window		     	  	 #
#				Also, we insert 100 zeros between each number 				 #
#																			 #
############################################################################## 

hamming_window = get_window('hamming',N) 
hamming_result = []
for index, number in enumerate(phone_number):
	for index2, d_i in enumerate(d[number]):
		hamming_result.append(d_i * hamming_window[index2]) 
	if index != phone_number_length - 1: 
		for _ in range(100):
			hamming_result.append(0)

figure_counter += 1
plt.figure(figure_counter)
plt.title('Signal with a hamming window')
plt.plot(np.arange(len(hamming_result)), hamming_result)
plt.savefig('diagrams/hamming_window_result.png')


##############################################################################
#																			 #
#		1.5 : Calculate a list with our peak points called frequency peaks	 #
#			This array consists of tuples									 #
#																			 #
############################################################################## 
#																			 # 
#   	We use the formula f = Ω  / (2π) * 8192 (Hz)						 # 
#																			 #
############################################################################## 
 
frequency_peaks = []
constant = total_frequency/(2*math.pi)
frequency_peaks.append( (round(0.7217 * constant), 
						 round(1.0247 * constant)))

for row in frequencies_row: 
	for column in frequencies_column: 
		if row == 0.7217: # Skip the last row since we already added 0 
			continue
		frequency_peaks.append( (
			round(row * constant), round(column * constant)
		) ) 

print('The frequency peaks are', frequency_peaks)



##############################################################################
#																			 #
#		1.6 : Calculate ttdecode that you pass your filename, your 			 #
#				peak frequency's array and returns the input number    	  	 #
#																			 #
##############################################################################
#																			 #
# 			To do so, we created 2 functions:								 #
#			i) findPaksInInterval: in which you pass the frequncy array of 	 #
#									your data 								 #
#			ii) mapToValues: in which you parse the peaks that your signal 	 #
#							 has and it maps to the original peaks we had 	 #
# 							 previously calculated							 #
#																			 #	 
############################################################################## 
#																			 #
#		The way that findPeaksInInterval works is that you pass your array   #
# 		and uses the find_peaks function. By experimenting, we concluded     #
#		that we should use a threshold of the the max value of the fft       #
#		divided by 10														 #
#																			 #
##############################################################################

def findPeaksInInterval(array ):
	from scipy.signal import find_peaks
	t = np.fft.fft(array)
	peaks, _ = find_peaks(abs(t), threshold=max(abs(t)/10))
	return peaks

# Caclulate the peaks array
peaks_array = []
for i in range(phone_number_length):
	start,last = i*1000 + 100*i, (i+1)*1000 + 100*(i+1)
	const = total_frequency / (N+100) 
	peaks_array.append(
		list(
			findPeaksInInterval(hamming_result[start:last]) * const
		) 
	) 

 
############################################################################## 
#																			 #
# 		The way that mapToValues work is that we pass the peaks calculated	 #
# 		for our new signal, the new_peaks_array which is the array 			 #
# 		that was calculated in the previous step (peaks_array) and ours		 #
#  		samples. 															 #
#																			 #
##############################################################################
#																			 #
#		In the interior of the mapToValues function we defined the 			 #
#  		findClosestFrequency function that does what it implies, you pass	 #
#		the frequency peaks of your signal and it matches with we closest 	 #
# 		frequency that we have calculated.									 #
#																			 #
##############################################################################
#																			 #
#		The findClosestFrequency uses the argmin() function that returns 	 #
#		the smallest element of an array. Hence, we pass the absolute 		 #
# 		value of the difference of our calculated frequencies and the 		 #
# 		frequency we seek to find 										     #
#																			 #
##############################################################################
#																			 #
#		To do that we have to first decompose the tuples in arrays of their  #
# 		own and calculate for each freq the respective possible frequencies  #
#		that correspond to it. Then we have 2 3x3 arrays that have only one  #
#		common element which is the peak 									 #
#																			 #
##############################################################################
#																			 #
#		In ttdecode	we pass our filename, and the peaks we have calculated   #
# 		and our samples (N). We read the audio, and then we calculate the 	 #
#		peak frequencies in the part-signal composed by the first N samples. #
#		The we calculate the number it corresponds based on the peaks. 		 #
#		Furthermore, to move our window we defined the findNext Start 		 #
#		function. After the execution of this function our windows shifts by #
#		a couple of zeros and then perform the previously mentioned method.  #
# 		It only finishes when there are no other data to examine			 #																	 
# 		and returns the number that the signal corresponds					 #
#																			 #
##############################################################################


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

mapped_frequencies = mapToValues(frequency_peaks, peaks_array, phone_number_length ) 

def ttdecode(filename, peaks, N):  
	def findNextStart(i, data, dataSize, maxValueAllowed):
		while True:
			if i + 1 > dataSize:
				break

			# Works even with some noise too
			if abs(data[i]) <= maxValueAllowed and abs(data[i+1]) <= maxValueAllowed: 
				i += 1
			else:
				break
		return i

	samplerate, data = read(filename)
	frequency_peaks = []   
	start, last, i, samples = 0, N, 0, 0 
	size = len(data) 

	while True:
		if samples > 0:
			i = start + 1000
		i = findNextStart(i, data, size, 0.01) 

		start = i+1
		last = start + 1000
		if start >= size:
			break
		if last >= size:
			last = size
 
		samples += 1 
		temp_peaks = findPeaksInInterval(data[start:last]) * samplerate / N
		frequency_peaks.append( (temp_peaks[0], temp_peaks[1]))  

	return mapToValues(peaks, frequency_peaks, samples)   

 
testOurNumber = ttdecode("tone_sequence.wav", frequency_peaks, N)



##############################################################################
#																			 #
#		Assert that our computed number is the same as the initial 			 #
#		If the condition returns false, AssertionError is raised			 #
#		If this fails the execution stops								     #
#																			 #
############################################################################## 
print(np.array(testOurNumber),np.array(phone_number))
assert (np.array(testOurNumber)==np.array(phone_number)).all()  



##############################################################################
#																			 #
#		1.7 : Read the 2 signals and caclulate the initial number     	  	 #
#																			 #
############################################################################## 

easySigArray = np.load("../easySig.npy")
hardSigArray = np.load("../hardSig.npy")

write("easySigInitial.wav", total_frequency, easySigArray)
write("hardSigInitial.wav", total_frequency, hardSigArray)

print(ttdecode("easySigInitial.wav", frequency_peaks, N))
print(ttdecode("hardSigInitial.wav", frequency_peaks, N)) 

plt.show()
