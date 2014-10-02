# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CaricaSiti
                                 A QGIS plugin
 Descri
                              -------------------
        begin                : 2014-07-08
        copyright            : (C) 2014 by aa
        email                : aa@aa.it
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
from caricasitidialog import CaricaSitiDialog
from seldistdialog import SelezionaDistanzaDialog
from connectdialog import ConnectDialog
import time
import os.path
import psycopg2
from string import replace
import pdb
import unicodedata
class CaricaSiti:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'caricasiti_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = CaricaSitiDialog()
        self.distdlg = SelezionaDistanzaDialog()
        self.conndlg = ConnectDialog()
        #self.dlg.swButton.clicked.connect(self.exec_grz)
        self.dlg.cb_prov.insertItems(0,[""])
        self.con = None
        

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/caricasiti/icon.png"),
            u"Carica_Siti", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&CaricaSitiPlugIn", self.action)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&CaricaSitiPlugIn", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        listL = self.iface.mapCanvas().layers()  # prende i layer
        isSitiLayer = False
        for j in listL :
            if isSitiLayer:
               break
            if j.name() == "Siti" :
               isSitiLayer = True
               if j.selectedFeatureCount() > 0 :

                  self.distdlg.show()
                  result = self.distdlg.exec_()
                  if result != 1:
                     return
                  srtDistanza = self.distdlg.dst.text()
                  try:
                     distanza = float(srtDistanza)
                  except ValueError:
                      QMessageBox.warning(self.iface.mainWindow(), "Errore","Errore nel numero inserito", QMessageBox.Ok, QMessageBox.Ok)
                      return
                  fecSelList = j.selectedFeatures()                    
                  geom = fecSelList[0].geometry()
                  punto = geom.asPoint()
                  px = punto.x()
                  py = punto.y()
                  self.ricarica_siti(j,px,py,srtDistanza)
               else:
                  self.Scrivi_dati(j)
               return


        # show the dialog
        if len(QgsProject.instance().fileName()) == 0:
           QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Prima di  selezionare i siti apri un progetto\n oppure salva un nuovo progetto\n in una cartella di lavoro.", QMessageBox.Ok, QMessageBox.Ok)
           return
        self.dlg.cb_prov.clear()
        self.dlg.cb_comune.clear()
        if self.con == None:
           if not self.connetti_db():
              return
        if not self.Cmd_sql('SELECT "idprov","nome" FROM etere.province ORDER BY "idprov"'):
           return
        self.tupla_prov = self.cur.fetchall()
        lista_prov = [""]
        for (j,nomepr) in self.tupla_prov:
            lista_prov.append(str(nomepr))
        self.dlg.cb_prov.insertItems(0,lista_prov)
        self.dlg.cb_prov.currentIndexChanged.connect(self.exec_modified)
        
        tupla_comuni = self.cur.fetchall();
        self.lista_comuni = [""]
        self.dlg.cb_comune.insertItems(0,self.lista_comuni)



        self.dlg.show()
        # Run the dialog event loop
        self.index_cor = self.dlg.cb_prov.currentIndex()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
           self.newProgBar("Scarico dal Database Etere i siti...",0)
           uri = QgsDataSourceURI()
           # set host name, port, database name, username and password
           uri.setConnection("arjuna.arpa.veneto.it", "5432", "etere", "etere", "etere2014")
           # set database schema, table name, geometry column and optionaly subset (WHERE clause)
           index_com = self.dlg.cb_comune.currentIndex()
           if index_com == 0:
              if self.index_cor == 0:
                 QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Seleziona almeno una provincia.", QMessageBox.Ok, QMessageBox.Ok)
                 return
              else:
                 uri.setDataSource("etere", "siti", "geom", '"idprov"=' + self.cod_prov + ' AND "idstato"!=2')
           else:
           
              cod_com = str(self.tupla_comuni[index_com-1][0])
              uri.setDataSource("etere", "siti", "geom", '"idcomune"=' + cod_com + ' AND "idstato"!=2')
           vlayer = QgsVectorLayer(uri.uri(), "Siti", "postgres")

           #QgsMapLayerRegistry.instance().addMapLayer(vlayer)

           self.scrivi_siti_shp(vlayer)
           del vlayer
           self.clearProgBar()

    def exec_modified(self):
