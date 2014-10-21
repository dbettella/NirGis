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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load configurazione class from file configurazione
    from configurazione import configurazione
    return configurazione(iface)
