#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample

from lase.core import KClient
from lase.drivers import Spectrum

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import peakutils

class CoherentVelocimeter:
    
    def __init__(self, lambda_opt=1.55E-6):
        self.lambda_opt = lambda_opt
        
    def get_simul_data(self, velocity, SNR=10, n_pts=8142, fs = 125e6, plot=False):
        time = np.linspace(0, n_pts/fs, n_pts)
        omega_doppler = 2*np.pi*velocity/self.lambda_opt # Doppler shift (rad/s)
        detected_signal = SNR * np.cos(omega_doppler*time) + np.random.randn(n_pts)
        f, PSD = signal.periodogram(detected_signal, fs)
        
        if plot:
            plt.semilogy(f/1E6, PSD)
            plt.ylim([1e-13, 1e-2])
            plt.xlabel('Frequency [MHz]')
            plt.ylabel('PSD')
            plt.show()

        self.f = f
        self.PSD = PSD
    
    def _psd_filter(self, plot=False):
        window = signal.general_gaussian(51, p=0.5, sig=10)
        psd_filtered = signal.fftconvolve(window, self.PSD)
        psd_filtered = (np.average(self.PSD) / np.average(psd_filtered)) * psd_filtered
        psd_filtered = np.roll(psd_filtered, -25)
        
        if plot:
            plt.semilogy(self.PSD)
            plt.semilogy(psd_filtered)
            plt.ylim([1e-13, 1e-2])
            plt.show()
        
        return psd_filtered
    
    def _peak_detection(self, plot=False):
        peakind = peakutils.indexes(self._psd_filter(), thres=0.5, min_dist=30)
        
        if plot:
            plt.semilogy(self.f, self.PSD)
            plt.scatter(self.f[peakind], self.PSD[peakind], color='red')
            plt.xlim([0, np.max(self.f)])
            plt.ylim([1e-13, 1e-2])
            plt.xlabel('Frequency [MHz]')
            plt.ylabel('PSD')
            plt.show()
        
if __name__ == "__main__":
    lidar = CoherentVelocimeter()
    lidar.get_simul_data(5.2, SNR=5, plot=False)
#    lidar._psd_filter(plot=True)
    lidar._peak_detection(plot=True)
