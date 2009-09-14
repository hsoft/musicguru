# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QHeaderView, QMenu, QIcon, QPixmap, QToolButton

import mg_rc
from board_model import BoardModel
from ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self, None)
        self.app = app
        self.boardModel = BoardModel(self.app)
        self._setupUi()
    
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
    
