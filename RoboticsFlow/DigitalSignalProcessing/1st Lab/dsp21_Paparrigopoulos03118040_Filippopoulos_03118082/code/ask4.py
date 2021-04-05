import numpy as np
from scipy.io import wavfile

import matplotlib
matplotlib.use('TkAgg') # To fix error

import matplotlib.pyplot as plt
import librosa
import pywt
import warnings

files = ['../foxtrot_excerpt1.mp3', 
         '../foxtrot_excerpt2.mp3', 
         '../salsa_excerpt.mp3' ]

file = files[2]
warnings.simplefilter("ignore", UserWarning)
figure_counter = 0 #for plots
data, samplerate = librosa.load(file) #default 22050 samplerate freq



#########################################################################
#                                                                       #
#  4.1 : Load the audio file, and isolate a window of length 2^16       #
#       and plot it                                                     #
#                                                                       #
#########################################################################

signal = data[10000:(2**16+10000)]
n = np.arange(0, len(signal))

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n, signal) 
plt.savefig('diagrams/signal.png')



#########################################################################
#                                                                       #
#  4.2 : Use Discrete Wavelet Transform (dwt) in our signal             #
#                                                                       #
#########################################################################
#                                                                       #
#   To do so, we calculate the                                          # 
#                                                                       #
#########################################################################  


signaled = signal
details, approximation = [], []

for index in range(7):
    cA, cD = pywt.dwt(signaled, 'db4')
    details.append(cD)
    signaled = cA
    if index == 6:
        approximation = cA

 
#########################################################################
#                                                                       #
#  4.3.a : Caclulate z_i[n] = | y_i[n]                                  #
#                                                                       #
#########################################################################

z = [abs(detail) for detail in details]
z.append(abs(approximation))
z = np.array(z)


#########################################################################
#                                                                       #
#  4.3.b : Caclulate z_i[n] = | y_i[n]                                  #
#                                                                       #
#########################################################################

import statistics as stat

a_array, x = [0.001, 0.002, 0.005], []

for i in range(8):
    x_i = np.zeros(len(z[i]))
    a_0 = (2**(i+1))*a_array[2]
    if i == 7:
        a_0 = a_0/2
    for j in range(len(x_i)):
        if j == 0:
            # x_i[j] = (1 - a_0) * x_i[j-1] + a_0 * z[i][j] 
            # but index -1 does not exist for x
            x_i[j] = a_0 * z[i][j]  
            continue
        x_i[j] = (1-a_0)*x_i[j-1] + a_0*z[i][j] 
    x.append(x_i)

print(np.array(x))



#########################################################################
#                                                                       #
#  4.3.c : Plot y_d2[n] and y_d4[n]  and calculate the new x            #
#                                                                       #
#########################################################################

x_new = [ (x[i] - stat.mean(x[i])) for i in range(8)]
x = x_new 

figure_counter += 1
plt.figure(figure_counter) 

ax = plt.subplot2grid( (2,1), (0,0) )
plt.title('Details[2]')
plt.plot(np.arange(len(z[1])), details[1])

ax = plt.subplot2grid( (2,1), (1,0) )
plt.title('x[2]')
plt.plot(np.arange(len(x[1])), x[1], 'b')
plt.tight_layout() 
plt.savefig('diagrams/x[2]_details[2].png')

figure_counter += 1
plt.figure(figure_counter) 

ax = plt.subplot2grid( (2,1), (0,0) )
plt.title('Details[4]')
plt.plot(np.arange(len(z[3])), details[3])

ax = plt.subplot2grid( (2,1), (1,0) )
plt.title('x[4]')
plt.plot(np.arange(len(x[3])), x[3], 'b') 
plt.tight_layout() 
plt.savefig('diagrams/x[4]_details[4].png') 


#########################################################################
#                                                                       #
#  4.4: Add the sourroundings                                           #
#                                                                       #
#########################################################################
  
length = int(len(signal))
x_new = [np.interp(np.linspace(0, len(x_new[i]), length) , np.arange(len(x_new[i])), x_new[i]) for i in range(8)  ]

 

figure_counter += 1
plt.figure(figure_counter)
for i in range(3):
    for j in range(3):
        if i == 2 and j == 2:
            continue
        ax = plt.subplot2grid((3,3), (i,j)) 
        if 3*i + j < 7:
            plt.title('x[' + str(3*i + j+1) +']')
        else:
            plt.title('a[' + str(3*i + j + 1) +']')
        plt.plot(np.arange(len(x_new[3*i + j])), x_new[3*i + j])

plt.tight_layout() 
plt.savefig("diagrams/x.png")


sum_of_x = np.zeros(length)
x_new = np.array(x_new)

for i in range(8):
    for j in range(length):
        sum_of_x[j] += x_new[i][j]


figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(sum_of_x)), sum_of_x)
plt.title("sum_of_x")
plt.savefig("diagrams/sum_of_x.png")


#########################################################################
#                                                                       #
#  autocorrelation                                                      #
#                                                                       #
#########################################################################


print(len(sum_of_x))

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[int(result.size/2):]

autocorrelation = autocorr(sum_of_x)  


#########################################################################
#                                                                       #
#  4.5: Find the bpm. We are instreaded in a range of 60-200 bpm.       #
#                                                                       #
######################################################################### 

from scipy.ndimage import gaussian_filter1d

def findPeaksInInterval(array):
    from scipy.signal import find_peaks
    #t = np.fft.fft(array)
    peaks, _ = find_peaks(array)
    return peaks



#########################################################################
#                                                                       #
#  Choose different standard deviation for our gaussian filter          #
#                                                                       #
#########################################################################

if file == files[0]:
    sigma = 1
elif file == files[1]:
    sigma = 350
elif file == files[2]:
    sigma = 350
else:
    assert False, "Wrong file was chosen"   # In case a typo occurs

autocorrelation_filtered = gaussian_filter1d(autocorrelation, sigma)

#########################################################################
#                                                                       #
#  plot autocorrelation filtered                                        #
#                                                                       #
#########################################################################

figure_counter += 1
plt.figure(figure_counter)
 
plt.title("Autocorrelation Filtered")
plt.plot(np.arange(len(autocorrelation_filtered)), autocorrelation_filtered) 
plt.savefig('diagrams/autocorrelation_filtered.png')

peaks = findPeaksInInterval(autocorrelation_filtered[6615:22051]) # So that 60 <= bpm <= 200

BPMs = []
print(peaks)

for peak in peaks:
    value = autocorrelation_filtered[peak+6615]
    bpm = int(60*22050 / (peak+6615))
    BPMs.append( (bpm, peak + 6615, value))
 
print(np.array(sorted(BPMs, key=lambda tup: tup[0])))

#########################################################################
#                                                                       #
#  Calculate the bpm that has the max value in the correlation diagram  #
#                                                                       #
#########################################################################

max_amplitude = 0
ans_bpm = 0
for bpm, peak, value in BPMs:
    if value > max_amplitude:
        ans_bpm = value
        ans_bpm = bpm

print(ans_bpm)
 

plt.show()

