#!/usr/bin/env python

import sys
from PySide2 import QtCore, QtGui, QtWidgets

#------------------------------------------------------------------------------


class LCDRange(QtWidgets.QWidget):

    # Signals shold be defined only within calsses inheriting from QObject
    # Define Signals as class variables
    # Connect/referenct Signals them as instance variables
    # Signals and Slots MUST be bound to object instances for them to work
    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        lcd = QtWidgets.QLCDNumber(2)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.slider.valueChanged[int].connect(lcd.display)
        self.slider.valueChanged[int].connect(self.valueChanged)

        # OLD STYLE signal/slot + signal/signal
        #self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
        #             lcd, QtCore.SLOT("display(int)"))
        #self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
        #             self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        quit.clicked.connect(QtWidgets.QApplication.quit)

        grid = QtWidgets.QGridLayout()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(quit)
        layout.addLayout(grid)
        self.setLayout(layout)

        previousRange = None
        for row in range(3):
            for column in range(3):
                lcdRange = LCDRange()
                grid.addWidget(lcdRange, row, column)

                if previousRange:
                    # connect a widgets signal to a previous instance slot
                    lcdRange.valueChanged[int].connect(previousRange.setValue)

                previousRange = lcdRange


#------------------------------------------------------------------------------

app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())
