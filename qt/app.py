# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QDesktopServices

from musicguru.app import MusicGuru as MusicGuruBase

from main_window import MainWindow
from locations_panel import LocationsPanel

class MusicGuru(MusicGuruBase, QObject):
    def __init__(self):
        appdata = unicode(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        MusicGuruBase.__init__(self, appdata)
        QObject.__init__(self)
        self._setup()
    
    #--- Private
    def _setup(self):
        self.mainWindow = MainWindow(app=self)
        self.mainWindow.show()
        self.locationsPanel = LocationsPanel(app=self)
        self.locationsPanel.show()
    
