#!/usr/bin/python

from sympy import *

# Cases currently supported by this mms generator are case0, case1 and case2
case="case2"


# Define symbolic variables that are used to generate the MMS
x, y, z, pi, mu, t = symbols('x y z pi mu t')


# Laplacian operator
def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

# Time derivative operator
def dtt(g,u,v):
    dg=diff(g,t)
    f = sqrt((u*u) + (v*v))
    df=diff(f,t)

    return dg + df

# Convection operator
def conv(u,v,f):
    cx = u * diff(f,x) 
    cy = v * diff(f,y) 

    return cx+cy

# Differentiate with respect to x
def dx(f):
    return diff(f,x)

# Differentaite with respect to y
def dy(f):
    return diff(f,y)

# Differentiate with respect ot time
def dt(f):
    return diff(f,t)  
    

# Three MMS cases that are defined for the VANS equations
if (case=="case0"):
    eps = 0.5 
    u = sin(pi*x) * sin(pi*x) * cos(pi*y) * sin(pi*y) 
    v = -cos(pi*x) * sin(pi*x) * sin(pi*y) * sin(pi*y)
    p =   0.5 + 0.5*sin(pi*x)*sin(pi*y)

if (case=="case1"):
    eps =0.5 + 0.25*sin(pi*x)*sin(pi*y)
    u = -2*sin(pi*x) * sin(pi*x) * cos(pi*y) * sin(pi*y)
    v = 2*cos(pi*x) * sin(pi*x) * sin(pi*y) * sin(pi*y)
    p = sin(pi*x)*sin(pi*y)

if (case=="case2"):
    eps =exp(-sin(pi*x)*sin(pi*y))/exp(1)
    u =  exp(sin(pi*x)*sin(pi*y))/exp(1)
    v =  exp(sin(pi*x)*sin(pi*y))/exp(1)
    p = 0.5 + 0.5*sin(pi*x)*sin(pi*y)


# Calculation of every source term for debugging purposes
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


# Total source term. Be careful, to implement in a muparser syntax, the ** need to be replaced by ^^^^
print("Total ")
print (simplify((eps*dt(u)+u*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))) - eps*laplacian(u) - 0*dx(eps)*dx(u)-0*dy(eps)*dy(u)+eps*dx(p) + conv(eps*u,eps*v,u))/eps), " ; ", simplify((eps*dt(v)+v*(dt(eps) + eps*(dx(u)+dy(v)) + u*(dx(eps)) + v*(dy(eps))) - eps*laplacian(v) - 0*dx(eps)*dx(v)-0*dy(eps)*dy(v)+eps*dy(p) + conv(eps*u,eps*v,v))/eps), " ; ", "0" )


