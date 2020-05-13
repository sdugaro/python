import sys

# This decorator supposedly makes connections faster as its explicit
# Probably not really noticable until there are many or threaded
#from PySide2.QtCore import Slot

from PySide2.QtWidgets import QApplication, QMainWindow, QAction


#------------------------------------------------------------------------------
# PEP8 Classes are 'CamelCase'

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        # QMainWindow has a menu bar, to use it you
        # need to call the method and populate it
        action_exit = QAction("Exit", self)
        action_exit.setShortcut("^+Q")
        action_exit.triggered.connect(self._app_exit)

        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        self.menu_file.addAction(action_exit)

    # PEP8: everything else including class methods are 'snake_case'
    # all lowercase, separate words with _, non-public methods start with _
    #@Slot()
    def _app_exit(self):
        QApplication.quit()


#------------------------------------------------------------------------------


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())

