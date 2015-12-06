# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

from kplot_widget import KPlotWidget
from lase_widget import LaseWidget
from cursor_widget import CursorWidget
from noise_floor_widget import NoiseFloorWidget
from lidar_widget import LidarWidget
from koheron_slider import KoheronSlider

from PyQt4.QtCore import SIGNAL, pyqtSignal

class SpectrumWidget(LaseWidget):

    offset_updated_signal = pyqtSignal(int)

    def __init__(self, spectrum, parent):
        super(SpectrumWidget, self).__init__(spectrum, parent)
        
        self.driver = spectrum
        self.driver.start_laser()
        
        self.spectrum_plot_widget = KPlotWidget(name="data") 
        self.spectrum_plot_widget.getPlotItem().getAxis('bottom').setLabel('Frequency', units='MHz')
        self.spectrum_plot_widget.getPlotItem().getAxis('left').setLabel('PSD')
            
        self.plot_widget = self.spectrum_plot_widget
        self.plot_widget.set_axis()
          
        self.lidar_widget = LidarWidget(self)
        self.cursor_widget = CursorWidget(self.plot_widget)
        self.calibration_widget = NoiseFloorWidget(self.driver)
        
        self.splitterV_1 = QtGui.QVBoxLayout()
        self.splitterV_1.addWidget(self.cursor_widget)
        self.splitterV_1.addWidget(self.calibration_widget)
        self.splitterV_1.addWidget(self.lidar_widget)

        self.splitterV_1.addStretch(1)
        self.right_panel_widget.setLayout(self.splitterV_1)
        self.left_panel_layout.insertWidget(1, self.plot_widget, 1)
        
    def update(self):
        super(SpectrumWidget, self).update()
        self.driver.get_spectrum()

        self.spectrum = self.driver.spectrum - self.calibration_widget.noise_floor
        self.lidar_widget.update(self.spectrum)
        
        if not self.lidar_widget.is_velocity_plot:
            self.plot_widget.dataItem.setData(
                        1e-6 * np.fft.fftshift(self.driver.sampling.f_fft), 
                        1e-15 * np.fft.fftshift(self.spectrum), 
                        pen=(0,4), clear=True, _callSync='off')
        
    def replace_plot_widget(self, new_plot_widget):
        self.plot_widget.setParent(None)
        self.plot_widget = new_plot_widget
        self.left_panel_layout.insertWidget(1, self.plot_widget, 1)

