import numpy as np
omega = 1 
L=1
R=1
k = 0.25/1
mu=1
torque = -4.*np.pi*mu*omega*R*R*L*(k*k/(1.-k*k))
#torque= -4*numpy.pi*mu*omega*L*(1./((k*R)**(-2.) - R**(-2.))) 
print(torque)
