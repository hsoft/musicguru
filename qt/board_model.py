# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL, QModelIndex, QMimeData, QByteArray

from hsfs.utils import smart_move
from hsutil.misc import dedupe
from hsutil.path import Path

from fs_model import FSModel

class BoardModel(FSModel):
    def __init__(self, app):
        self.app = app
        FSModel.__init__(self, app.board)
        
        self.connect(self.app, SIGNAL('boardChanged()'), self.boardChanged)
    
    def dropMimeData(self, mimeData, action, row, column, parentIndex):
        # In the test I have made, the row and column args always seem to be -1/-1 except when
        # parentIndex is invalid (which means that the drop destination is the root node).
        if not mimeData.hasFormat('application/musicguru.designboard.paths'):
            return False
        if parentIndex.isValid():
            destNode = parentIndex.internalPointer()
        else:
            destNode = self
        startLen = len(destNode.ref)
        paths = unicode(mimeData.data('application/musicguru.designboard.paths'), 'utf-8').split('\n')
        sourceItems = [self.ref.find_path(Path(path)[1:]) for path in paths]
        smart_move(sourceItems, destNode.ref, allow_merge=True)
        lenDiff = len(destNode.ref) - startLen # it's possible not all sourceItems are moved
        destNode.invalidate()
        self.insertRows(0, lenDiff, parentIndex)
        return True
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        if index.column() == 0:
            flags |= Qt.ItemIsEditable
        return flags
    
    def insertRows(self, row, count, parentIndex):
        self.beginInsertRows(parentIndex, row, row + count - 1)
        node = parentIndex.internalPointer() if parentIndex.isValid() else self
        node.invalidate()
        self.endInsertRows()
        return True
    
    def mimeData(self, indexes):
        nodes = dedupe(index.internalPointer() for index in indexes)
        paths = [unicode(node.ref.path) for node in nodes]
        data = '\n'.join(paths).encode('utf-8')
        mimeData = QMimeData()
        mimeData.setData('application/musicguru.designboard.paths', QByteArray(data))
        return mimeData
    
    def mimeTypes(self):
        return ['application/musicguru.designboard.paths']
    
    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row + count - 1)
        node = parentIndex.internalPointer() if parentIndex.isValid() else self
        node.invalidate()
        self.endRemoveRows()
        return True
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                value = unicode(value.toString())
                self.app.RenameNode(node.ref, value)
                node.invalidate()
                return True
        return False
    
    def supportedDropActions(self):
        return Qt.MoveAction
    
    #--- Events
    def boardChanged(self):
        self.reset()
    
