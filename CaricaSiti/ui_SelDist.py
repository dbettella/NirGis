# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_SelDist.ui'
#
# Created: Fri Aug  8 09:55:12 2014
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

class Ui_SelDist(object):
    def setupUi(self, SelDist):
        SelDist.setObjectName(_fromUtf8("SelDist"))
        SelDist.resize(400, 219)
        self.buttonBox = QtGui.QDialogButtonBox(SelDist)
        self.buttonBox.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(SelDist)
        self.label.setGeometry(QtCore.QRect(90, 20, 201, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(SelDist)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 321, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.layoutWidget = QtGui.QWidget(SelDist)
        self.layoutWidget.setGeometry(QtCore.QRect(110, 100, 182, 29))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.dst = QtGui.QLineEdit(self.layoutWidget)
        self.dst.setObjectName(_fromUtf8("dst"))
        self.gridLayout.addWidget(self.dst, 0, 1, 1, 1)

        self.retranslateUi(SelDist)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelDist.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelDist.reject)
        QtCore.QMetaObject.connectSlotsByName(SelDist)

    def retranslateUi(self, SelDist):
        SelDist.setWindowTitle(_translate("SelDist", "Nuova Selezione", None))
        self.label.setText(_translate("SelDist", "Nuova selezione dei Siti", None))
        self.label_2.setText(_translate("SelDist", "Importazione dei siti rispetto al sito selezionato", None))
        self.label_3.setText(_translate("SelDist", "Distanza in metri:", None))
        self.dst.setText(_translate("SelDist", "250", None))

