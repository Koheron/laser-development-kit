#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('temperature.csv', delimiter=',')


n = 10000000

#plt.plot(data[:,0], data[:,1])

T = data[-1,0] - data[0,0]
print(T/n)

f_fft = np.arange(n/2 + 1) / T

window = 0.5 * (1-np.cos(2 * np.pi * np.arange(n) / n))
fft = 10*np.log10(np.abs(np.fft.rfft(window * data[:,1])**2))
plt.semilogx(f_fft, fft)

plt.show()
