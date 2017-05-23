#!/usr/bin/env python
# -*- coding: utf-8 -*-

import init_example
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from koheron import connect
from ldk.drivers import Oscillo
from ldk.drivers import Laser

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='oscillo')
driver = Oscillo(client)
laser = Laser(client)

decimation_factor = 1
index_low = 0
index_high = 8191

# Enable laser
laser.start_laser()

# Set laser current
current = 30  # mA
laser.set_laser_current(current)

# Modulation on DAC
amp_mod = 0.2
freq_mod = 1e6
driver.dac[1, :] = amp_mod*np.sin(2 * np.pi * freq_mod * driver.sampling.t)
driver.set_dac()

# Signal on ADC
signal = driver.get_decimated_data(decimation_factor, index_low, index_high)
signal = signal[:8192]

plt.plot(driver.sampling.t, signal)
plt.show()

psd_signal = np.abs(np.fft.fft(signal)) ** 2

plt.semilogy(1e-6 * np.fft.fftshift(driver.sampling.f_fft), np.fft.fftshift(psd_signal))
plt.xlabel('Frequency (MHz)')
plt.show()

# Disable laser
laser.stop_laser()
