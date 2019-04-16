#!/usr/bin/python

from sympy import *

h,u = symbols('h u')


def du(f):
    return diff(f,u)


tau=h / (2*u)
print (du(tau))



