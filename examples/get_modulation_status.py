#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from koheron import connect
from drivers import Oscillo

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='oscillo')
driver = Oscillo(client)

while True:
    try:
        print driver.get_modulation_status()
        time.sleep(0.01)
    except KeyboardInterrupt:
        break
