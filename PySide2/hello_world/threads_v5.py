from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import time

#------------------------------------------------------------------------------
# Passing custom data into the execution function is done via __init__()
# Since Python function are objects, they can be passed in like any other arg


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.name = args[0]
        self.num = kwargs["thread_num"]

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)


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

    def execute_this_fn(self, *args, **kwargs):
        print("MAIN WINDOW CALLBACK FROM WORKER: Total Threads = [{}]"
              "".format(self.thread_count))
        print("  ARGS:", args)
        print("KWARGS:", kwargs)
        print("Sleeping...")
        time.sleep(1)
        # Unpack args and kwargs into string format
        print("{0} Thread#{thread_num} Done.".format(*args, **kwargs))


    def oh_no(self):
        self.thread_count += 1
        # pass a callback function to be executed by the worker
        worker = Worker(self.execute_this_fn,
                        "Thread{}".format(self.thread_count),
                        thread_num=self.thread_count)
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l_start.setText("Counter: %d" % self.counter)


#------------------------------------------------------------------------------

app = QApplication([])
window = MainWindow()
app.exec_()

