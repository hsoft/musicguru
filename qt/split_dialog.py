# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-18
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import unicode_literals

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog

from core.design import SplittingPanel

from ui.split_dialog_ui import Ui_SplitDialog

class SplitDialog(QDialog, Ui_SplitDialog, SplittingPanel):
    def __init__(self, app):
        QDialog.__init__(self, None)
        SplittingPanel.__init__(self, app.board)
        self.app = app
        self.setupUi(self)
        
        self.customModelField.setText(self.custom_model)
        self.modelOrder = [self.modelButton1, self.modelButton2, self.modelButton3,
            self.modelButton4]
        self.capacityOrder = [self.capacityButton1, self.capacityButton2, self.capacityButton3,
            self.capacityButton4]
        for button in self.modelOrder:
            self.connect(button, SIGNAL('toggled(bool)'), self.modelToggled)
        for button in self.capacityOrder:
            self.connect(button, SIGNAL('toggled(bool)'), self.capacityToggled)
        self.connect(self.changeExampleButton, SIGNAL('clicked()'), self.changeExampleClicked)
        self.connect(self.customModelField, SIGNAL('textChanged(QString)'), self.customModelChanged)
        self.connect(self.customCapacityField, SIGNAL('valueChanged(int)'), self.customCapacityChanged)
        self.connect(self.groupingLevelSlider, SIGNAL('valueChanged(int)'), self.groupingLevelChanged)
        self._updateExample()
    
    #--- Private
    def _updateExample(self):
        self.exampleLabel.setText(self.example)
    
    #--- Events
    def changeExampleClicked(self):
        self._updateExample()
    
    def customCapacityChanged(self, newValue):
        self.custom_capacity = newValue
    
    def customModelChanged(self, newText):
        self.custom_model = unicode(newText)
    
    def groupingLevelChanged(self, newValue):
        self.grouping_level = newValue
        self._updateExample()
    
    def modelToggled(self, checked):
        if not checked:
            return
        for index, button in enumerate(self.modelOrder):
            if button.isChecked():
                self.model_index = index
                break
    
    def capacityToggled(self, checked):
        if not checked:
            return
        for index, button in enumerate(self.capacityOrder):
            if button.isChecked():
                self.capacity_index = index
                break
    
