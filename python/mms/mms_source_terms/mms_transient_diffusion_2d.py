#!/usr/bin/python

from sympy import *

x, y, z, t, a = symbols('x y z t a')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

def dt(f):
    return  diff(f,t)

T=sin(a*x)*sin(a*y)*sin(t)



print ("Source term :")
print (simplify(laplacian(T)-dt(T)))
