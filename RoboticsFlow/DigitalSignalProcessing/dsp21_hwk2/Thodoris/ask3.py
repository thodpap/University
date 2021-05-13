import numpy as np
import matplotlib.pylab as plt
import math

figure_counter = 0
M = 21 
t = M / 2
n = np.arange(401) # 0, 1, 2 ,...,400  
phi = np.cos(np.pi * n / 5 + 4 * np.sin(3 * np.pi * n / 200)) # i guess there is a typo with "/n"

a = 1 + 0.6 * np.cos(np.pi * n / 100) 
x = a * np.cos(phi)

def calculate_hd(M,t):
	h_d = []
	for n in range(0, M+1):
		if n == t:
			h_d.append(0)
		else:
			h_d.append( (1 - np.cos(np.pi * (n - t))) / (np.pi * (n - t)) )
	return h_d

h_d = calculate_hd(M,t) 
y = np.convolve(x,h_d, "same") 

a_ = np.sqrt(x ** 2 + y ** 2)

phi_ = np.arctan2(y,x)

omega = [ phi[n] - phi[n-1]  for n in range(1,len(phi) - 1)] 
omega_ = [ (phi_[n + 1] - phi_[n-1])/2 for n in range(1, len(phi_) - 1)]


def RMS(signal, signal_):
	def rms(signal):
		signal = np.array(signal)
		return math.sqrt(sum(signal ** 2)) / len(signal)

	signal = np.array(signal)
	signal_ = np.array(signal_)

	res = []
	diff = signal - signal_
	for i in range(len(signal)):
		res.append( diff[i] / signal[i])

	return rms(res) * 100

print("Rms of a and a_ is : " + str(RMS(a,a_)) + "%")
print("Rms of omega and omega_ is : " + str(RMS(omega,omega_)) + "%") 

figure_counter += 1
plt.figure(figure_counter)
plt.title('x')
plt.xlabel('samples')
plt.plot(x)
plt.savefig("x.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('h_d')
plt.xlabel('samples')
plt.plot(h_d)
plt.savefig("h_d.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('y')
plt.xlabel('samples')
plt.plot(y)
plt.savefig("y.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('a')
plt.xlabel('samples')
plt.plot(a)
plt.savefig("a.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('a_')
plt.xlabel('samples')
plt.plot(a_)
plt.savefig("a_.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('phi')
plt.xlabel('samples')
plt.plot(phi)
plt.savefig("phi.png")


figure_counter += 1
plt.figure(figure_counter)
plt.title('phi_')
plt.xlabel('samples')
plt.plot(phi_)
plt.savefig("phi_.png")


figure_counter += 1
plt.figure(figure_counter)
plt.title('omega')
plt.xlabel('samples')
plt.plot(omega)
plt.savefig("omega.png")

figure_counter += 1
plt.figure(figure_counter)
plt.title('omega_')
plt.xlabel('samples')
plt.plot(omega_)
plt.savefig("omega_.png")

plt.show()