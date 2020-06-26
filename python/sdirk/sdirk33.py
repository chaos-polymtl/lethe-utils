from sympy import *
import numpy as np

un, dt, c0, c1, c2 = symbols('un dt c0 c1 c2 ')

#Coefficients from Pereira 2019

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
print("Coefficients from Pereira 2019")
print("fc0 : ", fc0)
print("fc1 : ", fc1)
print("fc2 : ", fc2)

#Coefficients from Kennedy and Carpenter 2016
gamma = 0.435866521508458999416019 
b= 1.20849664917601007033648
c=0.717933260754229499708010

a00= gamma
a11= gamma
a22= gamma
a10= c-gamma
a20= b
a21= 1-b-gamma

fc0= (c0 - un)/(a00*dt)
fc1 = 1/(a11*dt) * (c1 - un - a10 *dt *fc0)
fc2 = 1/(a22*dt) * (c2 - un - a20 * dt * fc0 - a21 * dt * fc1)
fc0=simplify(fc0)
fc1=simplify(fc1)
fc2=simplify(fc2)
print("Coefficients from Kennedy and Carpenter 2016")
print("fc0 : ", fc0)
print("fc1 : ", fc1)
print("fc2 : ", fc2)

