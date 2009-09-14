# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-13
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import unicode_literals

from PyQt4.QtCore import SIGNAL, QTimer
from PyQt4.QtGui import QDialog, QGroupBox, QFileDialog

from hsutil.path import Path

import platform
from ui.add_location_dialog_ui import Ui_AddLocationDialog
from ui.add_fixed_drive_groupbox_ui import Ui_AddFixedDriveGroupBox
from ui.add_removable_drive_groupbox_ui import Ui_AddRemovableDriveGroupBox

class AddFixedDriveGroupBox(QGroupBox, Ui_AddFixedDriveGroupBox):
    def __init__(self):
        QGroupBox.__init__(self, None)
        self.setupUi(self)
        
        self.connect(self.chooseButton, SIGNAL('clicked()'), self.chooseButtonClicked)
        self.connect(self.pathField, SIGNAL('textChanged(QString)'), self.pathFieldChanged)
    
    #--- Events
    def chooseButtonClicked(self):
        title = "Select a folder to add"
        flags = QFileDialog.ShowDirsOnly
        dirpath = unicode(QFileDialog.getExistingDirectory(self, title, '', flags))
        if dirpath:
            self.pathField.setText(dirpath)
    
    def pathFieldChanged(self, newText):
        path = Path(unicode(newText))
        name = path[-1] if path else ''
        self.emit(SIGNAL('locationChanged(QString,QString)'), unicode(newText), name)
    

class AddRemovableDriveGroupBox(QGroupBox, Ui_AddRemovableDriveGroupBox):
    def __init__(self):
        QGroupBox.__init__(self, None)
        self.timer = QTimer()
        self._selectedDrive = None
        self.setupUi(self)
        self._updateDriveList()
        self.timer.start(5000)
        
        self.connect(self.timer, SIGNAL('timeout()'), self.timerTimeout)
        self.connect(self.driveList, SIGNAL('currentRowChanged(int)'), self.driveListRowChanged)
        
        
    def _updateDriveList(self):
        self._drives = platform.getDriveList()
        names = [name for path, name in self._drives]
        self.driveList.clear()
        self.driveList.addItems(names)
        if self._selectedDrive in self._drives:
            self.driveList.setCurrentRow(self._drives.index(self._selectedDrive))
    
    #--- Events
    def driveListRowChanged(self, row):
        if row < 0:
            return
        drive = self._drives[row]
        if drive == self._selectedDrive:
            return
        self._selectedDrive = drive
        path, name = drive
        self.emit(SIGNAL('locationChanged(QString,QString)'), path, name)
    
    def timerTimeout(self):
        self._updateDriveList()
    

class AddLocationDialog(QDialog, Ui_AddLocationDialog):
    def __init__(self, app):
        QDialog.__init__(self, None)
        self.app = app
        self.fixedBox = AddFixedDriveGroupBox()
        self.removableBox = AddRemovableDriveGroupBox()
        self.locationPath = None
        self.locationName = None
        self.isLocationRemovable = False
        self._setupUi()
        
        self._updateVisibleGroupBox()
        self.connect(self.hardDriveButton, SIGNAL('toggled(bool)'), self.radioButtonToggled)
        self.connect(self.removableDriveButton, SIGNAL('toggled(bool)'), self.radioButtonToggled)
        self.connect(self.fixedBox, SIGNAL('locationChanged(QString,QString)'), self.locationChanged)
        self.connect(self.removableBox, SIGNAL('locationChanged(QString,QString)'), self.locationChanged)
    
    def _setupUi(self):
        self.setupUi(self)
    
    def _updateVisibleGroupBox(self):
        if self.hardDriveButton.isChecked():
            self.placeholderLayout.removeWidget(self.removableBox)
            self.removableBox.setParent(None)
            self.placeholderLayout.addWidget(self.fixedBox)
        elif self.removableDriveButton.isChecked():
            self.placeholderLayout.removeWidget(self.fixedBox)
            self.fixedBox.setParent(None)
            self.placeholderLayout.addWidget(self.removableBox)
    
    #--- Events
    def locationChanged(self, newPath, newName):
        self.locationPath = unicode(newPath)
        self.locationName = unicode(newName)
        self.isLocationRemovable = self.removableDriveButton.isChecked()
        self.nameField.setText(newName)
    
    def radioButtonToggled(self, checked):
        self._updateVisibleGroupBox()
    
