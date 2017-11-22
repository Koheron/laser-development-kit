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

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='spectrum')
driver = Spectrum(client)

fs = 125e6 # Hz
fft_size = 4096
doppler_shift = 1.29e6 # Hz / (m/s)

driver.set_address_range(1,fft_size/2)

n = np.uint32(fs/fft_size)

time = np.arange(n) / fs * fft_size
time = time[::-1]

velocity = np.zeros(n)

fig = plt.figure()
ax = fig.add_subplot(111)

li, = ax.plot(time, velocity)
fig.canvas.draw()
ax.set_xlim((1,0))
ax.set_ylim((0,50))
ax.set_xlabel('Elapsed time (s)')
ax.set_ylabel('Speed (m/s)')

while True:
    try:
        peak_fifo_data = driver.get_peak_fifo_data()
        fifo_length = np.size(peak_fifo_data)
        velocity = np.roll(velocity, -fifo_length)
        velocity[n-fifo_length:n] = peak_fifo_data * (fs / fft_size) / doppler_shift
        li.set_ydata(velocity)
        fig.canvas.draw()
        plt.pause(0.001)
    except KeyboardInterrupt:
        break
