# -*- coding: utf-8 -*-
"""
/***************************************************************************
 areadilavoro
                                 A QGIS plugin
 definizione dell'area di lavoro
                              -------------------
        begin                : 2014-08-14
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
from areadilavorodialog import areadilavoroDialog
import os
import shutil
from osgeo import gdal
from osgeo import osr
import numpy
from osgeo.gdalconst import *


class areadilavoro:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'areadilavoro_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = areadilavoroDialog()
        self.fileGlobDTM = ""
        self.updateGlVariable()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/areadilavoro/icon.png"),
            u"Area di Lavoro", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&NirGis", self.action)
        #

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&NirGis", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        self.updateGlVariable()
        # Controllo se è stato salvato un progetto per avere disposizione la cartella di destinazione dei files
        if len(QgsProject.instance().fileName()) == 0:
           QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Prima di definire l'area di lavoro apri un progetto\n oppure salva un nuovo progetto\n in una cartella di lavoro.", QMessageBox.Ok, QMessageBox.Ok)
           return

        # Controllo se è presente il layer Siti
        listLaySiti = QgsMapLayerRegistry.instance().mapLayersByName("Siti")
        if len(listLaySiti) > 0 :
           laySiti = listLaySiti[0]
           # Controllo se è stato selezionato un sito nel Layer siti
           if laySiti.selectedFeatureCount() > 0 :
              # Richiesta con finestradi dialogo della dimensione dell'area di lavoro
              self.dlg.show()
              result = self.dlg.exec_()
              if result != 1:
                 return
              srtDistanza = self.dlg.editDim.text()
              try:
                 distanza = float(srtDistanza)
              except ValueError:
                  QMessageBox.warning(self.iface.mainWindow(), "Errore","Errore nel numero inserito", QMessageBox.Ok, QMessageBox.Ok)
                  return
              # uso del primo sito selezionato per definire l'area di lavoro
              fecSelList = laySiti.selectedFeatures()                    
              geom = fecSelList[0].geometry()
              punto = geom.asPoint()
              px = punto.x()
              py = punto.y()
              self.def_area(px,py,distanza)
           else :
              QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Per definire l'area di lavoro selezionare\n un sito nel layer Siti", QMessageBox.Ok, QMessageBox.Ok)
        else :
           QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Per definire l'area di lavoro deve\n essere presente il layer Siti\n con un sito selezionato", QMessageBox.Ok, QMessageBox.Ok)
    def def_area(self,x,y,dist):
        # Funzione per definire l'area di lavoro partendo dalle coordinate centrali e dalla dimensione (dist*2)

        # Se esistono dei layer "Area di lavoro" vengono rimossi dalla legenda
        listL = self.iface.mapCanvas().layers()  
        for j in listL :
            if j.name() == "Area di lavoro" :
               QgsMapLayerRegistry.instance().removeMapLayer(j.id())
               del j
        # Istanza di un layer 
        vl = QgsVectorLayer("polygon?crs=epsg:3003", "Area di lavoro", "memory")
        pr = vl.dataProvider()
        fet = QgsFeature()
        fet.setGeometry( QgsGeometry.fromPolygon( [ [ QgsPoint(x-dist,y-dist),QgsPoint(x-dist,y+dist),\
        QgsPoint(x+dist,y+dist),QgsPoint(x+dist,y-dist) ] ] ))
        pr.addFeatures( [ fet ] )
        vl.commitChanges()

        nomeDir = os.path.dirname(QgsProject.instance().fileName())
        nomeFileArea = os.path.join(nomeDir,"areadilavoro.shp")
        theCoor= QgsCoordinateReferenceSystem(3003,QgsCoordinateReferenceSystem.EpsgCrsId)
        error = QgsVectorFileWriter.writeAsVectorFormat(vl,nomeFileArea,"CP1250", theCoor, "ESRI Shapefile")
        fileqmla = os.path.join(nomeDir,"areadilavoro.qml")
        if not os.path.isfile(fileqmla):
           filesrcqmla = os.path.join(self.plugin_dir,"areadilavoro.qml")
           shutil.copyfile(filesrcqmla,fileqmla)
        vlayer = QgsVectorLayer(nomeFileArea, "Area di lavoro", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        del vl
        self.getDTM()
    def getDTM(self):
    # Funzione per estrarre il la parte del DTM all'interno dell'area di lavoro
           listLayArea = QgsMapLayerRegistry.instance().mapLayersByName("Area di lavoro")
           if len(listLayArea) > 0 :
              layArea = listLayArea[0]            
              itero = layArea.getFeatures()
              fecl = QgsFeature()
              itero.nextFeature(fecl)
              geom = fecl.geometry()
              poligono = geom.asPolygon()
              xmin = poligono[0][0].x()
              xmax = xmin
              ymin = poligono[0][0].y()
              ymax = ymin
              for k in poligono[0]:
                 if k.x() < xmin:
                    xmin = k.x()
                 if k.x() > xmax:
                    xmax = k.x()
                 if k.y() < ymin:
                    ymin = k.y()
                 if k.y() > ymax:
                    ymax = k.y()


              #Apertura del file raster originale e lettura dei suoi parametri
              inDTM = gdal.Open(self.fileGlobDTM)
              if inDTM is None:
                QMessageBox.warning(self.iface.mainWindow(), "Informazioni","Manca il file DTM:  " + self.fileGlobDTM, QMessageBox.Ok, QMessageBox.Ok)
                return
              rows = inDTM.RasterYSize
              cols = inDTM.RasterXSize

              vDataDTM = inDTM.GetGeoTransform()
              xOrigin = vDataDTM[0]
              yOrigin = vDataDTM[3]
              pixelWidth = vDataDTM[1]
              pixelHeight = vDataDTM[5]



              # Calcolo del numero di celle del raster da estrarre e delle coordinate di spostaamento offset
              xoff = int((xmin - xOrigin)/pixelWidth)
              yoff = int((yOrigin - ymax)/pixelWidth)
              xcount = int((xmax - xmin)/pixelWidth)+1
              ycount = int((ymax - ymin)/pixelWidth)+1

              # Controllo che l'intervallo calcolato non esca dai limiti del raster originale ed
              # eventualmente vengono ridefiniti i limiti
              if xoff < 0:
                 xcount = xcount + xoff
                 xoff = 0
              if xoff > cols -1:
                 xoff = cols -1
                 xcount = 0
              if yoff < 0:
                 ycount = ycount + yoff
                 yoff = 0
              if yoff > rows -1:
                 yoff = rows -1
                 ycount = 0
              if xoff + xcount > cols -1:
                 xcount = cols -1 - xoff
              if yoff + ycount > rows -1:
                 ycount = rows -1 - yoff
              if xoff + xcount < 0:
                 xcount = 0
              if yoff + ycount < 0:
                 ycount = 0

              # se non ci sono dati da estrarre ycount e xcount uguali a zero uscita dalla funzione
              if xcount == 0 or ycount == 0 :
                 return


              # ridefinizione delle coordinate del punto di origine della parte di raster
              # estratta per fare in modo che si sovrapponga esattamente all'originale 
              redef_xmin = xoff * pixelWidth + xOrigin
              redef_ymax = yOrigin - yoff * pixelWidth  

              # estrazione dal raster della matrice di valori di interesse
              myband = inDTM.GetRasterBand(1)
              elev_data = myband.ReadAsArray(xoff,yoff,xcount,ycount).astype(numpy.float)

              # istanza al nuovo raster nella RAM e inserimento della matrice di valori
              target_mem = gdal.GetDriverByName('MEM').Create('', xcount, ycount, 1, gdal.GDT_Float32)
              target_mem.SetGeoTransform((
                      redef_xmin, pixelWidth, 0,
                      redef_ymax, 0, pixelHeight,
                      ))
              outBand = target_mem.GetRasterBand(1)
              outBand.SetNoDataValue(-9999)
              outBand.WriteArray(elev_data)
              outBand.FlushCache()

              # scrittura dei dati del DTM estratto in un file Asci Arc/info
              nomeDir = os.path.dirname(QgsProject.instance().fileName())
              fileNomeAAIGrid = os.path.join(nomeDir,"DTM.asc")
              drivergrid = gdal.GetDriverByName("AAIGrid")
              outRast_dg = drivergrid.CreateCopy(fileNomeAAIGrid, target_mem, 0 )

              # scrittura del DTM estratto in un file GeoTiff
              drivertiff = gdal.GetDriverByName("GTiff")
              nomeFileDTMtiff = os.path.join(nomeDir,"DTM.tiff")
              dtm_ds = drivertiff.CreateCopy( nomeFileDTMtiff, target_mem, 0 )
              #imposta la proj a Gauss  Boaga fuso Ovest 3003
              sr = osr.SpatialReference()
              sr.ImportFromEPSG(3003)
              sr_wkt = sr.ExportToWkt()
              dtm_ds.SetProjection(sr_wkt)

              # chiusura dei raster necessaria per terminare la scrittura
              dtm_ds = None
              outRast_dg = None
              inDTM = None
              target_mem = None

              # lettura de file DTM estrattocome GeoTiff e caricamento come layer
              rlayer = QgsRasterLayer(nomeFileDTMtiff, "DTM")
              # definire il file stile per il DTM
              #fileqmla = os.path.join(nomeDir,"dtm.qml")
              #if not os.path.isfile(fileqmla):
              #   filesrcqmla = os.path.join(self.plugin_dir,"dtm.qml")
              #   shutil.copyfile(filesrcqmla,fileqmla)
              #rlayer.loadNamedStyle(fileqmla)
              QgsMapLayerRegistry.instance().addMapLayer(rlayer)
    def updateGlVariable(self):
       setting = QSettings()
       self.fileGlobDTM= setting.value("configurazione/FILE_DTM", "")

