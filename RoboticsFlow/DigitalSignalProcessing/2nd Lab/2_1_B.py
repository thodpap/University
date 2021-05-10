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

fft_num = len(n_3) 

def calculate_hw(n_3, original, samplerate, fft_num):       
    noise = n_3 - original
    
    dft_n_3 = np.fft.fft(n_3, n=fft_num)

    f1, Sn_3       = welch(n_3, detrend=False, return_onesided=False, fs=samplerate, nfft=fft_num)
    f2, S_noise    = welch(noise, detrend=False, return_onesided=False, fs=samplerate, nfft=fft_num)
    f3, S_original = welch(original, detrend=False, return_onesided=False, fs=samplerate, nfft=fft_num) 

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
plt.savefig("Figures/2_1/B/S_noise.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title("Power Spectral Density of n_3")
plt.plot(Sn_3)
plt.savefig("Figures/2_1/B/Sn_3.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title("Original Signals' Power Spectral Density")
plt.plot(S_original)  
plt.savefig("Figures/2_1/B/S_original.png")

figure_counter += 1
fig = plt.figure(figure_counter)
ax = fig.add_subplot(111)
# plt.yscale('log')
plt.semilogy(freqs,np.real(Hw_PSD))
plt.title("Wiener Filter PSD")
plt.xlabel("Hertz")
plt.ylabel("Wiener Filter PSD Amplitude")
plt.savefig("Figures/2_1/B/Hw_PSD.png")
  
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
plt.savefig("Figures/2_1/B/nsd_semilogy.png")
 
# 3) 

def calculate_wiener_output(Hw):
    output_wiener = []  
    for i in range(len(Hw)): 
        output_wiener.append(dft_n_3[i]*Hw[i])   
    freqs = np.fft.fftfreq(len(output_wiener))  

    output_wiener_time = np.fft.ifft(output_wiener, n=fft_num)    
    f, S_output = welch(output_wiener_time, detrend=False, return_onesided=False, fs=48000, nfft=fft_num) 

    return output_wiener_time, output_wiener, freqs, f, S_output

output_wiener_time, output_wiener, freqs, f, S_output = calculate_wiener_output(Hw)

figure_counter += 1
plt.figure(figure_counter)
plt.plot(freqs*samplerate, np.real(output_wiener))
plt.title("DFT of Output Wiener")
plt.savefig("Figures/2_1/B/output_wiener.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.real(dft_n_3))
plt.title("DFT of Microphone 3")
plt.savefig("Figures/2_1/B/dft_n_3.png")



def fill_freqs(f_i, signal):
    freqs = [] 
    new_sig = []
    for i, f in enumerate(f_i):
        if 0 <= f <= 8000:
            freqs.append(f) 
            new_sig.append(signal[i])
        else:
            break
    return freqs, new_sig

figure_counter += 1
plt.figure(figure_counter)
plt.title('Wiener Graphs')
plt.xlim([0,8000]) 
f1, s1 = fill_freqs(f,S_output)
f2, s2 = fill_freqs(f1,Sn_3)
f3, s3 = fill_freqs(f2,S_noise)
f4, s4 = fill_freqs(f3,S_original)
plt.semilogy(f1 , np.real(s1), label="wiener filer output")
plt.semilogy(f2 , np.real(s2), label="microphone 3")
plt.semilogy(f3 , np.real(s3), label="noise")
plt.semilogy(f4 , np.real(s4), label="source signal")
plt.legend()
plt.savefig("Figures/2_1/B/Wiener_Graphs_semilogy.png")
 

figure_counter += 1
plt.figure(figure_counter)
plt.title('Wiener Graphs') 
plt.plot(S_output, label="wiener filer output")
plt.plot(Sn_3, label="microphone 3")
plt.plot(S_noise, label="noise")
plt.plot(S_original, label="source signal")
plt.legend()
plt.savefig("Figures/2_1/B/Wiener_Graphs.png")
 

## 4)

output_wiener_time = np.array(output_wiener_time) 

space = np.arange(len(original))
output_wiener_time = np.interp(space, np.arange(len(output_wiener_time)), output_wiener_time) 
 
figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.real(output_wiener_time))
plt.title("Output Wiener_Time")
plt.savefig("Figures/2_1/B/output_wiener_time.png")


def SNR(original, output):
    def signal_energy(signal):
        energy = 0.0
        for n in range(len(signal)):
            energy += math.pow(abs(signal[n]), 2)

        return energy

    noise = output - original
    SNR = 10 * np.log10(signal_energy(original) / signal_energy(noise))
    return SNR

 

################################################################################
   
theta_signal = math.pi / 4
theta_noise = 3 * math.pi / 4


path = "Material/MicArraySimulatedSignals/sensor_"
endpath = ".wav"

def read_from_files(path, endpath):
    n = []
    for i in range(7):
        data, y = lib.load(path + str(i) + endpath, sr=None, offset=start, duration=end-start)
        n.append(data)

    original, samplerate = lib.load("Material/MicArraySimulatedSignals/source.wav", sr=None, offset=start, duration=end-start)
    return samplerate, n, original
 
samplerate, n, original = read_from_files(path, endpath)
 
def time_delays():
    tn = []
    for i in range(7):
        tn.append(((-(i - (N - 1) / 2) * d * math.cos(theta_signal)) / c) * samplerate)
    return np.array(tn) 

tn = time_delays()
my_len = len(n[0])  # length of all signals

 
def calculate_beam_output(n, tn):
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


beam_output = np.array(calculate_beam_output(n, tn))

print(len(original))
SNR_beam = SNR(original, beam_output) 
SNR_weiner_output = SNR(original, output_wiener_time)
SNR_input = SNR(original,n_3)

print("SNR_input: ", SNR_input)  
print("SNR_beam: ", SNR_beam)
print("SNR_wiener_output: ", SNR_weiner_output) 

# write("wiener_ouput.wav", samplerate, output_wiener_time)  


figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.real(output_wiener_time))
plt.title("output_wiener")
plt.savefig("Figures/2_1/B/output_wiener_time.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(original)
plt.title("original")
plt.savefig("Figures/2_1/B/original.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.real(beam_output))
plt.title("beam_output")
plt.savefig("Figures/2_1/B/beam_output.png")

figure_counter += 1
plt.figure(figure_counter)
plt.plot(np.real(n_3))
plt.title("input")
plt.savefig("Figures/2_1/B/input.png")


plt.show()
