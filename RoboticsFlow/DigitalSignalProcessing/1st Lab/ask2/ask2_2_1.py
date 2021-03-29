# PART_2__2_1

import numpy as np
import math
import matplotlib.pyplot as plt
import librosa
import pywt

Fs = 1000  # Hz 
figure_counter = 0   


##############################################################################
#                                                                            #
#    2.1.a: Caclulate our noise array and then calculate our signal          #
#                                                                            #
############################################################################## 
#                                                                            #
#    x(t) = 2 cos(2π70t) + 3 2 cos(2π100t) + 0.1 v(t)                        #
#                                                                            #
############################################################################## 


time = np.linspace(0, 2, 2000)
noise = np.array([np.random.normal(0) for _ in range(len(time))])

signal = (2 * np.cos(2 * math.pi * 70 * time) 
        + 3 * np.sin(2 * math.pi * 100 * time) 
        + 0.1 * noise)
 
figure_counter += 1
plt.figure(figure_counter)
plt.plot(time, signal)
plt.title("given signal")
plt.xlabel("amplitude")
plt.ylabel("time")


##############################################################################
#                                                                            #
#    2.1.b,c: Calculate the stft of your signal in windows of 0,04 sec and   #
#           aliasing the half window. Repeat for each size window            #
#                                                                            #
############################################################################## 
#                                                                            #
#    We know that in 1 second we have 1000 samples, hence,                   #
#       0.04 s in 40 samples                                                 #
#       0.08 s in 80 samples                                                 #
#       0.16 s in 160 samples                                                #
#                                                                            #
##############################################################################
#                                                                            #
#   For each window, we calculate the absolute value of the stft and plot it #
#   using pcolormesh                                                         #
#                                                                            #
##############################################################################


windows_length = [40, 80,160]

for window_length in windows_length:
    n_fft = window_length
 
    stft_ed = librosa.stft(signal, n_fft=n_fft, hop_length=int(n_fft / 2))
    spectogram = np.abs(stft_ed) ** 2 

    freqs = np.linspace(0, Fs / 2, int(1 + n_fft / 2)) 

    figure_counter += 1
    plt.figure(figure_counter)
    timer = np.linspace(0, 2, int(2 * len(signal) / n_fft) + 1) 
    plt.pcolormesh(timer, freqs, spectogram)
    plt.xlabel("Time")
    plt.ylabel("Frequency Amplitude")
    plt.title("Spectrogram of Signal")



##############################################################################
#                                                                            #
#    2.1.d: Calculate the cwt using the cmor3.0-1.0 packet.                  #
#                                                                            #
############################################################################## 
#                                                                            # 
#   The tricky part here is to correctly define the scale array for the cwt  #
#   We realised that by using a scale of 1, it corresponds to the sampling   #
#   frequency.                                                               #
#                                                                            #
############################################################################## 
#                                                                            #
#   To have 16 wavelets per octave we need to have 14 in bitween notes       #
#   (besides the first and the last).                                        #
#   Hence, we add 14 in between points to our temp_scales variable           #
#                                                                            #
############################################################################## 
#                                                                            #
#   When 2 notes are an octave apart, it means that f1 = 2*f2                #
#   To incorpore that in the scale array, we start it with 2 and double it   #
#   in each iteration. The iteration stops when we exceed the 2^6 limit      #
#                                                                            #
##############################################################################

def flat_list(complicated_list):
    return [item for sublist in complicated_list for item in sublist] 
    
scales = [] 
samples_per_octave = 16
scale_temp = 2
ending_scale = 62
change_factor = 2

while True:
    if scale_temp > ending_scale:
        break

    temp_scales = np.linspace(scale_temp, change_factor * scale_temp, samples_per_octave) 
    if scale_temp != ending_scale:   
        temp_scales = temp_scales[:-1] # Skip the last element, to not repeat it twice
    scales.append(temp_scales)
    scale_temp *= change_factor

scales = list(flat_list(scales))
print(np.array(scales))

coefs, frequencies = pywt.cwt(signal, scales, 'cmor3.0-1.0', sampling_period=1/Fs) 
wavTransform = np.abs(coefs)

print("frqs: ", frequencies)

figure_counter += 1
plt.figure(figure_counter)
plt.pcolormesh(time, frequencies, wavTransform)
plt.title("Wavelet transform of signal")
plt.xlabel("Time")
plt.ylabel("Scales")

plt.show()
