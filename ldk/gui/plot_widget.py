import pyqtgraph as pg
import numpy as np

class PlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(PlotWidget, self).__init__(*args, **kwargs)

        self.dataItem = pg.PlotDataItem(pen=(0,4), clear=True, _callSync='off')
        self.addItem(self.dataItem)

    def set_axis(self):
        self.getPlotItem().setMouseEnabled(x=False, y=True)
        self.getViewBox().setMouseMode(self.getViewBox().PanMode)
        self.getPlotItem().enableAutoRange()


class RollingPlot(pg.PlotWidget):
    """ Rolling plot """
    def __init__(self, n_pts=30000, *args, **kwargs):
        super(RollingPlot, self).__init__(*args, **kwargs)
        self.dataItem = pg.PlotDataItem(pen=(0, 4), clear=True, _callSync='off')
        self.addItem(self.dataItem)
        self.values = np.zeros(n_pts)

    def set_axis(self):
        self.getPlotItem().setMouseEnabled(x=False, y=False)
        self.getPlotItem().enableAutoRange()

    def update(self, value):
        self.values = np.roll(self.values, -value.size)
        self.values[self.values.size-value.size:self.values.size] = value
        self.dataItem.setData(self.values, clear=True)


