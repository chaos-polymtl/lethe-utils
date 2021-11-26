#-------------------------------------
# MMS source term for a non newtonian solver
#------------------------------------
import math
from sympy import *
import numpy as np

dim = 2

x, y, z, pi = symbols("x, y, z, pi")

u = sin(pi*x) * sin(pi*x) * cos(pi*y) * sin(pi*y)
v = -cos(pi*x) * sin(pi*x) * sin(pi*y) * sin(pi*y)
w = 0
p = sin(pi*x)+sin(pi*y)

def dx(f):
    return diff(f,x)

def dy(f):
    return diff(f,y)

def dz(f):
    return diff(f,z)

if (dim == 2):
	velocity_gradient = np.array([[dx(u), dx(v)], [dy(u), dy(v)]])
else:
	velocity_gradient = np.array([[dx(u), dx(v), dx(w)], [dy(u), dy(v), dy(w)], [dz(u), dz(v), dz(w)]])

# Shear rate
shear_rate = velocity_gradient + velocity_gradient.transpose()
shear_rate_mag = (0.5 * np.sum(np.multiply(shear_rate, shear_rate)))**0.5

print('shear_rate_mag : ')
print(shear_rate_mag)


# Rheological model parameters (here, Carreau parameters, but they can be changed)
eta_0 = 1.0
eta_inf = 1.0
lambd = 1.0
a = 2
n = 0.5

eta = eta_inf + (eta_0 - eta_inf) * (1 + (lambd * shear_rate_mag)**a) ** ((n - 1)/a)
print('eta : ')
print(eta)

# Stress tensor
tau_xx = - 2 * eta * dx(u)
tau_yx = - eta * (dy(u) + dx(v))
tau_xy = - eta * (dy(u) + dx(v))
tau_yy = - 2 * eta * dy(v)
tau_xz = - eta * (dz(u) + dx(w))
tau_zx = - eta * (dz(u) + dx(w))
tau_yz = - eta * (dz(v) + dy(w))
tau_zy = - eta * (dz(v) + dy(w))
tau_zz = - 2 * eta * dz(w)

# Source term
f_x = u*dx(u) + v*dy(u) + w*dz(u) + dx(tau_xx) + dy(tau_yx) + dz(tau_zx) + dx(p)
f_y = u*dx(v) + v*dy(v) + w*dz(v) + dx(tau_xy) + dy(tau_yy) + dz(tau_zy) + dy(p)
f_z = u*dx(w) + v*dy(w) + w*dz(w) + dx(tau_xz) + dy(tau_yz) + dz(tau_zz) + dz(p)

print('f : ')
f_x_prm = str(f_x).replace("**", "^")
f_y_prm = str(f_y).replace("**", "^")
f_z_prm = str(f_z).replace("**", "^")

print(f_x_prm + "; " + f_y_prm + "; " + f_z_prm)

