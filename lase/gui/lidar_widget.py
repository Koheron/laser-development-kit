# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import numpy as np

class LidarWidget(QtGui.QWidget):
    def __init__(self, plot_widget):
        super(LidarWidget, self).__init__()
        self.plotWid = plot_widget

        self.layout = QtGui.QVBoxLayout()    
        self.lidar_layout = QtGui.QVBoxLayout()
        
        self.velocity_label = QtGui.QLabel()
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(0))
  
        self.velocity_plot_button = QtGui.QPushButton('Plot velocity')        
        self.velocity_plot_button.setStyleSheet('QPushButton {color: blue;}')
        self.velocity_plot_button.setCheckable(True)
        
        self.lidar_layout.addWidget(self.velocity_label)
        self.lidar_layout.addWidget(self.velocity_plot_button)
       
        self.lidar_box = QtGui.QGroupBox("Lidar")
        self.lidar_box.setLayout(self.lidar_layout)
        
        self.layout.addWidget(self.lidar_box)
        self.setLayout(self.layout)
        
        self.velocity_plot_button.clicked.connect(self.plot_velocity)
        
        self.velocities = np.zeros(1000)
        self.times = np.zeros(1000)
        
    def update(self, velocity = 0):
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(velocity))
        
        self.velocities = np.roll(self.velocities, -1)
        self.velocities[-1] = velocity
        
    def plot_velocity(self):
        if self.velocity_plot_button.text() == 'Plot spectrum':
            self.velocity_plot_status = False
            self.velocity_plot_button.setText('Plot velocity')
            
            self.plotWid.getPlotItem().getAxis('bottom').setLabel('Frequency (MHz)')
            self.plotWid.getPlotItem().getAxis('left').setLabel('PSD')
        else:
            self.velocity_plot_status = True
            self.velocity_plot_button.setText('Plot spectrum')
            
            self.plotWid.getPlotItem().getAxis('bottom').setLabel('Time')
            self.plotWid.getPlotItem().getAxis('left').setLabel('Velocity (m/s)')
            
