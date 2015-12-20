# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import numpy as np
import time


class MonitorWidget(QtGui.QWidget):

    def __init__(self, driver, laser_widget):
        super(MonitorWidget, self).__init__()
        self.driver = driver
        self.laser_widget = laser_widget

        # Layout
        self.layout = QtGui.QHBoxLayout()
        self.frame_layout = QtGui.QHBoxLayout()

        # Close button
        self.close_button = QtGui.QPushButton('Home')
        self.close_button.setStyleSheet('QPushButton {color: blue;}')
        self.close_button.setFixedWidth(80)

        # Frame rate
        self.frame_rate_label = QtGui.QLabel()
        self.frame_rate_label.setText('Frame rate (Hz) : '+"{:.1f}".format(0))
        # Laser power
        self.laser_power_label = QtGui.QLabel()
        self.laser_power_label.setText('Laser power (u.a.) : '+
                                       "{:.2f}".format(self.driver.get_laser_power()))

        # Laser current measured from the XADC
        self.laser_current_label = QtGui.QLabel()
        self.laser_current_label.setText('Measured current (mA) : '+
            "{:.2f}".format(0.01 * self.driver.get_laser_current()))

        self.layout.addWidget(self.close_button, 2)
        self.layout.addStretch(1)
        self.frame_layout.addWidget(self.frame_rate_label)
        self.layout.addLayout(self.frame_layout, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.laser_current_label, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.laser_power_label, 1)

        # Connections
        self.close_button.clicked.connect(self.close_session)

    def update(self, frame_rate = 0):
        # monitoring_data = self.driver.get_monitoring()
        # self.laser_current_label.setText('Measured current (mA) : '+"{:.2f}".format(0.01 * monitoring_data[0]))
        # self.laser_power_label.setText('Laser power (u.a.) : '+"{:.2f}".format(monitoring_data[1]))

        self.laser_current_label.setText('Measured current (mA) : '+
                                         "{:.2f}".format(0.01 * self.driver.get_laser_current()))
        self.laser_power_label.setText('Laser power (u.a.) : '+
                                       "{:.2f}".format(self.driver.get_laser_power()))
        self.frame_rate_label.setText('Frame rate (Hz) : '+
                                      "{:.2f}".format(frame_rate))

    def close_session(self):
        # Ramp down smoothly laser power
        current_ramp = np.linspace(self.laser_widget.laser_current, 0, 20)

        for current in current_ramp:
            self.driver.set_laser_current(current)
            time.sleep(0.01)

        self.laser_widget.stop_laser()
        self.driver.opened = False
