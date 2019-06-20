from sympy import *
import numpy as np

p=3
dt=np.array([0.1, 0.2, 0.3, 0.4,0.5])
t=np.zeros(p+1)
for i in range(0,np.size(t)):
    for j in range(0,i):
        t[i]-= dt[j]

print(t)
alpha=np.zeros(p+1)

def delta(po,n,j):
    if (j==0):
        arr=np.zeros(po+1)
        arr[n]=1
        return arr
    else:
        return ((delta(po,n,j-1)-delta(po,n+1,j-1))/(t[n]-t[n+j]))

scheme=np.zeros(p+1)
for j in range(1,p+1):
    factor=1;
    for i in range(1,j):
        factor = factor * (t[0]-t[i])
    scheme = scheme + factor * delta(p,0,j)

k=0
for term in scheme:
    print(k," ",simplify(term))
    k = k+1
