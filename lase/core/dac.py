from ..core import Device, command

class Dac(Device):
    def __init__(self, client, waveform_size = 8192):
        super(Dac, self).__init__(client)

        self.waveform_size = waveform_size
        self.open(self.waveform_size)

    @command
    def open(self, waveform_size):
        pass

    @command
    def set_dac_constant(self, dac_1_float, dac_2_float):
        pass

    @command
    def set_dac(self, data):
        send_handshaking(self, data)
