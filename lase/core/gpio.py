class Gpio():
    """ GPIO driver
    http://www.xilinx.com/support/documentation/ip_documentation/axi_gpio/v2_0/pg144-axi-gpio.pdf
    http://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit-in-c-c
    """
    def __init__(self, dvm, addr=int('0x41200000', 0),
                 map_size=16 * 4096, n_channel_1=8, n_channel_2=8,
                 dual_channel=True):
        self.dvm = dvm
        self.dev_num = self.dvm.add_memory_map(addr, map_size)

    def set_bit(self, index, channel=1):
        if channel == 2:
            offset = 8
        else:
            offset = 0

        self.dvm.set_bit(self.dev_num, offset, index)

    def clear_bit(self, index, channel=1):
        if channel == 2:
            offset = 8
        else:
            offset = 0

        self.dvm.clear_bit(self.dev_num, offset, index)

    def toggle_bit(self, index, channel=1):
        if channel == 2:
            offset = 8
        else:
            offset = 0

        self.dvm.toggle_bit(self.dev_num, offset, index)

    def set_as_input(self, index, channel=1):
        if channel == 2:
            offset = 12
        else:
            offset = 4

        self.dvm.set_bit(self.dev_num, offset, index)

    def set_as_output(self, index, channel=1):
        if channel == 2:
            offset = 12
        else:
            offset = 4

        self.dvm.clear_bit(self.dev_num, offset, index)
