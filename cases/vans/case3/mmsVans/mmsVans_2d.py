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
    


eps = (5*cos(pi*t/4))*(exp(-(x+2)*(y+2)))/(pi)
u = (pi/8)*tan(pi*t/4)*(-1/(y+2))
v = (pi/8)*tan(pi*t/4)*(-1/(x+2))

p =  0.5 + 0.5*(cos(pi*t/4))*sin(pi*x)*sin(pi*y)

#print ("dx(u)")
#print (simplify(dx(u)))

#print ("dy(v)")
#print (simplify(dy(v)))

#print ("dx(eps)")
#print (simplify(dx(eps)))

#print ("dy(eps)")
#print (simplify(dy(eps)))

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

#+u*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))) 
#+v*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps)))
print("Total X")
print (simplify((eps*dt(u) - laplacian(u)+dx(p) + conv(eps*u,eps*v,u))/eps))
print("Total Y")
print (simplify((eps*dt(v) - laplacian(v)+dy(p) + conv(eps*u,eps*v,v))/eps))


