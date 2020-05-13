import sys
import random

from PySide2 import QtWidgets, QtGui, QtCore

#------------------------------------------------------------------------------
# Object/Worker Thread Example using QObject.moveTothread()
# QtCore provides core infrastucture for Qt, it does not have any dependencies
#     on ui resources. It can be used for client server type programs
# QtGui extends QtCore with GUI functionality to abstract the qt framework
#     in so far as all base classes for GUI components including OpenGL
# QtWidgets is a UI module that leverages QtCore and QtGui for hi level UI
#     components such as buttons to create classic desktop-style UI,.


class Example(QtCore.QObject):
    """ Example """

    signalStatus = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # Create a gui object.
        self.gui = Window()

        # Create a new worker thread.
        self.createWorkerThread()

        # Make any cross object connections.
        self._connectSignals()

        self.gui.show()


    def _connectSignals(self):
        self.gui.button_cancel.clicked.connect(self.forceWorkerReset)
        self.signalStatus.connect(self.gui.updateStatus)
        self.parent().aboutToQuit.connect(self.forceWorkerQuit)


    def createWorkerThread(self):

        # Setup the worker object and the worker_thread.
        self.worker = WorkerObject()
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # Connect any worker signals to update gui
        self.worker.signalStatus.connect(self.gui.updateStatus)
        self.gui.button_start.clicked.connect(self.worker.startWork)


    def forceWorkerReset(self):
        if self.worker_thread.isRunning():
            print('Terminating thread.')
            self.worker_thread.terminate()

            print('Waiting for thread termination.')
            self.worker_thread.wait()

            self.signalStatus.emit('Idle.')

            print('building new working object.')
            self.createWorkerThread()


    def forceWorkerQuit(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


class WorkerObject(QtCore.QObject):
    """ Worker Object dispatched into its own thread """

    signalStatus = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @QtCore.Slot()
    def startWork(self):
        for ii in range(7):
            number = random.randint(0, 5000**ii)
            self.signalStatus.emit('Iteration: {}, Factoring: {}'.format(ii, number))
            factors = self.primeFactors(number)
            print('Number: ', number, 'Factors: ', factors)
        self.signalStatus.emit('Idle.')

    def primeFactors(self, n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors


class Window(QtWidgets.QWidget):
    """ Qt Gui harnessed in the main Thread (example) Object
    along with the QThread instance in which the heavy compute
    (worker) gets dispatched
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.button_start = QtWidgets.QPushButton('Start', self)
        self.button_cancel = QtWidgets.QPushButton('Cancel', self)
        self.label_status = QtWidgets.QLabel('', self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_cancel)
        layout.addWidget(self.label_status)

        self.setFixedSize(400, 200)

    @QtCore.Slot(str)
    def updateStatus(self, status):
        """ refresh the progress of the worker thread which emits data
        on each of its iterations via its signalStatus signal. Notice
        that the parent thread ALSO has a signalStatus connected to
        this updateStatus, which ALSO provides a string to display.
        Notice that the GUI logic is maintained in the main managing
        QObject Thread, which also manages the heavier child thread.
        """
        self.label_status.setText(status)


#------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    example = Example(app)
    sys.exit(app.exec_())
