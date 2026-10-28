#!/usr/bin/python

from sympy import *

# Transient MMS for model A of the VANS equations with a time-dependent void
# fraction. It is the model A counterpart of the transient MMS used by the
# lethe-fluid-vans case3_vans test. Since the continuity equation is not
# satisfied by the manufactured solution, a mass source term m is required.
# The time-dependent part of the void fraction has a zero mean over the
# [-1,1]x[-1,1] domain, so that the integral of the void fraction is constant
# in time. With Dirichlet boundary conditions on the whole boundary, the
# pressure is only defined up to a constant and the discrete global mass
# balance must be consistent: the error of the BDF approximation of the void
# fraction time derivative then integrates to zero over the domain. The
# exp(-sin(pi*x)*sin(pi*y)) void fraction of case3_vans does not satisfy this,
# and the linear solver of the matrix-free solver stagnates.
# As in Lethe, the mass source is added to the continuity equation and its
# momentum (m*u) is added to the momentum equations:
#   ∂t(ε) + ∇·(εu) = m
#   ε∂t(u) + m*u + ε(u·∇)u + ε∇p - εν(∆u + ∇(∇·u)) = εf
# The momentum source term f is multiplied by the void fraction in the solver,
# which is why the momentum source terms are divided by ε below.
# This code assumes a kinematic viscosity of 1.


# Define symbolic variables that are used to generate the MMS
x, y, z, pi, mu, t = symbols('x y z pi mu t')

# Differentiate with respect to x
def dx(f):
    return diff(f,x)

# Differentiate with respect to y
def dy(f):
    return diff(f,y)

# Differentiate with respect to time
def dt(f):
    return diff(f,t)

# Laplacian operator
def laplacian(f):
    d2dx=diff(f,x,x)
    d2dy=diff(f,y,y)

    return d2dx+d2dy

# Divergence operator
def div(u, v):

    return dx(u) + dy(v)

# Gradient of the divergence of a vector operator
def div_grad(u,v,component):
    cx = diff(div(u,v),x)
    cy = diff(div(u,v),y)

    if (component==1):
        return cx
    else:
        return cy

# Convection operator
def conv(u,v,f):
    cx = u * diff(f,x)
    cy = v * diff(f,y)

    return cx+cy

# Continuity operator ∂t(ε) + ∇·(εu)
def continuity(u,v,eps):
    return dt(eps) + eps*div(u,v) + u*dx(eps) + v*dy(eps)

# Convert a sympy expression to the muparser syntax used by Lethe
def to_muparser(f):
    return str(f).replace("**", "^")


# Manufactured solution
T = 2*pi
eps = (1 - 0.1*cos(T*t)*sin(pi*x)*sin(pi*y))/exp(1)
u = cos(T*t)*cos(pi*x)*cos(pi*y)
v = cos(T*t)*cos(pi*x)*cos(pi*y)
p = 0


# Mass source term
mass_source = simplify(continuity(u,v,eps))

# Momentum source terms
sx = simplify((eps*dt(u) + u*mass_source - eps*laplacian(u) - eps*div_grad(u,v,1) + eps*dx(p) + conv(eps*u,eps*v,u))/eps)
sy = simplify((eps*dt(v) + v*mass_source - eps*laplacian(v) - eps*div_grad(u,v,2) + eps*dy(p) + conv(eps*u,eps*v,v))/eps)

# Check that the muparser expressions are equivalent to the sympy expressions
for f in [sx, sy, mass_source]:
    parsed = sympify(to_muparser(f).replace("^", "**"), locals={"pi": pi})
    assert simplify(parsed - f) == 0


print("Void fraction:")
print(to_muparser(eps))

print("Analytical solution:")
print(to_muparser(u), " ; ", to_muparser(v), " ; ", to_muparser(p))

print("Mass source term:")
print(to_muparser(mass_source))

# Total source term, written in the muparser syntax
print("Total:")
print(to_muparser(sx), " ; ", to_muparser(sy), " ; ", to_muparser(mass_source))
