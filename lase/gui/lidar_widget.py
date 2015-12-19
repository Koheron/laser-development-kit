# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui

from .plot_widget import PlotWidget
from .plot_widget import TimeRollingPlot
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
        self.rolling_time_plot.getPlotItem().getAxis('left').setLabel('Velocity', units='m/s')
        self.rolling_time_plot.set_axis()

        self.lidar = CoherentVelocimeter()
        self.velocity = 0

    def update(self, spectrum):
        self.velocity = self.lidar.get_velocity(self.driver.base.sampling.f_fft,
                                                spectrum)
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".
                                    format(self.velocity)
                                   )
        self.rolling_time_plot.update(self.velocity)

    def swap_plots(self):
        if self.is_velocity_plot:  # switch to spectrum plot
            self.is_velocity_plot = False
            self.velocity_plot_button.setText('Velocity')
            self.spectrum_widget.set_plot_widget(self.spectrum_widget.spectrum_plot_widget)
        else:  # switch to velocity plot
            self.is_velocity_plot = True
            self.velocity_plot_button.setText('Spectrum')
            self.spectrum_widget.set_plot_widget(self.rolling_time_plot)
            self.rolling_time_plot.set_axis()

        self.spectrum_widget.plot_widget.getPlotItem().enableAutoRange()
        self.spectrum_widget.plot_widget.set_axis()
