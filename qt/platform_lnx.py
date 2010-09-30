# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-04-08
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os
import os.path as op

HELP_PATH = '/usr/local/share/musicguru/help'
def getDriveList():
    names = os.listdir('/mnt')
    return [(op.join('/mnt', name), name) for name in names]
