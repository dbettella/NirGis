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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load areadilavoro class from file areadilavoro
    from areadilavoro import areadilavoro
    return areadilavoro(iface)
