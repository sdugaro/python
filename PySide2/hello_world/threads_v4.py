from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import time

#------------------------------------------------------------------------------
# Passing custom data into the execution function is done via __init__()
# in the QRunnable Worker Class


class Worker(QRunnable):
    '''
    Worker thread

    :param args: Arguments to make available to the run code
    :param kwargs: Keywords arguments to make available to the run code

    '''

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed self.args, self.kwargs.
        '''
        print(self.args, self.kwargs)
        print("Thread start")
        time.sleep(5)
        print("Thread complete")


class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        self.thread_count = 0

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
        self.thread_count += 1
        worker = Worker("one", 1, {'one': 1}, name="uno", num_threads=self.thread_count)
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l_start.setText("Counter: %d" % self.counter)


#------------------------------------------------------------------------------

app = QApplication([])
window = MainWindow()
app.exec_()

