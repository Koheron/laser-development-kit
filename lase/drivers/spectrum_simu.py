#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from lase_simu import LaseSimu


class SpectrumSimu(LaseSimu):
    
    def __init__(self): 
        n = 4096
        super(SpectrumSimu, self).__init__(n)
                
        self.spectrum = np.zeros(self.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2,self.sampling.n))
        
        self.demod[0,:] = 0.49 * (1-np.cos(2*np.pi*np.arange(self.sampling.n)/self.sampling.n))
        self.demod[1,:] = 0
        
        self.reset()
        
    def set_velocity(self, velocity, SNR):
        """ Generates the velocity beat signal
        
            Args:
                - velocity: Object velocity (m/s)
                - SNR: Signal-to-noise
        """
        time = np.linspace(0, self.model.sampling.n*self.model.sampling.dt, self.model.sampling.n)
        omega_doppler = 2*np.pi*velocity/self.model._wavelength # Doppler shift (rad/s)
        self.velocity_signal = np.cos(omega_doppler*time) + np.random.randn(self.model.sampling.n)/SNR
    
    def get_spectrum(self):
        self.update()
        self.set_velocity(velocity=4.2, SNR=5)
        
        adc = self.model.adc_from_voltage(
                self.model.photodetection_voltage(self.model._optical_attenuation 
                                                  * self._live_laser_power 
                                                  * self.velocity_signal),
                n_avg=1)
        self.spectrum = np.abs(np.fft.fft(adc))
        
    def set_demod(self):
        pass
