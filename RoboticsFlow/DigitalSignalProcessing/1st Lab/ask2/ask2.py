# PART_2__2_1
import numpy as np
import math
import matplotlib.pyplot as plt
import librosa
import pywt

Fs = 1000  # Hz

time = (np.linspace(0, 2, 2000))

noise = []
for i in range(len(time)):
    noise.append((np.random.normal(0)))

noise = np.array(noise) 

signal = (2 * np.cos(2 * math.pi * 70 * time) 
        + 3 * np.sin(2 * math.pi * 100 * time) 
        + 0.1 * noise)


counter = 0  # for figure()

### a)
counter += 1
plt.figure(counter)

plt.plot(time, signal)
plt.title("given signal")
plt.xlabel("amplitude")
plt.ylabel("time")

# b) - g)

my_array = [20, 40, 80]

for i in my_array:
    n_fft = i

    stfted = librosa.stft(signal, n_fft=n_fft, hop_length=int(n_fft / 2))
    spectogram = np.abs(stfted) ** 2

    # print("size: ", np.shape(spectogram), np.size(stfted))
    # print("spectogram: ", spectogram)
    # (spectogram)

    freqs = np.linspace(0, Fs / 2, int(1 + n_fft / 2))
    # print(len(freqs))

    counter += 1
    plt.figure(counter)
    timer = np.linspace(0, len(time) / n_fft, 40)
    timer = np.linspace(0, 2, int(2 * len(signal) / n_fft) + 1) * Fs / n_fft
    plt.pcolormesh(timer, freqs, spectogram)
    plt.xlabel("time")
    plt.ylabel("frequency amplitude")
    plt.title("spectogram of signal")


### d) 

def flat_list(complicated_list):
    return [item for sublist in complicated_list for item in sublist]
 
# number of octaves = log_2(f2/f1)
scales = []
upper_bound_window = Fs / 2 # 500
limit_lower_bound = 15.625/2 # 15.625
samples_per_octave = 16
while True: 
    lower_bound_window = upper_bound_window/2
    if upper_bound_window <= limit_lower_bound: 
        break
    if lower_bound_window <= limit_lower_bound:
        lower_bound_window = limit_lower_bound

    if upper_bound_window < Fs/2: # delete last element of array
        interval_added = list(np.linspace(lower_bound_window,upper_bound_window, samples_per_octave + 1))
        del(interval_added[-1])
    else:
        interval_added = list(np.linspace(lower_bound_window,upper_bound_window, samples_per_octave + 1))

    # inverse list
    interval_added = list(reversed(interval_added)) 
    scales.append(interval_added)
    upper_bound_window = upper_bound_window / 2

# flat the scales list
scales = flat_list(scales)
# inverse list
scales = list(reversed(scales))

print(np.array(scales))

 
# scales = np.power(2, np.linspace(3, 9, 100)) 
# for i in range(len(scales)):
#      if scales[i] > 500:
#          scales[i] = 500
#      else: continue
# print(scales)


coefs, frequencies = pywt.cwt(signal, scales, 'cmor3.0-1.0') 

wavTransform = np.abs(coefs)

# print(np.shape(coefs))
# print("coeffs: ", wavTransform)
print("frqs: ", frequencies)

# frequencies = frequencies*Fs

counter += 1
plt.figure(counter)
plt.pcolormesh(time, frequencies * Fs, wavTransform)
plt.title("wavelet transform of signal")
plt.xlabel("time")
plt.ylabel("scales")

plt.show()
