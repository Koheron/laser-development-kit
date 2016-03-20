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

        self.avg_on = True

        self.spectrum = np.zeros(self.wfm_size, dtype=np.float32)
        self.demod = np.zeros((2, self.wfm_size))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi * np.arange(self.wfm_size) / self.wfm_size))
        self.demod[1, :] = 0

        self.noise_floor = np.zeros(self.wfm_size)

        # self.set_offset(0, 0)
 
        self.set_address_range(10, 50)

        self.set_demod()
        self.set_scale_sch(0)

        self.reset()

    @command('SPECTRUM')
    def open(self):
        return self.client.recv_int(4)

    def reset(self):
        super(Spectrum, self).reset()
        self.avg_on = True
        self.set_averaging(self.avg_on)

    @command('SPECTRUM')
    def set_scale_sch(self, scale_sch):
        pass

    @command('SPECTRUM')
    def set_offset(self, offset_real, offset_imag):
        pass

    @write_buffer('SPECTRUM')
    def set_demod_buffer(self, data):
        pass

    @write_buffer('SPECTRUM', format_char='f', dtype=np.float32)
    def set_noise_floor_buffer(self, data):
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
        
    def calibrate(self, noise_floor):
        self.noise_floor = noise_floor
        self.set_noise_floor_buffer(self.noise_floor)

    @command('SPECTRUM')
    def get_spectrum(self):
        self.spectrum = self.client.recv_buffer(self.wfm_size,
                                                data_type='float32')
        # self.spectrum[1] = 1
        #print self.get_peak_address()*self.sampling.df, self.get_peak_maximum()
        fifo_length = self.get_peak_fifo_occupancy()
        print fifo_length
        print self.get_peak_fifo_data(fifo_length)

    @command('SPECTRUM')
    def get_num_average(self):
        return self.client.recv_int(4)

    @command('SPECTRUM')
    def get_peak_address(self):
        return self.client.recv_int(4)

    @command('SPECTRUM')
    def get_peak_maximum(self):
        return self.client.recv_int(4, fmt='f')

    @command('SPECTRUM')
    def set_address_range(self, address_low, address_high):
        pass

    def set_averaging(self, avg_status):
        if avg_status:
            status = 1;
        else:
            status = 0;

        @command('SPECTRUM')
        def set_averaging(self, status):
            pass

        set_averaging(self, status)

    @command('SPECTRUM')
    def get_peak_fifo_occupancy(self):
        return self.client.recv_int(4)

    @command('SPECTRUM')
    def get_peak_fifo_length(self):
        return self.client.recv_int(4)

    @command('SPECTRUM')
    def get_peak_fifo_data(self, n_pts):
        return self.client.recv_buffer(n_pts, data_type='uint32')
