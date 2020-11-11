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

eps = exp(-sin(pi*x)*sin(pi*y))/exp(1)
u = exp(sin(pi*x)*sin(pi*y))/exp(1)
v = exp(sin(pi*x)*sin(pi*y))/exp(1)

p =  0.5 + 0.5*sin(pi*x)*sin(pi*y)

print ("Verifying divergence free")
print (eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps)))


print ("Stokes X Source term:")
print ((simplify(-laplacian(u)+dx(p))/eps))

print ("Stokes Y Source term:")
print ((simplify(-laplacian(v)+dy(p))/eps))

print ("Convection X source term:")
print ((simplify(conv(eps*u,eps*v,u))/eps))

print ("Convection Y source term:")
print ((simplify(conv(eps*u,eps*v,v))/eps))


