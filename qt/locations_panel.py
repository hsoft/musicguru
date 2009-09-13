# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import unicode_literals

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QHeaderView, QFileDialog

from hsutil.path import Path

from musicguru.sqlfs.music import VOLTYPE_CDROM

import mg_rc
from add_location_dialog import AddLocationDialog
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
        self.connect(self.changePathButton, SIGNAL('clicked()'), self.changePathButtonClicked)
        self.connect(self.addButton, SIGNAL('clicked()'), self.addButtonClicked)
    
    def _setupUi(self):
        self.setupUi(self)
        self.locationsView.setModel(self.locationsModel)
        h = self.locationsView.horizontalHeader()
        h.setResizeMode(QHeaderView.Fixed)
        h.resizeSection(1, 50)
        h.resizeSection(2, 50)
        h.setResizeMode(0, QHeaderView.Stretch)
    
    #--- Private
    def _selectedLocation(self):
        row = self.locationsView.selectionModel().currentIndex().row()
        return self.app.collection[row] if row >= 0 else None
    
    def _updateLocationInfo(self):
        location = self._selectedLocation()
        if location is not None:
            self.pathLabel.setText(unicode(location.physical_path))
            type_desc = "Removable (CD/DVD)" if location.vol_type == VOLTYPE_CDROM else "Fixed (Hard disk)"
            self.typeLabel.setText(type_desc)
        else:
            self.pathLabel.setText('')
            self.typeLabel.setText('')
    
    #--- Events
    def addButtonClicked(self):
        dialog = AddLocationDialog(self.app)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.app.addLocation(dialog.locationPath, dialog.locationName, dialog.isLocationRemovable)
    
    def changePathButtonClicked(self):
        location = self._selectedLocation()
        if location is None:
            return
        title = "Select a new root directory for this location"
        flags = QFileDialog.ShowDirsOnly
        dirpath = unicode(QFileDialog.getExistingDirectory(self, title, '', flags))
        if not dirpath:
            return
        location.initial_path = Path(dirpath)
        self._updateLocationInfo()
        self.app.updateLocation(location)
    
    def selectionChanged(self, selected, deselected):
        self._updateLocationInfo()
    
