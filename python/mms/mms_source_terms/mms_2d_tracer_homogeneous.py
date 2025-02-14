#!/usr/bin/python

from sympy import symbols, sin, cos, pi, diff, simplify

x, y, z = symbols('x y z')

# Constants
a = pi       # Wavenumber
D = 1        # Diffusivity
nu = 1       # Kinematic viscosity 
k = D * a**2 # Reaction coefficient

def laplacian(f):
    return diff(f, x, x) + diff(f, y, y)

def conv(u, v, f):
    return u * diff(f, x) + v * diff(f, y)

def dx(f):
    return diff(f, x)

def dy(f):
    return diff(f, y)

# Manufactured tracer solution: bounded between 0 and 1
T = (1 + sin(a*x) * cos(a*y)) / 2  

# Velocity field
u = sin(a*x)**2 * cos(a*y) * sin(a*y)
v = -cos(a*x) * sin(a*x) * sin(a*y)**2

# Pressure field 
p = sin(pi*x) + sin(pi*y)

# Verify divergence-free condition
print(str(simplify(dx(u) + dy(v))).replace("**", "^"))

# Source terms for the tracer equation
diffusion_term_T = -D * laplacian(T)
advection_term_T = conv(u, v, T)
reaction_term_T  = + k * T**2  

# Source term for the tracer equation
source_term_T = simplify(diffusion_term_T + advection_term_T + reaction_term_T)

# Source terms for velocity equations
advection_u = conv(u, v, u)
diffusion_u = -nu * laplacian(u)
grad_p_u    = dx(p)
source_term_u = simplify(advection_u + diffusion_u + grad_p_u)

advection_v = conv(u, v, v)
diffusion_v = -nu * laplacian(v)
grad_p_v    = dy(p)
source_term_v = simplify(advection_v + diffusion_v + grad_p_v)

source_term_p = simplify(dx(u)+dy(v)) # Should be 0


print("\n--- Manufactured Tracer Solution (T) ---")
print(str(T).replace("**", "^"))

print("\n--- Initial Velocity Field (u, v) ---")
print(f"u(x,y) = {str(u).replace('**', '^')}")
print(f"v(x,y) = {str(v).replace('**', '^')}")

print("\n--- Pressure Field (p) ---")
print(str(p).replace("**", "^"))

print("\n--- Reaction Coefficient (k) ---")
print(str(k).replace("**", "^"))

print("\n--- Source Term for Tracer Equation (f_T) ---")
print(str(source_term_T).replace("**", "^"))

print("\n--- Source Term for Velocity Equation (f_u) ---")
print(str(source_term_u).replace("**", "^"))

print("\n--- Source Term for Velocity Equation (f_v) ---")
print(str(source_term_v).replace("**", "^"))

print("\n--- Source Term for Pressure Equation (f_p) ---")
print(str(source_term_p).replace("**", "^"))
