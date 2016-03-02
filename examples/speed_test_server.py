#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
from lase.core import KClient
from lase.drivers import Oscillo

import numpy as np
import matplotlib.pyplot as plt
import time

def speed_test(host, n_pts=3, size=8192):
    time_total = np.zeros(n_pts)
    time_server = np.zeros(n_pts)
    client = KClient(host)
    driver = Oscillo(client)
    t0 = time.time()
    t_prev = t0    

    for i in range(n_pts):
        for j in range(1):
            time_server[i] = driver.speed_test(1,10,size=size)
        t = time.time()
        time_total[i] = t - t_prev
        t_prev = t

    driver.close()
    client.__del__()
    return [1e-3 *np.median(time_server), np.median(time_total)*1e6]

host = '192.168.1.2'

sizes = 10 * np.arange(100)
a = np.zeros((len(sizes),2))

for i, size in enumerate(sizes):
    a[i,:] = speed_test(host, size=size)

plt.plot(sizes, a[:,0])
plt.plot(sizes, a[:,1])

plt.show()
