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

from hsdocgen import generate_help, filters
from hsutil.build import (move_testdata_out, put_testdata_back, add_to_pythonpath,
    print_and_do, build_all_qt_ui)

def main():
    conf = yaml.load(open('conf.yaml'))
    ui = conf['ui']
    dev = conf['dev']
    print "Building musicGuru with UI {0}".format(ui)
    if dev:
        print "Building in Dev mode"
    add_to_pythonpath('.')
    
    print "Generating Help"
    windows = sys.platform == 'win32'
    tix = filters.tixgen("https://hardcoded.lighthouseapp.com/projects/31701-musicguru/tickets/{0}")
    basepath = op.abspath('help')
    destpath = op.abspath(op.join('help', 'musicguru_help'))
    generate_help.main(basepath, destpath, force_render=not dev, tix=tix, windows=windows)
    if ui == 'cocoa':
        move_log = move_testdata_out()
        try:
            os.chdir('cocoa')
            if dev:
                os.system('python gen.py --dev')
            else:
                os.system('python gen.py')
            os.chdir('..')
        finally:
            put_testdata_back(move_log)
        if dev:
            # In alias mode, the tweakings we do to the pythonpath aren't counted in. We have to
            # manually put a .pth in the plugin
            pluginpath = 'cocoa/build/Release/musicGuru.app/Contents/Resources/mg_cocoa.plugin'
            pthpath = op.join(pluginpath, 'Contents/Resources/dev.pth')
            open(pthpath, 'w').write(op.abspath('.'))
    elif ui == 'qt':
        build_all_qt_ui(op.join('qtlib', 'ui'))
        build_all_qt_ui(op.join('qt', 'ui'))
        os.chdir('qt')
        print_and_do("pyrcc4 mg.qrc > mg_rc.py")
        os.chdir('..')

if __name__ == '__main__':
    main()
