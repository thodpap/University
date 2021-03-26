import numpy as np 
from scipy.io import wavfile
import matplotlib.pyplot as plt

def short_time_energy(signal, len_divisor):
    window = []
    window_length = int(len(signal)/len_divisor)
    window = np.hamming(window_length)

    energy = []
    energy = np.convolve(signal, window)
    return energy

counter = 0


#conversion from type b-Nist to wav file from:https://convertio.co/
samplerate, data = wavfile.read('speech_utterance.wav')

length = len(data)

counter += 1
plt.figure(counter)
n = np.arange(0, length)
plt.plot(n, data)
plt.show()


energy = []
energy = short_time_energy(data, 50)
len_en = int(len(energy))
time = np.arange(0, len_en)

print(len(time))
print(len(n))

# counter += 1
# plt.figure(counter)
# plt.plot()
