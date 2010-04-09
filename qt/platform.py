# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-13
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import logging
import sys

if sys.platform == 'win32':
    from platform_win import *
elif sys.platform == 'darwin':
    from platform_osx import *
elif sys.platform == 'linux2':
    from platform_lnx import *
else:
    logging.warning("Unsupported Platform!!")