#        QMessageBox.warning(self.iface.mainWindow(), "Titolo della Finestra","Ciao Ciao", QMessageBox.Ok, QMessageBox.Ok)
        self.index_cor = self.dlg.cb_prov.currentIndex()
        
        self.dlg.cb_comune.clear()
        self.cod_prov = str(self.tupla_prov[self.index_cor-1][0])
        if not self.Cmd_sql('SELECT "idcomune","comune" FROM etere.comuni WHERE "provin"='+ self.cod_prov +' ORDER BY "comune"'):
           return
        self.tupla_comuni = self.cur.fetchall();
        lista_comuni = [""]
        for (j,nomepr) in self.tupla_comuni:
            lista_comuni.append(str(nomepr))
        self.dlg.cb_comune.insertItems(0,lista_comuni)
    def connetti_db(self):
        try:
           self.con = psycopg2.connect("host=arjuna.arpa.veneto.it dbname=etere user=etere password=etere2014 connect_timeout=8")
        except:
           QMessageBox.warning(self.iface.mainWindow(), "Problemi di connessione","Errore di connessione con il Data Base Etere", QMessageBox.Ok, QMessageBox.Ok)
           return False
        self.cur = self.con.cursor()
        return True
    def scrivi_siti_shp(self,lym):
       if self.con == None:
           if not self.connetti_db():
              return
       vl = QgsVectorLayer("point?crs=epsg:3003", "temporary_points", "memory")
       pr = vl.dataProvider()

       
       idx_sito = lym.fieldNameIndex('idsito')
       idx_nome = lym.fieldNameIndex('nome')
       idx_codsito = lym.fieldNameIndex('codsito')
       idx_stato = lym.fieldNameIndex('idstato')
       idx_gest = lym.fieldNameIndex('idgest')
       idx_slm = lym.fieldNameIndex('z_sito')
       itero = lym.getFeatures()
       fecpg = QgsFeature()

       # ModalitÃ  di editing
       vl.startEditing()
       # 
       while itero.nextFeature(fecpg):
          geom = fecpg.geometry()


          punto = geom.asMultiPoint()
          x = punto[0][0]
          y = punto[0][1]

          fet = QgsFeature()
          fet.setGeometry( QgsGeometry.fromPoint(QgsPoint(x,y)))

          vl.addAttribute(QgsField("idsito", QVariant.String, "", 255))
          vl.addAttribute(QgsField("nome", QVariant.String, "", 255))
          vl.addAttribute(QgsField("codsito", QVariant.String, "", 255))
          vl.addAttribute(QgsField("stato", QVariant.String, "", 255))
          vl.addAttribute(QgsField("gestore", QVariant.String, "", 255))
          vl.addAttribute(QgsField("slm", QVariant.String, "", 255))
          fet.initAttributes (6)
          fet.setAttribute(0,fecpg.attributes()[idx_sito])
          fet.setAttribute(1,fecpg.attributes()[idx_nome])
          fet.setAttribute(2,fecpg.attributes()[idx_codsito])

          indStato = "%d" % fecpg.attributes()[idx_stato]
          comandoSql = 'SELECT "stato" FROM etere.dec_stati WHERE "idstato" = ' + indStato
          if not self.Cmd_sql(comandoSql):
             return
          strStato = self.cur.fetchall()[0][0]
          fet.setAttribute(3,strStato)

          indGest = "%d" % fecpg.attributes()[idx_gest]
          comandoSql = 'SELECT "gestore" FROM etere.gestori WHERE "idgest" = ' + indGest
          if not self.Cmd_sql(comandoSql):
             return
          strGestore = self.cur.fetchall()[0][0]
          fet.setAttribute(4,strGestore)
          fet.setAttribute(5,fecpg.attributes()[idx_slm])
          pr.addFeatures( [ fet ] )
       vl.commitChanges()
       nomeDir = os.path.dirname(QgsProject.instance().fileName())
       nomeFileSiti = os.path.join(nomeDir,"Siti.shp")
       theCoor= QgsCoordinateReferenceSystem(3003,QgsCoordinateReferenceSystem.EpsgCrsId)
       error = QgsVectorFileWriter.writeAsVectorFormat(vl,nomeFileSiti,"CP1250", theCoor, "ESRI Shapefile")
       vlayer = QgsVectorLayer(nomeFileSiti, "Siti", "ogr")
       QgsMapLayerRegistry.instance().addMapLayer(vlayer)
       del vl
    def Scrivi_dati(self,lym):
       if self.con == None:
           if not self.connetti_db():
              return
       listaIdMod = []
       nMod = 0 # numero totale di diversi modelli di antenna scaricati dal database
       nomeDir = os.path.dirname(QgsProject.instance().fileName())
       nomeFileSorg = os.path.join(nomeDir,"Sorgenti.txt")
       nomeFileAnt = os.path.join(nomeDir,"Antenne.txt")
       numAnt = 0
       fileSorg = open(nomeFileSorg,'w')          
       itero = lym.getFeatures()
       fecl = QgsFeature()
       self.newProgBar("Scarico dal Database Etere la descrizione delle antenne",lym.featureCount())
       fileSorg.write("            \r\n")
       while itero.nextFeature(fecl):
          geom = fecl.geometry()

          punto = geom.asPoint()
          x = punto.x()
          y = punto.y()
  

          idx_sito = lym.fieldNameIndex('idsito')
          idx_slm = lym.fieldNameIndex('slm')
          strIdSito= fecl.attributes()[idx_sito]
          strSlm = fecl.attributes()[idx_slm]
          try:
             slm = float(replace(strSlm,',','.'))
          except ValueError:
             QMessageBox.warning(self.iface.mainWindow(), "Errore","Errore nel numero inserito slm: " + strSlm, QMessageBox.Ok, QMessageBox.Ok)
             return
          comandoSql = 'SELECT "attiva", "x_ant","y_ant","h","n_tx","pot_tx","tilt","direzione","idmod","fmin","fase","note1" FROM etere.antenne WHERE "idsito" = ' + strIdSito
          if not self.Cmd_sql(comandoSql):
             return
          tupAnt = self.cur.fetchall()
          #QMessageBox.warning(self.iface.mainWindow(), "Titolo della Finestra",str(len(tupAnt))+" "+strIdSito, QMessageBox.Ok, QMessageBox.Ok)
          for j in tupAnt:
             if (j[0] == "SI"): numAnt += 1 # solo antenne attive
             if (j[11] !="V") and (j[11] !="H") and (j[11] !="C"):
                note1 = "V"
             else:
                note1 = j[11]
             strIndMod = str(j[8])
