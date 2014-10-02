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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load CaricaSiti class from file CaricaSiti
    from caricasiti import CaricaSiti
    return CaricaSiti(iface)
