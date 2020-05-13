
import sys
import urllib2

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

#------------------------------------------------------------------------------
# QtWidgets are not thread sage and should not be accessed from any thread
# but the main thread. The correct waqy to use threads is via signals/slots.
# This separates the threading (network logic) from the display logic (gui)
# ie. you CANNOT call QListWidget.addItem() from a thread
#
# QRunnable::run() is well suited to performing some backround processing
# in one or more secondary threads without the need for an event loop.
# it has no built-in means of explicitly communicated something to other
# components, which you would need to code by hand with low-level threading
# primitives (ie mutex guarded queue to collect results)
# In other words, QRunnable ISNT a subclas of QObject, so it does not
# provide signals and slots
#
# QThread can run and event loop, and provides thread safe signals and slots


# Worker Thread
class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.Signal(object)

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        # initialize where the work is to be done
        self.url = url

    def run(self):
        # do the work, ie download some data from the initialized url
        info = urllib2.urlopen(self.url).info()
        # once we get it, emit a signal about it along with some data
        self.data_downloaded.emit('%s\n%s' % (self.url, info))


# Main GUI Thread
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtWidgets.QListWidget()
        self.button = QtWidgets.QPushButton("Start")
        self.button.clicked.connect(self.start_download)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def start_download(self):
        urls = ['http://google.com', 'http://twitter.com', 'http://yandex.ru',
                'http://stackoverflow.com/', 'http://www.youtube.com/']

        self.threads = []
        for url in urls:
            # create a worker thread
            downloader = DownloadThread(url)
            # connect the workers 'done' signal to a gui handler
            downloader.data_downloaded.connect(self.on_data_ready)
            # track the threads
            self.threads.append(downloader)
            # execute the thread
            downloader.start()

    def on_data_ready(self, data):
        print data
        self.list_widget.addItem(unicode(data))


#------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
