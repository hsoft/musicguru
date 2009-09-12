# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QHeaderView

from musicguru.sqlfs.music import VOLTYPE_CDROM

import mg_rc
from locations_panel_ui import Ui_LocationsPanel
from locations_model import LocationsModel

class LocationsPanel(QDialog, Ui_LocationsPanel):
    def __init__(self, app):
        QDialog.__init__(self, None)
        self.app = app
        self.locationsModel = LocationsModel(self.app)
        self._setupUi()
        self._updateLocationInfo()
        
        self.connect(self.locationsView.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.selectionChanged)
    
    def _setupUi(self):
        self.setupUi(self)
        self.locationsView.setModel(self.locationsModel)
        h = self.locationsView.horizontalHeader()
        h.setResizeMode(QHeaderView.Fixed)
        h.resizeSection(1, 50)
        h.resizeSection(2, 50)
        h.setResizeMode(0, QHeaderView.Stretch)
    
    def _updateLocationInfo(self):
        row = self.locationsView.selectionModel().currentIndex().row()
        if row < 0:
            self.pathLabel.setText('')
            self.typeLabel.setText('')
            return
        location = self.app.collection[row]
        self.pathLabel.setText(unicode(location.physical_path))
        type_desc = "Removable (CD/DVD)" if location.vol_type == VOLTYPE_CDROM else "Fixed (Hard disk)"
        self.typeLabel.setText(type_desc)
    
    #--- Events
    def selectionChanged(self, selected, deselected):
        self._updateLocationInfo()
    
