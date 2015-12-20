# -*- coding: utf-8 -*-

from ..base_simu import BaseSimu

class TestBaseSimu:

    def test_laser_enable(self):
        n = 8192
        base_simu = BaseSimu(n)
        laser_current = 1000 * base_simu.model._laser_threshold + 10
        base_simu.set_laser_current(laser_current)
        base_simu.update()
        assert base_simu.get_laser_power() == 0
        base_simu.start_laser()
        base_simu.update()
        assert base_simu.get_laser_power() > 0
        base_simu.stop_laser()
        base_simu.update()
        assert base_simu.get_laser_power() == 0
