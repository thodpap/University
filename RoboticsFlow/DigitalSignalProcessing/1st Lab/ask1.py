import numpy as np
import math 
import pylab 
n = np.array(range(1,1001))

frequencies_column    = [0.9273, 1.0247, 1.1328]
frequencies_row = [0.5346, 0.5906, 0.6535, 0.7217]

# Let our signals be named d[n]
d = []
d.append(np.sin(0.7217 * n) + np.sin(1.0247 * n)) # d[0]
for row in frequencies_row:
	for column in frequencies_column:
		if row == 0.7217:
			continue
		d.append(np.sin(row * n) + np.sin(column * n))
d = np.array(d)

# Caclulates the DFT of a signal x
def DFT(x):  

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X

X_2 = DFT(d[2])
X_7 = DFT(d[7])

# Caclulate the frequency
N_2,N_7 = len(X_2), len(X_7)
array_n_2,array_n_7 = np.arange(N_2), np.arange(N_7)
T =  N_2 / 1000
freq, freq7 = array_n_2 / T, array_n_7 / T 

pylab.figure()
pylab.subplot(121)
pylab.plot(freq, abs(X_2))
pylab.subplot(122)
pylab.plot(freq, abs(X_7))

pylab.show()


