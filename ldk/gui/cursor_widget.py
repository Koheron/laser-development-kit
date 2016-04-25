# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg


class CursorWidget(QtGui.QWidget):

    def __init__(self, plot_widget):
        super(CursorWidget, self).__init__()

        self.plot_widget = plot_widget
        
        self.cursor = [False, False]

        self.position_layout = QtGui.QVBoxLayout()
        self.cursor_layout = []
        for i in range(2):
            self.cursor_layout.append(QtGui.QVBoxLayout())

        self.delta_layout = QtGui.QVBoxLayout()
        self.Delta_layout = QtGui.QHBoxLayout()
        self.cursor_box_layout = QtGui.QHBoxLayout()
        self.global_layout = QtGui.QVBoxLayout()
        self.auto_scale_layout = QtGui.QHBoxLayout()

        self.layout = QtGui.QVBoxLayout()

        self.position_box = QtGui.QGroupBox('Position')
        self.position_box.setAlignment(5)

        self.delta_box = QtGui.QGroupBox('Delta')
        self.delta_box.setAlignment(5)

        # Cursor

        self.cursor_button = QtGui.QPushButton('ON')
        self.cursor_button.setStyleSheet('QPushButton {color: green;}')
        self.cursor_button.setCheckable(True)

        self.cursor_X = QtGui.QLabel('X')
        self.cursor_X.setAlignment(QtCore.Qt.AlignCenter)
        self.cursor_Y = QtGui.QLabel('Y')
        self.cursor_Y.setAlignment(QtCore.Qt.AlignCenter)
        
        self.XLabel = []
        self.YLabel = []
        for i in range(2):
            self.XLabel.append(QtGui.QLabel(''))
            self.XLabel[i].setAlignment(QtCore.Qt.AlignCenter)
            self.YLabel.append(QtGui.QLabel(''))
            self.YLabel[i].setAlignment(QtCore.Qt.AlignCenter)

        self.delta_X = QtGui.QLabel('X')
        self.delta_X.setAlignment(QtCore.Qt.AlignCenter)
        self.delta_Y = QtGui.QLabel('Y')
        self.delta_Y.setAlignment(QtCore.Qt.AlignCenter)

        # Cursor
        self.vLine = []
        self.hLine = []
        for i in range(2):
            self.vLine.append(pg.InfiniteLine(angle=90, movable=False))     
            self.hLine.append(pg.InfiniteLine(angle=0, movable=False))
            self.plot_widget.addItem(self.vLine[i], ignoreBounds=True)
            self.plot_widget.addItem(self.hLine[i], ignoreBounds=True)
            self.vLine[i].setVisible(self.cursor[0])
            self.hLine[i].setVisible(self.cursor[0])

        self.view_box = self.plot_widget.getViewBox()

        self.layout.addWidget(self.cursor_button)

        self.position_layout.addWidget(self.cursor_X)
        self.position_layout.addWidget(self.cursor_Y)
        
        for i in range(2):
            self.cursor_layout[i].addWidget(self.XLabel[i])
            self.cursor_layout[i].addWidget(self.YLabel[i])

        self.position_box.setLayout(self.position_layout)
        self.cursor_box_layout.addWidget(self.position_box)

        self.cursor_box = []
        for i in range(2):
            self.cursor_box.append(QtGui.QGroupBox('Cursor '+str(i+1)))
            self.cursor_box[i].setLayout(self.cursor_layout[i])
            self.cursor_box[i].setAlignment(5)

        for box in self.cursor_box:
            self.cursor_box_layout.addWidget(box)

        self.delta_layout.addWidget(self.delta_X)
        self.delta_layout.addWidget(self.delta_Y)
        self.delta_box.setLayout(self.delta_layout)

        self.Delta_layout.addStretch(1)
        self.Delta_layout.addWidget(self.delta_box)
        self.Delta_layout.addStretch(1)

        self.delta_box.setVisible(self.cursor[1])

        self.layout.addLayout(self.cursor_box_layout)
        self.layout.addLayout(self.Delta_layout)

        self.setLayout(self.layout)

        # Connections

        self.cursor_button.clicked.connect(self.cursor_on)
        self.plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)

    def auto_scale(self):
        self.plot_widget.enableAutoRange()

    def cursor_on(self):
        self.cursor[0] = not self.cursor[0]
        if self.cursor[0]:
            self.cursor_button.setStyleSheet('QPushButton {color: red;}')
            self.cursor_button.setText('OFF')
            self.set_visible()
        else:
            self.cursor[1] = False
            self.cursor_button.setStyleSheet('QPushButton {color: green;}')
            self.cursor_button.setText('ON')
            self.set_visible()
            self.reset_text()
            self.delta_box.setVisible(False)

    def is_inbounds(self, coord):
        return 1e-2 < np.abs(coord) < 1e3

    def mouseMoved(self, pos):
        if self.plot_widget.sceneBoundingRect().contains(pos):
            self.mousePoint = self.view_box.mapSceneToView(pos)
            x = self.mousePoint.x()
            y = self.mousePoint.y()
            self.vLine[0].setPos(x)
            self.hLine[0].setPos(y)
            if self.cursor[0]:
                self.XLabel[0].setText('{:.2f}'.format(x) if self.is_inbounds(x) else '%.2e' % x)
                self.YLabel[0].setText('{:.2f}'.format(y) if self.is_inbounds(y) else '%.2e' % y)
                if self.cursor[1]:
                    delta_x = x - self.cursor_2_x
                    delta_y = y - self.cursor_2_y
                    self.delta_X.setText('X   ' + ('{:.2f}'.format(delta_x) if self.is_inbounds(delta_x) else '%.2e' % delta_x))
                    self.delta_Y.setText('Y   ' + ('{:.2f}'.format(delta_y) if self.is_inbounds(delta_y) else '%.2e' % delta_y))
        else:
            self.reset_text()
            self.delta_X.setText('X')
            self.delta_Y.setText('Y')
            self.delta_box.setVisible(False)

    def mouseClicked(self, evt):
        if self.cursor[0]:
            self.cursor_2_x = self.mousePoint.x()
            self.cursor_2_y = self.mousePoint.y()
            self.vLine[1].setPos(self.mousePoint.x())
            self.hLine[1].setPos(self.mousePoint.y())
            self.cursor[1] = True
            self.delta_box.setVisible(True)
            self.vLine[1].setVisible(self.cursor[1])
            self.hLine[1].setVisible(self.cursor[1])
            if self.is_inbounds(self.mousePoint.x()):
                self.XLabel[1].setText('{:.2f}'.format(self.mousePoint.x()))
            else:
                self.XLabel[1].setText('%.2e' % (self.mousePoint.x()))
            if self.is_inbounds(self.mousePoint.y()):
                self.YLabel[1].setText('{:.2f}'.format(self.mousePoint.y()))
            else:
                self.YLabel[1].setText('%.2e' % (self.mousePoint.y()))

    def set_visible(self):
        for i in range(2):
            self.vLine[i].setVisible(self.cursor[i])
            self.hLine[i].setVisible(self.cursor[i])

    def reset_text(self):
        for i in range(2):
            self.XLabel[i].setText('')
            self.YLabel[i].setText('')
