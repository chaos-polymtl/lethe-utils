#!/usr/bin/python

from sympy import *

# Cases currently supported by this mms generator are case1 
case="case1"


# Define symbolic variables that are used to generate the MMS
x, y, z, pi, mu, t = symbols('x y z pi mu t')


# Laplacian operator
def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)
    d2dz=diff(f,z,z)


    return d2dx+d2dy+d2dz

# Time derivative operator
def dtt(g,u,v):
    dg=diff(g,t)
    f = sqrt((u*u) + (v*v))
    df=diff(f,t)

    return dg + df

# Convection operator
def conv(u,v,w,f):
    cx = u * diff(f,x) 
    cy = v * diff(f,y) 
    cz = w * diff(f,z)

    return cx+cy+cz

def continuity(u,v,w,eps):
   return  dt(eps) + eps*(dx(u)+dy(v)+dz(w)) + u*(dx(eps)) + v*(dy(eps))+w*(dz(eps))

# Differentiate with respect to x
def dx(f):
    return diff(f,x)

# Differentiate with respect to y
def dy(f):
    return diff(f,y)

# Differentaite with respect to z
def dz(f):
    return diff(f,z)


# Differentiate with respect ot time
def dt(f):
    return diff(f,t)  

    

# MMS cases that are defined for the VANS equations
if (case=="case1"):
    eps =0.5 + 0.25*sin(pi*x)*sin(pi*y)*sin(pi*z)
    u = -2*sin(pi*x) * sin(pi*x) * cos(pi*y) * sin(pi*y)*sin(pi*z)
    v = 2*cos(pi*x) * sin(pi*x) * sin(pi*y) * sin(pi*y)*sin(pi*z)
    w = 0

    p = sin(pi*x)*sin(pi*y)*sin(pi*z)


# Calculation of every source term for debugging purposes
print ("Mass Source Term")
cont = simplify(continuity(u,v,w,eps))
print(cont)


print("X source term")
sx=simplify((eps*dt(u)+u*(continuity(u,v,w,eps)) - eps*laplacian(u) +eps*dx(p) + conv(eps*u,eps*v,eps*w,u))/eps)
print(sx)


print("Y source term")
sy=simplify((eps*dt(v)+v*(continuity(u,v,w,eps)) - eps*laplacian(v) +eps*dy(p) + conv(eps*u,eps*v,eps*w,v))/eps)
print (sy)

print("Z source term")
sz=simplify((eps*dt(w)+w*(continuity(u,v,w,eps)) - eps*laplacian(w) +eps*dz(p) + conv(eps*u,eps*v,eps*w,w))/eps)
print (sz)

# Total source term. Be careful, to implement in a muparser syntax, the ** need to be replaced by ^^^^
print("Total ")
print (sx, " ; ",sy, " ; ", sz , " ; ", "0" )


