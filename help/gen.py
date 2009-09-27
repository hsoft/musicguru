#!/usr/bin/env python
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os

from hsdocgen import generate_help, filters

tix = filters.tixgen("https://hardcoded.lighthouseapp.com/projects/31701-musicguru/overview")

generate_help.main('.', 'musicguru_help', force_render=True, tix=tix)