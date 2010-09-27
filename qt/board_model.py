# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL

from fs_model import FSModel, DESIGN_BOARD_NAME

class BoardModel(FSModel):
    def __init__(self, app):
        FSModel.__init__(self, app, app.board, DESIGN_BOARD_NAME)
        
        self.connect(self.app, SIGNAL('boardChanged()'), self.boardChanged)
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                value = str(value.toString())
                self.app.RenameNode(node.ref, value)
                node.invalidate()
                return True
        return False
    
    #--- Events
    def boardChanged(self):
        self.reset()
    
