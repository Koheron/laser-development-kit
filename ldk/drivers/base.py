#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

from ..signal import Sampling
from koheron_tcp_client import command, write_buffer

class Base(object):
    """ This class is used as a base class for `Oscillo` and `Spectrum`

    args:
        wfm_size: number of points in the waveform.
        client : instance of KClient class, used to connect to the board.
    """

    def __init__(self, wfm_size, client):
        self.client = client
        self.open_dac(wfm_size)
        self.open_laser()

        self.n = wfm_size
        self.max_current = 40  # mA
        self.sampling = Sampling(wfm_size, 125e6)

        self.opened = True
        self.dac = np.zeros((2, self.sampling.n))

        self.failed = False

    def open_dac(self, wfm_size):
        @command('DAC', 'u')
        def open(self, wfm_size):
            return self.client.recv_int32()

        open(self, wfm_size)

    def open_laser(self):
        @command('LASER')
        def open(self):
            return self.client.recv_int32()

        open(self)

    def update(self):
        pass  # Used in BaseSimu

    def close(self):
        self.stop_laser()
        self.reset()

    def reset(self):
        self.reset_laser()
        self.reset_dac()

    def reset_laser(self):
        @command('LASER')
        def reset(self): pass

        reset(self)

    def reset_dac(self):
        @command('DAC')
        def reset(self): pass

        reset(self)

    @command('LASER')
    def start_laser(self): pass

    @command('LASER')
    def stop_laser(self): pass

    @command('LASER')
    def get_laser_current(self):
            return (0.0001/21.) * self.client.recv_uint32()

    @command('LASER')
    def get_laser_power(self):
            return self.client.recv_int(4)

    @command('LASER')
    def get_monitoring(self):
        return self.client.recv_tuple()

    @command('LASER', 'f')
    def set_laser_current(self, current):
        """ current: The bias in mA """
        pass

    @write_buffer('DAC')
    def set_dac_buffer(self, data): pass

    def twoint14_to_uint32(self, data):
        data1 = np.mod(np.floor(8192 * data[0, :]) + 8192,16384) + 8192
        data2 = np.mod(np.floor(8192 * data[1, :]) + 8192,16384) + 8192
        return data1 + 65536 * data2

    def set_dac(self, warning=False, reset=False):
        if warning:
            if np.max(np.abs(self.dac)) >= 1:
                print('WARNING : dac out of bounds')
        self.set_dac_buffer(self.twoint14_to_uint32(self.dac))

        if reset:
            self.reset_acquisition()

    @command('COMMON')
    def get_bitstream_id(self): pass

    @command('COMMON', 'u')
    def set_led(self, value): pass

    @command('COMMON')
    def init(self): pass

    @command('DAC')
    def reset_acquisition(self): pass
