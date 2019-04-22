import numpy as np
import matplotlib.pyplot as plt

mat=np.loadtxt("force.00.dat",skiprows=1)
plt.plot(mat[:,0],mat[:,1])
plt.show()
plt.plot(mat[:,0],mat[:,2])
plt.show()
