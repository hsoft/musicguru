# Created By: Virgil Dupras
# Created On: 2009-09-11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QHeaderView, QFileDialog

from hscommon.path import Path

import mg_rc
from ui.locations_panel_ui import Ui_LocationsPanel
from locations_model import LocationsModel

class LocationsPanel(QWidget, Ui_LocationsPanel):
    def __init__(self, app):
        QWidget.__init__(self, None)
        self.app = app
        self.locationsModel = LocationsModel(self.app)
        self._setupUi()
        self._updateLocationInfo()
        
        self.connect(self.locationsView.selectionModel(), SIGNAL('selectionChanged(QItemSelection,QItemSelection)'), self.selectionChanged)
        self.connect(self.changePathButton, SIGNAL('clicked()'), self.changePathButtonClicked)
        self.connect(self.addButton, SIGNAL('clicked()'), self.addButtonClicked)
        self.connect(self.removeButton, SIGNAL('clicked()'), self.removeButtonClicked)
    
    def _setupUi(self):
        self.setupUi(self)
        self.setWindowFlags(Qt.Tool)
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
            self.pathLabel.setText(str(location.physical_path))
            type_desc = "Removable (CD/DVD)" if location.is_removable else "Fixed (Hard disk)"
            self.typeLabel.setText(type_desc)
            self.changePathButton.setEnabled(not location.is_removable)
            self.removeButton.setEnabled(True)
        else:
            self.pathLabel.setText('')
            self.typeLabel.setText('')
            self.changePathButton.setEnabled(False)
            self.removeButton.setEnabled(False)
    
    #--- Events
    def addButtonClicked(self):
        self.app.addLocationPrompt()
    
    def changePathButtonClicked(self):
        location = self._selectedLocation()
        if location is None:
            return
        title = "Select a new root directory for this location"
        flags = QFileDialog.ShowDirsOnly
        dirpath = str(QFileDialog.getExistingDirectory(self, title, '', flags))
        if not dirpath:
            return
        location.initial_path = Path(dirpath)
        self._updateLocationInfo()
        self.app.updateLocation(location)
    
    def removeButtonClicked(self):
        self.app.removeLocationPrompt()
    
    def selectionChanged(self, selected, deselected):
        self.app.selectLocation(self._selectedLocation())
        self._updateLocationInfo()
    
