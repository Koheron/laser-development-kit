#!/usr/bin/env python
# -*- coding: utf-8 -*-

from koheron import command

class Laser(object):

    def __init__(self, client):
        self.client = client

    @command()
    def start(self):
        pass

    @command()
    def stop(self):
        pass

    @command()
    def get_measured_power(self):
        return self.client.recv_float()

    @command()
    def get_measured_current(self):
        return self.client.recv_float()

    @command()
    def set_current(self, current):
        ''' Laser current in mA '''
        pass

    @command(classname='Eeprom', funcname='write')
    def write_eeprom(self, address, value):
        pass

    @command(classname='Eeprom', funcname='read')
    def read_eeprom(self, address):
        return self.client.recv_uint32()