# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QMainWindow, QHeaderView, QMenu, QIcon, QPixmap, QToolButton, QDialog

import mg_rc
from board_model import BoardModel
from mass_rename_dialog import MassRenameDialog
from split_dialog import SplitDialog
from ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self, None)
        self.app = app
        self.boardModel = BoardModel(self.app)
        self._setupUi()
        
        self.connect(self.browserView.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.browserSelectionChanged)
        self.connect(self.actionShowLocations, SIGNAL('triggered()'), self.showLocationsTriggered)
        self.connect(self.actionShowDetails, SIGNAL('triggered()'), self.showDetailsTriggered)
        self.connect(self.actionShowIgnoreBox, SIGNAL('triggered()'), self.showIgnoreBoxTriggered)
        self.connect(self.actionNewFolder, SIGNAL('triggered()'), self.newFolderTriggered)
        self.connect(self.actionRemoveEmptyFolders, SIGNAL('triggered()'), self.removeEmptyFoldersTriggered)
        self.connect(self.actionRenameSelected, SIGNAL('triggered()'), self.renameSelectedTriggered)
        self.connect(self.actionMoveSelectedToIgnoreBox, SIGNAL('triggered()'), self.moveSelectedToIgnoreBoxTriggered)
        self.connect(self.actionSwitchConflictAndOriginal, SIGNAL('triggered()'), self.switchConflictAndOriginalTriggered)
        self.connect(self.actionMassRename, SIGNAL('triggered()'), self.massRenameTriggered)
        self.connect(self.actionSplit, SIGNAL('triggered()'), self.splitTriggered)
    
    def _setupUi(self):
        self.setupUi(self)
        self.browserView.setModel(self.boardModel)
        h = self.browserView.header()
        h.setResizeMode(QHeaderView.Fixed)
        h.resizeSection(1, 120)
        h.setResizeMode(0, QHeaderView.Stretch)
        
        # Action menu
        actionMenu = QMenu('Actions', self.toolBar)
        actionMenu.setIcon(QIcon(QPixmap(":/actions")))
        actionMenu.addAction(self.actionNewFolder)
        actionMenu.addAction(self.actionRemoveEmptyFolders)
        actionMenu.addAction(self.actionRenameSelected)
        actionMenu.addAction(self.actionMoveSelectedToIgnoreBox)
        actionMenu.addAction(self.actionSwitchConflictAndOriginal)
        actionMenu.addSeparator()
        actionMenu.addAction(self.actionMassRename)
        actionMenu.addAction(self.actionSplit)
        actionMenu.addAction(self.actionUndoSplit)
        actionMenu.addAction(self.actionMoveConflicts)
        actionMenu.addAction(self.actionMoveConflictsAndOriginals)
        self.actionActions.setMenu(actionMenu)
        button = QToolButton(self.toolBar)
        button.setDefaultAction(actionMenu.menuAction())
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.actionsButton = button
        self.toolBar.insertWidget(self.actionActions, button) # the action is a placeholder
        self.toolBar.removeAction(self.actionActions)
        
        # Materialize menu
        materializeMenu = QMenu('Materialize', self.toolBar)
        materializeMenu.setIcon(QIcon(QPixmap(":/materialize")))
        materializeMenu.addAction(self.actionRenameInRespectiveLocations)
        materializeMenu.addAction(self.actionCopyToOtherLocation)
        materializeMenu.addAction(self.actionMoveToOtherLocation)
        self.actionMaterialize.setMenu(materializeMenu)
        button = QToolButton(self.toolBar)
        button.setDefaultAction(materializeMenu.menuAction())
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.materializeButton = button
        self.toolBar.insertWidget(self.actionMaterialize, button) # the action is a placeholder
        self.toolBar.removeAction(self.actionMaterialize)
    
    #--- Actions
    def splitTriggered(self):
        dialog = SplitDialog(self.app)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.app.split(dialog.model, dialog.capacity, dialog.grouping_level)
    
    def massRenameTriggered(self):
        dialog = MassRenameDialog(self.app)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.app.massRename(dialog.model, dialog.whitespace)
    
    def moveSelectedToIgnoreBoxTriggered(self):
        self.app.moveSelectedToIgnoreBox()
    
    def newFolderTriggered(self):
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        nodes = [index.internalPointer() for index in selectedIndexes]
        parent = nodes[0].ref if nodes else self.app.board
        newname = self.app.new_folder(parent)
        parentNode = nodes[0] if nodes else None
        self.boardModel.insertFolder(parentNode)
        children = parentNode.subnodes if parentNode is not None else self.boardModel.subnodes
        for node in children:
            if node.ref.name == newname:
                index = node.index
                self.browserView.setCurrentIndex(index)
                self.browserView.edit(index)
                break
    
    def removeEmptyFoldersTriggered(self):
        self.app.removeEmptyFolders()
    
    def renameSelectedTriggered(self):
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        if not selectedIndexes:
            return
        index = selectedIndexes[0]
        self.browserView.setCurrentIndex(index)
        self.browserView.edit(index)
    
    def showDetailsTriggered(self):
        self.app.detailsPanel.show()
    
    def showIgnoreBoxTriggered(self):
        self.app.ignoreBox.show()
    
    def showLocationsTriggered(self):
        self.app.locationsPanel.show()
    
    def switchConflictAndOriginalTriggered(self):
        currentIndex = self.browserView.currentIndex()
        if not currentIndex.isValid():
            return
        currentNode = currentIndex.internalPointer()
        self.app.SwitchConflictAndOriginal(currentNode.ref)
        self.boardModel.refreshNode(currentNode.parent)
        newIndex = self.boardModel.index(currentIndex.row(), currentIndex.column(), currentNode.parent.index)
        self.browserView.setCurrentIndex(newIndex)
    
    #--- Events
    def browserSelectionChanged(self, selected, deselected):
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        nodes = [index.internalPointer() for index in selectedIndexes]
        items = [node.ref for node in nodes]
        self.app.selectBoardItems(items)
    
