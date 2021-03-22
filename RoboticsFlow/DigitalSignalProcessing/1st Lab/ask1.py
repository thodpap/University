import numpy as np
import math
import simpleaudio as sa

n = np.array(range(1,1001))

frequencies_column    = [0.9273, 1.0247, 1.1328]
frequencies_row = [0.5346, 0.5906, 0.6535, 0.7217]

# Let our signals be named d[n]

numbers = []
for i in range(1,10):
	numbers.append(i)
numbers.append(0)

d = []
for N in n:
	temp = []
	for row in frequencies_row:
		for column in frequencies_column:
			if row == 0.7217 and (column == 0.9273 or column == 1.1328) :
				continue

			temp.append(math.sin(row * N) + math.sin(column * N))
	d.append(temp)

# print(d)
# print(d[0])
playsound(d[0])