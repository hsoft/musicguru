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

from PyQt4.QtCore import SIGNAL, Qt, QObject
from PyQt4.QtGui import QDesktopServices, QMessageBox

from hsutil import job
from qtlib.progress import Progress

from musicguru.app import MusicGuru as MusicGuruBase

from main_window import MainWindow
from locations_panel import LocationsPanel
from details_panel import DetailsPanel

JOB_UPDATE = 'job_update'
JOB_ADD = 'job_add'
JOB_MASS_RENAME = 'job_mass_rename'
JOB_SPLIT = 'job_split'

JOBID2TITLE = {
    JOB_UPDATE: "Updating location",
    JOB_ADD: "Adding location",
    JOB_MASS_RENAME: "Renaming",
    JOB_SPLIT: "Splitting",
}

class MusicGuru(MusicGuruBase, QObject):
    def __init__(self):
        appdata = unicode(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        MusicGuruBase.__init__(self, appdata)
        QObject.__init__(self)
        self.mainWindow = MainWindow(app=self)
        self.locationsPanel = LocationsPanel(app=self)
        self.detailsPanel = DetailsPanel(app=self)
        self.progress = Progress(self.mainWindow)
        self.selectedBoardItems = []
        self.mainWindow.show()
        
        self.connect(self.progress, SIGNAL('finished(QString)'), self.jobFinished)
    
    #--- Private
    
    def _startJob(self, jobid, func):
        title = JOBID2TITLE[jobid]
        try:
            j = self.progress.create_job()
            self.progress.run(jobid, title, func, args=(j, ))
        except job.JobInProgressError:
            msg = "A previous action is still hanging in there. You can't start a new one yet. Wait a few seconds, then try again."
            QMessageBox.information(self.mainWindow, "Action in progress", msg)
    
    #--- Public
    def addLocation(self, path, name, removeable):
        def do(j):
            MusicGuruBase.AddLocation(self, path, name, removeable, j)
        
        error_msg = self.CanAddLocation(path, name)
        if error_msg:
            QMessageBox.warning(self.mainWindow, "Add Location", error_msg)
            return
        self._startJob(JOB_ADD, do)
    
    def massRename(self, model, whitespace):
        def do(j):
            self.board.MassRename(model, whitespace, j)
        
        self._startJob(JOB_MASS_RENAME, do)
    
    def removeEmptyFolders(self):
        MusicGuruBase.RemoveEmptyDirs(self)
        self.emit(SIGNAL('boardChanged()'))
    
    def removeLocation(self, location):
        self.board.RemoveLocation(location)
        location.delete()
        self.emit(SIGNAL('locationsChanged()'))
        self.emit(SIGNAL('boardChanged()'))
    
    def selectBoardItems(self, items):
        self.selectedBoardItems = items
        self.emit(SIGNAL('boardSelectionChanged()'))
    
    def split(self, model, capacity, grouping_level):
        def do(j):
            self.board.Split(model, capacity, grouping_level, j)
        
        self._startJob(JOB_SPLIT, do)
    
    def toggleLocation(self, location):
        self.board.ToggleLocation(location)
        self.emit(SIGNAL('locationsChanged()'))
        self.emit(SIGNAL('boardChanged()'))
    
    def updateLocation(self, location):
        def do(j):
            location.update(None, j)
        
        self._startJob(JOB_UPDATE, do)
    
    #--- Events
    def jobFinished(self, jobid):
        if jobid in (JOB_UPDATE, JOB_ADD):
            self.emit(SIGNAL('locationsChanged()'))
        if jobid in (JOB_MASS_RENAME, JOB_SPLIT):
            self.emit(SIGNAL('boardChanged()'))
    
