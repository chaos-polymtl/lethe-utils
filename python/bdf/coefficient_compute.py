from sympy import *
import numpy as np

dt0, dt1, dt2, dt3, dt4, dt5 = symbols('dt0 dt1 dt2 dt3 dt4 dt5')

t=[0,-dt0,-dt0-dt1,-dt0-dt1-dt2,-dt0-dt1-dt2-dt3,-dt0-dt1-dt2-dt3-dt4,-dt0-dt1-dt2-dt3-dt4-dt4-dt5]
alpha=Array([0,0,0,0,0])

def delta(n,j):
    if (j==0):
        arr=MutableDenseNDimArray([0,0,0,0,0,0])
        arr[n]=1
        return arr
    else:
        return ((delta(n,j-1)-delta(n+1,j-1))/(t[n]-t[n+j]))

scheme=Array([0,0,0,0,0,0]);
p=5
for j in range(1,p+1):
    factor=1;
    for i in range(1,j):
        factor = factor * (t[0]-t[i])
    scheme = scheme + factor * delta(0,j)

k=0
for term in scheme:
    print(k," ",simplify(term))
    k = k+1
