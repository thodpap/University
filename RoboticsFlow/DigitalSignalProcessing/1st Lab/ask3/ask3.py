import numpy as np
from scipy.io import wavfile
import pylab

from scipy.io.wavfile import write

##########################################################################
#                                                                        #
# 							IMPORTANT									 #
#                                                                        #
##########################################################################
#                                                                        #
# We converted  the initial .wav file to a new .wav, because we coudn't  #
# read it. We used this website for the conversion:https://convertio.co/ #
#                                                                        #
########################################################################## 

samplerate, data = wavfile.read('../speech_utterance.wav')

data = data/((max(abs(data))))



##SHORT_TIME_ENERGY
def short_time_energy(signal, len_divisor):
    window = []
    window = np.hamming(len_divisor)
    energy = []
    energy = np.convolve(signal, window)
    energy = list(energy)
    for i in range(len(window)):
        energy.pop(i)
    energy = np.array(energy)
    return energy


# assert samplerate % 1000 == 0
#
# sampsPerMilli = int(samplerate / 1000)
# millisPerFrame = 20
# sampsPerFrame = sampsPerMilli * millisPerFrame
# nFrames = int(len(data) / sampsPerFrame)  # number of non-overlapping _full_ frames
#
# print
# 'samples/millisecond  ==> ', sampsPerMilli
# print
# 'samples/[%dms]frame  ==> ' % millisPerFrame, sampsPerFrame
# print
# 'number of frames     ==> ', nFrames
#
# STEs = []                                      # list of short-time energies
# for k in range(nFrames):
#      startIdx = k * sampsPerFrame
#      stopIdx = startIdx + sampsPerFrame
#      window = np.zeros(data.shape)
#      window[startIdx:stopIdx] = 1               # rectangular window
#      STE = sum((data ** 2) * (window ** 2))
#      STEs.append(STE)
#
# pylab.figure(1)
# pylab.plot(STEs)
# pylab.title('Short-Time Energy')
# pylab.ylabel('ENERGY')
# pylab.xlabel('FRAME')
# pylab.autoscale(tight='both');

# energy = []
#
# # 1 16κ
# # 25*16
energy = short_time_energy(abs(data) ** 2, 200) #### FRIJO DIABASE EKFWNHSH NA BALEIS SWSTA SHMEIA ANTI GIA DIAKOSSIA H PARE CALL
energy = energy/(max(abs(energy)))

len_en = int(len(energy))
time_en = np.arange(0, len_en)

# energy_normalized = energy

counter = 0
# pylab.figure(counter)
# pylab.subplot(121)
# pylab.plot(time, energy, 'r')
# pylab.subplot(122)
# pylab.plot(np.arange(0, len(data)), data, 'b')

counter += 1
pylab.figure(counter)
pylab.xlabel("time in sec")
pylab.ylabel("normalized amplitudes")
pylab.plot(np.arange(0, len(data))*(1/samplerate), data, 'b', label="initial signal")
pylab.plot(time_en*(1/samplerate), energy, 'r', label="energy")
pylab.legend()


# newArray = []
# for i in range(11000,len(data)-1, 6000):
# 	for j in range(i,min(len(data),i+6000)):
# 		newArray.append(data[j])
# 	for j in range(10000):
# 		newArray.append(0.0)
# 	break
# newArray = np.array(newArray)


# write("easySigInitial.wav", samplerate, newArray)

##ZERO_CROSS_RATING

def zero_crossing_rate(signal, len_divisor):
    window = []
    window = np.hamming(len_divisor)
    cross = []
    for i in range(1, len(signal)):
        cross.append(abs(np.sign(signal[i]) - np.sign(signal[i-1])))
    cross_rate = np.convolve(cross, window)
    cross_rate = list(cross_rate)
    for i in range(len(window)):
        cross_rate.pop(i)
    cross_rate = np.array(cross_rate)
    return cross_rate

cross_rate = zero_crossing_rate(data, 400)
cross_rate = cross_rate/max(abs(cross_rate))


# counter += 1
# pylab.figure(counter)
# pylab.subplot(121)
# time = np.arange(0, len(cross_rate))
# pylab.plot(time, cross_rate, 'r')
# pylab.subplot(122)
# pylab.plot(np.arange(0, len(data)), data, 'b')

len_cross = int(len(cross_rate))
time_cross = np.arange(0, len_cross)

counter += 1
pylab.figure(counter)
pylab.xlabel("time in sec")
pylab.ylabel("normalized amplitudes")
pylab.plot(np.arange(0, len(data))*(1/samplerate), data, 'b', label="initial signal")
pylab.plot(time_cross*(1/samplerate), cross_rate, 'orange', label="cross rate")
pylab.legend()

counter += 1
pylab.figure(counter)
pylab.title("combined plot")
pylab.xlabel("tim in sec")
pylab.ylabel("normalized amplitudes")
pylab.plot(np.arange(0, len(data))*(1/samplerate), data, 'b', label="initial signal")
pylab.plot(time_cross*(1/samplerate), cross_rate, 'green', label="cross rate")
pylab.plot(time_en*(1/samplerate), energy, 'r', label="energy")
pylab.legend()

pylab.show()