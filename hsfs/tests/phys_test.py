# Created By: Virgil Dupras
# Created On: 2005/01/14
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os
import time
import os.path as op
import shutil
import sys

from pytest import raises
from hscommon import io
from hscommon.testutil import log_calls, TestData
from hscommon.path import Path
from hscommon.testutil import eq_

from .. import phys
from .. import _fs as fs

testdata = TestData(op.join(op.dirname(__file__), 'testdata'))

def create_fake_fs(rootpath):
    rootpath = op.join(rootpath, 'fs')
    os.makedirs(rootpath)
    os.mkdir(op.join(rootpath, 'dir1'))
    os.mkdir(op.join(rootpath, 'dir2'))
    os.mkdir(op.join(rootpath, 'dir3'))
    fp = open(op.join(rootpath, 'file1.test'), 'w')
    fp.write('1')
    fp.close()
    fp = open(op.join(rootpath, 'file2.test'), 'w')
    fp.write('12')
    fp.close()
    fp = open(op.join(rootpath, 'file3.test'), 'w')
    fp.write('123')
    fp.close()
    fp = open(op.join(rootpath, 'dir1', 'file1.test'), 'w')
    fp.write('1')
    fp.close()
    fp = open(op.join(rootpath, 'dir2', 'file2.test'), 'w')
    fp.write('12')
    fp.close()
    fp = open(op.join(rootpath, 'dir3', 'file3.test'), 'w')
    fp.write('123')
    fp.close()
    return rootpath

def create_unicode_test_dir(rootpath):
    io.mkdir(rootpath + '\xe9_dir')
    io.open(rootpath + '\xe9_file', 'w').close()
    io.open(rootpath + ('\xe9_dir', '\xe9_file'), 'w').close()

