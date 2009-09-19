# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-19
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QHeaderView

from fs_model import FSModel
from ui.ignore_box_ui import Ui_IgnoreBox

class IgnoreBoxModel(FSModel):
    def __init__(self, app):
        FSModel.__init__(self, app.board.ignore_box)
        self.app = app
        
        self.connect(self.app, SIGNAL('ignoreBoxChanged()'), self.ignoreBoxChanged)
    
    #--- Events
    def ignoreBoxChanged(self):
        self.reset()
    

class IgnoreBox(QWidget, Ui_IgnoreBox):
    def __init__(self, app):
        QWidget.__init__(self, None)
        self.app = app
        self.boxModel = IgnoreBoxModel(app)
        self._setupUi()
        
    def _setupUi(self):
        self.setupUi(self)
        self.browserView.setModel(self.boxModel)
        h = self.browserView.header()
        h.setResizeMode(QHeaderView.Fixed)
        h.resizeSection(1, 120)
        h.setResizeMode(0, QHeaderView.Stretch)
    
