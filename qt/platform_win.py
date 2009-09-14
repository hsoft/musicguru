# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-13
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import wmi

wmi_command = wmi.WMI()

def getDriveList():
    drives = wmi_command.query("select * from win32_logicaldisk where drivetype=5")
    return [(drive.DeviceID, drive.VolumeName) for drive in drives]
