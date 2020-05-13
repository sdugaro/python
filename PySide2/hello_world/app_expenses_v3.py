import sys

# This decorator supposedly makes connections faster as its explicit
# Probably not really noticable until there are many or threaded
# Still a good way to distinguish class methods that are signal callacks
#from PySide2.QtCore import Slot

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)

#------------------------------------------------------------------------------


class MyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.items = 0

        # Example data
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                      "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
                      "Public transportation": 60.0, "Coffee": 22.45,
                      "Restaurants": 120}

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # QWidget Layout
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.table)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Fill example data when the widget is constructed
        self.fill_table()

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(price)))
            self.items += 1

#------------------------------------------------------------------------------


class MainWindow(QMainWindow):

    def __init__(self, widget):
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

        self.setCentralWidget(widget)

    #@Slot()
    def _app_exit(self):
        QApplication.quit()


#------------------------------------------------------------------------------


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)

    widget = MyWidget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())

