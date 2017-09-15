#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import matplotlib.pyplot as plt

from koheron import connect
from drivers import Oscillo

host = os.getenv('HOST','192.168.1.100')
cmd = os.getenv('CMD','get_decimated_data')

decimation_factor = 1
index_low = 0
index_high = 8191

def speed_test(host, n_pts=1000):
    time_array = np.zeros(n_pts)
    client = connect(host, name='oscillo')
    driver = Oscillo(client)
    driver.set_average(False)

    t0 = time.time()
    t_prev = t0

    for i in range(n_pts):
        if cmd == 'get_decimated_data':
        	driver.get_decimated_data(decimation_factor, index_low, index_high)
        elif cmd == 'get_num_average':
            driver.get_num_average(0)
        t = time.time()
        time_array[i] = t - t_prev
        print host, i, time_array[i]
        t_prev = t

    print '{} us'.format(1E6 * np.median(time_array))
#    assert(np.median(time_array) < 0.003)
    return time_array

plt.plot(1E6 * speed_test(host))
plt.xlabel('Trial #')
plt.ylabel('Time (us)')
plt.show()
