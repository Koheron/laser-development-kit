# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
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
    
    Note:
        When the connection is established, the drivers are `Oscillo` and 
        `Spectrum`. Otherwise the drivers are in simulation mode (`OscilloSimu`
        and `SpectrumSimu`). A web page is also displayed on the left side.
    
    """
    def __init__(self, parent, ip_path):
        super(WelcomeWidget, self).__init__()
        
        with open('config.yaml') as config_file:
            self.config = yaml.load(config_file)

        self.parent = parent
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
        self.oscillo_button = self.set_button('Oscillo (Simu)')
        self.spectrum_button = self.set_button('Spectrum (Simu)')
        self.drivers_layout.addWidget(self.oscillo_button,1,QtCore.Qt.AlignCenter)
        self.drivers_layout.addWidget(self.spectrum_button,1,QtCore.Qt.AlignCenter)

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
        
        # Connections
        self.oscillo_button.clicked.connect(self.oscillo_onclick)
        self.spectrum_button.clicked.connect(self.spectrum_onclick)

    def update(self):
        pass

    def set_button(self, name):
        button = QtGui.QPushButton(name)
        button.setStyleSheet('QPushButton {color: green;}')
        button.setFixedWidth(200)
        button.setFixedHeight(150)
        return button

    def set_connected(self):
        self.oscillo_button.setText('Oscillo')
        self.spectrum_button.setText('Spectrum')

    def set_disconnected(self):
        self.oscillo_button.setText('Oscillo (Simu)')
        self.spectrum_button.setText('Spectrum (Simu)')

    def install_instrument(self, instrument_name):
        self.connect_widget.http.install_instrument(instrument_name)
        time.sleep(0.5)
        return self.connect_widget.connect_to_tcp_server()

    def oscillo_onclick(self):
        if self.connect_widget.is_connected:
            self.install_instrument("oscillo")
            driver = Oscillo(self.connect_widget.client)
            driver.set_led(driver.client.host.split('.')[-1])
        else:
            driver = OscilloSimu()
        index = self.parent.stacked_widget.addWidget(OscilloWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)

    def spectrum_onclick(self):
        if self.connect_widget.is_connected:
            self.install_instrument("spectrum")
            driver = Spectrum(self.connect_widget.client)
            driver.set_led(driver.client.host.split('.')[-1])
        else:
            driver = SpectrumSimu()
        index = self.parent.stacked_widget.addWidget(
            SpectrumWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)

