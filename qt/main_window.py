# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt, SIGNAL, QModelIndex
from PyQt4.QtGui import QMainWindow, QHeaderView, QMenu, QIcon, QPixmap, QToolButton, QDialog

from hsutil.conflict import is_conflicted

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
        self._refreshActionsState()
        
        self.connect(self.browserView.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.browserSelectionChanged)
        self.connect(self.app, SIGNAL('boardChanged()'), self.boardChanged)
        
        # Actions
        self.connect(self.actionShowLocations, SIGNAL('triggered()'), self.showLocationsTriggered)
        self.connect(self.actionShowDetails, SIGNAL('triggered()'), self.showDetailsTriggered)
        self.connect(self.actionShowIgnoreBox, SIGNAL('triggered()'), self.showIgnoreBoxTriggered)
        self.connect(self.actionAddLocation, SIGNAL('triggered()'), self.addLocationTriggered)
        self.connect(self.actionRemoveLocation, SIGNAL('triggered()'), self.removeLocationTriggered)
        self.connect(self.actionUpdateLocation, SIGNAL('triggered()'), self.updateLocationTriggered)
        self.connect(self.actionNewFolder, SIGNAL('triggered()'), self.newFolderTriggered)
        self.connect(self.actionRemoveEmptyFolders, SIGNAL('triggered()'), self.removeEmptyFoldersTriggered)
        self.connect(self.actionRenameSelected, SIGNAL('triggered()'), self.renameSelectedTriggered)
        self.connect(self.actionMoveSelectedToIgnoreBox, SIGNAL('triggered()'), self.moveSelectedToIgnoreBoxTriggered)
        self.connect(self.actionSwitchConflictAndOriginal, SIGNAL('triggered()'), self.switchConflictAndOriginalTriggered)
        self.connect(self.actionMassRename, SIGNAL('triggered()'), self.massRenameTriggered)
        self.connect(self.actionSplit, SIGNAL('triggered()'), self.splitTriggered)
        self.connect(self.actionUndoSplit, SIGNAL('triggered()'), self.undoSplitTriggered)
        self.connect(self.actionMoveConflicts, SIGNAL('triggered()'), self.moveConflictsTriggered)
        self.connect(self.actionMoveConflictsAndOriginals, SIGNAL('triggered()'), self.moveConflictsAndOriginalsTriggered)
        self.connect(self.actionRenameInRespectiveLocations, SIGNAL('triggered()'), self.renameInRespectiveLocationsTriggered)
        self.connect(self.actionCopyToOtherLocation, SIGNAL('triggered()'), self.copyToOtherLocationTriggered)
        self.connect(self.actionMoveToOtherLocation, SIGNAL('triggered()'), self.moveToOtherLocationTriggered)
        self.connect(self.actionShowHelp, SIGNAL('triggered()'), self.showHelpTriggered)
        self.connect(self.actionAbout, SIGNAL('triggered()'), self.aboutTriggered)
    
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
    
    def _refreshActionsState(self):
        boardEmpty = len(self.app.board) == 0
        hasConflicts = len(self.app.board.allconflicts) > 0
        hasSelection = len(self.app.selectedBoardItems) > 0
        selectedIsConflicted = False
        if hasSelection:
            node = self.app.selectedBoardItems[0]
            selectedIsConflicted = is_conflicted(node.name)
        boardIsSplit = self.app.board.splitted
        for action in [self.actionMassRename, self.actionNewFolder, self.actionRemoveEmptyFolders, 
            self.actionRenameInRespectiveLocations, self.actionCopyToOtherLocation, 
            self.actionMoveToOtherLocation]:
            action.setEnabled(not boardEmpty)
        self.actionMoveConflicts.setEnabled(not boardEmpty and hasConflicts)
        self.actionMoveConflictsAndOriginals.setEnabled(not boardEmpty and hasConflicts)
        self.actionSwitchConflictAndOriginal.setEnabled(not boardEmpty and selectedIsConflicted)
        self.actionRenameSelected.setEnabled(not boardEmpty and hasSelection)
        self.actionMoveSelectedToIgnoreBox.setEnabled(not boardEmpty and hasSelection)
        self.actionSplit.setEnabled(not boardEmpty and not boardIsSplit)
        self.actionUndoSplit.setEnabled(not boardEmpty and boardIsSplit)
    
    #--- Actions
    def aboutTriggered(self):
        self.app.showAboutBox()
    
    def addLocationTriggered(self):
        self.app.addLocationPrompt()
    
    def copyToOtherLocationTriggered(self):
        self.app.copyOrMove(copy=True)
    
    def massRenameTriggered(self):
        dialog = MassRenameDialog(self.app)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.app.massRename(dialog.model, dialog.whitespace)
    
    def moveConflictsTriggered(self):
        self.app.moveConflicts()
    
    def moveConflictsAndOriginalsTriggered(self):
        self.app.moveConflicts(with_original=True)
    
    def moveSelectedToIgnoreBoxTriggered(self):
        self.app.moveSelectedToIgnoreBox()
    
    def moveToOtherLocationTriggered(self):
        self.app.copyOrMove(copy=False)
    
    def newFolderTriggered(self):
        # We're not using browserView.currentIndex as a base index here because it's impossible
        # for the user to set the currentIndex to "None" after a node has been selected (even if
        # you deselect all nodes, the current index will stay on the last selected node).
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        currentIndex = selectedIndexes[0] if selectedIndexes else QModelIndex()
        parent = currentIndex.internalPointer().ref if currentIndex.isValid() else self.app.board
        newname = self.app.new_folder(parent)
        self.boardModel.insertRow(0, currentIndex)
        parentNode = currentIndex.internalPointer() if currentIndex.isValid() else self.boardModel
        for node in parentNode.subnodes:
            if node.ref.name == newname:
                index = node.index
                self.browserView.setCurrentIndex(index)
                self.browserView.edit(index)
                break
    
    def removeEmptyFoldersTriggered(self):
        self.app.removeEmptyFolders()
    
    def removeLocationTriggered(self):
        self.app.removeLocationPrompt()
    
    def renameInRespectiveLocationsTriggered(self):
        self.app.renameInRespectiveLocations()
    
    def renameSelectedTriggered(self):
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        if not selectedIndexes:
            return
        index = selectedIndexes[0]
        self.browserView.setCurrentIndex(index)
        self.browserView.edit(index)
    
    def showDetailsTriggered(self):
        self.app.showDetailsPanel()
    
    def showHelpTriggered(self):
        self.app.showHelp()
    
    def showIgnoreBoxTriggered(self):
        self.app.showIgnoreBox()
    
    def showLocationsTriggered(self):
        self.app.showLocationPanel()
    
    def splitTriggered(self):
        dialog = SplitDialog(self.app)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.app.split(dialog.model, dialog.capacity, dialog.grouping_level)
    
    def switchConflictAndOriginalTriggered(self):
        currentIndex = self.browserView.currentIndex()
        if not currentIndex.isValid():
            return
        currentNode = currentIndex.internalPointer()
        self.app.SwitchConflictAndOriginal(currentNode.ref)
        self.boardModel.refreshNode(currentNode.parent)
        newIndex = self.boardModel.index(currentIndex.row(), currentIndex.column(), currentNode.parent.index)
        self.browserView.setCurrentIndex(newIndex)
    
    def undoSplitTriggered(self):
        self.app.undoSplit()
    
    def updateLocationTriggered(self):
        if self.app.selectedLocation is not None:
            self.app.updateLocation(self.app.selectedLocation)
    
    #--- Events
    def boardChanged(self):
        self.app.selectBoardItems([])
        self._refreshActionsState()
    
    def browserSelectionChanged(self, selected, deselected):
        selectedIndexes = self.browserView.selectionModel().selectedRows()
        nodes = [index.internalPointer() for index in selectedIndexes]
        items = [node.ref for node in nodes]
        self.app.selectBoardItems(items)
        self._refreshActionsState()
    
