import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.fftpack as fftpack
import cmath
from sklearn.metrics import mean_squared_error


# b1    

n = np.arange(32)
figure_counter = 0
signal = [(0.8 ** i) * (math.cos(0.15 * math.pi * i)) for i in n]

figure_counter += 1
plt.figure(figure_counter)
plt.plot(n, signal) 
plt.title("y[n]")
plt.xlabel("n")
plt.savefig("signal.png")
# b2

dft_signal = np.fft.fft(signal)

figure_counter += 1
plt.figure(figure_counter)
plt.stem(n, np.abs(dft_signal), use_line_collection = True)
plt.xlabel("k")
plt.title("32-points DFT of signal in absolute value")
plt.savefig("dft_signal.png")
# b3

dct_signal = fftpack.dct(signal, 2)

figure_counter += 1
plt.figure(figure_counter)
plt.stem(n, np.abs(dct_signal), use_line_collection = True)
plt.xlabel("k")
plt.title("32-points DCT-2 of signal in absolute value")
plt.savefig("dct_signal.png")

# b4 

M_list = np.arange(31)
b = np.ones(32)
b[0] = 0.5
yM, ycM= [], [] 
mean_square_error_yM = []
mean_squared_error_ycM = []

for M in M_list:  
    yM, ycM= [], [] 
    for i in n:
        sum_at_n = 0
        for k in range(M+1):  
            sum_at_n += dft_signal[k] * cmath.exp(2j * math.pi * k * i / 32)   
        for k in range(32-M,32,1):      
            sum_at_n += dft_signal[k] * cmath.exp(2j * math.pi * k * i / 32)      
        yM.append(sum_at_n/32)

    for i in n:
        sum_at_n = 0
        for k in range(M+1):  
            sum_at_n += b[k] * dct_signal[k] * math.cos(math.pi * k * (2*i + 1)/64)
        ycM.append(sum_at_n/32)
    
    if M <= 15: 
        mean_square_error_yM.append(mean_squared_error(np.real(np.array(yM)),signal)) 

    mean_squared_error_ycM.append(mean_squared_error(np.real(np.array(ycM)), signal))
 
 
figure_counter += 1
plt.figure(figure_counter)
plt.title("Mean squared error of yM and ycM")
plt.plot(M_list[0:16], mean_square_error_yM,"g", label="MSE of yM")
plt.plot(M_list, mean_squared_error_ycM, "r", label="MSE of ycM")
plt.xlabel("M") 
plt.legend()
plt.savefig("mse.png")

plt.show()