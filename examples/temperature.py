#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from scipy import signal
from lase.core import KClient, ZynqSSH
from lase.drivers import Oscillo

host = os.getenv('HOST','192.168.1.12')
password = os.getenv('PWD', 'changeme')

# Connect to the board
client = KClient(host)

# Load the bitstream
ssh = ZynqSSH(host, 'changeme')
ssh.load_pl('bitstreams/oscillo.bit')

driver = Oscillo(client)

current = 30 #mA

freq = 1
mod_amp = 0.2
driver.dac[1,:] = mod_amp * signal.sawtooth(2 * np.pi * freq / driver.n * np.arange(driver.n), width=0.5)
driver.set_dac()

driver.start_laser()
driver.set_averaging(True)
driver.set_laser_current(current)
time.sleep(0.1)

#plt.ylim([-8192, 8191])
plt.ylim([-2*np.pi, 2*np.pi])
plt.ion()
plt.show()

phase_previous1 = 0
phase_previous2 = 0

temp = 20
data = np.zeros((1000,2)) + temp
window = 0.5 * (1-np.cos(2 * np.pi * np.arange(4095) / 4095))

f = open('temperature.csv','a')

for i in range(50000000):
    driver.get_adc()
    
    # plt.ylim([-8192, 8191])
    #plt.ylim([-np.pi, np.pi])
    #plt.ylim([19.5, 20.5])
    adc1 = driver.adc[0,0:4095]
    adc2 = driver.adc[0,4096:8191]

    fft_adc1 = np.fft.fft(adc1 * window)
    fft_adc2 = np.fft.fft(adc2 * window)
        

    phase_adc1 = np.angle(fft_adc1)
    phase_adc2 = np.angle(fft_adc2)
    
    phase1 = phase_adc1[6]
    phase2 = phase_adc2[6]

    plt.clf()

    #plt.plot(driver.adc[0,:])
    #plt.plot(np.abs(fft_adc1[0:20]))
    #plt.plot(np.abs(fft_adc2[0:20]))
    
    diff1 = -(phase1 - phase_previous1 + np.pi)%(2*np.pi)-np.pi
    diff2 = +(phase2 - phase_previous2 + np.pi)%(2*np.pi)-np.pi
  
    diff = diff1 + diff2/2

    data = np.roll(data, -1, axis=0)
    temp = temp + 0.015 * diff / (2*np.pi)
    data[-1] = temp
    f.write(str(time.time())+','+str(temp)+'\n')
    print(temp)
    phase_previous1 = phase1
    phase_previous2 = phase2

    #if i % 100 == 0:
    #    plt.plot(data[:,0])
    #    plt.plot(data[:,1])
    #    plt.draw()


f.close()

driver.stop_laser()
driver.close()
plt.show()
