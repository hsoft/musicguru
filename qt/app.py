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
from PyQt4.QtGui import QDesktopServices, QMessageBox, QApplication, QFileDialog, QDialog

from hsutil import job
from qtlib.app import Application as ApplicationBase
from qtlib.about_box import AboutBox
from qtlib.progress import Progress
from qtlib.reg import Registration

from musicguru.app import MusicGuru as MusicGuruBase
from musicguru.fs_utils import smart_move

from main_window import MainWindow
from locations_panel import LocationsPanel
from details_panel import DetailsPanel
from ignore_box import IgnoreBox
from disk_needed_dialog import DiskNeededDialog
from add_location_dialog import AddLocationDialog
from preferences import Preferences

JOB_UPDATE = 'job_update'
JOB_ADD = 'job_add'
JOB_MASS_RENAME = 'job_mass_rename'
JOB_SPLIT = 'job_split'
JOB_MATERIALIZE = 'job_materialize'

JOBID2TITLE = {
    JOB_UPDATE: "Updating location(s)",
    JOB_ADD: "Adding location",
    JOB_MASS_RENAME: "Renaming",
    JOB_SPLIT: "Splitting",
    JOB_MATERIALIZE: "Materializing",
}

def demo_check(method):
    def wrapper(self, *args, **kwargs):
        if not self.registered:
            msg = "It's not possible to materialize your design in demo mode."
            QMessageBox.information(self.mainWindow, "Demo Limitation", msg)
        else:
            return method(self, *args, **kwargs)
    
    return wrapper

