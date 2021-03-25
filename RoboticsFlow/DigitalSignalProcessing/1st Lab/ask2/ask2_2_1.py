# PART_2__2_1

import numpy as np
import math
import matplotlib.pyplot as plt
import librosa
import pywt

Fs = 1000  # Hz

time = np.linspace(0, 2, 2000)
noise = np.array([np.random.normal(0) for _ in range(len(time))])

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
# 1s se 1000 digmata
# 0.04s se 40
# 0.08s se 80
# 0.16s se 160

windows_length = [40, 80,160]

for window_length in windows_length:
    n_fft = window_length
 
    stft_ed = librosa.stft(signal, n_fft=n_fft, hop_length=int(n_fft / 2))
    spectogram = np.abs(stft_ed) ** 2

    # print("size: ", np.shape(spectogram), np.size(stft_ed))
    # print("spectogram: ", spectogram)
    # (spectogram)

    freqs = np.linspace(0, Fs / 2, int(1 + n_fft / 2))
    # print(len(freqs))

    counter += 1
    plt.figure(counter)
    timer = np.linspace(0, 2, int(2 * len(signal) / n_fft) + 1) 
    plt.pcolormesh(timer, freqs, spectogram)
    plt.xlabel("Time")
    plt.ylabel("Frequency Amplitude")
    plt.title("Spectrogram of Signal")


### d) 

def flat_list(complicated_list):
    return [item for sublist in complicated_list for item in sublist]
 
# number of octaves = log_2(f2/f1)

# 2 -> 500 
# 4 -> 250
# 62 -> 15.625
scales = [] 
samples_per_octave = 16
scale = 2
ending_scale = 62
change_factor = 2

while True:
    if scale > ending_scale:
        break

    temp_scales = np.linspace(scale, change_factor * scale, samples_per_octave) 
    if scale != ending_scale:
        temp_scales = temp_scales[:-1]
    scales.append(temp_scales)
    scale *= change_factor

scales = list(flat_list(scales))
print(np.array(scales))
 
coefs, frequencies = pywt.cwt(signal, scales, 'cmor3.0-1.0', sampling_period=1/Fs) 
wavTransform = np.abs(coefs)

print("frqs: ", frequencies)

counter += 1
plt.figure(counter)
plt.pcolormesh(time, frequencies, wavTransform)
plt.title("Wavelet transform of signal")
plt.xlabel("Time")
plt.ylabel("Scales")

plt.show()
