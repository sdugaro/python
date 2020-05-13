from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import time

#------------------------------------------------------------------------------
# Boiler plate of some code that takes awhile to process 


class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.l_start = QLabel("Start")
        b_danger = QPushButton("DANGER!")
        b_danger.pressed.connect(self.oh_no)

        layout.addWidget(self.l_start)
        layout.addWidget(b_danger)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        time.sleep(5)
        # Intermittedly processEvents() where there is a lot of work happening
        # This passes control back to QT, allowing it to respond to events as
        # normal. It will make the UI a touch more responsive as OS windowing
        # events are flushed so that work can return to the QT Event Loop
        #for n in range(5):
        #    QApplication.processEvents()
        #    time.sleep(1)

    def recurring_timer(self):
        self.counter += 1
        self.l_start.setText("Counter: %d" % self.counter)


#------------------------------------------------------------------------------

app = QApplication([])
window = MainWindow()
app.exec_()

