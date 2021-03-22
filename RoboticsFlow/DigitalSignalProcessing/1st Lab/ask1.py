import numpy as np
import math 

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



 
# print(d[0]) 
