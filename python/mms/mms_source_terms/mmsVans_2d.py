#!/usr/bin/python

from sympy import *

x, y, z, pi, mu = symbols('x y z pi mu')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy


def conv(u,v,f):
    cx = u * diff(f,x) 
    cy = v * diff(f,y) 

    return cx+cy

def dx(f):
    return diff(f,x)

def dy(f):
    return diff(f,y)

eps = 0.5 
u=sin(pi*x)*sin(pi*x)*sin(pi*y)*cos(pi*y)
v=-sin(pi*x)*cos(pi*x)*sin(pi*y)*sin(pi*y)
p=sin(pi*x)*sin(pi*y)

print ("Verifying divergence free")
print (dx(u)+dy(v))

print ("Stokes X Source term:")
print (simplify(-laplacian(u)+dx(p)))

print ("Stokes Y Source term:")
print (simplify(-laplacian(v)+dy(p)))

print ("Convection X source term:")
print (simplify(conv(eps*u,v,u)))

print ("Convection Y source term:")
print (simplify(conv(eps*u,v,v)))


