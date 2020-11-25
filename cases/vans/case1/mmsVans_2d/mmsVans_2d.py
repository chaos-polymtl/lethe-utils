#!/usr/bin/python

from sympy import *


x, y, z, pi, mu, t = symbols('x y z pi mu t')

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

eps = 0.5 + 0.25*sin(pi*x)*sin(pi*y)
u = -2*sin(pi*x) * sin(pi*x) * cos(pi*y) * sin(pi*y) 
v = 2*cos(pi*x) * sin(pi*x) * sin(pi*y) * sin(pi*y)

p = sin(pi*x)*sin(pi*y)

print ("Verifying divergence free")
print (simplify(eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))))


print ("Stokes X Source term:")
print ((simplify(-laplacian(u)+dx(p))/eps))

print ("Stokes Y Source term:")
print ((simplify(-laplacian(v)+dy(p))/eps))

print ("Convection X source term:")
print ((simplify(conv(eps*u,eps*v,u))/eps))

print ("Convection Y source term:")
print ((simplify(conv(eps*u,eps*v,v))/eps))

print("Total X")
print (simplify((-laplacian(u)+dx(p) + conv(eps*u,eps*v,u))/eps))
print("Total Y")
print (simplify((-laplacian(v)+dy(p) + conv(eps*u,eps*v,v))/eps))

