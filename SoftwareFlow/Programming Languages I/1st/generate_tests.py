N = 500
M = 50000
f = open("./C++/longest.txt", "w")
f.write(str(M) + " " + str(N) + '\n')

import random

for i in range(M):
	t = random.randint(-10001,10001)
	if i == M - 1:
		f.write(str(t) + '\n')
	else:
		f.write(str(t) + " ") 

f.close() 