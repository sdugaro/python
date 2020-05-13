#!/usr/bin/python

import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Slot, Signal, QObject

#------------------------------------------------------------------------------
# Overloaded Slot


@Slot(int)
@Slot(str)
def say_something(something):
    print(something)


# Create 2 new signals on the fly; each handling the different types
# How the new style array definitions are managed; all inline
# This can be done
class Communicate(QObject):
    speak = Signal((int,), (str,))

#------------------------------------------------------------------------------


app = QApplication(sys.argv)

someone = Communicate()
someone.speak.connect(say_something)
someone.speak[str].connect(say_something)

someone.speak.emit(87)
someone.speak[str].emit("Hello World!")

# do not want to engage the PyQt event loop
#sys.exit(app.exec_())
