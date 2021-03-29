import numpy as np
from scipy.io import wavfile
import pylab

from scipy.io.wavfile import write 


##############################################################################
#                                                                            #
#    3.1: Analysie speech utterance.wav file						         #
#                                                                            #
##############################################################################


##########################################################################
#                                                                        #
# 							IMPORTANT									 #
#                                                                        #
##########################################################################
#                                                                        #
# We converted  the initial .wav file to a new .wav,				     #
# so there is a likelihood that the audio quality maybe slightly damaged #
# The initial conversion was required since we could not read the audio  #
# We used this website for the conversion: https://convertio.co/		 #
#                                                                        #
##########################################################################



samplerate, data = wavfile.read('../speech_utterance.wav')

data = data/(max(abs(data)))



##############################################################################
#                                                                            #
#    
#                                                                            #
############################################################################## 

##SHORT_TIME_ENERGY
def short_time_energy(signal, len_divisor):
    window = []
    window = np.hamming(len_divisor)
    energy = []
    energy = np.convolve(signal, window)
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
energy = short_time_energy(abs(data) ** 2, 400)
# energy = energy/max(abs(data))**2

len_en = int(len(energy))
time = np.arange(0, len_en)

energy_normalized = energy/max(abs(data))

counter = 1
pylab.figure(counter)
pylab.subplot(121)
pylab.plot(time, energy, 'r')
pylab.subplot(122)
pylab.plot(np.arange(0, len(data)), data, 'b')

# counter += 1
# pylab.figure(counter)
pylab.show()


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
