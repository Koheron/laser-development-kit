#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
from lase.core import KClient
from lase.drivers import Oscillo

import numpy as np
import matplotlib.pyplot as plt
import time

def speed_test(host, n_pts=200):
    time_array = np.zeros(n_pts)
    client = KClient(host)
    driver = Oscillo(client)
    t0 = time.time()
    t_prev = t0    

    for i in range(n_pts):
        for j in range(10):
            a = driver.get_laser_current()
            b = driver.get_adc()
            c = driver.get_laser_power()
        t = time.time()
        time_array[i] = t - t_prev
        print host, i, time_array[i]
        t_prev = t

    plt.plot(time_array)
    driver.close()

hosts = ['192.168.1.{0}'.format(i) for i in [15,8,7,2]]

for host in hosts:
    speed_test(host)

plt.show()
