# -*- coding: utf-8 -*-
"""
/***************************************************************************
 configurazione
                                 A QGIS plugin
 Configurazione NirGis
                              -------------------
        begin                : 2014-10-19
        copyright            : (C) 2014 by Arpav
        email                : lpasquini@arpa.veneto.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from configurazionedialog import configurazioneDialog
import psycopg2
import os.path
from conf import config

class configurazione:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'configurazione_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        (dirPlugins,plugDir) = os.path.split(self.plugin_dir)
        self.cfg = config(dirPlugins)
        self.updateGlobalVariable()
        self.dlg = configurazioneDialog()
        self.dlg.terstBtn.clicked.connect(self.test_connetti_db)
        self.dlg.fileButton.clicked.connect(self.select_DTM_file)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/configurazione/icon.png"),
            u"Configurazione", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&NirGis", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&NirGis", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.leggiOpzioni()
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
           self.scriviOpzioni()
           self.updateGlobalVariable()
    def leggiOpzioni(self):
      self.dlg.DB_ADDR.setText(self.cfg.cercaOpzione("DB_ADDR"))
      self.dlg.DB_NAME.setText(self.cfg.cercaOpzione("DB_NAME"))
      self.dlg.DB_USERNAME.setText(self.cfg.cercaOpzione("DB_USERNAME"))
      self.dlg.DB_PASSWORD.setText(self.cfg.cercaOpzione("DB_PASSWORD"))
      self.dlg.FILE_DTM.setText(self.cfg.cercaOpzione("FILE_DTM"))
      self.dlg.SAVE_PRG_BEFORE_DB_CONN.setChecked(self.cfg.cercaOpzione("SAVE_PRG_BEFORE_DB_CONN"))

    def scriviOpzioni(self):
       self.cfg.impostaOpzione("DB_ADDR",self.dlg.DB_ADDR.text())
       self.cfg.impostaOpzione("DB_NAME",self.dlg.DB_NAME.text())
       self.cfg.impostaOpzione("DB_USERNAME",self.dlg.DB_USERNAME.text())
       self.cfg.impostaOpzione("DB_PASSWORD",self.dlg.DB_PASSWORD.text())
       self.cfg.impostaOpzione("FILE_DTM",self.dlg.FILE_DTM.text())
       self.cfg.impostaOpzione("SAVE_PRG_BEFORE_DB_CONN",self.dlg.SAVE_PRG_BEFORE_DB_CONN.isChecked())
       self.cfg.salvaFileOpzioni()

    def updateGlobalVariable(self):
         setting = QSettings()
         setting.setValue("configurazione/DB_ADDR", self.cfg.cercaOpzione("DB_ADDR"))
         setting.setValue("configurazione/DB_NAME", self.cfg.cercaOpzione("DB_NAME"))
         setting.setValue("configurazione/DB_USERNAME", self.cfg.cercaOpzione("DB_USERNAME"))
         setting.setValue("configurazione/DB_PASSWORD", self.cfg.cercaOpzione("DB_PASSWORD"))
         setting.setValue("configurazione/FILE_DTM", self.cfg.cercaOpzione("FILE_DTM"))
         setting.setValue("configurazione/SAVE_PRG_BEFORE_DB_CONN", self.cfg.cercaOpzione("SAVE_PRG_BEFORE_DB_CONN"))
    def test_connetti_db(self):
        try:
           comd = "host="+self.dlg.DB_ADDR.text()+" dbname="+self.dlg.DB_NAME.text()+" user="+self.dlg.DB_USERNAME.text()
           comd = comd + " password="+self.dlg.DB_PASSWORD.text()+" connect_timeout=8"
           connessione = psycopg2.connect(comd)
        except:
           QMessageBox.warning(self.dlg, "Problemi di connessione","Errore di connessione con il Data Base Etere", QMessageBox.Ok, QMessageBox.Ok)
           return False
        connessione.close()
        QMessageBox.warning(self.dlg, "Connessione a Etere","Collegamento OK", QMessageBox.Ok, QMessageBox.Ok)
        return True
    def select_DTM_file(self):
       theFile = QFileDialog.getOpenFileName(self.dlg,"Open Image",os.environ['HOME'],"File Tiff o adr (*.tiff *.tif *.adr);;Tutti i file (*)")
       if len(theFile) > 0 :
          self.dlg.FILE_DTM.setText(theFile)

