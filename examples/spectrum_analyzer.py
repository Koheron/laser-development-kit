#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt

from koheron import connect
from drivers import Spectrum
from drivers import Laser

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='spectrum')
driver = Spectrum(client)
laser = Laser(client)

laser.start()

current = 30 # mA
laser.set_current(current)

# driver.reset_acquisition()

wfm_size = 4096
decimation_factor = 1
index_low = 0
index_high = wfm_size / 2

signal = driver.get_decimated_data(decimation_factor, index_low, index_high)
print('Signal')
print(signal)

mhz = 1e6
sampling_rate = 125e6
freq_min = 0
freq_max = sampling_rate / mhz / 2

# Plot parameters
fig = plt.figure()
ax = fig.add_subplot(111)

x = np.linspace(freq_min, freq_max, (wfm_size / 2))
print('X')
print(len(x))

y = 10*np.log10(signal)

print('Y')
print(len(y))

li, = ax.plot(x, y)
fig.canvas.draw()
ax.set_xlim((x[0],x[-1]))
ax.set_ylim((0,200))
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Power spectral density (dB)')

while True:
    try:
        signal = driver.get_decimated_data(decimation_factor, index_low, index_high)
        li.set_ydata(10*np.log10(signal))
        fig.canvas.draw()
        plt.pause(0.001)
    except KeyboardInterrupt:
        # Save last spectrum in a csv file
        np.savetxt("psd.csv", signal, delimiter=",")
        laser.stop()
        driver.close()
        break