#             if not (strIndMod in listaIdMod) and (j[0]=="SI"):
             if not (strIndMod in listaIdMod):
                listaIdMod.append(strIndMod) # aggiunge il modello solo per antenna attiva e nuova
                nMod += 1
             rigaOut = str(j[1]) + " " + str(j[2]) + " " + str(j[3]+slm) + " " + str(j[4]) + " " + str(j[5]) + " " + str(j[6]) + " "
             rigaOut = rigaOut + str(j[7]) + " " + str(j[8]) + " " + str(j[9]) + " " + str(j[10]) + " " + strIdSito + " " + note1 +"\r\n" 
             if j[0] == "SI": fileSorg.write(rigaOut) # aggiunge l'antenna solo se è attiva
          self.aggProgBar()
       self.clearProgBar()
       fileSorg.seek(0)
       fileSorg.write(str(numAnt))
       fileSorg.close()

       fileAnt = open(nomeFileAnt,'w')
       fileAnt.write(str(nMod)+'\r\n') # scrivo il numero totale di modelli di antenne
       self.newProgBar("Scarico dal Database Etere i diagrammi delle antenne",len(listaIdMod))
       for j in listaIdMod:
          comandoSql = 'SELECT "marca","modello","lunghezza","guadagno","frequenza" FROM etere.modelli WHERE "idmod" = ' + j
          if not self.Cmd_sql(comandoSql):
             return
          tupMod = self.cur.fetchall()
          comandoSql = 'SELECT "grado","atto","attv" FROM etere.diagrammi WHERE "idmod" = ' + j + ' ORDER BY "grado"'
          if not self.Cmd_sql(comandoSql):
             return
          try:
            tupDia = self.cur.fetchall()
            fileAnt.write(str(tupMod[0][0])+'\r\n') # marca antenna
            fileAnt.write(str(tupMod[0][1])+'\r\n') # nome del modello dell'antenna
            fileAnt.write(j+'\r\n')                 # id del modello nel database
            lungant = "%.6f" % tupMod[0][2]         # specifico 6 decimali per la lunghezza
            fileAnt.write(lungant+'\r\n')      # lunghezza
            gvolte = "%.6f" % tupMod[0][3]          # specifico 6 decimali per il guadagno
            fileAnt.write(gvolte+'\r\n')       # guadagno (in volte)
            gfreq = "%.6f" % tupMod[0][4]          # specifico 6 decimali per la frequenza
            fileAnt.write(gfreq+'\r\n')       # frequenza in Mhz
          except:
             pyqtRemoveInputHook()
             pdb.set_trace()
             print unicodedata.normalize('NFKD', tupMod[0][1]).encode('ascii','ignore')
          
          for k in tupDia:
             orizz = "%.6f" % k[1] # specifico che devono esserci 6 decimali (no esponenziale)
             fileAnt.write(str(k[0]) + ' ' + str(orizz) + '\r\n')
          for k in tupDia:
             vert = "%.6f" % k[2] # specifico che devono esserci 6 decimali (no esponenziale)
             fileAnt.write(str(k[0]) + ' ' + str(vert) + '\r\n')
          self.aggProgBar()
       self.clearProgBar()
       fileAnt.close() 

    def Cmd_sql(self,cmd):
       try:
          self.cur.execute(cmd)
       except:
          QMessageBox.warning(self.iface.mainWindow(), "Problemi di connessione","Errore di connessione con il Database Etere", QMessageBox.Ok, QMessageBox.Ok)
          return False
       return True

    def newProgBar(self,messaggio,num):
       
       if num > 0:
          progressMessageBar = self.iface.messageBar().createMessage(messaggio)
          self.progress = QProgressBar()
          self.progress.setMaximum(num)
          self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
          progressMessageBar.layout().addWidget(self.progress)
          self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
       else:          
          self.iface.messageBar().pushMessage(messaggio)
       self.iface.mainWindow().repaint()
    def aggProgBar(self):
       self.progress.setValue(self.progress.value() + 1)
    def clearProgBar(self):
       self.iface.messageBar().clearWidgets()
    def ricarica_siti(self,jLay,x,y,Distanza):
       self.newProgBar("Scarico dal Database Etere i siti nel raggio di " + Distanza + " metri",0)
       QgsMapLayerRegistry.instance().removeMapLayer(jLay.id())
       del jLay
       uri = QgsDataSourceURI()
       # set host name, port, database name, username and password
       uri.setConnection("arjuna.arpa.veneto.it", "5432", "etere", "etere", "etere2014")
       #laRiga = "geom && 'BOX3D(" + str(x-5000) +" "+ str(y-5000) +","+ str(x+5000) +" "+  str(y+5000) + ")'::box3d"
       laRiga = "ST_Distance(geom,ST_GeomFromText('POINT(" + str(x) + " " + str(y) + ")',3003)) < " + Distanza + ' AND "idstato"!=2'

       uri.setDataSource("etere", "siti", "geom", laRiga)
       vlayerD = QgsVectorLayer(uri.uri(), "Siti", "postgres")
       #QgsMapLayerRegistry.instance().addMapLayer(vlayerD)
       self.scrivi_siti_shp(vlayerD)
       del vlayerD
       self.clearProgBar()




#
#
