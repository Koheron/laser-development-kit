#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .base import Base
from ..core import command, write_buffer

from ..core import DevMem

class Spectrum(Base):
    """ Driver for the spectrum bitstream """

    def __init__(self, client, verbose=False):
        self.wfm_size = 4096
        super(Spectrum, self).__init__(self.wfm_size, client)
        
        if self.open() < 0:
            print('Cannot open device SPECTRUM')

        self.dvm = DevMem(self.client)
        self._noise_addr = int('0x86000000',0)
        self._noise = self.dvm.add_memory_map(self._noise_addr, 16384)

        self.spectrum = np.zeros(self.wfm_size, dtype=np.float32)
        self.demod = np.zeros((2, self.wfm_size))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi * np.arange(self.wfm_size) / self.wfm_size))
        self.demod[1, :] = 0

        # self.set_offset(0, 0)

        self.set_demod()

        self.reset()

    @command('SPECTRUM')
    def open(self):
        return self.client.recv_int(4)

    @command('SPECTRUM')
    def set_scale_sch(self, scale_sch):
        pass

    @command('SPECTRUM')
    def set_offset(self, offset_real, offset_imag):
        pass

    @write_buffer('SPECTRUM')
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

    def set_noise(self):
        self.dvm.write_buffer(self._noise, 0, self.spectrum, format_char='f', dtype=np.float32)

    @command('SPECTRUM')
    def get_spectrum(self):
        self.spectrum = self.client.recv_buffer(self.wfm_size,
                                                data_type='float32')
        # self.spectrum[1] = 1

    def get_num_average(self):
        return self.client.recv_int(4)
