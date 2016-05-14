# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore

class SelectChannelWidget(QtGui.QWidget):
    def __init__(self, plot_widget):
        super(SelectChannelWidget, self).__init__()
        
        self.plot_widget = plot_widget

        self.layout = QtGui.QGridLayout()        
        
        self.adc_checkbox = []
        self.add_checkbox(self.adc_checkbox, 0, 'ADC')

        self.dac_checkbox = []
        self.add_checkbox(self.dac_checkbox, 1, 'DAC')
        
        self.adc_checkbox[0].stateChanged.connect(lambda: self.show_adc(0))
        self.adc_checkbox[1].stateChanged.connect(lambda: self.show_adc(1))
        self.dac_checkbox[0].stateChanged.connect(lambda: self.show_dac(0))
        self.dac_checkbox[1].stateChanged.connect(lambda: self.show_dac(1))

    def add_checkbox(self, checkbox, y_pos, text):
        for i in range(2):
            checkbox.append(QtGui.QCheckBox(text +' '+str(i+1), self))
            checkbox[i].setCheckState(QtCore.Qt.Checked)
            self.layout.addWidget(checkbox[i], y_pos, i, QtCore.Qt.AlignCenter)

    def show_adc(self, index):
        self.plot_widget.show_adc[index] = self.adc_checkbox[index].isChecked()
        self.plot_widget.dataItem[index].setVisible(self.plot_widget.show_adc[index])        
        self.plot_widget.enableAutoRange()

    def show_dac(self, index):
        self.plot_widget.show_dac[index] = self.dac_checkbox[index].isChecked()
        self.plot_widget.dataItem[2+index].setVisible(self.plot_widget.show_dac[index])
        self.plot_widget.enableAutoRange()
        
    def uncheck_all(self):
        for i in range(2):
            self.adc_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
            self.dac_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
    
