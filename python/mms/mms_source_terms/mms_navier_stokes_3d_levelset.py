#!/usr/bin/python

from sympy import *

x, y, z, a, mu, r, pi = symbols('x y z a mu r pi')

def levelset_sphere(x,y,z,r):
    return (x*x + y*y + z*z)**(1/2) - r
    
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

d = levelset_sphere(x,y,z,r)
u=(sin(a*x)*sin(a*x)*cos(a*y)*sin(a*y)*cos(a*z)*sin(a*z))*d
v=(cos(a*x)*sin(a*x)*sin(a*y)*sin(a*y)*cos(a*z)*sin(a*z))*d
w=(-2*cos(a*x)*sin(a*x)*cos(a*y)*sin(a*y)*sin(a*z)*sin(a*z))*d
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

print("Analytical solution:")
analytical_solution = "("+str(d)+">0)?("+str(simplify(u)) + "):0;" \
                    + "("+str(d)+">0)?("+str(simplify(v)) + "):0;" \
                    + "("+str(d)+">0)?("+str(simplify(w)) + "):0;" \
                    + "("+str(d)+">0)?("+str(simplify(p))  + "):0"
print(analytical_solution.replace("**","^"))

print("Total source term X:")
source_term_x = str(simplify(+laplacian(u) \
     + conv(u,v,w,u) \
     + dx(p) ))
print(source_term_x.replace("**","^"))

print("Total source term Y:")
source_term_y = str(simplify(+laplacian(v) \
     + conv(u,v,w,v) \
     + dy(p) ))
print(source_term_y.replace("**","^"))

print("Total source term Z:")
source_term_z = str(simplify(+laplacian(w) \
     + conv(u,v,w,w) \
     + dz(p) ))
print(source_term_z.replace("**","^"))

print("Mass source term")
source_term_mass = str((dx(u)+dy(v)+dz(w)))
source_term_mass = source_term_mass.replace("**","^")
print(source_term_mass)

print("Total source term")
total_source_term = "("+str(d)+">0)?("+source_term_x+"):0;"+\
      "("+str(d)+">0)?("+source_term_y+"):0;"+\
      "("+str(d)+">0)?("+source_term_z+"):0;"+\
      "("+str(d)+">0)?("+source_term_mass+"):0"
print(total_source_term.replace("**","^"))
