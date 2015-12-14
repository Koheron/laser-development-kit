#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .lase import Lase
from ..core import Device, command

class Spectrum(Device):
    """ Driver for the spectrum bitstream """ 
    
    def __init__(self, client, map_size=4096, verbose=False):
        super(Spectrum, self).__init__(client)
        
        n = 4096        
        self.lase_base = Lase(n, client, map_size)
        
        self.open(n)
                
        # Addresses of memory maps
        _spectrum_addr = int('0x42000000',0)
        _demod_addr = int('0x44000000',0)
        
        # Config offsets
        self._subtract_mean_off = 24
        self._cfg_fft_off = 28
        self._demod_off = 32
        self._avg_off_off = 36

        # Add memory maps
        self._spectrum = self.lase_base.dvm.add_memory_map(_spectrum_addr, self.lase_base.sampling.n/1024*map_size)
        self._demod = self.lase_base.dvm.add_memory_map(_demod_addr, self.lase_base.sampling.n/1024*map_size)
        
        # TODO Ckeck memory map ID is not NaN

        self.spectrum = np.zeros(self.lase_base.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2,self.lase_base.sampling.n))
        
        self.demod[0,:] = 0.49 * (1- np.cos(2*np.pi*np.arange(self.lase_base.sampling.n)/self.lase_base.sampling.n))   #0.5*np.real(demod) 
        self.demod[1,:] = 0#0.5*np.imag(demod)

        self.set_offset(-199, -21)
        #self.set_offset(0, 0)

        self.set_demod()
#        self.dvm.write(self._config, self._scale_sch_off, 427)
        
        self.lase_base.reset()
    
    @command
    def open(self, samples_num):
        pass       
    
    @command
    def set_scale_sch(self, scale_sch):
        pass
       
    @command
    def set_offset(self, offset_real, offset_imag):
        pass

#    def set_demod(self):
#        self.dvm.write(self._config,self._demod_off, 8192 + 65356 * 8192)

    def set_demod(self, warning=False):
        if warning:
            if np.max(np.abs(self.demod)) >= 1:
                print('WARNING : dac out of bounds')
        demod_data_1 = np.mod(np.floor(8192*self.demod[0,:]) + 8192,16384)+8192
        demod_data_2 = np.mod(np.floor(8192*self.demod[1,:]) + 8192,16384)+8192
        self.lase_base.dvm.write_buffer(self._demod, 0, demod_data_1 + 65536 * demod_data_2)
        
    @command
    def get_spectrum(self):
        self.spectrum = self.client.recv_buffer(self.lase_base.sampling.n, data_type='float32')
        n_avg = self.get_num_average()
        print 10*n_avg
        #self.spectrum = self.spectrum / n_avg
        #self.spectrum[1] = 1
        
    @command
    def get_num_average(self):
        return self.client.recv_int(4)
