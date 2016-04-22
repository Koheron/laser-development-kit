#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .base import Base
from koheron_tcp_client import command, write_buffer

# Lorentzian fit
from scipy.optimize import leastsq

def lorentzian(f, p):
    return p[0]/(1+f**2/p[1])

def residuals(p, y, f):
    return y - lorentzian(f, p)


class Spectrum(Base):
    """ Driver for the spectrum bitstream """

    def __init__(self, client, verbose=False):
        self.wfm_size = 4096
        super(Spectrum, self).__init__(self.wfm_size, client)
        
        if self.open() < 0:
            print('Cannot open device SPECTRUM')

        self.fifo_start_acquisition(1000)

        self.avg_on = True

        self.spectrum = np.zeros(self.wfm_size, dtype=np.float32)
        self.demod = np.zeros((2, self.wfm_size))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi * np.arange(self.wfm_size) / self.wfm_size))
        self.demod[1, :] = 0

        self.noise_floor = np.zeros(self.wfm_size)

        # self.set_offset(0, 0)
 
        self.set_address_range(0, 0)

        self.set_demod()
        self.set_scale_sch(0)

        self.reset()

        # Laser linewidth estimation
        self.fit_linewidth = False
        self.fit = np.zeros((2,100))
        self.i = 0

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
        #print self.get_peak_values()

        if self.fit_linewidth:
            idx = np.arange(2,200)
            f = self.sampling.f_fft[idx]
            y = self.spectrum[idx]
            params_init = [2e17, 3e6**2]
            best_params = leastsq(residuals, params_init, args=(y,f), full_output=1)
            self.fit[:, self.i % 100] = best_params[0]
            self.i += 1
            print("Linewidth = {0:2f} kHz".format(1e-3 * np.sqrt(np.mean(self.fit[1,:]))))

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

    # === Peak data stream

    def get_peak_values(self):
        @command('SPECTRUM')
        def store_peak_fifo_data(self):
            return self.client.recv_int(4)

        self.peak_stream_length = store_peak_fifo_data(self)

        @command('SPECTRUM')
        def get_peak_fifo_data(self):
            return self.client.recv_buffer(self.peak_stream_length, data_type='uint32')

        return get_peak_fifo_data(self)

    @command('SPECTRUM')
    def get_peak_fifo_length(self):
        return self.client.recv_int(4)


    @command('SPECTRUM')
    def fifo_start_acquisition(self, acq_period): pass

    @command('SPECTRUM')
    def fifo_stop_acquisition(self): pass

    #def __del__(self):
    #    self.fifo_stop_acquisition()
