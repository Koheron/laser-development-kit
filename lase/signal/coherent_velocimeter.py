# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal
#import peakutils

class CoherentVelocimeter:
    """ Coherent velocimeter based on the Spectrum bitstream
    """
    
    def __init__(self, lambda_opt=1.55E-6):
        """
            Args:
                - lambda_opt: Optical wavelength (m)
        """        
        self.lambda_opt = lambda_opt
    
    def _psd_filter(self):
        """ Filter the PSD
        
            Args:
                - plot: Set to True to plot the result
        """    
        window = signal.general_gaussian(51, p=0.5, sig=10)
        psd_filtered = signal.fftconvolve(window, self.PSD)
        psd_filtered = (np.average(self.PSD) / np.average(psd_filtered)) * psd_filtered
        psd_filtered = np.roll(psd_filtered, -25)
        
        return psd_filtered
    
#    def _peak_detection(self, plot=False):
#        """ Performs the peak detection on the PSD
#        
#             Args:
#                - plot: Set to True to plot the result       
#        """
#        peakind = peakutils.indexes(self._psd_filter(), thres=0.5, min_dist=30)
#        return peakind
#   
    def get_velocity(self, f, PSD):
        """ Return the velocity in m/s
        """
        self.PSD = PSD
     
#        f_peak = f[self._peak_detection()]
        f_peak = np.abs(f[np.argmax(self.PSD)])
        
        # TODO Handle the case where several peaks are detected
        
        return self.lambda_opt * f_peak
        