class MusicGuru(MusicGuruBase, ApplicationBase):
    LOGO_NAME = 'mg_logo'
    DEMO_LIMIT_DESC = "In the demo version, it's not possible to materialize designs."
    
    def __init__(self):
        appdata = unicode(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        MusicGuruBase.__init__(self, appdata)
        ApplicationBase.__init__(self)
        self.prefs = Preferences()
        self.prefs.load()
        self.selectedBoardItems = []
        self.selectedLocation = None
        self.mainWindow = MainWindow(app=self)
        self.locationsPanel = LocationsPanel(app=self)
        self.detailsPanel = DetailsPanel(app=self)
        self.ignoreBox = IgnoreBox(app=self)
        self.progress = Progress(self.mainWindow)
        self.aboutBox = AboutBox(self.mainWindow, self)
        
        self.connect(self.progress, SIGNAL('finished(QString)'), self.jobFinished)
        self.connect(self, SIGNAL('applicationFinishedLaunching()'), self.applicationFinishedLaunching)
    
    #--- Private
    def _placeDetailsPanel(self):
        # locations panel must be placed first
        if self.detailsPanel.isVisible():
            return
        desktop = QApplication.desktop()
        w = self.locationsPanel.width()
        h = self.detailsPanel.height()
        x = self.locationsPanel.x()
        windowBottom = self.locationsPanel.frameGeometry().y() + self.locationsPanel.frameGeometry().height()
        y = windowBottom
        self.detailsPanel.move(x, y)
        self.detailsPanel.resize(w, h)
    
    def _placeIgnoreBox(self):
        if self.ignoreBox.isVisible():
            return
        desktop = QApplication.desktop()
        windowWidth = self.mainWindow.frameGeometry().width()
        frameWidth = self.ignoreBox.frameGeometry().width() - self.ignoreBox.width()
        w = windowWidth - frameWidth
        h = self.ignoreBox.height()
        x = self.mainWindow.x()
        windowBottom = self.mainWindow.frameGeometry().y() + self.mainWindow.frameGeometry().height()
        y = min(windowBottom, desktop.height() - h)
        self.ignoreBox.move(x, y)
        self.ignoreBox.resize(w, h)
    
    def _placeLocationsPanel(self):
        if self.locationsPanel.isVisible():
            return
        desktop = QApplication.desktop()
        w = self.locationsPanel.width()
        windowHeight = self.mainWindow.frameGeometry().height()
        frameHeight = self.locationsPanel.frameGeometry().height() - self.locationsPanel.height()
        h = windowHeight - frameHeight - self.detailsPanel.frameGeometry().height()
        windowRight = self.mainWindow.frameGeometry().x() + self.mainWindow.frameGeometry().width()
        x = min(windowRight, desktop.width() - w)
        y = self.mainWindow.y()
        self.locationsPanel.move(x, y)
        self.locationsPanel.resize(w, h)
    
    def _setup_as_registered(self):
        self.prefs.registration_code = self.registration_code
        self.prefs.registration_email = self.registration_email
        self.mainWindow.actionRegister.setVisible(False)
        self.aboutBox.registerButton.hide()
        self.aboutBox.registeredEmailLabel.setText(self.prefs.registration_email)
    
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
    
    def addLocationPrompt(self):
        dialog = AddLocationDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.addLocation(dialog.locationPath, dialog.locationName, dialog.isLocationRemovable)
    
    def askForRegCode(self):
        if self.reg.ask_for_code():
            self._setup_as_registered()
    
    @demo_check
    def copyOrMove(self, copy):
        def onNeedCd(location):
            # We can't do anything GUI related in a separate thread with Qt. Since copy/move
            # operations are performed asynchronously, the calls made to needCdDialog (created in
            # the main thread) must also be made asynchronously.
            return needCdDialog.askForDiskAsync(location.name)
        
        def do(j):
            MusicGuruBase.CopyOrMove(self, copy, dirpath, j, onNeedCd)
        
        needCdDialog = DiskNeededDialog()
        title = "Choose a destination"
        flags = QFileDialog.ShowDirsOnly
        dirpath = unicode(QFileDialog.getExistingDirectory(self.mainWindow, title, '', flags))
        if dirpath:
            self._startJob(JOB_MATERIALIZE, do)
    
    def massRename(self, model, whitespace):
        def do(j):
            self.board.MassRename(model, whitespace, j)
        
        self._startJob(JOB_MASS_RENAME, do)
    
    def moveConflicts(self, with_original=False):
        if self.board.MoveConflicts(with_original=with_original) > 0:
            self.emit(SIGNAL('boardChanged()'))
            self.emit(SIGNAL('ignoreBoxChanged()'))
    
    def moveSelectedToIgnoreBox(self):
        smart_move(self.selectedBoardItems, self.board.ignore_box, allow_merge=True)
        self.emit(SIGNAL('boardChanged()'))
        self.emit(SIGNAL('ignoreBoxChanged()'))
    
    def removeEmptyFolders(self):
        MusicGuruBase.RemoveEmptyDirs(self)
        self.emit(SIGNAL('boardChanged()'))
    
    def removeLocation(self, location):
        self.board.RemoveLocation(location)
        location.delete()
        self.emit(SIGNAL('locationsChanged()'))
        self.emit(SIGNAL('boardChanged()'))
    
    def removeLocationPrompt(self):
        location = self.selectedLocation
        if location is None:
            return
        title = "Remove location"
        msg = "Do you really want to remove location {0}?".format(location.name)
        buttons = QMessageBox.Yes | QMessageBox.No
        answer = QMessageBox.question(self.mainWindow, title, msg, buttons, QMessageBox.Yes)
        if answer != QMessageBox.Yes:
            return
        self.removeLocation(location)
    
    @demo_check
    def renameInRespectiveLocations(self):
        def do(j):
            MusicGuruBase.RenameInRespectiveLocations(self, j)
        
        self._startJob(JOB_MATERIALIZE, do)
    
    def selectBoardItems(self, items):
        self.selectedBoardItems = items
        self.emit(SIGNAL('boardSelectionChanged()'))
    
    def selectLocation(self, location):
        self.selectedLocation = location
    
    def showAboutBox(self):
        self.aboutBox.show()
    
    def showDetailsPanel(self):
        self._placeLocationsPanel()
        self._placeDetailsPanel()
        self.detailsPanel.show()
        self.detailsPanel.activateWindow()
    
    def showHelp(self):
        url = QUrl.fromLocalFile(op.abspath('help/intro.htm'))
        QDesktopServices.openUrl(url)
    
    def showIgnoreBox(self):
        self._placeIgnoreBox()
        self.ignoreBox.show()
        self.ignoreBox.activateWindow()
    
    def showLocationPanel(self):
        self._placeLocationsPanel()
        self.locationsPanel.show()
        self.locationsPanel.activateWindow()
    
    def split(self, model, capacity, grouping_level):
        def do(j):
            self.board.Split(model, capacity, grouping_level, j)
        
        self._startJob(JOB_SPLIT, do)
    
    def toggleLocation(self, location):
        self.board.ToggleLocation(location)
        self.emit(SIGNAL('locationsChanged()'))
        self.emit(SIGNAL('boardChanged()'))
    
    def undoSplit(self):
        self.board.Unsplit()
        self.emit(SIGNAL('boardChanged()'))
    
    def updateCollection(self):
        def do(j):
            self.collection.update_volumes(j)
        
        self._startJob(JOB_UPDATE, do)
    
    def updateLocation(self, location):
        def do(j):
            location.update(None, j)
        
        self._startJob(JOB_UPDATE, do)
    
    #--- Events
    def applicationFinishedLaunching(self):
        self.reg = Registration(self)
        self.set_registration(self.prefs.registration_code, self.prefs.registration_email)
        if not self.registered:
            self.reg.show_nag()
        self.mainWindow.show()
        self.showLocationPanel()
        self.showDetailsPanel()
        self.updateCollection()
    
    def jobFinished(self, jobid):
        if jobid in (JOB_UPDATE, JOB_ADD):
            self.emit(SIGNAL('locationsChanged()'))
        if jobid in (JOB_MASS_RENAME, JOB_SPLIT):
            self.emit(SIGNAL('boardChanged()'))
    
