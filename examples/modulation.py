#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import matplotlib.pyplot as plt

from koheron import connect
from drivers import Oscillo
from drivers import Laser

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='oscillo')
driver = Oscillo(client)
laser = Laser(client)

decimation_factor = 1
index_low = 0
index_high = 8192

# Enable laser
laser.start()

# Set laser current
current = 30  # mA
laser.set_current(current)

# Modulation on DAC
amp_mod = 0.2
freq_mod = driver.sampling_rate / driver.wfm_size * 10
driver.dac[1, :] = amp_mod*np.sin(2 * np.pi * freq_mod * driver.t)
driver.set_dac()

time.sleep(0.001)

# Signal on ADC
signal = driver.get_decimated_data(decimation_factor, index_low, index_high)
signal = np.reshape(signal, (2, np.size(signal)/2))

plt.plot(driver.t, signal[0,:])
plt.show()

psd_signal = np.abs(np.fft.fft(signal[0,:])) ** 2

freqs = np.fft.fftfreq(driver.wfm_size, d=1/driver.sampling_rate)
plt.semilogy(1e-6 * np.fft.fftshift(freqs), np.fft.fftshift(psd_signal))
plt.xlabel('Frequency (MHz)')
plt.show()

# Disable laser
laser.stop()
