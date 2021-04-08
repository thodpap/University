import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import expon


figure_counter = -1

figure_titles = [ 
	"Probability Density Function of Exponential Process",
	"Cumulative Density Function of Exponential Process", 
]

labelTuple = [ 
	("k values","Probability"),
	("k values","Probability"), 
]
  
##############################
# A 						 #
##############################

colors = ['red','green','blue','black'] 
inverse_lamdas = [0.5,1,3]
axis = np.arange(0,8,0.00001)

figure_counter += 1
plt.figure(figure_counter)
plt.title(figure_titles[figure_counter])
for i, lamda in enumerate(inverse_lamdas): 
	plt.plot(axis, expon.pdf(axis, 0,lamda), label=str(lamda))


xlabel, ylabel = labelTuple[figure_counter]
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid() 	
plt.legend()  
plt.savefig("../figures/ExponentialDistribution/" + str(figure_counter) + ".png")

##############################
# B 						 #
##############################

figure_counter += 1
plt.figure(figure_counter)
for i, lamda in enumerate(inverse_lamdas): 
	plt.plot(axis, expon.cdf(axis, 0,lamda), label=str(lamda))  

xlabel, ylabel = labelTuple[figure_counter]
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid() 	
plt.legend()
plt.savefig("../figures/ExponentialDistribution/" + str(figure_counter) + ".png")


##############################
# C 						 #
##############################

print ("Pr(X>30.000) = ", 1 - expon.cdf(axis[30000],0,2.5))
print ("Pr(X>50.000) = ", 1 - expon.cdf(axis[50000],0,2.5))
print ("Pr(X>20.000) = ", 1 - expon.cdf(axis[20000],0,2.5))
print ("Pr(X>50.000 | X>20.000) = ",(1 - expon.cdf(axis[50000],0,2.5))/(1-expon.cdf(axis[20000],0,2.5)))


plt.show()