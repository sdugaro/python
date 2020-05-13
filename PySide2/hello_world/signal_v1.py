#!/usr/bin/python

import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Slot, Signal, QObject

#------------------------------------------------------------------------------
# Overloaded Slot

@Slot(str)
def say_something(something):
    print(something)


# Signal handlder
class Communicate(QObject):
    speak = Signal(str)


#------------------------------------------------------------------------------


app = QApplication(sys.argv)

someone = Communicate()
someone.speak.connect(say_something)
someone.speak.emit("Hello World!")

# do not want to engage the PyQt event loop
#sys.exit(app.exec_())
