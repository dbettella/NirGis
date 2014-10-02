# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_connect.ui'
#
# Created: Fri Aug  8 13:00:51 2014
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

class Ui_ConnectDialog(object):
    def setupUi(self, ConnectDialog):
        ConnectDialog.setObjectName(_fromUtf8("ConnectDialog"))
        ConnectDialog.resize(468, 135)
        self.centralwidget = QtGui.QWidget(ConnectDialog)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 70, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 30, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        ConnectDialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(ConnectDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectDialog)

    def retranslateUi(self, ConnectDialog):
        ConnectDialog.setWindowTitle(_translate("ConnectDialog", "MainWindow", None))
        self.label_2.setText(_translate("ConnectDialog", "dal Data Base Etere", None))
        self.label.setText(_translate("ConnectDialog", "Collegamento e trasferimento dati", None))

