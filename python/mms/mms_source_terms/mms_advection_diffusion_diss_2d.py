#!/usr/bin/python

from sympy import *

x, y, z, a, mu = symbols('x y z a mu')

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


u=y*y#sin(a*x)*sin(a*x)*cos(a*y)*sin(a*y)
v=x*x#-cos(a*x)*sin(a*x)*sin(a*y)*sin(a*y)
#u=sin(a*y)
#v=sin(a*x)

T=x*(x-1)*y*(y-1)

print ("Verifying divergence free")
print (dx(u)+dy(v))

print ("Source term diffusion:")
print (simplify(-laplacian(T)))

print ("Source term convection:")
print(conv(u,v,T))

print ("Final source term")
print (simplify(-laplacian(T)+conv(u,v,T)))
#
#print ("Stokes Y Source term:")
#print (-laplacian(v)+dy(p))
#
#print ("Convection X source term:")
#print (simplify(conv(u,v,u)))
#
#print ("Convection Y source term:")
#print (simplify(conv(u,v,v)))
