# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import numpy as np

class LidarWidget(QtGui.QWidget):
    def __init__(self, driver):
        super(LidarWidget, self).__init__()
        self.driver = driver 

        self.layout = QtGui.QVBoxLayout()    
        self.window_layout = QtGui.QVBoxLayout()
        
        self.velocity_label = QtGui.QLabel()
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(0))
  
        
        self.calibrate_button = QtGui.QPushButton('Calibrate')        
        self.calibrate_button.setStyleSheet('QPushButton {color: orange;}')
        
        self.window_layout.addWidget(self.velocity_label)
       
        self.window_box = QtGui.QGroupBox("Lidar")
        self.window_box.setLayout(self.window_layout)
        
        self.layout.addWidget(self.calibrate_button)
        self.layout.addWidget(self.window_box)
        self.setLayout(self.layout)        
        
    def update(self, velocity = 0):
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(velocity))
        
