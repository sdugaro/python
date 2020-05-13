import sys
import time

from PySide2.QtCore import (
    QCoreApplication, QObject, Signal,
    QRunnable, QThread, QThreadPool
)

#------------------------------------------------------------------------------
# Subclassing QThread
# https://doc.qt.io/qt-5/qthread.html
# Override the default implementation of QThread.run():
# The thread will exit after the run function has returned.
# There will not be any event loop running in the thread unless you call exec()
# The QThread instance lives in the thread that instantiated it, not in the new
# thread that invokes run(). This means all of QThreads methods/queued slots
# will execute in the parent thread. The run() method will be the only one in
# the calss that will actually run in another thread. New Slots should NOT be
# implemented in a subclassed QThread
# The constructor executes in the old thread while run() will execute in the
# new thread. If a member variable is accessed from inside of run as well as
# other subclassed methods, then the variable is accessed from two different
# threads, and one needs to check that it is safe to do so. The run() method will be the
# only one in the class that will actually run on another thread. Any other
# subclass method or functino calls inside run() will run from the main thread.


class AThread(QThread):

    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("A Increasing")
            count += 1


def using_q_thread():
    app = QCoreApplication([])
    thread = AThread()
    thread.setObjectName("Subclassed QThread")
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

#------------------------------------------------------------------------------
# Subclassing QObject and using moveToThread
# moveToThread() is used to control the objects thread affinty: setting the
# thread (NEW Qt event loop) from which the object will emit signals
#
# A worker object is created, and it is 'moved' to a new thread in the app
# The worker object emits a signal when its done (finished) and this event
# is listened for to quit the thread and the app
# The Threads started signal is connected to the workers 'run' function
# which begins executing when the Thread is started programatically
#
# Note that once the do_work() slot has started, the whole (new) event loop
# will be busy until it exits; meaning any incoming signals will be queued


class SomeObject(QObject):

    finished = Signal()

    def do_work(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("B Increasing")
            count += 1
        self.finished.emit()


def using_move_to_thread():
    app = QCoreApplication([])
    objThread = QThread()
    objThread.setObjectName("Move To Thread")
    obj = SomeObject()
    obj.moveToThread(objThread)
    obj.finished.connect(objThread.quit)
    objThread.started.connect(obj.do_work)
    objThread.finished.connect(app.exit)
    objThread.start()
    sys.exit(app.exec_())

#------------------------------------------------------------------------------
# Using a QRunnable
# http://qt-project.org/doc/latest/qthreadpool.html
# Each Qt application has one global QThreadpool object to reduce thread
# creation costs in programs that use threads. To use a QThreadPool you
# need to subclass a QRunnable, implement run() and pass the object
# instance to the QThreadPool.start().


class Runnable(QRunnable):

    def run(self):
        count = 0
        app = QCoreApplication.instance()
        while count < 5:
            print("C Increasing")
            time.sleep(1)
            count += 1
        app.quit()


def using_q_runnable():
    app = QCoreApplication([])
    runnable = Runnable()
    QThreadPool.globalInstance().start(runnable)
    sys.exit(app.exec_())


#------------------------------------------------------------------------------

if __name__ == "__main__":
    #using_q_thread()
    #using_move_to_thread()
    using_q_runnable()
