# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class StatsWidget(QtGui.QWidget):

    def __init__(self, driver):
        super(StatsWidget, self).__init__()

        self.driver = driver

        self.layout = QtGui.QHBoxLayout()

        self.mean_labels = []
        self.ampl_labels = []
        self.n_channels = 2

        for i in range(self.n_channels+1):
            self.mean_labels.append(QtGui.QLabel(''))
            self.ampl_labels.append(QtGui.QLabel(''))
            self.mean_labels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.ampl_labels[i].setAlignment(QtCore.Qt.AlignCenter)

        self.mean_labels[0].setText('Average')
        self.ampl_labels[0].setText('Amplitude')

        self.boxes = []
        self.box_names = ['Measures', 'ADC 1', 'ADC 2']
        for i in range(self.n_channels+1):
            self.boxes.append(QtGui.QGroupBox(self.box_names[i]))
            self.boxes[i].setAlignment(5)

        self.name_layout = QtGui.QVBoxLayout()
        self.name_layout.addWidget(self.mean_labels[0])
        self.name_layout.addWidget(self.ampl_labels[0])
        self.boxes[0].setLayout(self.name_layout)

        self.adc_1_layout = QtGui.QVBoxLayout()
        self.adc_1_layout.addWidget(self.mean_labels[1])
        self.adc_1_layout.addWidget(self.ampl_labels[1])
        self.boxes[1].setLayout(self.adc_1_layout)

        self.adc_2_layout = QtGui.QVBoxLayout()
        self.adc_2_layout.addWidget(self.mean_labels[2])
        self.adc_2_layout.addWidget(self.ampl_labels[2])
        self.boxes[2].setLayout(self.adc_2_layout)

        for i in range(self.n_channels+1):
            self.layout.addWidget(self.boxes[i])

    def update(self):
        for i in range(self.n_channels):
            if 1e-2 < np.abs(np.mean(self.driver.adc[i,:])) < 1e3:
                mean_text = '{:.2f}'.format(np.mean(self.driver.adc[i,:]))
            else:
                mean_text = '%.2e'%(np.mean(self.driver.adc[i,:]))
            self.mean_labels[i+1].setText(mean_text)
            if 1e-2 < np.abs(np.max(self.driver.adc[i,:])-np.min(self.driver.adc[i,:])) < 1e3:
                ampl_text = '{:.2f}'.format(np.max(self.driver.adc[i,:])-np.min(self.driver.adc[i,:]))
            else:
                ampl_text = '%.2e'%(np.max(self.driver.adc[i,:])-np.min(self.driver.adc[i,:]))
            self.ampl_labels[i+1].setText(ampl_text)
