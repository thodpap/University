import numpy as np
import matplotlib.pyplot as plt 


figure_counter = -1

figure_titles = [  
	"Poisson Process"
]

labelTuple = [  
	("Time","k count")
]



##############################
# A 						 #
##############################

lamda = 5

grid = np.random.exponential(1/lamda,100)
#print ("This is MEAN",np.mean(grid))
grid = [sum(grid[0:i]) for i in range(100)]


figure_counter += 1
plt.figure(figure_counter)
plt.title(figure_titles[figure_counter])

 
plt.step(range(100), grid,label = "Poisson Process Counting", color = "red")


xlabel, ylabel = labelTuple[figure_counter]
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid() 	 
plt.savefig("../figures/PoissonProcesses/" + str(figure_counter) + ".png")
plt.show()


##############################
# B 						 #
##############################

for i in [2,3,5,10,100]:
    grid = np.random.poisson(lamda,i*100)
    print ("For Lambda = {}, mean is {}".format(i*100,np.mean(grid)))
 