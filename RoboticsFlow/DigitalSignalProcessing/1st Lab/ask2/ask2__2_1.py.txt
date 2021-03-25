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
print(noise)

signal = 2 * np.cos(2 * math.pi * 70 * time) + 3 * np.sin(2 * math.pi * 100 * time) + 0.1 * noise

counter = 0  # for figure()

### a)
counter += 1
plt.figure(counter)

plt.plot(time, signal)
plt.title("given signal")
plt.xlabel("amplitude")
plt.ylabel("time")

# b) - g)

my_array = [80, 160, 240]

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


#SE AUTA TA ORIO PAIZEIS MPALA
#------------------------------------------------------------

def flat_me(listed):
    flat = []
    for sublist in listed:
        for item in sublist:
            flat.append(item)
    return flat


my_val = Fs / 2
scales = []
counter_me = 0
my_val1 = 0

for i in range(int(math.log2(Fs / 2))):
    if my_val1 == 15.625 and my_val == 15.625:
        break
    my_val1 = my_val / 2
    # print("my_val: ", my_val)
    # print("my_val1: ", my_val1)
    if my_val1 <= 15.625:
        my_val1 = 15.625
    # print("my_val1: ", my_val1)
    scales.append(list(np.linspace(my_val, my_val1, 16)))
    my_val = my_val / 2

# print(scales)
# scales = scales[1]
scales = flat_me(scales)
scales = scales[::-1]  # reverse
# scales = [int(i) for i in scales]
print("scales: ", scales)

sampling_perion = 1/Fs

scales = np.power(2, np.linspace(2, 9, 100))
for i in range(len(scales)):
     if scales[i] > 500:
         scales[i] = 500
     else: continue

print("scales: ", scales)

# -------------------------------------------------------------------------------------

#PERMISSION DENIED FRIJO


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
