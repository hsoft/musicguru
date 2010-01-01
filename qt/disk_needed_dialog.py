# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-22
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import unicode_literals

import time

from PyQt4.QtCore import SIGNAL, QTimer
from PyQt4.QtGui import QDialog

import platform
from ui.disk_needed_dialog_ui import Ui_DiskNeededDialog

class DiskNeededDialog(QDialog, Ui_DiskNeededDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self._selectedDrive = None
        self._updateDriveList()
        self.timer = QTimer()
        self.timer.start(5000)
        
        self.connect(self.timer, SIGNAL('timeout()'), self.timerTimeout)
        self.connect(self.driveList, SIGNAL('currentRowChanged(int)'), self.driveListRowChanged)
        self.connect(self, SIGNAL('diskAskedAsync(QString)'), self.diskAskedAsync)
    
    def _updateDriveList(self):
        self._drives = platform.getDriveList()
        names = [name for path, name in self._drives]
        self.driveList.clear()
        self.driveList.addItems(names)
        if self._selectedDrive in self._drives:
            self.driveList.setCurrentRow(self._drives.index(self._selectedDrive))
    
    def askForDisk(self, diskName):
        self.promptLabel.setText("Insert disk labelled '%s'." % diskName)
        if self.exec_() == QDialog.Accepted and self._selectedDrive:
            return self._selectedDrive[0]
    
    def askForDiskAsync(self, diskName):
        if hasattr(self, 'asyncResult'):
            del self.asyncResult
        self.emit(SIGNAL('diskAskedAsync(QString)'), diskName)
        while not hasattr(self, 'asyncResult'):
            time.sleep(1)
        return self.asyncResult
    
    #--- Events
    def diskAskedAsync(self, diskName):
        self.asyncResult = self.askForDisk(diskName)
    
    def driveListRowChanged(self, row):
        if row < 0:
            self._selectedDrive = None
            return
        self._selectedDrive = self._drives[row]
    
    def timerTimeout(self):
        self._updateDriveList()
    
