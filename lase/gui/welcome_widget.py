# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor
import time
import os
import yaml
import sys

if sys.version_info[0] == 3:
    import urllib.request
else:
    import urllib
# http://stackoverflow.com/questions/17960942/attributeerror-module-object-has-no-attribute-urlretrieve

from ..drivers import Oscillo, Spectrum
from ..drivers import OscilloSimu, SpectrumSimu
from .oscillo_widget import OscilloWidget
from .spectrum_widget import SpectrumWidget
from .connect_widget import ConnectWidget

class WelcomeWidget(QtGui.QWidget):
    """ This widget allows to connect to one of the available drivers.
    """
    def __init__(self, parent, ip_path):
        super(WelcomeWidget, self).__init__()
        
        with open('config.yaml') as config_file:
            self.config = yaml.load(config_file)

        self.parent = parent
        self.instrument_list = self.parent.instrument_list
        self.ip_path = ip_path
        self.opened = True
        self.select_opened = True

        # Define layouts
        self.lay = QtGui.QHBoxLayout()
        self.left_layout = QtGui.QVBoxLayout()
        self.right_layout = QtGui.QVBoxLayout()

        # Connection (ip address and password)
        self.connect_layout = QtGui.QVBoxLayout()
        self.connect_widget = ConnectWidget(self, self.ip_path)
        self.connect_layout.addWidget(self.connect_widget)

        # Select between drivers
        self.drivers_layout = QtGui.QVBoxLayout()

        self.instrument_buttons = []
        for i, instrument in enumerate(self.instrument_list):
            self.instrument_buttons.append(self.set_button(instrument.capitalize() +' (Simu)'))
            self.drivers_layout.addWidget(self.instrument_buttons[i], 1, QtCore.Qt.AlignCenter)
            def make_callback(instrument):
                return lambda : self.instrument_onclick(instrument)
            self.instrument_buttons[i].clicked.connect(make_callback(instrument))

        # Left Layout
        self.view = QWebView()
        self.view.load(QtCore.QUrl.fromLocalFile(
                       os.path.join(self.parent.static_path, 'welcome.html')))       
        self.left_layout.addWidget(self.view)

        # Right layout
        self.right_layout.addLayout(self.connect_layout)
        self.right_layout.addLayout(self.drivers_layout)
        self.right_layout.addStretch(1)
        self.right_frame = QtGui.QFrame(self)
        self.right_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.right_frame.setLayout(self.right_layout)

        # Add layouts to main layout
        self.lay.addLayout(self.left_layout, 1)
        self.lay.addWidget(self.right_frame)
        self.setLayout(self.lay)

    def update(self):
        pass

    def set_button(self, name):
        button = QtGui.QPushButton(name)
        button.setStyleSheet('QPushButton {color: green;}')
        button.setFixedWidth(200)
        button.setFixedHeight(150)
        return button

    def set_connected(self):
        for i, button in enumerate(self.instrument_buttons):
            button.setText(self.parent.instrument_list[i].capitalize())

    def set_disconnected(self):
        for i, button in enumerate(self.instrument_buttons):
            button.setText(self.parent.instrument_list[i].capitalize()+' (Simu)')

    def instrument_onclick(self, instrument):
        print 'Instrument = ', instrument
        if self.connect_widget.is_connected:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.connect_widget.install_instrument(instrument)
            driver = globals()[instrument.capitalize()](self.connect_widget.client)
            driver.set_led(driver.client.host.split('.')[-1])
            QApplication.restoreOverrideCursor()
        else:
            driver = globals()[instrument.capitalize()+'Simu']()
        index = self.parent.stacked_widget.addWidget(globals()[instrument.capitalize()+'Widget'](driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)