class TestPhys:
    def test_dir_and_files(self, tmpdir):
        rootpath = create_fake_fs(str(tmpdir))
        root = phys.Directory(None, rootpath)
        eq_(root.dircount,3)
        eq_(root.filecount,3)
        dir1 = root.dirs[0]
        dir2 = root.dirs[1]
        dir3 = root.dirs[2]
        file1 = root.files[0]
        file2 = root.files[1]
        file3 = root.files[2]
        file11 = dir1.files[0]
        file22 = dir2.files[0]
        file33 = dir3.files[0]
        eq_(dir1.name,'dir1')
        eq_(dir1.dircount,0)
        eq_(dir1.filecount,1)
        eq_(dir2.name,'dir2')
        eq_(dir2.dircount,0)
        eq_(dir2.filecount,1)
        eq_(dir3.name,'dir3')
        eq_(dir3.dircount,0)
        eq_(dir3.filecount,1)
        eq_(file1.name,'file1.test')
        eq_(file1.size,1)
        eq_(file2.name,'file2.test')
        eq_(file2.size,2)
        eq_(file3.name,'file3.test')
        eq_(file3.size,3)
        eq_(file11.name,'file1.test')
        eq_(file11.size,1)
        eq_(file22.name,'file2.test')
        eq_(file22.size,2)
        eq_(file33.name,'file3.test')
        eq_(file33.size,3)
    
    def test_operations(self, tmpdir):
        tmppath = str(tmpdir.join('tmppath'))
        os.mkdir(tmppath)
        rootpath = create_fake_fs(str(tmpdir.join('fakefs')))
        tmpdir = phys.Directory(None, tmppath)
        fsdir = phys.Directory(None, rootpath)
        fsdir.copy(tmpdir)
        assert 'fs' in tmpdir
        fsdir = tmpdir['fs']
        eq_(str(fsdir.path), op.join(tmppath, 'fs'))
        assert 'dir1' in fsdir
        d1 = fsdir['dir1']
        assert 'dir1' not in tmpdir
        d1 = d1.move(tmpdir)
        assert 'dir1' in tmpdir
        eq_(d1.parent,tmpdir)
        f1 = d1['file1.test']
        assert 'file1.test' not in tmpdir
        f1 = f1.move(tmpdir)
        assert 'file1.test' in tmpdir
        eq_(str(f1.path),op.join(tmppath, 'file1.test'))
        assert 'file2.test' not in tmpdir
        f2 = f1.copy(tmpdir,'file2.test')
        assert 'file2.test' in tmpdir
        f2.delete()
        assert 'file2.test' not in tmpdir
    
    def test_unicode(self, tmpdir):
        #The problem here is that \u00e9 and e\u0301 both are eacute.
        #Under mac, I get e\u0301, and under windows I get \u00e9.
        p = Path(str(tmpdir))
        create_unicode_test_dir(p)
        d = phys.Directory(None, str(p))
        assert d.dirs[-1].name in ('\u00e9_dir','e\u0301_dir')
        assert d.files[0].name in ('\u00e9_file','e\u0301_file')
        assert d.dirs[-1].files[0].name in ('\u00e9_file','e\u0301_file')
    
    def test_mtime(self):
        """We don't test for actual mtime here because it can change in the
        testdata dir. Let's just assume that if it's not zero, it has been
        correctly fetched.
        """
        root = phys.Directory(None, testdata.filepath('utils'))
        assert root._get_mtime() > 1
        assert root.files[0].mtime > 1
    
    def test_always_put_slash_at_the_end_of_windows_drive_letter(self, monkeypatch):
        #This test is only for windows, but it will not fail under other platforms
        def listdir(path):
            if not path.endswith('\\'):
                self.fail()
            return []
        
        monkeypatch.setattr(os, 'listdir', listdir)
        d = phys.Directory(None,'C:\\')
        d.dirs
        d.files
    
    def test_InvalidPath_error(self):
        #InvalidPath should be raised when phys dir has been manually created (parent == None)
        #But it shouldn't be raised when it is a subdirectory.
        d = phys.Directory(None,'does_not_exist')
        try:
            d.dirs
            self.fail()
        except fs.InvalidPath:
            pass
        root = phys.Directory(None, testdata.filepath('utils'))
        d = phys.Directory(root, 'does_not_exist')
        eq_([],d.dirs)
        eq_([],d.files)
    
    def test_that_move_keeps_the_same_instance(self, tmpdir):
        tmpdir = phys.Directory(None, str(tmpdir))
        refdir = phys.Directory(None, testdata.filepath('utils'))
        f = refdir.files[0]
        f.copy(tmpdir)
        f = tmpdir.files[0]
        time.sleep(1) #Let MTime enough time to mean something to fs.auto.
        moved = f.move(tmpdir,'renamed')
        assert moved is f
    
    def test_raise_FSError_on_EnvironmentError(self, tmpdir, monkeypatch):
        def fake_copy_move(src,dest):
            raise EnvironmentError
            
        refdir = phys.Directory(None, testdata.filepath('utils'))
        tmpdir = phys.Directory(None, str(tmpdir))
        monkeypatch.setattr(shutil, 'move', fake_copy_move)
        f = refdir.files[0]
        with raises(fs.FSError):
            f.move(tmpdir, '', True)
        monkeypatch.setattr(shutil, 'copy', fake_copy_move)
        with raises(fs.FSError):
            f.copy(tmpdir, '', True)
    
    def test_child_keeps_its_parent_if_move_fails(self, tmpdir, monkeypatch):
        def fake_copy_move(src,dest):
            raise EnvironmentError
        
        refdir = phys.Directory(None, testdata.filepath('utils'))
        tmpdir = phys.Directory(None, str(tmpdir))
        monkeypatch.setattr(shutil, 'move', fake_copy_move)
        f = refdir.files[0]
        with raises(fs.FSError):
            f.move(tmpdir, '', True)
        assert f.parent is refdir
    
    def test_dont_follow_symlinks(self, tmpdir):
        if sys.platform == 'win32':
            return
        p = str(tmpdir)
        os.mkdir(op.join(p,'foodir'))
        os.symlink(op.join(p,'foodir'),op.join(p,'foodirlink'))
        fp = open(op.join(p,'foofile'),'w')
        fp.close()
        os.symlink(op.join(p,'foofile'),op.join(p,'foofilelink'))
        tmpdir = phys.Directory(None,p)
        eq_(1,tmpdir.dircount)
        eq_(1,tmpdir.filecount)
    
    def test_rename_to_a_unicode_name(self, tmpdir):
        #The problem that happened here is that an OperationError is raised because \u00e9 is
        #compared with e\u0301. in auto._do_update(). Thus f is removed from tmpdir because it
        #thinks that it's not there anymore. We can fix this by normalizing the rename.
        #Directory.move, as well as copy should be tested too, but I move all this normalization
        #down to fs.Node level. Therefore, no need to test them.
        tmppath = str(tmpdir)
        to_rename = open(op.join(tmppath, 'gotta_rename'),'w')
        to_rename.close()
        tmpdir = phys.Directory(None, tmppath)
        if 'renamede\u0301' in tmpdir:
            tmpdir['renamede\u0301'].delete()
        f = tmpdir['gotta_rename']
        f.move(tmpdir,'renamed\u00e9')
        assert f.parent is not None # f should still be present in tmpdir
        f.delete()
    
    def test_path_str_on_path_that_dont_exist(self):
        #The __GetPathStr code had a bug where it would look in str(parent.path) even if parent
        #was None, thus causing an AttributeError.
        d = phys.Directory(None, 'does_not_exist')
        eq_('does_not_exist', str(d.path))
    
    def test_listdir_is_always_called_with_unicode(self, monkeypatch):
        def listdir(path):
            self.lastcall = path
            return []
        
        monkeypatch.setattr(os, 'listdir', listdir)
        d = phys.Directory(None, '')
        d[:]
        assert isinstance(self.lastcall, str)
    
    def test_get_mtime_cooldown(self, tmpdir, monkeypatch):
        monkeypatch.setattr(os, 'stat', log_calls(os.stat))
        tmppath = str(tmpdir)
        d = phys.Directory(None, tmppath) #empty
        d[:]
        len(d)
        'foo' in d
        eq_(1, len(os.stat.calls))
        time.sleep(1)
        # Create a new file
        open(op.join(tmppath, 'somefile'), 'w').close()
        assert 'somefile' in d
    
    def test_is_Node(self):
        assert issubclass(phys.Directory, phys.Node)
    
    def test_handle_subdir_deletion_gracefully(self, tmpdir):
        tmppath = Path(str(tmpdir))
        io.mkdir(tmppath + 'sub')
        io.mkdir(tmppath + 'sub/dir')
        root = phys.Directory(None, str(tmppath))
        root.dirs[0].dirs
        io.rmdir(tmppath + 'sub/dir')
        io.rmdir(tmppath + 'sub')
        root.force_update()
        try:
            root.dirs
        except fs.InvalidPath:
            self.fail()
    

