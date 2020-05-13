# -*- coding: utf-8 -*-

# 
#  % pyside2-uic mixer.ui > ui_mixer.py
#  

################################################################################
## Form generated from reading UI file 'mixer.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MargaritaMixer(object):
    def setupUi(self, MargaritaMixer):
        if MargaritaMixer.objectName():
            MargaritaMixer.setObjectName(u"MargaritaMixer")
        MargaritaMixer.resize(536, 368)
        self.gridLayout = QGridLayout(MargaritaMixer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(MargaritaMixer)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(MargaritaMixer)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.tripleSecSpinBox = QSpinBox(MargaritaMixer)
        self.tripleSecSpinBox.setObjectName(u"tripleSecSpinBox")
        self.tripleSecSpinBox.setMaximum(11)
        self.tripleSecSpinBox.setValue(4)

        self.gridLayout.addWidget(self.tripleSecSpinBox, 1, 2, 1, 1)

        self.label_3 = QLabel(MargaritaMixer)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.limeJuiceLineEdit = QLineEdit(MargaritaMixer)
        self.limeJuiceLineEdit.setObjectName(u"limeJuiceLineEdit")

        self.gridLayout.addWidget(self.limeJuiceLineEdit, 2, 1, 1, 2)

        self.label_4 = QLabel(MargaritaMixer)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.iceHorizontalSlider = QSlider(MargaritaMixer)
        self.iceHorizontalSlider.setObjectName(u"iceHorizontalSlider")
        self.iceHorizontalSlider.setMinimum(0)
        self.iceHorizontalSlider.setMaximum(20)
        self.iceHorizontalSlider.setValue(12)
        self.iceHorizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.iceHorizontalSlider, 3, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(MargaritaMixer)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.tequilaScrollBar = QScrollBar(MargaritaMixer)
        self.tequilaScrollBar.setObjectName(u"tequilaScrollBar")
        self.tequilaScrollBar.setEnabled(True)
        self.tequilaScrollBar.setMaximum(11)
        self.tequilaScrollBar.setValue(8)
        self.tequilaScrollBar.setSliderPosition(8)
        self.tequilaScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.tequilaScrollBar, 0, 1, 1, 2)

        self.groupBox = QGroupBox(MargaritaMixer)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.speedButton1 = QRadioButton(self.groupBox)
        self.speedButtonGroup = QButtonGroup(MargaritaMixer)
        self.speedButtonGroup.setObjectName(u"speedButtonGroup")
        self.speedButtonGroup.addButton(self.speedButton1)
        self.speedButton1.setObjectName(u"speedButton1")

        self.gridLayout_2.addWidget(self.speedButton1, 0, 0, 1, 1)

        self.speedButton3 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton3)
        self.speedButton3.setObjectName(u"speedButton3")

        self.gridLayout_2.addWidget(self.speedButton3, 0, 2, 1, 1)

        self.speedButton4 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton4)
        self.speedButton4.setObjectName(u"speedButton4")

        self.gridLayout_2.addWidget(self.speedButton4, 1, 0, 1, 1)

        self.speedButton5 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton5)
        self.speedButton5.setObjectName(u"speedButton5")
        self.speedButton5.setChecked(True)

        self.gridLayout_2.addWidget(self.speedButton5, 1, 1, 1, 1)

        self.speedButton6 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton6)
        self.speedButton6.setObjectName(u"speedButton6")

        self.gridLayout_2.addWidget(self.speedButton6, 1, 2, 1, 1)

        self.speedButton9 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton9)
        self.speedButton9.setObjectName(u"speedButton9")

        self.gridLayout_2.addWidget(self.speedButton9, 3, 2, 1, 1)

        self.speedButton8 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton8)
        self.speedButton8.setObjectName(u"speedButton8")

        self.gridLayout_2.addWidget(self.speedButton8, 3, 1, 1, 1)

        self.speedButton7 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton7)
        self.speedButton7.setObjectName(u"speedButton7")

        self.gridLayout_2.addWidget(self.speedButton7, 3, 0, 1, 1)

        self.speedButton2 = QRadioButton(self.groupBox)
        self.speedButtonGroup.addButton(self.speedButton2)
        self.speedButton2.setObjectName(u"speedButton2")

        self.gridLayout_2.addWidget(self.speedButton2, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 4, 0, 1, 3)

        QWidget.setTabOrder(self.buttonBox, self.tripleSecSpinBox)
        QWidget.setTabOrder(self.tripleSecSpinBox, self.limeJuiceLineEdit)
        QWidget.setTabOrder(self.limeJuiceLineEdit, self.iceHorizontalSlider)
        QWidget.setTabOrder(self.iceHorizontalSlider, self.speedButton1)
        QWidget.setTabOrder(self.speedButton1, self.speedButton2)
        QWidget.setTabOrder(self.speedButton2, self.speedButton3)

        self.retranslateUi(MargaritaMixer)
        self.buttonBox.accepted.connect(MargaritaMixer.accept)
        self.buttonBox.rejected.connect(MargaritaMixer.reject)

        QMetaObject.connectSlotsByName(MargaritaMixer)
    # setupUi

    def retranslateUi(self, MargaritaMixer):
        MargaritaMixer.setWindowTitle(QCoreApplication.translate("MargaritaMixer", u"Margarita Mixer", None))
        self.label.setText(QCoreApplication.translate("MargaritaMixer", u"Tequila", None))
        self.label_2.setText(QCoreApplication.translate("MargaritaMixer", u"Triple Sec", None))
#if QT_CONFIG(tooltip)
        self.tripleSecSpinBox.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Jiggers of triple sec", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MargaritaMixer", u"Lime Juice", None))
#if QT_CONFIG(tooltip)
        self.limeJuiceLineEdit.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Jiggers of lime juice", None))
#endif // QT_CONFIG(tooltip)
        self.limeJuiceLineEdit.setText(QCoreApplication.translate("MargaritaMixer", u"12.0", None))
        self.label_4.setText(QCoreApplication.translate("MargaritaMixer", u"Ice", None))
#if QT_CONFIG(tooltip)
        self.iceHorizontalSlider.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Chunks of ice", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.buttonBox.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Press OK to make the drinks", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.tequilaScrollBar.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Jiggers of tequila", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox.setToolTip(QCoreApplication.translate("MargaritaMixer", u"Speed of the blender", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("MargaritaMixer", u"Blender Speed", None))
        self.speedButton1.setText(QCoreApplication.translate("MargaritaMixer", u"&Mix", None))
        self.speedButton3.setText(QCoreApplication.translate("MargaritaMixer", u"&Puree", None))
        self.speedButton4.setText(QCoreApplication.translate("MargaritaMixer", u"&Chop", None))
        self.speedButton5.setText(QCoreApplication.translate("MargaritaMixer", u"&Karate Chop", None))
        self.speedButton6.setText(QCoreApplication.translate("MargaritaMixer", u"&Beat", None))
        self.speedButton9.setText(QCoreApplication.translate("MargaritaMixer", u"&Vaporize", None))
        self.speedButton8.setText(QCoreApplication.translate("MargaritaMixer", u"&Liquefy", None))
        self.speedButton7.setText(QCoreApplication.translate("MargaritaMixer", u"&Smash", None))
        self.speedButton2.setText(QCoreApplication.translate("MargaritaMixer", u"&Whip", None))
    # retranslateUi

