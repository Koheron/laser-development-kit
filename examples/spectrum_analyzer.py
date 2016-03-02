#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
from lase.core import KClient, HTTPInterface
from lase.drivers import Spectrum

# Modules to import
import numpy as np
import matplotlib.pyplot as plt
import time

# Load the spectrum instrument
host = os.getenv('HOST','192.168.1.100')
http = HTTPInterface(host)
http.install_instrument('spectrum')

client = KClient(host)
driver = Spectrum(client)

# Enable laser
driver.start_laser()

# Set laser current
current = 30  # mA
driver.set_laser_current(current)

# Signal on ADC
driver.get_spectrum()

# Plot
plt.plot(np.fft.fftshift(driver.sampling.f_fft), np.log10(driver.spectrum))
plt.show()

# Disable laser
driver.stop_laser()
driver.close()
