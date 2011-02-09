# -*- coding: utf-8 -*-
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
import compileall

import yaml

from hscommon.build import (print_and_do, build_dmg, add_to_pythonpath, copy_qt_plugins,
    copy_packages, build_debian_changelog)

def package_windows(dev):
    if sys.platform != "win32":
        print("Qt packaging only works under Windows.")
        return
    add_to_pythonpath('.')
    add_to_pythonpath('qt')
    os.chdir('qt')
    from app import MusicGuru
    
    if op.exists('dist'):
        shutil.rmtree('dist')
    
    cmd = 'cxfreeze --base-name Win32GUI --target-name musicGuru.exe --icon ..\\images\\mg_logo.ico start.py'
    print_and_do(cmd)
    
    if not dev:
        # Copy qt plugins
        plugin_dest = op.join('dist', 'qt4_plugins')
        plugin_names = ['accessible', 'codecs', 'iconengines', 'imageformats']
        copy_qt_plugins(plugin_names, plugin_dest)
        
        # Compress with UPX 
        libs = [name for name in os.listdir('dist') if op.splitext(name)[1] in ('.pyd', '.dll', '.exe')]
        for lib in libs:
            print_and_do("upx --best \"dist\\{0}\"".format(lib))

    print_and_do("xcopy /Y /S /I ..\\help\\musicguru_help dist\\help")

    # AdvancedInstaller.com has to be in your PATH
    # this copying is so we don't have to re-commit installer.aip at every version change
    shutil.copy('installer.aip', 'installer_tmp.aip')
    print_and_do('AdvancedInstaller.com /edit installer_tmp.aip /SetVersion %s' % MusicGuru.VERSION)
    print_and_do('AdvancedInstaller.com /build installer_tmp.aip -force')
    os.remove('installer_tmp.aip')
    os.chdir(op.join('..', '..'))

def package_debian():
    if op.exists('build'):
        shutil.rmtree('build')
    add_to_pythonpath('qt')
    from app import MusicGuru
    destpath = op.join('build', 'musicguru-{0}'.format(MusicGuru.VERSION))
    srcpath = op.join(destpath, 'src')
    os.makedirs(destpath)
    shutil.copytree('qt', srcpath)
    copy_packages(['hsaudiotag', 'hsfs', 'core', 'qtlib', 'hscommon', 'jobprogress'], srcpath)
    shutil.copytree('debian', op.join(destpath, 'debian'))
    build_debian_changelog(op.join('help', 'changelog.yaml'), op.join(destpath, 'debian', 'changelog'), 'musicguru', from_version='1.3.6')
    shutil.copytree(op.join('help', 'musicguru_help'), op.join(srcpath, 'help'))
    shutil.copy(op.join('images', 'mg_logo_big.png'), srcpath)
    compileall.compile_dir(srcpath)
    os.chdir(destpath)
    os.system("dpkg-buildpackage")

def main():
    conf = yaml.load(open('conf.yaml'))
    ui = conf['ui']
    dev = conf['dev']
    print("Packaging musicGuru with UI {0}".format(ui))
    if ui == 'cocoa':
        build_dmg('cocoa/build/Release/musicGuru.app', '.')
    elif ui == 'qt':
        if sys.platform == "win32":
            package_windows(dev)
        elif sys.platform == "linux2":
            package_debian()

if __name__ == '__main__':
    main()
