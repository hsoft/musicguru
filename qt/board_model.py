# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL, QModelIndex

from fs_model import FSModel

class BoardModel(FSModel):
    def __init__(self, app):
        self.app = app
        FSModel.__init__(self, app.board)
        
        self.connect(self.app, SIGNAL('boardChanged()'), self.boardChanged)
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 0:
            flags |= Qt.ItemIsEditable
        return flags
    
    def insertFolder(self, parentNode):
        if parentNode is not None:
            parentNode.reset()
            insertIndex = self.createIndex(0, 0, parentNode)
        else:
            self._subnodes = None
            insertIndex = QModelIndex()
        self.emit(SIGNAL('rowsInserted(QModelIndex,int,int)'), insertIndex, 0, 0)
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                value = unicode(value.toString())
                self.app.RenameNode(node.ref, value)
                node.reset()
                return True
        return False
    
    #--- Events
    def boardChanged(self):
        self.reset()
    
