#!/usr/bin/python

from sympy import symbols, sin, cos, pi, diff, tanh, exp

x, y = symbols('x y')

# Constants
a = pi                       # Wavenumber
D = 1                        # Diffusivity
nu = 1                       # Kinematic viscosity
k_interface = 9.86960440109  # Reaction coefficient at the interface of the particle
k_bulk = 0                   # Reaction coefficient in the bulk of each phase
t = 0.1                      # Interface thickness
order = 1.3                  # Reaction order

# Signed distance function (SDF) for a circle centered at (0.5, 0.5) with radius 0.1
sdf = ((x - 0.5)**2 + (y - 0.5)**2)**0.5 - 0.1

# Reaction coefficient using SDF
k = k_bulk + (k_interface - k_bulk) * exp(-(sdf * sdf)/(t*t))

def laplacian(f):
    return diff(f, x, x) + diff(f, y, y)

def conv(u, v, f):
    return u * diff(f, x) + v * diff(f, y)

def dx(f):
    return diff(f, x)

def dy(f):
    return diff(f, y)

# Tracer MMS Solution
T = (0.5 + 0.5 * tanh(sdf / 0.5)) * (1 + sin(a*x) * cos(a*y)) / 2

# Velocity field multiplied by SDF to ensure zero at the interface
u = sdf * sin(a*x)**2 * cos(a*y) * sin(a*y)
v = sdf * (-cos(a*x) * sin(a*x) * sin(a*y)**2)

# Pressure field
p = sin(pi*x) + sin(pi*y)

# Terms for the tracer equation
diffusion_term_T = -D * laplacian(T)
advection_term_T = conv(u, v, T)
reaction_term_T  = + k * T**order  

# Source term for the tracer 
source_term_T = diffusion_term_T + advection_term_T + reaction_term_T

# Source terms for velocity and pressure
advection_u = conv(u, v, u)
diffusion_u = -nu * laplacian(u)
grad_p_u    = dx(p)
source_term_u = advection_u + diffusion_u + grad_p_u

advection_v = conv(u, v, v)
diffusion_v = -nu * laplacian(v)
grad_p_v    = dy(p)
source_term_v = advection_v + diffusion_v + grad_p_v

source_term_p = dx(u) + dy(v)


print("\n--- Signed Distance Function (SDF) ---")
print(str(sdf).replace("**", "^"))

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
