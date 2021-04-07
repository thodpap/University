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

plt.show()

plt.savefig("../figures/PoissonProcesses/" + str(figure_counter) + ".png")

##############################
# B 						 #
##############################

for i in [2,3,5,10,100]:
    grid = np.random.poisson(lamda,i*100)
    print ("For Lambda = {}, mean is {}".format(i*100,np.mean(grid)))

# For Lambda = 200, mean is 4.775
# For Lambda = 300, mean is 5.036666666666667
# For Lambda = 500, mean is 5.038
# For Lambda = 1000, mean is 4.966
# For Lambda = 10000, mean is 5.0013
