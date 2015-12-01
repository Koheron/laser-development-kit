# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui

class LidarWidget(QtGui.QWidget):
    def __init__(self, driver):
        super(LidarWidget, self).__init__()
        
        self.driver = driver        
        
        # Layout
        self.layout = QtGui.QHBoxLayout()  
        
        # Velocity
        self.velocity_rate_label = QtGui.QLabel()
        self.velocity_rate_label.setText('Velocity (m/s) : '+"{:.2f}".format(0))
        self.layout.addWidget(self.velocity_rate_label)      
        
    def update(self, velocity = 0):
        print velocity
        self.velocity_rate_label.setText('Velocity (m/s) : '+"{:.2f}".format(velocity))
        

