#!/usr/bin/env python
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os

os.chdir('help')
os.system('python -u gen.py')
os.system('/Developer/Applications/Utilities/Help\\ Indexer.app/Contents/MacOS/Help\\ Indexer musicguru_help')
os.chdir('..')

os.chdir('py')
os.system('python -u gen.py')
os.chdir('..')