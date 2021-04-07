import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

from scipy.io.wavfile import write 

##########################################################################
#                                                                        #
# We converted  the initial .wav file to a new .wav, because we coudn't  #
# read it. We used this website for the conversion:https://convertio.co/ #
#                                                                        #
########################################################################## 

figure_counter = 0 
file = ['../speech_utterance.wav',
        '../music.wav']

samplerate, data = wavfile.read(file[1])
data = data/((max(abs(data)))) # normalize our data

##########################################################################
#                                                                        #
# Short time energy function 											 #
#                                                                        #
########################################################################## 

def short_time_energy(signal, len_divisor):
    window = np.hamming(len_divisor)
    energy = list(np.convolve(signal, window))

    for i in range(len(window)):
        energy.pop(i)

    return np.array(energy)


energy = short_time_energy(abs(data) ** 2, 400)  
energy = energy/(max(abs(energy)))

len_en = int(len(energy))
time_en = np.arange(0, len_en)
 

figure_counter += 1
plt.figure(figure_counter)
plt.xlabel("time in sec")
plt.ylabel("normalized amplitudes")
plt.plot(np.arange(0, len(data))*(1/samplerate), data, 'b', label="initial signal")
plt.plot(time_en*(1/samplerate), energy, 'r', label="energy")
plt.legend() 
plt.savefig('diagrams/signal.png')
 

##########################################################################
#                                                                        #
# Zero crossing Rate													 #
#                                                                        #
########################################################################## 

def zero_crossing_rate(signal, len_divisor): 
    window = np.hamming(len_divisor) ** 2
    cross = [(abs(np.sign(signal[i+1]) - np.sign(signal[i]))) for i in range(len(signal) - 1)]
     
    cross_rate = list(np.convolve(cross, window))

    for i in range(len(window)):
        cross_rate.pop(i)

    return np.array(cross_rate)

cross_rate = zero_crossing_rate(data, 400)
cross_rate = cross_rate/max(abs(cross_rate))   




figure_counter += 1
plt.figure(figure_counter)
plt.xlabel("time in sec")
plt.ylabel("normalized amplitudes")
plt.plot(np.arange(len(data))*(1/samplerate), data, 'b', label="initial signal")
plt.plot(np.arange(int(len(cross_rate)) )*(1/samplerate), cross_rate, 'orange', label="cross rate")
plt.legend()
plt.savefig('diagrams/data_cross_rate.png')

figure_counter += 1
plt.figure(figure_counter)
plt.title("combined plot")
plt.xlabel("tim in sec")
plt.ylabel("normalized amplitudes")
plt.plot(np.arange(0, len(data))*(1/samplerate), data, 'b', label="initial signal")
plt.plot(np.arange(0, int(len(cross_rate)) )*(1/samplerate), cross_rate, 'green', label="cross rate")
plt.plot(time_en*(1/samplerate), energy, 'r', label="energy")
plt.legend()
plt.savefig('diagrams/combined_plot.png') 

plt.show() 