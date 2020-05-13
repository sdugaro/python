import sys
from PySide2 import QtCore, QtGui, QtWidgets


class RegExpValidator(QtGui.QRegExpValidator):
    validationChanged = QtCore.Signal(QtGui.QValidator.State)

    def validate(self, input, pos):
        # python > 3
        #state, input, pos = super().validate(input, pos)
        # python < 3
        state, input, pos = super(RegExpValidator, self).validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        regexp = QtCore.QRegExp(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        validator = RegExpValidator(regexp, self)
        validator.validationChanged.connect(self.handleValidationChange)
        self.edit = QtWidgets.QLineEdit()
        self.edit.setValidator(validator)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.edit)

    def handleValidationChange(self, state):
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.edit.setStyleSheet('border: 3px solid %s' % colour)
        QtCore.QTimer.singleShot(1000, lambda: self.edit.setStyleSheet(''))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
