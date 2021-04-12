import numpy as np
import matplotlib.pyplot as plt 

axis = np.arange(12000)

line_ic = 20000 + axis*20
line_fpgas = 10000 + axis*40
line_soc_1 = 100000 + 4*axis
line_soc_2 = 200000 + 2*axis

plt.figure(1)
plt.title('Production Lines')
plt.xlabel('Pieces')
plt.ylabel('Euro')

plt.plot(axis, line_ic, label="Use discrete elements and IC")
plt.plot(axis, line_fpgas, label="Use FPGAs")
plt.plot(axis,line_soc_1, label="Design SoC-1 with small board")
plt.plot(axis,line_soc_2, label="Design Soc-2 with tiny board")

plt.legend()
plt.savefig("figure.png")
plt.show()
