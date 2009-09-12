# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex

from hsutil.str import format_size

class LocationsModel(QAbstractTableModel):
    HEADER = ['Name', 'Files', 'GB']
    
    def __init__(self, app):
        QAbstractTableModel.__init__(self)
        self.app = app
    
    def columnCount(self, parent):
        if parent.isValid():
            return 0
        return 3
    
    def data(self, index, role):
        if not index.isValid():
            return None
        location = self.app.collection[index.row()]
        if role == Qt.DisplayRole:
            column = index.column()
            if column == 0:
                return location.name
            elif column == 1:
                return location.get_stat('filecount')
            elif column == 2:
                return format_size(location.get_stat('size'), 2, 3, False)
        return None
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < 3:
            return self.HEADER[section]
        return None
    
    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self.app.collection)
    

