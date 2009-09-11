#!/usr/bin/env python
# Created By: Virgil Dupras
# Created On: 2009-09-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from hsutil.build import print_and_do

print_and_do("pyuic4 main_window.ui > main_window_ui.py")
print_and_do("pyuic4 locations_panel.ui > locations_panel_ui.py")
print_and_do("pyrcc4 mg.qrc > mg_rc.py")
