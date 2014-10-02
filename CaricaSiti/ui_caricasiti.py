# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_caricasiti.ui'
#
# Created: Mon Aug  4 18:14:19 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CaricaSiti(object):
    def setupUi(self, CaricaSiti):
        CaricaSiti.setObjectName(_fromUtf8("CaricaSiti"))
        CaricaSiti.resize(420, 211)
        self.buttonBox = QtGui.QDialogButtonBox(CaricaSiti)
        self.buttonBox.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.cb_prov = QtGui.QComboBox(CaricaSiti)
        self.cb_prov.setGeometry(QtCore.QRect(40, 100, 91, 27))
        self.cb_prov.setObjectName(_fromUtf8("cb_prov"))
        self.cb_comune = QtGui.QComboBox(CaricaSiti)
        self.cb_comune.setGeometry(QtCore.QRect(170, 100, 211, 27))
        self.cb_comune.setObjectName(_fromUtf8("cb_comune"))
        self.label = QtGui.QLabel(CaricaSiti)
        self.label.setGeometry(QtCore.QRect(50, 70, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(CaricaSiti)
        self.label_2.setGeometry(QtCore.QRect(180, 70, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(CaricaSiti)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 331, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(CaricaSiti)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CaricaSiti.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CaricaSiti.reject)
        QtCore.QMetaObject.connectSlotsByName(CaricaSiti)

    def retranslateUi(self, CaricaSiti):
        CaricaSiti.setWindowTitle(_translate("CaricaSiti", "CaricaSiti", None))
        self.label.setText(_translate("CaricaSiti", "Provincia", None))
        self.label_2.setText(_translate("CaricaSiti", "Comune", None))
        self.label_3.setText(_translate("CaricaSiti", "Selezionare una Provincia e poi un comune", None))

