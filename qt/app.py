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

from PyQt4.QtCore import SIGNAL, Qt, QObject, QTimer
from PyQt4.QtGui import QProgressDialog, QDesktopServices, QMessageBox

from hsutil import job

from musicguru.app import MusicGuru as MusicGuruBase

from main_window import MainWindow
from locations_panel import LocationsPanel

JOB_UPDATE = 'job_update'
JOB_ADD = 'job_add'

JOBID2TITLE = {
    JOB_UPDATE: "Updating location",
    JOB_ADD: "Adding location",
}

class Progress(QProgressDialog, job.ThreadedJobPerformer):
    def __init__(self, parent):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QProgressDialog.__init__(self, '', "Cancel", 0, 100, parent, flags)
        self.setModal(True)
        self.setAutoReset(False)
        self.setAutoClose(False)
        self._timer = QTimer()
        self._jobid = ''
        self.connect(self._timer, SIGNAL('timeout()'), self.updateProgress)
    
    def updateProgress(self):
        # the values might change before setValue happens
        last_progress = self.last_progress
        last_desc = self.last_desc
        if not self._job_running or last_progress is None:
            self._timer.stop()
            self.close()
            self.emit(SIGNAL('finished(QString)'), self._jobid)
            if self._last_error is not None:
                s = ''.join(traceback.format_exception(*self._last_error))
                dialog = ErrorReportDialog(self.parent(), s)
                dialog.exec_()
            return
        if self.wasCanceled():
            self.job_cancelled = True
            return
        if last_desc:
            self.setLabelText(last_desc)
        self.setValue(last_progress)
    
    def run(self, jobid, title, target, args=()):
        self._jobid = jobid
        self.reset()
        self.setLabelText('')
        self.run_threaded(target, args)
        self.setWindowTitle(title)
        self.show()
        self._timer.start(500)
    

class MusicGuru(MusicGuruBase, QObject):
    def __init__(self):
        appdata = unicode(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        MusicGuruBase.__init__(self, appdata)
        QObject.__init__(self)
        self.mainWindow = MainWindow(app=self)
        self.locationsPanel = LocationsPanel(app=self)
        self.progress = Progress(self.mainWindow)
        self.mainWindow.show()
        self.locationsPanel.show()
        
        self.connect(self.progress, SIGNAL('finished(QString)'), self.jobFinished)
    
    #--- Private
    
    def _startJob(self, jobid, func):
        title = JOBID2TITLE[jobid]
        try:
            j = self.progress.create_job()
            self.progress.run(jobid, title, func, args=(j, ))
        except job.JobInProgressError:
            msg = "A previous action is still hanging in there. You can't start a new one yet. Wait a few seconds, then try again."
            QMessageBox.information(self.main_window, "Action in progress", msg)
    
    #--- Public
    def addLocation(self, path, name, removeable):
        def do(j):
            MusicGuruBase.AddLocation(self, path, name, removeable, j)
        
        self._startJob(JOB_ADD, do)
    
    def removeLocation(self, location):
        self.board.RemoveLocation(location)
        location.delete()
        self.emit(SIGNAL('locationsChanged()'))
    
    def updateLocation(self, location):
        def do(j):
            location.update(None, j)
        
        self._startJob(JOB_UPDATE, do)
    
    #--- Events
    def jobFinished(self, jobid):
        if jobid in (JOB_UPDATE, JOB_ADD):
            self.emit(SIGNAL('locationsChanged()'))
    
