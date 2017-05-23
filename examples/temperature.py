#!/usr/bin/env python
# -*- coding: utf-8 -*-

import init_example
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from scipy import signal

from koheron import connect
from ldk.drivers import Oscillo

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='oscillo')
driver = Oscillo(client)

current = 30 #mA

freq = 1
mod_amp = 0.2
# Modulate with a triangle waveform of period 8192 x 8 ns
n = driver.wfm_size
driver.dac[1,:] = mod_amp * signal.sawtooth(2 * np.pi * freq / n * np.arange(n), width=0.5)
driver.set_dac()

decimation_factor = 1
index_low = 0
index_high = 8191

driver.start_laser()
driver.set_averaging(True)
driver.set_laser_current(current)
time.sleep(0.1)

plt.ylim([-2*np.pi, 2*np.pi])
plt.ion()
plt.show()

phase_previous_pos = 0
phase_previous_neg = 0

temperature = 20 # degrees Celsius
data = np.zeros((1000,2)) + temperature
# Hanning FFT Window
window = 0.5 * (1-np.cos(2 * np.pi * np.arange(4095) / 4095))

with open('temperature.csv','w') as f:
    for i in range(5):

        adc = driver.get_decimated_data(decimation_factor, index_low, index_high)

        # Separate positive and negative slopes in the triangle waveform
        adc_pos = adc[:4095]
        adc_neg = adc[-4095:]

        fft_pos = np.fft.fft(adc_pos * window)
        fft_neg = np.fft.fft(adc_neg * window)

        phase_adc_pos = np.angle(fft_pos)
        phase_adc_neg = np.angle(fft_neg)

        # The phase of the frequency modulation
        phase_pos = phase_adc_pos[6]
        phase_neg = phase_adc_pos[6]

        plt.clf()

        diff_pos = -(phase_pos - phase_previous_neg + np.pi)%(2*np.pi)-np.pi
        diff_neg = +(phase_neg - phase_previous_neg + np.pi)%(2*np.pi)-np.pi

        diff = diff_pos + diff_neg/2

        data = np.roll(data, -1, axis=0)
        temperature = temperature + 0.015 * diff / (2*np.pi)
        data[-1] = temperature
        string = str(time.time())+','+str(temperature)+'\n'
        f.write(string)
        print(string)
        phase_previous_pos = phase_pos
        phase_previous_neg = phase_neg

f.close()

driver.stop_laser()
plt.show()

# Plot temperature

temperature_data = np.genfromtxt('temperature.csv', delimiter=',')

n_pts = len(temperature_data[:,0])

time = temperature_data[:,0]-temperature_data[0,0]
T = time[-1]
f_fft = np.arange(n_pts/2 + 1) / T

temperature = temperature_data[:,1]

# Compute the power spectral density
window = 0.5 * (1-np.cos(2 * np.pi * np.arange(n_pts) / n_pts))
psd = np.abs(np.fft.rfft(window * temperature)**2)

# Fit the psd
c1 = 0.1
c2 = 50
f0 = 0.4
psd_fit = c2/f_fft**2.2 /(1+f_fft**2/f0**2) + c1/f_fft**0.75

plt.figure(1)
plt.semilogx(f_fft, 10*np.log10(psd))
plt.semilogx(f_fft, 10*np.log10(psd_fit), color='r', linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (dB)')

plt.figure(2)
plt.plot(time, temperature)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')

plt.show(block=True)
