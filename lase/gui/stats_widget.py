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
        self.window_size = 50

        self.average = np.zeros(self.n_channels)
        self.amplitude = np.zeros(self.n_channels)

        self.average_vec = np.zeros((self.n_channels, self.window_size))
        self.amplitude_vec = np.zeros((self.n_channels, self.window_size))

        for i in range(self.n_channels):
            self.average_vec[i,:] = self.get_average(i)
            self.amplitude_vec[i,:] = self.get_amplitude(i)

        for i in range(self.n_channels+1):
            self.mean_labels.append(QtGui.QLabel(''))
            self.ampl_labels.append(QtGui.QLabel(''))
            self.mean_labels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.ampl_labels[i].setAlignment(QtCore.Qt.AlignCenter)

        self.mean_labels[0].setText('Average')
        self.ampl_labels[0].setText('Peak-Peak')

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

    def get_average(self, channel):
        return np.mean(self.driver.adc[channel,:])

    def get_amplitude(self, channel):
        return np.max(self.driver.adc[channel,:])-np.min(self.driver.adc[channel,:])

    def update(self):
        self.average_vec = np.roll(self.average_vec, 1, axis=1)
        self.amplitude_vec = np.roll(self.amplitude_vec, 1, axis=1)
        for i in range(self.n_channels):            
            self.average_vec[i,0] = self.get_average(i)                
            self.amplitude_vec[i,0] = self.get_amplitude(i)

            self.average[i] = np.mean(self.average_vec[i,:])
            if 1e-2 < abs(self.average[i]) < 1e4:
                mean_text = '{:.2f}'.format(self.average[i])
            else:
                mean_text = '%.4e'%(self.average[i])
            self.mean_labels[i+1].setText(mean_text)

            self.amplitude[i] = np.mean(self.amplitude_vec[i,:])
            if 1e-2 < self.amplitude[i] < 1e4:
                ampl_text = '{:.2f}'.format(self.amplitude[i])
            else:
                ampl_text = '%.4e'%(self.amplitude[i])
            self.ampl_labels[i+1].setText(ampl_text)

