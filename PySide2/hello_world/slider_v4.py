#!/usr/bin/env python

import sys
from PySide2 import QtCore, QtGui, QtWidgets

#------------------------------------------------------------------------------


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        lcd = QtWidgets.QLCDNumber(2)

        # slider has a keyboard interface: arrows/home/end/pgup/pgdn
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.slider.valueChanged[int].connect(lcd.display)
        self.slider.valueChanged[int].connect(self.valueChanged)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        # set this widget to have its focus on the slider, not the indicator
        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)

    # Allow for range to be configured programmatically
    # qWarning, like a printf, sends its output to stderr
    def setRange(self, minValue, maxValue):
        if minValue < 0 or maxValue > 99 or minValue > maxValue:
            QtCore.qWarning(
                "LCDRange.setRange(%d, %d)\n"
                "\tRange must be 0..99\n\tand minValue must not be "
                "greater than maxValue" % (minValue, maxValue)
            )
            return

        self.slider.setRange(minValue, maxValue)


# A Custom Widget that can paint/display itself
# Emit the angleChanged signal to tell the outside world the angle changed
# We only emit the signal when the angle has actually changed and then
# update/repaint the widget accordingly
class CannonField(QtWidgets.QWidget):

    # Class Variable Signal
    angleChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.currentAngle = 45
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)  # use other colors suitably

    def angle(self):
        return self.currentAngle

    @QtCore.Slot(int)
    def setAngle(self, angle):
        if angle < 5:
            angle = 5
        if angle > 70:
            angle = 70
        if self.currentAngle == angle:
            return
        self.currentAngle = angle
        self.update()

        # OLD Style
        #self.emit(QtCore.SIGNAL("angleChanged(int)"), self.currentAngle)
        # NEW Style - instance variable Signal/Slot
        self.angleChanged.emit(self.currentAngle)

    # one of many event handler in QWidget; a virtual function called
    # by QT whenever a widget needs to update() itself (refresh/paint)
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter_text = "Angle = {}".format(self.currentAngle)
        painter.drawText(event.rect(), QtCore.Qt.AlignCenter, painter_text)


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Widgets
        quit = QtWidgets.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        quit.clicked.connect(QtWidgets.QApplication.quit)

        angle = LCDRange()
        angle.setRange(5, 70)  # programmatic w/ shell warning
        angle.setValue(60)
        angle.setFocus()

        field = CannonField()

        # Connections
        angle.valueChanged.connect(field.setAngle)
        field.angleChanged.connect(angle.setValue)


        # Layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(quit, 0, 0)
        grid.addWidget(angle, 1, 0)
        grid.addWidget(field, 1, 1, 2, 1)
        grid.setColumnStretch(1, 10)
        # stretch factor biases the column resizing
        # alternatively add spacing with addItem QSpacerItem
        #grid.setColumnStretch(0, 50)

        self.setLayout(grid)


#------------------------------------------------------------------------------

app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec_())
