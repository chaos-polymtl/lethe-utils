# This program analyses the X and Y drag coefficient (drag and lift) from the cylinder immersed
# boundary test cases
# It can be compared visually afterward to experimental data
# Currently is not generic and can only load 2 data set, but anyway more makes it an unreadable mess
#
# USAGE : python force1 force2
#
# Author : Bruno Blais

#Python imports
#----------------
import os
import sys
import numpy as np
import time
import scipy
import matplotlib.pyplot as plt
import re
#----------------


#********************************
#   OPTIONS AND USER PARAMETERS
#********************************
skip=30
png=True
pdf=False
tminFFT=50.
#Figure size
plt.rcParams['figure.figsize'] = 10, 7

params = {'backend': 'ps',
             'axes.labelsize': 24,
             'font.size': 16,
             'legend.fontsize': 18,
             'xtick.labelsize': 16,
             'ytick.labelsize': 16,
             }

plt.rcParams.update(params)

#======================
#   MAIN
#======================
tFold= 0

#Read the logs files
if (len(sys.argv)<1):
    print ('A force file must be  specified')
    sys.exit("Crashed because force file was not specified")

if (len(sys.argv)>3):
    print ('Too many arguments, only the first two text files can be processed')

file=sys.argv[1]

t1, fx1, fy1, dz1 = np.loadtxt(file, unpack=True,skiprows=1)

fx1=fx1*2
fy1=fy1*2

index = np.where(t1>tminFFT)

# Manual FFT to get amplitude and frequencies right!
Fs = 1. / (t1[2]-t1[1]) # Sampling frequency
df = 1. /  (t1[-1]-tminFFT)
N= len(fy1[index]) # Number of points

# First normalise the amplitude with respect to the number of points
spectrum = abs(np.fft.fft(fy1[index])) / N
f1 = np.arange(0.,Fs/2.-df,df)

print ("Number of point for FFT:", N)
# Keep positive part of the FFT spectrum
Nf = (N)/2
spectrum1 = 2 * spectrum[0:len(f1)]

# Plotting stage
axfft=plt.figure("FFT C_L")
axfftp = axfft.add_subplot(111)
plt.ylabel(' Amplitude ')
plt.xlabel('Strouhal Number ($St$)')
#plt.title('Frequency spectrum of $C_L$  ')
plt.yscale('log')
plt.xscale('log')

plt.plot(f1,spectrum1,linewidth=2.0,color="black")

axfftp.grid(b=True, which='minor', color='grey', linestyle='--')
axfftp.grid(b=True, which='major', color='k', linestyle='--')
if (pdf): plt.savefig("./fftcylinder.pdf")
if (png): plt.savefig("./fftcylinder.png")


ax = plt.figure("Drag coefficient") #Create window
axp=ax.add_subplot(111)
plt.ylabel('$C_D$, $C_L$ ')
plt.xlabel('time [s]')

plt.plot(t1[skip:],fx1[skip:],'-', label='$C_D$',linewidth=2.0,color='grey')
plt.plot(t1[skip:],-fy1[skip:],'-', label='$C_L$',linewidth=2.0,color='black')

plt.legend(loc=3)

print ("Averaged CD:\t", np.average(fx1[index]))
print ("Amplitude CD:\t", (np.max(fx1[index])-np.min(fx1[index]))/2)

print ("Amplitude CL:\t", (np.max(fy1[index])-np.min(fy1[index]))/2)
print ("Average CL:\t", np.average(fy1[index]))
axp.grid(b=True, which='major', color='k', linestyle='--')
plt.axis((0,300,-1,1.5))
if (pdf): plt.savefig("./dragcylinder.pdf")
if (png): plt.savefig("./dragcylinder.png")
plt.show()
