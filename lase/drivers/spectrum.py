#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .base import Base
from ..core import Device, command, write_buffer


class Spectrum(Device):
    """ Driver for the spectrum bitstream """

    def __init__(self, client, map_size=4096, verbose=False):
        super(Spectrum, self).__init__(client)

        n = 4096
        self.base = Base(n, client, map_size)
        self.open(n)

        # TODO Check memory map ID is not NaN

        self.spectrum = np.zeros(self.base.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2, self.base.sampling.n))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi *
                                              np.arange(self.base.sampling.n) /
                                              self.base.sampling.n))
        # 0.5*np.real(demod)
        self.demod[1, :] = 0  # 0.5*np.imag(demod)

        # self.set_offset(-199, -21)
        # self.set_offset(0, 0)

        self.set_demod()
        # self.dvm.write(self._config, self._scale_sch_off, 427)

        self.base.reset()

    @command
    def open(self, samples_num):
        pass

    @command
    def set_scale_sch(self, scale_sch):
        pass

    @command
    def set_offset(self, offset_real, offset_imag):
        pass

    @write_buffer
    def set_demod_buffer(self, data):
        pass

    def set_demod(self, warning=False):
        if warning:
            if np.max(np.abs(self.demod)) >= 1:
                print('WARNING : dac out of bounds')
        demod_data_1 = np.mod(np.floor(8192 * self.demod[0, :]) +
                              8192, 16384) + 8192
        demod_data_2 = np.mod(np.floor(8192 * self.demod[1, :]) +
                              8192, 16384) + 8192
        self.set_demod_buffer(demod_data_1 + 65536 * demod_data_2)

    @command
    def get_spectrum(self):
        self.spectrum = self.client.recv_buffer(self.base.sampling.n,
                                                data_type='float32')
        # self.spectrum[1] = 1

    @command
    def get_num_average(self):
        return self.client.recv_int(4)
