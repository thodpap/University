import numpy as np
from scipy.stats import binom
from scipy.stats import poisson
import matplotlib.pyplot as plt

figure_counter = -1

figure_titles = [
	"Probability Mass Function using Poisson Process",
	"Convolution of 2 Poisson processes",
	"Poisson process as the limit of the Binomial process", 
]

labelTuple = [
	("k values","Probability"),
	("k values","Probability"),
	("k values","Probability"), 
] 
 


##############################
# A 						 #
##############################

lamdas = [3,10,30,50]
axis = np.arange(70)

figure_counter += 1
plt.figure(figure_counter)
plt.title(figure_titles[figure_counter])
colors = ['red','green','blue','black'] 
for i, lamda in enumerate(lamdas): 
	markerline, stemlines, baseline = plt.stem(axis, poisson.pmf(axis, lamda), colors[i] , use_line_collection=True,label="lamda = " + str(lamda) ) 
	markerline.set_markerfacecolor(colors[i])


xlabel, ylabel = labelTuple[figure_counter]
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid() 
plt.legend()
plt.savefig("../figures/PoissonDistribution/" + str(figure_counter) + ".png")

##############################
# B 						 #
##############################

for lamda in lamdas:
	mean,var ,skew, kurt = poisson.stats(lamda,moments='mvsk')
	print ("For lamda = ", lamda, ", we have mean = ", mean, " and variance = ", var)



##############################
# C 						 #
##############################

lamdas = [10,50]

conv = np.convolve(poisson.pmf(axis, lamdas[0]),poisson.pmf(axis, lamdas[1])) 

figure_counter += 1
plt.figure(figure_counter)
plt.title(figure_titles[figure_counter])

for i, lamda in enumerate(lamdas): 
	markerline, stemlines, baseline = plt.stem(axis, poisson.pmf(axis, lamda), label="lamda = " + str(lamda) , use_line_collection=True) 
	markerline.set_markerfacecolor(colors[i])


	xlabel, ylabel = labelTuple[figure_counter]
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)


markerline, stemlines, baseline = plt.stem(np.arange(len(conv)),conv, label="Convolution" , use_line_collection=True) 
markerline.set_markerfacecolor(colors[3])
xlabel, ylabel = labelTuple[figure_counter]
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.grid()  
plt.legend()
plt.savefig("../figures/PoissonDistribution/" + str(figure_counter) + ".png")


##############################
# D 						 #
##############################

axis = np.arange(200)
lamdas = [30,60,90,120]
P = [30/lamda for lamda in lamdas]

figure_counter += 1
plt.figure(figure_counter)
plt.title(figure_titles[figure_counter])

for i, p in enumerate(P):
	markerline, stemlines, baseline = plt.stem(axis, binom.pmf(axis,lamdas[i],p),label=('lamda = '+ str(lamdas[i])),use_line_collection=True)
	markerline.set_markerfacecolor(colors[i])

	xlabel, ylabel = labelTuple[figure_counter]
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

plt.grid()  
plt.legend()
plt.savefig("../figures/PoissonDistribution/" + str(figure_counter) + ".png")




plt.show()