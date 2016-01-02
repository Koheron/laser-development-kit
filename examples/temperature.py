#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv
import time
from lase.core import KClient
from lase.drivers import Oscillo

# Connect to the board
host = os.getenv('HOST','192.168.1.12')
client = KClient(host)
driver = Oscillo(client)

current = 30 #mA

driver.start_laser()
driver.set_averaging(True)
driver.set_laser_current(current)
time.sleep(0.1)

freq = 1
mod_amp = 0.2

driver.dac[1,:] = mod_amp * signal.sawtooth(2 * np.pi * freq / driver.n * np.arange(driver.n), width=0.5)
driver.set_dac()

#plt.ylim([-8192, 8191])
plt.ylim([-2*np.pi, 2*np.pi])
plt.ion()
plt.show()

phase_previous = 0

temp = 20
data = np.zeros(1000)+temp

window = 0.5 * (1-np.cos(2 * np.pi * np.arange(4096) / 4096))

f = open('temperature.csv','a')

for i in range(10000000):
    driver.get_adc()
    
    # plt.ylim([-8192, 8191])
    #plt.ylim([-np.pi, np.pi])
    #plt.ylim([19.5, 20.5])
    adc = driver.adc[0,0:4096]
    fft_adc = np.fft.fft(adc * window)
    phase_adc = np.angle(fft_adc)
    
    phase = phase_adc[6]

    data = np.roll(data, -1)
    diff = (phase - phase_previous + np.pi)%(2*np.pi)-np.pi
    temp = temp - 0.015 * diff / (2*np.pi)
    data[-1] = temp
    f.write(str(time.time())+','+str(temp)+'\n')
    print(temp)
    phase_previous = phase


    if i % 10 == 0:
        plt.clf()
        plt.plot(data)
        plt.draw()
    plt.pause(0.001)

f.close()

driver.stop_laser()
driver.close()
plt.show()
