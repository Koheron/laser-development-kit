# laser-development-kit

[![Circle CI](https://circleci.com/gh/Koheron/laser-development-kit.svg?style=shield)](https://circleci.com/gh/Koheron/laser-development-kit) [![Code Climate](https://codeclimate.com/github/Koheron/laser-development-kit/badges/gpa.svg)](https://codeclimate.com/github/Koheron/laser-development-kit)

#### `Python API for Koheron Laser Development Kit`

## Installation

1) Get [latest release](https://github.com/Koheron/zynq-sdk/releases/download/v0.4.0-beta.4/oscillo-6ea06b3.img) of SD card image.
On Windows, you can use [win32diskimager](http://sourceforge.net/projects/win32diskimager/) to burn the SD card.

2) Insert the SD card on the Red Pitaya, then plug ethernet and power cables. 
The last number of the board IP address is displayed on binary format on the 8 Red Pitaya LEDs for convenience.

3) Make sure the following packages are installed:
* Python (2.7+ or 3.5+) with Numpy and Scipy
* PyQtGraph (`pip install pyqtgraph`)
* paramiko (`pip install paramiko`)

4) Run demo:

```sh
python interface.py
```

You will need to enter the board IP adress and the root password (`changeme` by default) to connect to the board.

![Demo](https://cloud.githubusercontent.com/assets/1735094/9765362/317e8212-5714-11e5-8480-ab3e311260c9.gif)

## Build your custom FPGA bitstream

You can build custom bitstreams from the reference designs in the [zynq-sdk](https://github.com/Koheron/zynq-sdk) repository.

## Simulation mode

The software can also run in simulation mode i.e. without a board:

```python
from lase.drivers import OscilloSimu
import numpy as np
import matplotlib.pyplot as plt

driver = OscilloSimu()

# Set laser current to 30 mA
current = 30 # mA
driver.set_laser_current(current)
print 'Laser power = ', driver.get_laser_power(), 'a.u.'

# Enable laser
driver.start_laser()
print 'Laser power = ', driver.get_laser_power(), 'a.u.'

# Modulate laser current
n = driver.sampling.n # Number of points in the waveform
fs = driver.sampling.fs # Sampling frequency (Hz)
mod_amp = 0.4 # Modulation amplitude in V
freq = 10
print 'Modulation frequency = ', freq * fs / n, 'Hz'
driver.dac[1,:] = mod_amp * np.cos(2*np.pi* freq/n*np.arange(n))
driver.set_dac()

# Retrieve the modulation signal from the photodiode on ADC 1
driver.get_adc()
signal = driver.adc[0,:]

# Plot the result
plt.plot(driver.sampling.t, signal)

#
driver.stop_laser()
driver.close()

```

## Copyright

Copyright 2015 Koheron SAS. The code is released under [the MIT licence](https://github.com/Koheron/laser-development-kit/blob/master/LICENSE).

