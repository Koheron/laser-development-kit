#!/usr/bin/env python
# -*- coding: utf-8 -*-

from koheron import command

class Laser(object):

    def __init__(self, client, verbose=False):
        self.client = client

    @command(funcname='start')
    def start_laser(self): pass

    @command(funcname='stop')
    def stop_laser(self): pass

    @command(funcname='get_measured_current')
    def get_laser_current(self):
        return (0.0001/21.) * self.client.recv_float()

    @command(funcname='get_measured_power')
    def get_laser_power(self):
        return self.client.recv_float()

    @command(classname='Laser')
    def get_status(self):
        return self.client.recv_tuple()

    @command(classname='Laser', funcname='set_current')
    def set_laser_current(self, current):
        """ current: The bias in mA """
        pass
