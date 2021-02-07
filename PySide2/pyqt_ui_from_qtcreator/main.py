#!/usr/bin/env python

import sys, os
# the programs name is always the [0]th command line arg
print(sys.argv)
# dispose of it, and use pyside if any cl arg id provided
sys.argv.pop()

USE_PYSIDE = True if sys.argv else False
# note expressions can be nested in f-strings so we can
# use a ternary operator inside for cleaner debugging
print(f"Using [{'PySide2' if USE_PYSIDE else 'PyQt5'}]")
if USE_PYSIDE:
    from PySide2 import QtWidgets
    from MainWindow2 import Ui_MainWindow
else:
    from PyQt5 import QtWidgets
    from MainWindow import Ui_MainWindow

# instead of using a cl arg to import the qt binding of our
# choice at runtime, we could leverage an environment variable,
# or even attempt to import them in a preferred order in a try
# block failing gracefully and reporting that these required
# libraries are not installed on the system

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()

    # note that in PyQt5 app.exec() and app.exec_() are
    # interchangeable, but this isnt the case in PySide2
    # where exec() will raise an AttributeError
    app.exec_()
