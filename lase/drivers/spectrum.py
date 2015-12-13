#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from .lase import Lase

class Spectrum(Lase):
    """ Driver for the spectrum bitstream """ 
    def __init__(self, client, map_size = 4096, verbose = False, current_mode = 'pwm'): 
        n = 4096
        super(Spectrum, self).__init__(n, client, map_size = 4096, current_mode = 'pwm')   
                
        # Addresses of memory maps
        _spectrum_addr = int('0x42000000',0)
        _demod_addr = int('0x44000000',0)
        
        # Config offsets
        self._subtract_mean_off = 24
        self._cfg_fft_off = 28
        self._demod_off = 32
        self._avg_off_off = 36

        # Add memory maps
        self._spectrum = self.dvm.add_memory_map(_spectrum_addr, self.sampling.n/1024*map_size)
        self._demod = self.dvm.add_memory_map(_demod_addr, self.sampling.n/1024*map_size)

        self.spectrum = np.zeros(self.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2,self.sampling.n))
        
        self.demod[0,:] = 0.49 * (1- np.cos(2*np.pi*np.arange(self.sampling.n)/self.sampling.n))   #0.5*np.real(demod) 
        self.demod[1,:] = 0#0.5*np.imag(demod)

        self.set_offset(-199, -21)
        #self.set_offset(0, 0)

        self.set_demod()
#        self.dvm.write(self._config, self._scale_sch_off, 427)
        
        self.reset()
    
    def set_scale_sch(self, scale_sch):
        self.dvm.write(self._config,self._cfg_fft_off, 1 + 2 * scale_sch)
           
    def set_offset(self, offset_real, offset_imag):
        self.dvm.write(self._config,self._subtract_mean_off, offset_real + 2**14 * offset_imag)

#    def set_demod(self):
#        self.dvm.write(self._config,self._demod_off, 8192 + 65356 * 8192)

    def set_demod(self, warning=False):
        if warning:
            if np.max(np.abs(self.demod)) >= 1:
                print('WARNING : dac out of bounds')
        demod_data_1 = np.mod(np.floor(8192*self.demod[0,:]) + 8192,16384)+8192
        demod_data_2 = np.mod(np.floor(8192*self.demod[1,:]) + 8192,16384)+8192
        self.dvm.write_buffer(self._demod, 0, demod_data_1 + 65536 * demod_data_2)
        
    def get_spectrum(self):
        self.dvm.set_bit(self._config, self._addr_off,1)
        time.sleep(0.001)
        self.spectrum = self.dvm.read_buffer(self._spectrum, 0, self.sampling.n, data_type='float32')

        # Check reception
        if np.isnan(self.spectrum[0]):
            self._is_failed = True
            return        
        
        n_avg = self.dvm.read(self._status, self._n_avg1_off)
        self.spectrum = self.spectrum / np.float(n_avg)
        self.spectrum[1] = 1
        self.dvm.clear_bit(self._config, self._addr_off,1)
        
