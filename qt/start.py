#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys
import gc
import sip
sip.setapi('QVariant', 1)

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QApplication, QIcon, QPixmap

import mg_rc

from app import MusicGuru

if sys.platform == 'win32':
    # cx_Freeze workarounds
    import hsfs.tree
    import os
    os.environ['QT_PLUGIN_PATH'] = 'qt4_plugins'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap(":/mg_logo")))
    QCoreApplication.setOrganizationName('Hardcoded Software')
    QCoreApplication.setApplicationName('musicGuru')
    QCoreApplication.setApplicationVersion(MusicGuru.VERSION)
    mgapp = MusicGuru()
    exec_result = app.exec_()
    del mgapp
    # Since PyQt 4.7.2, I had crashes on exit, and from reading the mailing list, it seems to be
    # caused by some weird crap about C++ instance being deleted with python instance still living.
    # The worst part is that Phil seems to say this is expected behavior. So, whatever, this
    # gc.collect() below is required to avoid a crash.
    gc.collect()
    del app
    sys.exit(exec_result)
