# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_configurazione.ui'
#
# Created: Mon Oct 27 09:58:53 2014
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

class Ui_configurazione(object):
    def setupUi(self, configurazione):
        configurazione.setObjectName(_fromUtf8("configurazione"))
        configurazione.resize(666, 348)
        self.buttonBox = QtGui.QDialogButtonBox(configurazione)
        self.buttonBox.setGeometry(QtCore.QRect(310, 300, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(configurazione)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 631, 281))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.FILE_DTM = QtGui.QLineEdit(self.tab)
        self.FILE_DTM.setGeometry(QtCore.QRect(30, 200, 531, 27))
        self.FILE_DTM.setObjectName(_fromUtf8("FILE_DTM"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 331, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.fileButton = QtGui.QPushButton(self.tab)
        self.fileButton.setGeometry(QtCore.QRect(570, 200, 41, 27))
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.DB_ADDR = QtGui.QLineEdit(self.tab_3)
        self.DB_ADDR.setGeometry(QtCore.QRect(20, 40, 591, 27))
        self.DB_ADDR.setObjectName(_fromUtf8("DB_ADDR"))
        self.label = QtGui.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.DB_NAME = QtGui.QLineEdit(self.tab_3)
        self.DB_NAME.setGeometry(QtCore.QRect(20, 100, 171, 27))
        self.DB_NAME.setObjectName(_fromUtf8("DB_NAME"))
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.DB_USERNAME = QtGui.QLineEdit(self.tab_3)
        self.DB_USERNAME.setGeometry(QtCore.QRect(240, 100, 131, 27))
        self.DB_USERNAME.setObjectName(_fromUtf8("DB_USERNAME"))
        self.label_3 = QtGui.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(240, 80, 91, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.DB_PASSWORD = QtGui.QLineEdit(self.tab_3)
        self.DB_PASSWORD.setGeometry(QtCore.QRect(410, 100, 201, 27))
        self.DB_PASSWORD.setEchoMode(QtGui.QLineEdit.Password)
        self.DB_PASSWORD.setObjectName(_fromUtf8("DB_PASSWORD"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(410, 80, 66, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.terstBtn = QtGui.QPushButton(self.tab_3)
        self.terstBtn.setGeometry(QtCore.QRect(450, 170, 161, 27))
        self.terstBtn.setObjectName(_fromUtf8("terstBtn"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))

        self.retranslateUi(configurazione)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), configurazione.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), configurazione.reject)
        QtCore.QMetaObject.connectSlotsByName(configurazione)

    def retranslateUi(self, configurazione):
        configurazione.setWindowTitle(_translate("configurazione", "configurazione", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("configurazione", "Edifici", None))
        self.label_5.setText(_translate("configurazione", "File DTM (Modello digitale del terreno utilizzato)", None))
        self.fileButton.setText(_translate("configurazione", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("configurazione", "Sezioni Orizzontali", None))
        self.label.setText(_translate("configurazione", "Indirizzo del database Etere", None))
        self.label_2.setText(_translate("configurazione", "Nome del database", None))
        self.label_3.setText(_translate("configurazione", "Nome Utente", None))
        self.label_4.setText(_translate("configurazione", "Password", None))
        self.terstBtn.setText(_translate("configurazione", "Test di connessione", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("configurazione", "Database", None))

