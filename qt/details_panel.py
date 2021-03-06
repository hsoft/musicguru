# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QWidget, QTableWidgetItem

from ui.details_panel_ui import Ui_DetailsPanel

class DetailsPanel(QWidget, Ui_DetailsPanel):
    def __init__(self, app):
        QWidget.__init__(self, None)
        self.app = app
        self._setupUi()
        
        self.connect(self.app, SIGNAL('boardSelectionChanged()'), self.boardSelectionChanged)
    
    def _setupUi(self):
        self.setupUi(self)
        self.setWindowFlags(Qt.Tool)
    
    #--- Private
    def _updateInfo(self):
        originals = [item.original for item in self.app.selectedBoardItems]
        info = self.app.GetSelectionInfo(originals)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(info))
        for index, (name, value) in enumerate(info):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(value)))
    
    #--- Events
    def boardSelectionChanged(self):
        self._updateInfo()
    
