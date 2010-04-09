# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from __future__ import unicode_literals

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog

from core.design import MassRenamePanel

from ui.mass_rename_dialog_ui import Ui_MassRenameDialog

class MassRenameDialog(QDialog, Ui_MassRenameDialog, MassRenamePanel):
    def __init__(self, app):
        QDialog.__init__(self, None)
        MassRenamePanel.__init__(self, app.board)
        self.app = app
        self.setupUi(self)
        
        self.customModelField.setText(self.custom_model)
        self.modelOrder = [self.modelButton1, self.modelButton2, self.modelButton3,
            self.modelButton4, self.modelButton5]
        self.whitespaceOrder = [self.whitespaceButton1, self.whitespaceButton2,
            self.whitespaceButton3]
        for button in self.modelOrder:
            self.connect(button, SIGNAL('toggled(bool)'), self.modelToggled)
        for button in self.whitespaceOrder:
            self.connect(button, SIGNAL('toggled(bool)'), self.whitespaceToggled)
        self.connect(self.changeExampleButton, SIGNAL('clicked()'), self.changeExampleClicked)
        self.connect(self.customModelField, SIGNAL('textChanged(QString)'), self.customModelChanged)
        self._updateExamples()
    
    #--- Private
    def _changeExample(self):
        self.ChangeExample()
        self._updateExamples()
    
    def _updateExamples(self):
        self.exampleBeforeLabel.setText("Before: {0}".format(self.example_before))
        self.exampleAfterLabel.setText("After: {0}".format(self.example_after))
    
    #--- Events
    def changeExampleClicked(self):
        self._changeExample()
    
    def customModelChanged(self, newText):
        self.custom_model = unicode(newText)
        self._updateExamples()
    
    def modelToggled(self, checked):
        if not checked:
            return
        for index, button in enumerate(self.modelOrder):
            if button.isChecked():
                self.model_index = index
                break
        self._updateExamples()
    
    def whitespaceToggled(self, checked):
        if not checked:
            return
        for index, button in enumerate(self.whitespaceOrder):
            if button.isChecked():
                self.whitespace_index = index
                break
        self._updateExamples()
    
