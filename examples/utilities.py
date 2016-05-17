#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ldk.core import HTTPInterface
from koheron_tcp_client import KClient

def load_instrument(host, instrument='oscillo'):
    http = HTTPInterface(host)
    http.install_instrument(instrument)
    client = KClient(host)
    return client
