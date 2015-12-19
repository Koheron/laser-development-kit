#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
from lase.core import KClient

# Driver to use
from lase.drivers import Oscillo

# Modules to import
import numpy as np
import matplotlib.pyplot as plt
import time

# Connect to Lase
host = os.getenv('HOST','192.168.1.100')
client = KClient(host)
driver = Oscillo(client)  # Replace with appropriate driver

# Enable laser
driver.base.start_laser()

# Set laser current
current = 30  # mA
driver.base.set_laser_current(current)

# Modulation on DAC
amp_mod = 0.2
freq_mod = 1e6
driver.base.dac[1, :] = amp_mod*np.sin(2 * np.pi * freq_mod * driver.base.sampling.t)
driver.base.set_dac()

# Signal on ADC
driver.get_adc()
signal = driver.adc[0, :]

# Plot
plt.plot(driver.base.sampling.t, signal)
plt.show()

# Plot
psd_signal = np.abs(np.fft.fft(signal)) ** 2

plt.semilogy(1e-6 * np.fft.fftshift(driver.base.sampling.f_fft), np.fft.fftshift(psd_signal))
plt.xlabel('Frequency (MHz)')
plt.show()

# Disable laser
driver.base.stop_laser()
driver.base.close()
