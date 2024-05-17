#!/usr/bin/python

from sympy import *


x, y, z, pi, mu, t = symbols('x y z pi mu t')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

def dtt(g,u,v):
    dg=diff(g,t)
    f = sqrt((u*u) + (v*v))
    df=diff(f,t)

    return dg + df

def conv(u,v,f):
    cx = u * diff(f,x) 
    cy = v * diff(f,y) 

    return cx+cy

def dx(f):
    return diff(f,x)

def dy(f):
    return diff(f,y)

def dt(f):
    return diff(f,t)  
    

T = 2*pi
eps = (1 - 0.1*cos(T*t))*exp(-sin(pi*x)*sin(pi*y))/exp(1)
u = cos(T*t)*exp(sin(pi*x)*sin(pi*y))/exp(1)
v = cos(T*t)*exp(sin(pi*x)*sin(pi*y))/exp(1)

p =  0.5 + 0.5*cos(T*t)*sin(pi*x)*sin(pi*y)

print ("Mass Source Term")
print (simplify(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))))

print ("Unsteady X Source term:")
print (simplify(eps*dt(u)))

print ("Unsteady Y Source term:")
print (simplify(eps*dt(v)))

print ("Stokes X Source term:")
print (simplify((-laplacian(u)+dx(p))/eps))

print ("Stokes Y Source term:")
print (simplify((-laplacian(v)+dy(p))/eps))

print ("Convection X source term:")
print (simplify((conv(eps*u,eps*v,u))/eps))

print ("Convection Y source term:")
print (simplify((conv(eps*u,eps*v,v))/eps))

print("Total X")
print (simplify((eps*dt(u)+u*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))) - laplacian(u)+dx(p) + conv(eps*u,eps*v,u))/eps))
print("Total Y")
print (simplify((eps*dt(v)+v*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))) - laplacian(v)+dy(p) + conv(eps*u,eps*v,v))/eps))


