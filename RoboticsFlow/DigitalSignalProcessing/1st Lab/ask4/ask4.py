import numpy as np
from scipy.io import wavfile

import matplotlib
matplotlib.use('TkAgg') # To fix error

import matplotlib.pyplot as plt 
import librosa
import pywt 
import warnings
warnings.simplefilter("ignore", UserWarning)

figure_counter = 0   

# default at 22050 samplerate frequency
data, samplerate = librosa.load('../foxtrot_excerpt1.mp3') 
 

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
plt.show()

#########################################################################
#                                                                       #
#  4.2 : Use Discrete Wavelet Transform (dwt) in our signal             #
#                                                                       #
#########################################################################
#                                                                       #
#   To do so,                                                                        
#                                                                       #
#########################################################################  

from scipy.signal import butter, lfilter, freqz
### source: https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


high = samplerate / 2
diff = high/2
array = []

while True:
    if high <= 0:
        break
    array.append((high-diff, high))
    high -= diff
    diff /= 2


array = array[:7]
array = np.array(array)
array[6][0] = 0
print(array)

filtered_high, filtered_low = [], []
y = []

signaled = signal 
details, approximation = [], []

for index in range(7):
    # filtered_high = (butter_bandpass_filter(cutt_offed, low, high, samplerate, order=5))
    cA, cD = pywt.dwt(signaled, 'db4')
    details.append(cD)
    signaled = cA
    if index == 6:
        approximation = cA

# counter += 1
# plt.figure(counter)
# plt.plot(approximation)
#
# counter += 1
# plt.figure(counter)
# plt.plot(details[0])

# wavfile.write("approximation.wav", 44100,  approximation)
# wavfile.write("detail.wav", 44100, details[0])


### 4_3

#a)

z = []
for i in details:
    z.append(abs(i))

z.append(abs(approximation))

z = np.array(z)
#print(z)


#b)
import statistics as stat

a_array = [0.001, 0.002, 0.005]

x = []

for i in range(8):
    x_i = np.zeros(len(z[i]))
    a_0 = (2**(i+1))*a_array[0]
    if i == 7:
        a_0 = a_0/2
    for j in range(len(x_i)):
        if j == 0:
            x_i[j] = a_0 * z[i][j]  # x_i[j] = (1 - a_0) * x_i[j-1] + a_0 * z[i][j] but index -1 does not exist for x
            continue
        x_i[j] = (1-a_0)*x_i[j-1] + a_0*z[i][j]

    x.append(x_i)

print(np.array(x))

for i in range(8):
    mean = stat.mean(x[i])
    x[i] = x[i] - mean
    #  x[i] = x[i]

n = np.arange(len(z[1]))

figure_counter += 2
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle("yd2 and xd2")
ax1.plot(n, details[1])
ax2.plot(n, x[1], 'b')


n = np.arange(len(z[3]))

fig, (ax3, ax4) = plt.subplots(2)
fig.suptitle("yd4 and xd4")
ax3.plot(n, details[3])
ax4.plot(n, x[3], 'b')


## 4_4

length = 0

for i in range(8):
    length_ = len(z[i])
    if length < length_:
        length = length_

# print(length)
length = length*2# length of original signal, (maybe should be length and not length*2, garoufh pou eisai <3)
length = len(signal)

for i in range(8):
    values = np.linspace(0, len(x[i]), length)
    # print(len(x[i]))
    x[i] = np.interp(values, np.arange(0, len(x[i])), x[i])
    # print(len(x[i]))

for i in range(8):
    figure_counter
    plt.figure(figure_counter)
    plt.plot(np.arange(0, length), x[i])



sum_of = np.zeros(length)
x = np.array(x)
for i in range(length):
    for j in range(8):
        sum_of[i] += x[j][i]

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(0, length), sum_of)
plt.title("sum_of")



## autocorrelation


print(len(sum_of))

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[int(result.size/2):]

autocorrelation = autocorr(sum_of)


figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(autocorrelation)), autocorrelation)
plt.title("autocorrelation")


## 4_5

## mas endiaferei to diasthma (se BPM): 60-200 (hdh apo to xroniko diagramma tou shmatos blepoume oti tha exoume sigoura 60 BPM kathws epanalambanete
## enas xtupos ana 1 deutero


from scipy.ndimage import gaussian_filter1d

def findPeaksInInterval(array):
    from scipy.signal import find_peaks
    #t = np.fft.fft(array)
    peaks, _ = find_peaks(array)
    return peaks

autocorrelation_filtered = gaussian_filter1d(autocorrelation, 1)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.arange(len(autocorrelation)), autocorrelation)
plt.title("autocorrelation_filtered")

peaks = findPeaksInInterval(autocorrelation_filtered[6615:22051])
print(peaks)
for i in range(len(peaks)):
    peaks[i] += 6615
print(peaks)
BPM = []

for i in peaks:
    BPM.append(60*22050/i)

BPM_sorted = BPM.sort()

print(BPM)

plt.show()
