from sympy import *
import numpy as np

un, dt, c0, c1, c2 = symbols('un dt c0 c1 c2 ')

a00= 0.4358665215
a11= 0.4358665215
a22= 0.4358665215
a10= 0.2820667392
a20= 1.208496649
a21= -0.644363171

fc0= (c0 - un)/(a00*dt)
fc1 = 1/(a11*dt) * (c1 - un - a10 *dt *fc0)
fc2 = 1/(a22*dt) * (c2 - un - a20 * dt * fc0 - a21 * dt * fc1)
fc0=simplify(fc0)
fc1=simplify(fc1)
fc2=simplify(fc2)
