import sys

# This decorator supposedly makes connections faster as its explicit
# Probably not really noticable until there are many or threaded
# Still a good way to distinguish class methods that are signal callacks
#from PySide2.QtCore import Slot

from PySide2.QtCore import QRegExp, Signal
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QHeaderView,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel
)
from PySide2.QtGui import QDoubleValidator, QRegExpValidator, QValidator

#------------------------------------------------------------------------------


class RegExpValidator(QRegExpValidator):
    # create a signal which we can connect to a slot
    validationChanged = Signal(QValidator.State)

    def validate(self, input, pos):
        #state, input, pos = super().validate(input, pos) # python > 3
        state, input, pos = super(RegExpValidator, self).validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos

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

        #----------------------------------------------------------------------
        # Validators - block user input

        regex = QRegExp("[A-Za-z- _]+")
        validator_desc = QRegExpValidator(regex)
        validator_price = QDoubleValidator(0, 99999999, 2)
        validator_price.setNotation(QDoubleValidator.StandardNotation)  # no e

        #----------------------------------------------------------------------
        # Widgets

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.description = QLineEdit()
        self.description.setPlaceholderText("Some Description")
        self.description.setValidator(validator_desc)

        self.price = QLineEdit()
        self.price.setPlaceholderText("99.99")
        self.price.setValidator(validator_price)

        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")

        #----------------------------------------------------------------------
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

        #----------------------------------------------------------------------
        # Connections

        self.add.clicked.connect(self._add_element)
        self.quit.clicked.connect(self._quit_application)
        self.clear.clicked.connect(self._clear_table)
        self.description.textChanged[str].connect(self._validate)
        self.price.textChanged[str].connect(self._validate)

        #----------------------------------------------------------------------
        # Initialize

        self.fill_table()
        self.add.setEnabled(False)

    #@Slot()
    def _validate(self, state):
        sender = self.sender()  # identify the sender of the signal
        validator = sender.validator()  # may not always have one
        state = validator.validate(sender.text(), 0)[0]
        print(state)
        # (PySide2.QtGui.QValidator.State.Acceptable, u'Some', 0)
        # The only way QLineEdit can be in an Invalid State is if the text is
        # changed programmatically. Validators block the user from entering
        # undesirable values at all. We color just for fun

        sender.setStyleSheet('')
        if state == QValidator.Acceptable:
            colour = 'lime'
            colour = '#C4DF9B'
        elif state == QValidator.Intermediate:
            colour = 'gold'
            colour = '#FFF79A'
        else:
            colour = 'red'
            colour = '#F6989D'

        fmt_validated = 'QLineEdit {{ background-color: {0} }}'.format(colour)
        fmt_validated = 'QLineEdit {{ border: 2px solid {0} }}'.format(colour)
        sender.setStyleSheet(fmt_validated)

        has_price = self.price.text().strip()
        has_description = self.description.text().strip()
        if not has_price or not has_description:
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

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

