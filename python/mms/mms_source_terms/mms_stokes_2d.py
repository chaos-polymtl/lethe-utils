#!/usr/bin/python

from sympy import *

x, y, z, a, mu = symbols('x y z a mu')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

def dx(f):
    return diff(f,x)

def dy(f):
    return diff(f,y)


u=sin(a*x)*sin(a*x)*cos(a*y)*sin(a*y)
v=-cos(a*x)*sin(a*x)*sin(a*y)*sin(a*y)

p=0#x**2.*y**2.

print ("Verifying divergence free")
print (dx(u)+dy(v))

print ("Stokes X Source term:")
print (-laplacian(u)+dx(p))

print ("Stokes Y Source term:")
print (-laplacian(v)+dy(p))




