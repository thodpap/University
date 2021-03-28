import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import librosa
import pywt

import warnings
warnings.simplefilter("ignore", UserWarning)

counter = 0 #for plots

data, samplerate = librosa.load('foxtrot_excerpt1.mp3') #default 22050 samplerate freq



## 4_1
signal = data[10000:(2**16+10000)]
n = np.arange(0, len(signal))

counter += 1
plt.figure(counter)
plt.plot(n, signal)



## 4_2

from scipy.signal import butter, lfilter, freqz
#
# def butter_lowpass(cutoff, fs, order=5):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     return b, a
#
#
# def butter_lowpass_filter(data, cutoff, fs, order=5):
#     b, a = butter_lowpass(cutoff, fs, order=order)
#     y = lfilter(b, a, data)
#     return y


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

## max_freq of the signal
# from scipy.fft import fft
# fft_ed = fft(signal)
# spectogram = np.abs(fft_ed) ** 2
#
# for i in range(len(spectogram)-1, 0, -1):
#     if spectogram[i] != 0:
#         index = i
#         break
#
#
# max_freq = i*samplerate/(len(spectogram))
#
# n = np.arange(0, len(fft_ed))
#
# counter += 1
# plt.figure(counter)
# plt.plot(n*22050, abs(fft_ed))



# counter += 1
# plt.figure(counter)
#
#
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
filtered_high = []
filtered_low = []
y = []

signaled = signal

details = []
approximation = []

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
    a_0 = (2**(i+1))*a_array[2]
    if i == 7:
        a_0 = a_0/2
    for j in range(len(x_i)):
        if j == 0:
            x_i[j] = a_0 * z[i][j] # x_i[j] = (1 - a_0) * x_i[j-1] + a_0 * z[i][j] but index -1 does not exist
            continue
        x_i[j] = (1-a_0)*x_i[j-1] + a_0*z[i][j]

    x.append(x_i)

print(np.array(x))

for i in range(8):
    mean = stat.mean(x[i])
    x[i] = x[i] - mean

n = np.arange(len(z[1]))

counter += 2
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
length = length*2 # length of original signal, (maybe should be length and not length*2, garoufh pou eisai <3)

for i in range(8):
    values = np.linspace(0, len(x[i]), length)
    # print(len(x[i]))
    x[i] = np.interp(values, np.arange(0, len(x[i])), x[i])
    # print(len(x[i]))

for i in range(8):
    counter += 1
    plt.figure(counter)
    plt.plot(np.arange(0, length), x[i])



sum_of_ = np.zeros(length)

for i in range(length):
    for j in range(8):
        sum_of_[i] += x[j][i]

counter += 1
plt.figure(counter)
plt.plot(np.arange(0, length), sum_of_)
plt.title("sum_of_")



## autocorrelation


print(len(sum_of_))

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[int(result.size/2):]

autocorrelation = autocorr(sum_of_)


counter += 1
plt.figure(counter)
plt.plot(np.arange(len(autocorrelation)), autocorrelation)
plt.title("autocorrelation")


plt.show()