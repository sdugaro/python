
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import time

#------------------------------------------------------------------------------
# processEvents() can return control back to Qt to accept more events while
# we have a heavy logic block churning away. Sensible for progress bars,
# that eventually refresh the interface, but:
# 1. when th control is passed back to QT/host, 'long logic' is no longer
#    running which means Gui will stick less, bt 'long logic' will take longer
# 2. As illustrated here, accepting events while a process is running could
#    put your app in an ambiguous state which is bad if code depends on or
#    responds to this switchy state.
#
# ie. pressing ? while oh_no is still running changes the message, indicating
# that the state of the app is being changed from OUTSIDE the loop. This gets
# more unpredictable when there are multiple long running processes
# THEREFORE THIS IS NOT A GOOD ALTERNATIVE TO THREADS


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Widgets

        self.l_start = QLabel("Start")  # instance variable as we are using elsewhere
        b_danger = QPushButton("DANGER!")
        b_danger.pressed.connect(self.oh_no)
        b_what = QPushButton("?")
        b_what.pressed.connect(self.change_message)

        layout = QVBoxLayout()
        layout.addWidget(self.l_start)
        layout.addWidget(b_danger)
        layout.addWidget(b_what)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        self.show()

    def change_message(self):
        self.message = "OH NO"

    def oh_no(self):
        self.message = "Pressed"

        for n in range(100):
            time.sleep(0.1)
            self.l_start.setText(self.message)
            QApplication.processEvents()


#------------------------------------------------------------------------------

app = QApplication([])
window = MainWindow()
app.exec_()
