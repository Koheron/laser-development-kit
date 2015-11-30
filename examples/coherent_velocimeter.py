#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample

from lase.core import KClient
from lase.drivers import Spectrum

import numpy as np
from scipy import signal # for find_peaks_cwt
import matplotlib.pyplot as plt

class CoherentVelocimeter:
    
    def __init__(self, lambda_opt=1.55E-6):
        self.lambda_opt = lambda_opt
        
    def get_simul_data(self, velocity, SNR=10, n_pts=8142, fs = 125e6, plot=False):
        time = np.linspace(0, n_pts/fs, n_pts)
        omega_doppler = 2*np.pi*velocity/self.lambda_opt # Doppler shift (rad/s)
        detected_signal = SNR * np.cos(omega_doppler*time) + np.random.randn(n_pts)
        f, PSD = signal.periodogram(detected_signal, fs)
        
        if plot:
            plt.semilogy(f, PSD)
            plt.ylim([1e-13, 1e-2])
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD')
            plt.show()
    
    def _peak_detection(self):
        pass
        
if __name__ == "__main__":
    lidar = CoherentVelocimeter()
    lidar.get_simul_data(2.5, plot=True)
