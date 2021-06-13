import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import welch
import statistics

figure_counter = 0
omega1 = 0.4 * np.pi
omega2 = 0.5 * np.pi
omega3 = 0.8 * np.pi

N = 1024
n = np.arange(N)

phi1 = np.random.uniform(0.0, 2*np.pi, size=N)
phi2 = np.random.uniform(0.0, 2*np.pi, size=N)
 
x = (
	  3 * np.cos(omega1 * n + phi1) 
	+  	  np.sin(omega2 * n + phi2) 
	+ 5 * np.sin(omega3 * n + phi2) 
	+ np.random.randint(1)
)

f, welch = welch(x , window='hamming')

per = 1/N  * np.abs(np.fft.fft(x)) ** 2

var_per = statistics.variance(per)
var_welch = statistics.variance(welch)

file = open('variances.txt', 'w+')
file.write(
	'var_per = ' + str(var_per) 
	+ '\n' + 'var_welch = ' + str(var_welch)
)
file.close() 

# Figures
figure_counter += 1
plt.figure(figure_counter)
plt.title('x[n]')
plt.plot(n,x)

figure_counter += 1
plt.figure(figure_counter)
plt.title('Welch Method')
plt.plot(f, welch)
plt.savefig('welch.png')

figure_counter += 1
plt.figure(figure_counter)
plt.title('Periodogram Method')
plt.plot(n, per)
plt.savefig('periodogram.png')

plt.show()