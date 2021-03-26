import numpy as np 
from scipy.io import wavfile
import pylab 

##########################################################################
# 							IMPORTANT									 #
##########################################################################
# We converted  the initial .wav file to .mp3 and then back to .wav,     #
# so there is a likelihood that the audio quality maybe slightly damaged #
# The initial conversion was required since we could not read the audio  #
# We used this website for the conversion: https://convertio.co/		 #
##########################################################################

samplerate, data = wavfile.read('speech_utterance.wav') 

def short_time_energy(signal, len_divisor):
    window = [] 
    window = np.hamming(len_divisor)

    energy = []
    energy = np.convolve(signal, window)
    return energy

energy = []

# 1 16κ 
# 25*16  
energy = short_time_energy(abs(data)**2, 40) 
energy /= max(abs(data) )

len_en = int(len(energy))
time = np.arange(0, len_en)
 
counter = 1
pylab.figure(counter)
pylab.subplot(121)
pylab.plot(time,energy, 'b')
pylab.subplot(122)
pylab.plot(np.arange(0,len(data)),data, 'r')


# counter += 1
# pylab.figure(counter)
pylab.show()
	