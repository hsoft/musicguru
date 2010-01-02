#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import sys

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QApplication, QIcon, QPixmap

import mg_rc

from app import MusicGuru

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap(":/mg_logo")))
    QCoreApplication.setOrganizationName('Hardcoded Software')
    QCoreApplication.setApplicationName('musicGuru')
    QCoreApplication.setApplicationVersion(MusicGuru.VERSION)
    mgapp = MusicGuru()
    sys.exit(app.exec_())