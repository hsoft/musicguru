# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtGui import QDialog

import mg_rc
from locations_panel_ui import Ui_LocationsPanel
from locations_model import LocationsModel

class LocationsPanel(QDialog, Ui_LocationsPanel):
    def __init__(self, app):
        QDialog.__init__(self, None)
        self.app = app
        self._setupUi()
    
    def _setupUi(self):
        self.setupUi(self)
        self.locationsModel = LocationsModel(self.app)
        self.locationsView.setModel(self.locationsModel)
    