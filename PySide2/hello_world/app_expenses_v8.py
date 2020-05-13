import sys

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt, QRegExp, Signal, Slot
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QHeaderView,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel
)
from PySide2.QtGui import (
    QDoubleValidator, QRegExpValidator, QValidator, QPainter
)

#------------------------------------------------------------------------------


class MyRegExpValidator(QRegExpValidator):
    # create a signal which we can connect to a slot
    validationChanged = Signal(QValidator.State)

    def validate(self, input, pos):
        #state, input, pos = super().validate(input, pos)  # python > 3
        state, input, pos = super(MyRegExpValidator, self).validate(input, pos)
        print state, input, pos
        self.validationChanged.emit(state)
        return state, input, pos

#------------------------------------------------------------------------------


class MyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self._items = 0
        self._valid_descr = False
        self._valid_price = False

        # Example data
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                      "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
                      "Public transportation": 60.0, "Coffee": 22.45,
                      "Restaurants": 120}

        #----------------------------------------------------------------------
        # Validators - block user input

        regex_descr = QRegExp("[A-Za-z- _]+")
        regex_price = QRegExp("\\d+(\\.\\d{1,2})?$")  # escape \ for binding
        self._validator_descr = MyRegExpValidator(regex_descr)
        self._validator_price = MyRegExpValidator(regex_price)

        #----------------------------------------------------------------------
        # Widgets

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.description = QLineEdit()
        self.description.setPlaceholderText("Some Description")
        self.description.setValidator(self._validator_descr)

        self.price = QLineEdit()
        self.price.setPlaceholderText("99.99")
        self.price.setValidator(self._validator_price)

        self.chart_view = QtCharts.QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.plot = QPushButton("Plot")
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
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
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
        self.plot.clicked.connect(self._plot_data)
        self._validator_descr.validationChanged.connect(self._validator)
        self._validator_price.validationChanged.connect(self._validator)

        #----------------------------------------------------------------------
        # Initialize

        self.fill_table()
        self.add.setEnabled(False)

    @Slot()
    def _validator(self, state):

        if state == QValidator.Invalid:
            colour = 'red'
            colour = '#F6989D'
        elif state == QValidator.Intermediate:
            colour = 'gold'
            colour = '#FFF79A'
        elif state == QValidator.Acceptable:
            colour = 'lime'
            colour = '#C4DF9B'

        sender = self.sender()  # identify the sender of the signal
        fmt_validated = 'QLineEdit {{ border: 2px solid {0} }}'.format(colour)
        validator_fmt = 'QLineEdit {{ background-color: {0} }}'.format(colour)
        if sender is self._validator_price:
            self.price.setStyleSheet(validator_fmt)
            self._valid_price = (False, True)[state == QValidator.Acceptable]
        elif sender is self._validator_descr:
            self.description.setStyleSheet(validator_fmt)
            self._valid_descr = (False, True)[state == QValidator.Acceptable]

        self.add.setEnabled(False)
        has_price = self.price.text().strip()
        has_descr = self.description.text().strip()
        if self._valid_descr and has_descr and \
           self._valid_price and has_price:
            self.add.setEnabled(True)

    @Slot()
    def _add_element(self):
        des = self.description.text()
        price = self.price.text()

        self.table.insertRow(self._items)
        self.table.setItem(self._items, 0, QTableWidgetItem(des))
        self.table.setItem(self._items, 1, QTableWidgetItem(price))

        self.description.setText("")
        self.price.setText("")

        self._items += 1

    @Slot()
    def _quit_application(self):
        QApplication.quit()

    @Slot()
    def _clear_table(self):
        self.table.setRowCount(0)
        self._items = 0

    @Slot()
    def _plot_data(self):
        series = QtCharts.QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, price in data.items():
            self.table.insertRow(self._items)
            self.table.setItem(self._items, 0, QTableWidgetItem(desc))
            self.table.setItem(self._items, 1, QTableWidgetItem(str(price)))
            self._items += 1

#------------------------------------------------------------------------------


class MainWindow(QMainWindow):

    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        # QMainWindow has a menu bar, to use it you need to get the
        # Qt object via the class method and populate the object
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

    app = QApplication(sys.argv)

    widget = MyWidget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())

