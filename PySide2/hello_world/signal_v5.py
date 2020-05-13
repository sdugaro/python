#!/usr/bin/python

import sys
from PySide2.QtCore import Slot, Signal, QObject, QThread

#------------------------------------------------------------------------------
# Emit a Signal from another thread
# Signals are runtime objects owned by instances
# Signals are NOT class attributes


@Slot(int)
def update_int_field(value):
    print(value)


@Slot(str)
def update_str_field(something):
    print(something)


# Create 2 new signals on the fly; each handling the different types
# How the new style array definitions are managed; all inline
# This can be done
class Communicate(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)


class WorkerThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.signals = Communicate()

        # connect the signals tothe main threads slots
        self.signals.signal_str.connect(update_str_field)
        self.signals.signal_int.connect(update_int_field)

    def run(self):
        self.signals.signal_int.emit(8763)
        self.signals.signal_str.emit("Hello World")

#------------------------------------------------------------------------------


#app = QApplication(sys.argv)

thread = WorkerThread()
thread.run()

# do not want to engage the PyQt event loop
#sys.exit(app.exec_())
