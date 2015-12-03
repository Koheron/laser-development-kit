from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import datetime as datetime

class KPlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(KPlotWidget, self).__init__(*args, **kwargs)
        
        self.dataItem = pg.PlotDataItem(pen=(0,4), clear=True, _callSync='off')
        self.addItem(self.dataItem)
        
    def set_axis(self):
        self.getPlotItem().setMouseEnabled(x=False, y=True)
        self.getViewBox().setMouseMode(self.getViewBox().PanMode)
        self.getPlotItem().enableAutoRange()
            
class TimeRollingPlot(KPlotWidget):
    def __init__(self, *args, **kwargs):
        super(TimeRollingPlot, self).__init__(*args, 
                      axisItems={'bottom': TimeAxisItem(orientation='bottom')}, **kwargs)

# https://gist.github.com/friendzis/4e98ebe2cf29c0c2c232
class TimeAxisItem(pg.AxisItem):
    """ Axis display time in H:M:S
    """
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]
