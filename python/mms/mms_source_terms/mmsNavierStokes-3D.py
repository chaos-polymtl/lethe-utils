#!/usr/bin/python

from sympy import *

x, y, z, a, mu = symbols('x y z a mu')

def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)
    d2dz=diff(f,z,z)

    return d2dx+d2dy+d2dz

def conv(u,v,w,f):
    cx = u * diff(f,x)
    cy = v * diff(f,y)
    cz = w * diff(f,z)
   
    return cx+cy+cz


def dx(f):
    return diff(f,x)

def dy(f):
    return diff(f,y)

def dz(f):
    return diff(f,z)

u=sin(a*x)*sin(a*x)*cos(a*y)*sin(a*y)*cos(a*z)*sin(a*z)
v=cos(a*x)*sin(a*x)*sin(a*y)*sin(a*y)*cos(a*z)*sin(a*z)
w=-2*cos(a*x)*sin(a*x)*cos(a*y)*sin(a*y)*sin(a*z)*sin(a*z)

p=x*x+y*y+z*z

print("Verifying divergence free")
print(dx(u)+dy(v)+dz(w))

print("Stokes X Source term:")
print(simplify(-laplacian(u)))

print("Stokes Y Source term:")
print(simplify(-laplacian(v)))

print("Stokes Z Source term:")
print(simplify(-laplacian(w)))

print("Convection X source term:")
print(simplify(conv(u,v,w,u)))

print("Convection Y source term:")
print(simplify(conv(u,v,w,v)))

print("Convection Z source term:")
print(simplify(conv(u,v,w,w)))

print("Pressure X source term:")
print(simplify(dx(p)))

print("Pressure Y source term:")
print(simplify(dy(p)))

print("Pressure Z source term:")
print(simplify(dz(p)))


