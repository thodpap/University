import numpy as np

def d_kapelos(d_n):
	if d_n >= 0:
		return 1
	else:
		return -1

x = np.array([0,0,1,1,1,1,2,4,5,7,9,0,0,0,0]) 
d = []
x_kapelo = [0]
d_kapelo = []
x_perispomeni = []
c = []

for n in range(1, len(x)):
	d_value = x[n] - x_kapelo[n-1] 
	d_fun = d_kapelos(d_value)

	d.append(d_value) 
	d_kapelo.append(d_fun)

	x_kapelo.append(d_fun + x_kapelo[n-1])
	x_perispomeni.append(x_kapelo[n-1])

	if d_fun == 1:
		c.append(0)
	else:
		c.append(1)

print("x: ", x[1:])
print("x_perispomeni: ", x_perispomeni)
print("d: ", d)
print("d_kapelo: ", d_kapelo)
print("c: ", c)
print("x_kapelo: ", x_kapelo[1:])


