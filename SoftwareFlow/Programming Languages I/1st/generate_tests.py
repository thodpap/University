N = 1000
M = 500000
f = open("./C++/longest.txt", "w")
f.write(str(M) + " " + str(N) + '\n')

import random

for i in range(M):
	t = random.randint(-100001,100001)
	if i == M - 1:
		f.write(str(t) + '\n')
	else:
		f.write(str(t) + " ") 

f.close() 