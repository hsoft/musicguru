# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-12-31
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import sys
import os
import os.path as op

import yaml

from hsutil.build import add_to_pythonpath

def main():
    conf = yaml.load(open('conf.yaml'))
    ui = conf['ui']
    print "Running musicGuru with UI {0}".format(ui)
    if ui == 'cocoa':
        os.system('open cocoa/build/Release/musicGuru.app')
    elif ui == 'qt':
        add_to_pythonpath('.')
        os.chdir('qt')
        os.system('python start.py')
        os.chdir('..')

if __name__ == '__main__':
    main()