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
    host = os.getenv('HOST','192.168.1.100')
    client = load_instrument(host, instrument='oscillo')
    driver = Oscillo(client)

    t0 = time.time()
    t_prev = t0

    for i in range(n_pts):
        for j in range(1):
            #a = driver.get_laser_current()
            b = driver.get_adc()
            for k in range(10):
               pass
               #a = driver.get_laser_current()
               #c = driver.get_laser_power()
        t = time.time()
        time_array[i] = t - t_prev
        #print host, i, time_array[i]
        t_prev = t
        
    print np.median(time_array)

    plt.plot(time_array)
    driver.close()

hosts = ['192.168.1.{0}'.format(i) for i in [2]]

for host in hosts:
    speed_test(host)

plt.show()
