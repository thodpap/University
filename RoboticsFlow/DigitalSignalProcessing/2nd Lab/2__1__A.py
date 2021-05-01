import numpy as np
import matplotlib.pylab as plt
import math
import librosa
import cmath
from scipy.fft import fft, ifft
from scipy.io.wavfile import read, write

import warnings

warnings.filterwarnings('ignore')

N = 7
d = 0.08  # meter
c = 340  # m/s
figure_counter = 0

theta_signal = math.pi / 4
theta_noise = 3 * math.pi / 4

samplerate, n_0 = read("Material/MicArraySimulatedSignals/sensor_0.wav")
print(n_0[5000])
_, n_1 = read("Material/MicArraySimulatedSignals/sensor_1.wav")
_, n_2 = read("Material/MicArraySimulatedSignals/sensor_2.wav")
_, n_3 = read("Material/MicArraySimulatedSignals/sensor_3.wav")
_, n_4 = read("Material/MicArraySimulatedSignals/sensor_4.wav")
_, n_5 = read("Material/MicArraySimulatedSignals/sensor_5.wav")
_, n_6 = read("Material/MicArraySimulatedSignals/sensor_6.wav")
_, original = read("Material/MicArraySimulatedSignals/source.wav")
print(original[5000])

n = [list(n_0), list(n_1), list(n_2), list(n_3), list(n_4), list(n_5), list(n_6)]

## calculate τn

tn = []
for i in range(7):
    tn.append(-(i - (N - 1) / 2) * d * math.cos(theta_signal) / c)

my_len = len(n[0])  # length of all signals


# DFT OF SIGNALS

dfts = []



for i in range(7):
    dfts.append(fft(n[i]))

dft_len = len(dfts[0]) 

new_dfts = []

for i in range(7):
    temp = []
    for k in range(len(dfts[0])):
        temp.append(dfts[i][k] * np.exp(-1j * 2*math.pi * k * tn[i] / dft_len))
    new_dfts.append(temp)



idfts = []
for i in range(7):
    idfts.append(np.fft.ifft(new_dfts[i]))

print("gsfgfgdg: ", idfts[2][5001])

print("idft: ", idfts[0])

output = []
for i in range(len(idfts[0])):
    output.append(idfts[0][i] + idfts[1][i] + idfts[2][i] + idfts[3][i] + idfts[4][i] + idfts[5][i] + idfts[6][i])
print("00: ", output[5000])
output = np.array(output)
original = np.array(original)
diff = []
for i in range(len(output)):
    diff.append(output[i] - original[i])

diff = np.array(diff)

# diff = np.real(diff)
print(diff)
print(diff.astype(n_3.dtype))
write("beam_former_ouput.wav", samplerate, diff.astype(n_3.dtype))
