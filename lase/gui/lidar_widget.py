# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import time

from kplot_widget import KPlotWidget
from kplot_widget import TimeAxisItem

class LidarWidget(QtGui.QWidget):
    def __init__(self, left_panel_layout):
        super(LidarWidget, self).__init__()
        self.left_panel_layout = left_panel_layout
        self.plotWid = KPlotWidget(name="data")

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
        
        self.velocity_plot_button.clicked.connect(self.plot_velocity)
        self.is_velocity_plot = False
        
        self.velocities_plot_length = 1000
        self.velocities = np.zeros(self.velocities_plot_length)
        self.times = np.zeros(self.velocities_plot_length)
        
    def update(self, velocity = 0):
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(velocity))
        
        self.velocities = np.roll(self.velocities, -1)
        self.velocities[-1] = velocity
        
        self.times = np.roll(self.times, -1)
        self.times[-1] = time.time()
        
    def plot_velocity(self):
        if self.is_velocity_plot:
            self.is_velocity_plot = False
            self.velocity_plot_button.setText('Velocity')
            
            self.plotWid.setParent(None)
            self.plotWid = KPlotWidget(name="data")
            self.left_panel_layout.insertWidget(1, self.plotWid, 1)
            
            self.plotWid.getPlotItem().getAxis('bottom').setLabel('Frequency (MHz)')
            self.plotWid.getPlotItem().getAxis('left').setLabel('PSD')
        else: # spectrum_plot
            self.is_velocity_plot = True
            self.velocity_plot_button.setText('Spectrum')
            
            self.plotWid.setParent(None)
            time_axis_item = TimeAxisItem(orientation='bottom')
            self.plotWid = KPlotWidget(axisItems={'bottom': time_axis_item})
            self.left_panel_layout.insertWidget(1, self.plotWid, 1)
            self.plotWid.getPlotItem().getAxis('bottom').setLabel('Time')
            self.plotWid.getPlotItem().getAxis('left').setLabel('Velocity (m/s)')
            
        self.plotWid.getPlotItem().enableAutoRange()
        self.set_axis()
        
    def set_axis(self):
        self.plotWid.getPlotItem().setMouseEnabled(x=False, y=True)
        self.plotWid.getViewBox().setMouseMode(self.plotWid.getViewBox().PanMode)
        self.plotWid.getPlotItem().enableAutoRange()
        
            
