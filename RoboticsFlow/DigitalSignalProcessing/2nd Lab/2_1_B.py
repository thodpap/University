import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import welch, spectrogram 
from scipy.fft import fft, ifft 
import librosa as lib 

N = 7
d = 0.08  # meter
figure_counter = 0
theta_signal = math.pi / 4
start, end = 0.47, 0.5
c = 340 # m/s 

path = "Material/MicArraySimulatedSignals/"
def read_from_inputs(path):
    n_3, samplerate  = lib.load(path + "sensor_3.wav",sr=None, offset=start, duration=end-start)
    original, samplerate = lib.load(path + "source.wav", sr=None, offset=start, duration=end-start) 

    return n_3, original, samplerate

n_3, original, samplerate = read_from_inputs(path)
fft_num = 2*len(n_3)

def calculate_hw(n_3, original, samplerate, fft_num): 
    fft_ = np.fft.fft(original)
    freqs = np.fft.fftfreq(len(fft_)) 
     
    noise = n_3 - original
    
    dft_n_3 = np.fft.fft(n_3, n=fft_num)

    f1, Sn_3       = welch(n_3, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
    f2, S_noise    = welch(noise, detrend=False, return_onesided=False, fs=48000, nfft=fft_num)
    f3, S_original = welch(original, detrend=False, return_onesided=False, fs=48000, nfft=fft_num) 

    Hw = []
    for i in range(len(S_noise)):
        Hw.append(1 - S_noise[i] / Sn_3[i]) 

    freqs = []
    Hw_PSD = []
    for i in range(len(f1)):
        if 0 <= f1[i] <= 8000:
            freqs.append(f1[i])
            Hw_PSD.append(Hw[i])
        else:
            break

    return Hw, f1,f2,f3, Sn_3, S_noise, S_original, noise, freqs, Hw_PSD, dft_n_3


Hw, f1,f2,f3, Sn_3, S_noise, S_original, noise, freqs, Hw_PSD, dft_n_3 = calculate_hw(n_3, original, samplerate, fft_num)

figure_counter += 1
plt.figure(figure_counter)
plt.title("S_noise")
plt.plot(S_noise)

figure_counter += 1
plt.figure(figure_counter)
plt.title("Power Spectral Density of n_3")
plt.plot(Sn_3)

figure_counter += 1
plt.figure(figure_counter)
plt.title("Original Signals' Power Spectral Density")
plt.plot(S_original)  

figure_counter += 1
fig = plt.figure(figure_counter)
ax = fig.add_subplot(111)
# plt.yscale('log')
plt.semilogy(freqs,Hw_PSD)
plt.title("Wiener Filter PSD")
plt.xlabel("Hertz")
plt.ylabel("Wiener Filter PSD Amplitude")
  
# 2) 
def calculate_nsd():
    nsd = []
    for i in range(len(freqs)): 
        nsd.append(math.pow(1 - Hw_PSD[i], 2)) ## error with ** 2
    return nsd

nsd = calculate_nsd()
  
figure_counter += 1
fig = plt.figure(figure_counter)
ax = fig.add_subplot(111)
# plt.yscale('log')
plt.semilogy(freqs, nsd)
plt.title("speech Distortion PSD")
plt.xlabel("Hertz")
plt.ylabel("speech Distortion PSD Amplitude")
 
# 3) 

def calculate_wiener_output(Hw):
    output_wiener = []  
    for i in range(len(Hw)): 
        output_wiener.append(dft_n_3[i]*Hw[i])   
    freqs = np.fft.fftfreq(len(output_wiener))  

    output_wiener_time = np.fft.ifft(output_wiener, n=fft_num)    
    f, S_output = welch(output_wiener_time, detrend=False, return_onesided=False, fs=48000) 

    return output_wiener_time, output_wiener, freqs, f, S_output

output_wiener_time, output_wiener, freqs, f, S_output = calculate_wiener_output(Hw)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(freqs*samplerate, output_wiener)
plt.title("DFT of Output Wiener")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(dft_n_3)
plt.title("DFT of Microphone 3")
 
figure_counter += 1
plt.figure(figure_counter)
plt.title('Wiener Graphs')
plt.plot(S_original, label="source signal")
plt.plot(Sn_3, label="microphone 3")
plt.plot(S_output, label="wiener filer output")
plt.plot(S_noise, label="noise")
plt.legend()
 

## 4)

output_wiener_time = np.array(output_wiener_time) 

space = np.arange(len(original))
output_wiener_time = np.interp(space, np.arange(len(output_wiener_time)), output_wiener_time) 
 
figure_counter += 1
plt.figure(figure_counter)
plt.plot(output_wiener_time)
plt.title("Output Wiener_Time")


def SNR(original, output):
    def signal_energy(signal):
        energy = 0.0
        for n in range(len(signal)):
            energy += math.pow(abs(signal[n]), 2)

        return energy

    noise = output - original
    SNR = 10 * np.log10(signal_energy(original) / signal_energy(noise))
    return SNR

SNR_output = SNR(original, output_wiener_time)  
SNR_input = SNR(original, n_3) 

print("SNR input: ", SNR_input)
print("SNR output: ", SNR_output)
 

################################################################################
   
theta_signal = math.pi / 4
theta_noise = 3 * math.pi / 4


path = "Material/MicArraySimulatedSignals/sensor_"
endpath = ".wav"


def read_from_files(path, endpath):
    n = []
    for i in range(7):
        data, y = lib.load(path + str(i) + endpath, sr=None)
        n.append(data)

    original, samplerate = lib.load("Material/MicArraySimulatedSignals/source.wav", sr=None)
    return samplerate, n, original
 
samplerate, n, original = read_from_files(path, endpath)
 
def time_delays():
    tn = []
    for i in range(7):
        tn.append(((-(i - (N - 1) / 2) * d * math.cos(theta_signal)) / c) * samplerate)
    return np.array(tn) 

tn = time_delays()
my_len = len(n[0])  # length of all signals


# DFT OF SIGNALS
def calculate_output(n, tn):
    def calculate_dfts(n):
        dfts = []
        for i in range(7):
            dfts.append(list(fft(n[i])))
        return np.array(dfts)

    def calculate_idfts(dfts, dft_len):
        idfts = []
        for i in range(7):
            temp = []
            for k in range(dft_len):
                temp.append(dfts[i][k] * np.exp(-1j * 2 * math.pi * k * tn[N - 1 - i] / dft_len))  # m = tn[i]

            idfts.append(np.fft.ifft(temp))
        return idfts

    def find_output(idfts):
        output = []
        for i in range(len(idfts[0])):
            sum = 0.0
            for j in range(7):
                sum += idfts[j][i]

            output.append((1 / 7) * sum)
        return output

    dfts = calculate_dfts(n)
    dft_len = len(dfts[0])
    idfts = calculate_idfts(dfts, dft_len)

    return find_output(idfts)


output = np.array(calculate_output(n, tn))

SNR_beam = SNR(original, output) 
print("SNR_beam: ", SNR_beam)
print("SNR_input: ", SNR_input)
print("SNR_wiener_output: ", SNR_output) 

write("wiener_ouput.wav", samplerate, output_wiener_time.astype(n[3].dtype))  

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output_wiener_time)
plt.title("output_wiener")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title("original")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(output)
plt.title("beam_output")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n_3)
plt.title("input")

plt.show()
