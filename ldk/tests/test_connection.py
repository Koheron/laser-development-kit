# -*- coding: utf-8 -*-

import os
import pytest
from koheron_tcp_client import KClient
from ..core import HTTPInterface
from ..drivers import Oscillo

@pytest.mark.real
class TestConnection:
      
    def test(self):
        current_path = os.getcwd()
        host = os.getenv('HOST','192.168.1.100')
        http = HTTPInterface(host)
        http.install_instrument('oscillo')
        client = KClient(host)  
        assert client.is_connected
        driver = Oscillo(client)
        current = 30 #mA
        driver.set_laser_current(current)
        driver.start_laser()
        assert driver.get_laser_power() > 400
