#!/usr/bin/python

import sys
from PySide2.QtCore import Slot, Signal, QObject

#------------------------------------------------------------------------------
# Object Method Emitting a Signal; Must Inherit QObject


class Communicate(QObject):

    speak = Signal((int,), (str,))

    def __init__(self):
        super(Communicate, self).__init__()
        self.speak[int].connect(self.say_something)
        self.speak[str].connect(self.say_something)

    @Slot(int)
    @Slot(str)
    def say_something(self, something):
        print(something)

    def speaking(self, something):
        if isinstance(something, str):
            self.speak[str].emit(something)
        elif isinstance(something, int):
            self.speak[int].emit(something)

#------------------------------------------------------------------------------


someone = Communicate()
someone.speaking("Hello World!")
someone.speaking(45)

