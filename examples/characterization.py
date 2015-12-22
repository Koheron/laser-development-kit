#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
from lase.core import KClient
import matplotlib.pyplot as plt

# Driver to use
from lase.drivers import Oscillo

# Modules to import
import numpy as np
import matplotlib.pyplot as plt
import time

# Connect to Lase
host = os.getenv('HOST','192.168.1.12')
client = KClient(host)
driver = Oscillo(client)

# Enable laser
driver.start_laser()

# Set laser current
driver.set_laser_current(0)
time.sleep(0.1)

current_max = 50
currents = np.linspace(0,current_max, num=100)

print(currents)
laser_powers = 0 * currents
measured_currents = 0 * currents

for i, current in enumerate(currents):
    driver.set_laser_current(current)
    time.sleep(0.01)
    laser_powers[i] = driver.get_laser_power()
    measured_currents[i] = driver.get_laser_current()
    print('laser power = ' + str(laser_powers[i]) + ' arb. units')

# Plot
fig1 = plt.figure('Power vs current')
plt.plot(currents, laser_powers)
plt.xlabel('Control current (mA)')
plt.ylabel('Laser power (arb. units)')

np.savetxt('power_vs_current.csv', 
           np.transpose([currents, laser_powers]),
           delimiter=',',
           fmt='%1.4e')

#laser_powers = np.convolve(laser_powers, np.ones(500)/500.,'same')
#deriv = np.diff(laser_powers)

# Disable laser
driver.stop_laser()
driver.close()

plt.show()
