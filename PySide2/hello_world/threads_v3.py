from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import time

#------------------------------------------------------------------------------
# QRunnable - the container for the work you want to perform
#  Subclass this to define a custom QRunnable
#  Place the code to execute within the run() method
# QThreadPool - handles queuing and execution of workers
#
# Hitting the button multiple times should show threads executed immediately
# up to the number reported by .maxThreadCount. any more than this will be
# queued until more threads become available
#


class Worker(QRunnable):
    '''
    Worker thread
    '''

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        time.sleep(5)
        print("Thread complete")


class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        # Manage a pool of threads to feed QRunnables
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

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
        worker = Worker()
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l_start.setText("Counter: %d" % self.counter)


#------------------------------------------------------------------------------

app = QApplication([])
window = MainWindow()
app.exec_()

