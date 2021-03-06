# PART_2__2_1

import numpy as np
import math
import matplotlib.pyplot as plt
import librosa
import pywt
from scipy import signal

from scipy.signal import get_window

Fs = 1000  # Hz
figure_counter = 0

##############################################################################
#                                                                            #
#    2.2.a: Caclulate our noise array and then calculate our signal          #
#                                                                            #
##############################################################################
#                                                                            #
#    x(t) = 1.5 cos(2π80t) + 0.15v(t) + 1.7(δ(t − 0.725) − δ(t − 0.900))     #
#                                                                            #
##############################################################################


time = np.linspace(0, 2, 2000)
# noise = np.array([np.random.normal(0) for _ in range(len(time))])
noise = np.random.normal(0, 1, 2000)  
dirac1 = signal.unit_impulse(2000, 725)
dirac2 = signal.unit_impulse(2000, 900)

signal = 1.5*np.cos(2*math.pi*80*time) + 0.15*noise + 1.7*dirac1 - 1.7*dirac2

figure_counter += 1
plt.figure(figure_counter)
plt.plot(time, signal)
plt.title("Signal")
plt.xlabel("amplitude")
plt.ylabel("time")
plt.savefig('ask2_2/signal.png')


##############################################################################
#                                                                            #
#    2.2.b,c: Calculate the stft of your signal in windows of 0,04 sec and   #
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

windows_length = [40, 80, 160]

for window_length in windows_length:
    n_fft = window_length

    stft_ed = librosa.core.stft(signal, n_fft=2000, win_length=n_fft, hop_length=int(n_fft/2))   
    spectogram = np.abs(stft_ed)
    print(spectogram.shape)
    freqs = np.linspace(0, Fs / 2, spectogram.shape[0])  

    figure_counter += 1
    plt.figure(figure_counter)
    ax = plt.subplot2grid((2,1), (0,0))    
    timer = np.linspace(0, 2, spectogram.shape[1])  
    plt.contour(timer, freqs, np.abs(spectogram), 15)
    plt.xlabel("Time")
    plt.ylabel("Frequency Amplitude") 
    plt.title("Spectogram of Signal with window " + str(window_length) + " samples") 
     
    ax = plt.subplot2grid((2,1), (1,0))    
    plt.pcolormesh(np.linspace(0, 2, int(2 * len(signal) / n_fft) + 1), freqs, spectogram) 
    plt.xlabel("Time")
    plt.ylabel("frequencies")
    plt.savefig('ask2_2/spectograms_' + str(window_length) + '.png')



##############################################################################
#                                                                            #
#    2.2.d: Calculate the cwt using the cmor3.0-1.0 packet.                  #
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

coefs, frequencies = pywt.cwt(signal, scales, 'cmor3.0-1.0', sampling_period=1 / Fs)
wavTransform = np.abs(coefs)

print("frqs: ", frequencies)

figure_counter += 1
plt.figure(figure_counter)
plt.contour(time, frequencies, wavTransform, 15)
plt.title("Wavelet transform of signal with contour")
plt.xlabel("Time")
plt.ylabel("Scales")


ax = plt.subplot2grid((2,1),(0,0))
plt.contour(time, frequencies, wavTransform, 15)
plt.title("Wavelet transform of signal")
plt.xlabel("Time")
plt.ylabel("Scales")

ax = plt.subplot2grid((2,1),(1,0))
plt.pcolormesh(time, frequencies, wavTransform) 
plt.xlabel("Time")
plt.ylabel("Scales")
plt.tight_layout()
plt.savefig('ask2_2/wavelet_transform.png')

plt.show()
