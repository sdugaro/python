import sys

# This decorator supposedly makes connections faster as its explicit
# Probably not really noticable until there are many or threaded
# Still a good way to distinguish class methods that are signal callacks
#from PySide2.QtCore import Slot

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QHeaderView,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel

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

        # Widgets
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")

        # Layout
        self.right = QVBoxLayout()
        self.right.setMargin(10)
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Price"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addStretch()
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)

        # Connections
        self.add.clicked.connect(self._add_element)
        self.quit.clicked.connect(self._quit_application)
        self.clear.clicked.connect(self._clear_table)

        # Initialize
        self.fill_table()

    #@Slot()
    def _add_element(self):
        des = self.description.text()
        price = self.price.text()

        self.table.insertRow(self.items)
        self.table.setItem(self.items, 0, QTableWidgetItem(des))
        self.table.setItem(self.items, 1, QTableWidgetItem(price))

        self.description.setText("")
        self.price.setText("")

        self.items += 1

    #@Slot()
    def _quit_application(self):
        QApplication.quit()

    #@Slot()
    def _clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

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