class TestNode:
    # These tests are done on a directory, but they apply to both Directory and File
    def test_rename(self, tmpdir):
        tmppath = str(tmpdir)
        os.mkdir(op.join(tmppath,'gotta_rename'))
        root = phys.Directory(None, tmppath)
        gotta_rename = root['gotta_rename']
        gotta_rename.rename('foo\xe9')
        eq_('foo\xe9', gotta_rename.name)
        assert op.exists(str(gotta_rename.path))
    
    def test_rename_already_exists(self, tmpdir):
        tmppath = str(tmpdir)
        os.mkdir(op.join(tmppath,'dir1'))
        os.mkdir(op.join(tmppath,'dir2'))
        root = phys.Directory(None, tmppath)
        dir1 = root['dir1']
        with raises(fs.AlreadyExistsError):
            dir1.rename('dir2')
        assert op.exists(str(dir1.path))
    
    def test_rename_goes_wrong(self, tmpdir, monkeypatch):
        # On osx, a rename fails with a OSError[1] when the file is locked. For testing, we'll fake it.
        def rename(old, new):
            raise OSError()
        
        monkeypatch.setattr(os, 'rename', rename)
        tmppath = str(tmpdir)
        os.mkdir(op.join(tmppath,'gotta_rename'))
        root = phys.Directory(None, tmppath)
        gotta_rename = root['gotta_rename']
        with raises(phys.OperationError):
            gotta_rename.rename('foo')
        eq_('gotta_rename', gotta_rename.name)
    
    def test_rename_auto_update_happens_before_name_is_changed(self, tmpdir):
        tmppath = str(tmpdir)
        os.mkdir(op.join(tmppath,'gotta_rename'))
        root = phys.Directory(None, tmppath)
        gotta_rename = root['gotta_rename']
        root._Directory__lastupdate = 0
        try:
            gotta_rename.rename('foo')
        except fs.AlreadyExistsError:
            self.fail('Renaming shouldnt cause a false AlreadyExistsError')
    
    def test_rename_auto_update_happens_during_rename_operation(self, tmpdir, monkeypatch):
        # The auto updates happens during the rename operation. When it fails, it means that trying 
        # to revert to the old name will fail as well when using a "revert to the old name" paradigm.
        def rename(old, new):
            root._Directory__lastupdate = 0
            raise OSError()
        
        monkeypatch.setattr(os, 'rename', rename)
        tmppath = str(tmpdir)
        os.mkdir(op.join(tmppath,'gotta_rename'))
        root = phys.Directory(None, tmppath)
        gotta_rename = root['gotta_rename']
        try:
            gotta_rename.rename('foo')
        except fs.AlreadyExistsError:
            self.fail()
        except phys.OperationError:
            pass #This is what we expect
    

class TestFile:
    def test_is_Node(self):
        assert issubclass(phys.File, phys.Node)
    
