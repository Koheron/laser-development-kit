from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import datetime as datetime
import time

class KPlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(KPlotWidget, self).__init__(*args, **kwargs)
        
        self.dataItem = pg.PlotDataItem(pen=(0,4), clear=True, _callSync='off')
        self.addItem(self.dataItem)
        
    def set_axis(self):
        self.getPlotItem().setMouseEnabled(x=False, y=True)
        self.getViewBox().setMouseMode(self.getViewBox().PanMode)
        self.getPlotItem().enableAutoRange()
            
class TimeRollingPlot(pg.PlotWidget):
    """ Time rolling plot """
    def __init__(self, n_pts=1000, *args, **kwargs):
        super(TimeRollingPlot, self).__init__(
                      *args, 
                      axisItems={'bottom': TimeAxisItem(orientation='bottom')}, 
                      **kwargs)
                      
        self.dataItem = pg.PlotDataItem(pen=(0,4), clear=True, _callSync='off')
        self.addItem(self.dataItem)
                      
        self.values = np.zeros(n_pts)
        self.times = np.zeros(n_pts) + time.time()
        
    def set_axis(self):
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        self.getPlotItem().enableAutoRange()
        
    def update(self, value):
        self.values = np.roll(self.values, -1)
        self.values[-1] = value
        
        self.times = np.roll(self.times, -1)
        self.times[-1] = time.time()
        
        self.dataItem.setData(self.times, self.values, clear=True)
        self.getViewBox().setXRange(self.times[0], self.times[-1])

# https://gist.github.com/friendzis/4e98ebe2cf29c0c2c232
class TimeAxisItem(pg.AxisItem):
    """ Axis display time in H:M:S """
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]
