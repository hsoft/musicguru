# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import SIGNAL, Qt, QAbstractTableModel, QModelIndex
from PyQt4.QtGui import QBrush

from hsutil.str import format_size

class LocationsModel(QAbstractTableModel):
    HEADER = ['Name', 'Files', 'GB']
    
    def __init__(self, app):
        QAbstractTableModel.__init__(self)
        self.app = app
        
        self.connect(self.app, SIGNAL('locationsChanged()'), self.locationsChanged)
    
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
        elif role == Qt.ForegroundRole:
            if location.is_removable:
                return QBrush(Qt.blue)
            elif not location.is_available:
                return QBrush(Qt.red)
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                return Qt.Checked if location in self.app.board.locations else Qt.Unchecked
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable
        return flags
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < 3:
            return self.HEADER[section]
        return None
    
    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return len(self.app.collection)
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        location = self.app.collection[index.row()]
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                self.app.toggleLocation(location)
                return True
        return False
    
    #--- Events
    def locationsChanged(self):
        self.reset()
    

