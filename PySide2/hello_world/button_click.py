#!/usr/bin/python

import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Slot

#------------------------------------------------------------------------------


@Slot()
def say_hello():
    print("Button clicked, Hello!")

#------------------------------------------------------------------------------


app = QApplication(sys.argv)

button = QPushButton("Click me")
button.clicked.connect(say_hello)
button.show()

# Run the main Qt loop, propogate any error code to parent process
# app.exec_() returns an exit code, non-zero indicating an error
# This can tell the parent process (ie shell) if everyting ran ok
# Probably more meaningful for QCoreApplication (batched app)
sys.exit(app.exec_())
