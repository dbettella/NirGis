# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_areadilavoro.ui'
#
# Created: Thu Aug 14 15:54:28 2014
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

class Ui_areadilavoro(object):
    def setupUi(self, areadilavoro):
        areadilavoro.setObjectName(_fromUtf8("areadilavoro"))
        areadilavoro.resize(407, 197)
        self.buttonBox = QtGui.QDialogButtonBox(areadilavoro)
        self.buttonBox.setGeometry(QtCore.QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(areadilavoro)
        self.label.setGeometry(QtCore.QRect(70, 20, 261, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.editDim = QtGui.QLineEdit(areadilavoro)
        self.editDim.setGeometry(QtCore.QRect(150, 70, 113, 27))
        self.editDim.setAlignment(QtCore.Qt.AlignCenter)
        self.editDim.setObjectName(_fromUtf8("editDim"))

        self.retranslateUi(areadilavoro)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), areadilavoro.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), areadilavoro.reject)
        QtCore.QMetaObject.connectSlotsByName(areadilavoro)

    def retranslateUi(self, areadilavoro):
        areadilavoro.setWindowTitle(_translate("areadilavoro", "Definizione dell\'area di lavoro", None))
        self.label.setText(_translate("areadilavoro", "Dimensione dell\'area di lavoro in metri", None))
        self.editDim.setText(_translate("areadilavoro", "250", None))

