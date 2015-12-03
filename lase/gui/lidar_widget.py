# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import time

from kplot_widget import KPlotWidget
from kplot_widget import TimeRollingPlot
from kplot_widget import TimeAxisItem
from ..signal import CoherentVelocimeter

class LidarWidget(QtGui.QWidget):
    def __init__(self, spectrum_widget):
        super(LidarWidget, self).__init__()
        self.spectrum_widget = spectrum_widget
        self.driver = spectrum_widget.driver

        self.layout = QtGui.QVBoxLayout()    
        self.lidar_layout = QtGui.QVBoxLayout()
        
        self.velocity_label = QtGui.QLabel()
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(0))
  
        self.velocity_plot_button = QtGui.QPushButton('Velocity')        
        self.velocity_plot_button.setStyleSheet('QPushButton {color: blue;}')
        self.velocity_plot_button.setCheckable(True)
        
        self.lidar_layout.addWidget(self.velocity_label)
        self.lidar_layout.addWidget(self.velocity_plot_button)
       
        self.lidar_box = QtGui.QGroupBox("Lidar")
        self.lidar_box.setLayout(self.lidar_layout)
        
        self.layout.addWidget(self.lidar_box)
        self.setLayout(self.layout)
        
        self.velocity_plot_button.clicked.connect(self.swap_plots)
        self.is_velocity_plot = False
        
        self.rolling_time_plot = TimeRollingPlot()
        self.rolling_time_plot.getPlotItem().getAxis('bottom').setLabel('Time')
        self.rolling_time_plot.getPlotItem().getAxis('left').setLabel('Velocity (m/s)')
        
        self.lidar = CoherentVelocimeter()
        self.velocity = 0
                
    def update(self, spectrum):
        self.velocity = self.lidar.get_velocity(self.driver.sampling.f_fft, spectrum)
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(self.velocity))
        self.rolling_time_plot.update(self.velocity)
        
    def swap_plots(self):
        if self.is_velocity_plot: # switch to spectrum plot
            self.is_velocity_plot = False
            self.velocity_plot_button.setText('Velocity')
            
            self.spectrum_widget.replace_plot_widget(self.spectrum_widget.spectrum_plot_widget)
        else: # switch to velocity plot
            self.is_velocity_plot = True
            self.velocity_plot_button.setText('Spectrum')
            self.spectrum_widget.replace_plot_widget(self.rolling_time_plot)
            
        self.spectrum_widget.plot_widget.getPlotItem().enableAutoRange()
        self.spectrum_widget.plot_widget.set_axis()
        


        
            
