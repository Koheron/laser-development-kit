#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from .base_simu import BaseSimu


class OscilloSimu(BaseSimu):
    def __init__(self):
        n = 8192
        super(OscilloSimu, self).__init__(n)

        self.avg_on = False
        self.waveform_size = n

        self.adc = np.zeros((2, self.sampling.n))
        self.spectrum = np.zeros((2, self.sampling.n / 2))
        self.avg_spectrum = np.zeros((2, self.sampling.n / 2))

        # Calibration
        self.adc_offset = np.zeros(2)
        self.optical_power = np.ones(2)
        self.power = np.ones(2)

        self.reset()

    def update(self):
        super(OscilloSimu, self).update()

    def reset(self):
        super(OscilloSimu, self).reset()
        self.avg_on = False
        self.set_averaging(self.avg_on)

    def set_averaging(self, avg_on):
        self.avg_on = avg_on

    def get_adc(self):
        n_avg = 1
        if self.avg_on:
            n_avg = 100
        self.update()
        self.adc[0, :] = self.model.adc_from_voltage(
            self.model.photodetection_voltage(
            self.model._optical_attenuation * self._live_laser_power),
            n_avg=n_avg)
        self.adc[1, :] = self.model.adc_from_voltage(
            self.model.photodetection_voltage(
            self.model._optical_attenuation * self._live_mach_zehnder_power),
            n_avg=n_avg)
        self.adc[0, :] -= self.adc_offset[0]
        self.adc[1, :] -= self.adc_offset[1]
        self.adc[0, :] *= self.optical_power[0] / self.power[0]
        self.adc[1, :] *= self.optical_power[1] / self.power[1]

    def get_spectrum(self):
        fft_adc = np.fft.fft(self.adc, axis=1)
        self.spectrum = fft_adc[:, 0:self.base.sampling.n / 2]

    def get_avg_spectrum(self, n_avg=1):
        self.avg_spectrum = np.zeros((2, self.base.sampling.n / 2))
        for i in range(n_avg):
            self.get_adc()
            fft_adc = np.abs(np.fft.fft(self.adc, axis=1))
            self.avg_spectrum += fft_adc[:, 0:self.base.sampling.n / 2]
        self.avg_spectrum = self.avg_spectrum / n_avg
