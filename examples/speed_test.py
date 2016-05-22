#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from utilities import load_instrument
from ldk.drivers import Oscillo

def speed_test(host, n_pts=1000):
    time_array = np.zeros(n_pts)
    client = load_instrument(host, instrument='oscillo')
    driver = Oscillo(client)
    driver.set_averaging(True)

    t0 = time.time()
    t_prev = t0

    for i in range(n_pts):
        driver.get_adc()
        t = time.time()
        time_array[i] = t - t_prev
        print host, i, time_array[i]
        t_prev = t
        
    print np.median(time_array)

    plt.plot(time_array)
    driver.close()

hosts = ['192.168.1.{0}'.format(i) for i in [12]]

for host in hosts:
    speed_test(host,n_pts=10000)

plt.ylabel('Time (s)')
plt.show()
