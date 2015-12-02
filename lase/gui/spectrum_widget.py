# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

from lase_widget import LaseWidget
from cursor_widget import CursorWidget
from noise_floor_widget import NoiseFloorWidget
from lidar_widget import LidarWidget

from ..signal import CoherentVelocimeter

class SpectrumWidget(LaseWidget):
    def __init__(self, spectrum, parent):
        super(SpectrumWidget, self).__init__(spectrum, parent)
        
        self.driver = spectrum
        self.driver.start_laser()
        self.lidar = CoherentVelocimeter()
        self.lidar_widget = LidarWidget(self.left_panel_layout)
             
        # Plot Widget
        self.cursor_widget = CursorWidget(self.lidar_widget.plotWid)
        
        # Save widget
        self.splitterV_1 = QtGui.QVBoxLayout()
        self.splitterV_1.addWidget(self.cursor_widget)
        self.calibration_widget = NoiseFloorWidget(self.driver)
        self.splitterV_1.addWidget(self.calibration_widget)
        
        self.velocity = 0
        self.splitterV_1.addWidget(self.lidar_widget)
        
        self.splitterV_1.addStretch(1)
        self.right_panel_widget.setLayout(self.splitterV_1)
        self.left_panel_layout.insertWidget(1, self.lidar_widget.plotWid, 1)
        
        self.lidar_widget.set_axis()
        
    def update(self):
        super(SpectrumWidget, self).update()
        self.driver.get_spectrum()
        self.spectrum = self.driver.spectrum - self.calibration_widget.noise_floor
                           
        # Get velocity
        self.velocity = self.lidar.get_velocity(self.driver.sampling.f_fft, self.spectrum)
        self.lidar_widget.update(self.velocity)
        
        if self.lidar_widget.is_velocity_plot:
            self.lidar_widget.plotWid.dataItem.setData(self.lidar_widget.times,
                                          self.lidar_widget.velocities, clear=True)
        else:
            self.lidar_widget.plotWid.dataItem.setData(1e-6 * np.fft.fftshift(self.driver.sampling.f_fft), 
                                          1e-15* np.fft.fftshift(self.spectrum), 
                                          pen=(0,4), clear=True, _callSync='off')
        
    def refresh_dac(self):
        pass
        
