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
class Communicate(QObject):
    speak_num = Signal(int)
    speak_word = Signal(str)


#------------------------------------------------------------------------------


app = QApplication(sys.argv)

someone = Communicate()
someone.speak_num.connect(say_something)
someone.speak_word.connect(say_something)

someone.speak_num.emit(87)
someone.speak_word.emit("Hello World!")

# do not want to engage the PyQt event loop
#sys.exit(app.exec_())
