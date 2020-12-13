#!/usr/bin/python

from sympy import *

x, y, z, a, mu = symbols('x y z a mu')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

T=sin(a*x)*sin(a*y)


print ("Source term diffusion:")
print (simplify(laplacian(T)))

#print ("Stokes Y Source term:")
#print (-laplacian(v)+dy(p))
#
#print ("Convection X source term:")
#print (simplify(conv(u,v,u)))
#
#print ("Convection Y source term:")
#print (simplify(conv(u,v,v)))
