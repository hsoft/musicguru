# Created By: Virgil Dupras
# Created On: 2009-12-31
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys
import os
import os.path as op
import shutil

from setuptools import setup
import yaml

import helpgen
from hscommon.build import (add_to_pythonpath, print_and_do, build_all_qt_ui, copy_packages,
    build_all_qt_locs)

def build_cocoa(dev):
    if not dev:
        print("Building help index")
        help_path = op.abspath('help/musicguru_help')
        os.system('open -a /Developer/Applications/Utilities/Help\\ Indexer.app {0}'.format(help_path))
    
    print("Building mg_cocoa.plugin")
    if op.exists('build'):
        shutil.rmtree('build')
    os.mkdir('build')
    if not dev:
        copy_packages(['core', 'hsaudiotag', 'hsfs', 'hscommon', 'jobprogress'], 'build')
    shutil.copy('cocoa/mg_cocoa.py', 'build')
    os.chdir('build')
    script_args = ['py2app', '-A'] if dev else ['py2app']
    setup(
        script_args = script_args,
        plugin = ['mg_cocoa.py'],
        setup_requires = ['py2app'],
    )
    os.chdir('..')
    if op.exists('cocoa/mg_cocoa.plugin'):
        shutil.rmtree('cocoa/mg_cocoa.plugin')
    shutil.move('build/dist/mg_cocoa.plugin', 'cocoa/mg_cocoa.plugin')
    if dev:
        # In alias mode, the tweakings we do to the pythonpath aren't counted in. We have to
        # manually put a .pth in the plugin
        pluginpath = 'cocoa/mg_cocoa.plugin'
        pthpath = op.join(pluginpath, 'Contents/Resources/dev.pth')
        open(pthpath, 'w').write(op.abspath('.'))
    os.chdir('cocoa')
    print("Building the XCode project")
    os.system('xcodebuild')
    os.chdir('..')

def build_qt():
    print("Building .ts files")
    build_all_qt_locs(op.join('qtlib', 'lang'))
    print("Building Qt stuff")
    build_all_qt_ui(op.join('qt', 'ui'))
    os.chdir('qt')
    print_and_do("pyrcc4 -py3 mg.qrc > mg_rc.py")
    os.chdir('..')

def main():
    conf = yaml.load(open('conf.yaml'))
    ui = conf['ui']
    dev = conf['dev']
    print("Building musicGuru with UI {0}".format(ui))
    if dev:
        print("Building in Dev mode")
    add_to_pythonpath('.')
    
    print("Generating Help")
    windows = sys.platform == 'win32'
    profile = 'win_en' if windows else 'osx_en'
    basepath = op.abspath('help')
    destpath = op.abspath(op.join('help', 'musicguru_help'))
    helpgen.gen(basepath, destpath, profile=profile)
    if ui == 'cocoa':
        build_cocoa(dev)
    elif ui == 'qt':
        build_qt()

if __name__ == '__main__':
    main()
