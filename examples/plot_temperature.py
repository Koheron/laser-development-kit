#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('temperature.csv', delimiter=',')

n = len(data[:,0])

time = data[:,0]-data[0,0]
T = time[-1]
f_fft = np.arange(n/2 + 1) / T

temperature = data[:,1]

# Compute the power spectral density
window = 0.5 * (1-np.cos(2 * np.pi * np.arange(n) / n))
psd = np.abs(np.fft.rfft(window * data[:,1])**2)

# Fit the psd
c1 = 0.1
c2 = 60
f0 = 0.4
psd_fit = c2/f_fft**2 /(1+f_fft**2/f0**2) + c1/f_fft**0.75

plt.figure(1)
plt.semilogx(f_fft, 10*np.log10(psd))
plt.semilogx(f_fft, 10*np.log10(psd_fit), color='r', linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (dB)')

plt.figure(2)
plt.plot(time, temperature)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')

plt.show()
