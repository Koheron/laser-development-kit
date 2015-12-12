# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
import time
import os
import urllib
import yaml

from ..drivers import Oscillo, Spectrum
from ..drivers import OscilloSimu, SpectrumSimu
from oscillo_widget import OscilloWidget
from spectrum_widget import SpectrumWidget
from connect_widget import ConnectWidget

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
        self.oscillo_button.clicked.connect(self.oscillo_on)
        self.spectrum_button.clicked.connect(self.spectrum_on)

    def update(self):
        pass

    def set_button(self, name):
        button = QtGui.QPushButton(name)
        button.setStyleSheet('QPushButton {color: green;}')
        button.setFixedWidth(200)
        button.setFixedHeight(150)
        return button

    def connected(self):
        self.oscillo_button.setText('Oscillo')
        self.spectrum_button.setText('Spectrum')

    def disconnected(self):
        self.oscillo_button.setText('Oscillo (Simu)')
        self.spectrum_button.setText('Spectrum (Simu)')

    def load_bitstream(self, bitstream_name):
        bitstream_path = os.path.join(self.parent.bitstreams_path, bitstream_name+'.bit')
        if not os.path.isfile(bitstream_path):
            bitstream_url = self.config["bitstreams"][bitstream_name+"_url"]
            urllib.urlretrieve(bitstream_url, bitstream_path)
        self.connect_widget.ssh.load_pl(bitstream_path)

    def oscillo_on(self):
        if self.connect_widget.is_connected:
            time.sleep(0.01)
            self.load_bitstream("oscillo")
            time.sleep(0.01)
            driver = Oscillo(self.connect_widget.client)
            driver.lase_base.set_led(driver.lase_base.client.host.split('.')[-1])
        else:
            driver = OscilloSimu()
        index = self.parent.stacked_widget.addWidget(OscilloWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)

    def spectrum_on(self):
        if self.connect_widget.is_connected:
            time.sleep(0.01)
            self.load_bitstream("spectrum")
            time.sleep(0.01)
            driver = Spectrum(self.connect_widget.client, current_mode='pwm')
            driver.set_led(driver.client.host.split('.')[-1])
        else:
            driver = SpectrumSimu()
        index = self.parent.stacked_widget.addWidget(
            SpectrumWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)
