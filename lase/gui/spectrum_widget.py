# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph.Qt import QtGui

from .plot_widget import PlotWidget
from .lase_widget import LaseWidget
from .cursor_widget import CursorWidget
from .noise_floor_widget import NoiseFloorWidget
from .lidar_widget import LidarWidget

from PyQt4.QtCore import pyqtSignal

class SpectrumWidget(LaseWidget):

    #offset_updated_signal = pyqtSignal(int)

    def __init__(self, spectrum, parent):
        super(SpectrumWidget, self).__init__(spectrum, parent)
        
        self.driver = spectrum

        # Layouts
        self.control_layout = QtGui.QVBoxLayout()

        # Plot widget
        self.init_plot_widget()
        self.set_plot_widget(self.spectrum_plot_widget)

        self.cursor_widget = CursorWidget(self.plot_widget)
        self.calibration_widget = NoiseFloorWidget(self.driver)
        self.lidar_widget = LidarWidget(self)

        self.control_layout.addWidget(self.cursor_widget)
        self.control_layout.addWidget(self.calibration_widget)
        self.control_layout.addWidget(self.lidar_widget)
        self.control_layout.addStretch(1)

        self.right_panel_widget.setLayout(self.control_layout)
        
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

        if self.driver.is_failed:
            print("An error occured during update\nLeave Spectrum")
            self.monitor_widget.close_session()

    def refresh_dac(self):
        pass

    def init_plot_widget(self):
        self.spectrum_plot_widget = PlotWidget(name="data")
        self.spectrum_plot_widget.getPlotItem().getAxis('bottom').setLabel('Frequency', units='MHz')
        self.spectrum_plot_widget.getPlotItem().getAxis('left').setLabel('PSD')
        self.spectrum_plot_widget.plotItem.setMouseEnabled(x=False, y=True)

    def set_plot_widget(self, new_plot_widget):
        self.plot_widget.setParent(None)
        self.plot_widget = new_plot_widget
        self.left_panel_layout.insertWidget(1, self.plot_widget, 1)

