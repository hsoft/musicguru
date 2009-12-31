# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2005-01-14
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import weakref
import gc

from nose.tools import eq_, assert_raises

from hsutil import job
from hsutil.decorators import log_calls
from hsutil.path import Path

import hsfs as fs
from .manualfs import *

SUBDIR_COUNT = 5

class TestDir(Directory):
    def AddDir(self,dirname):
        return TestDir(self,dirname)
    
    def AddFile(self,filename):
        return self._create_sub_file(filename)
    

def BuildBigSample():
    root = TestDir(None,'root')
    for i in xrange(SUBDIR_COUNT):
        root.AddFile('file%d' % i)
        xDir1 = root.AddDir('dir%d' % i)
        for j in xrange(SUBDIR_COUNT):
            xDir1.AddFile('file%d' % j)
            xDir2 = xDir1.AddDir('dir%d%d' % (i,j))
            for k in xrange(SUBDIR_COUNT):
                xDir2.AddFile('file%d' % k)
                xDir2.AddDir('dir%d%d%d' % (i,j,k))
    return root

def testadd_path():
    root = TestDir(None,'root')
    mypath = 'foo/bar'
    addeddir = root.add_path(Path(mypath))
    eq_(addeddir.name,'bar')
    eq_(addeddir.path,('root','foo','bar'))
    eq_(addeddir.parent.name,'foo')
    assert root.find_sub_dir('foo') is not None
    eq_(root.find_sub_dir('FOO'),None)
    root.AddFile('bar')
    try:
        addeddir = root.add_path(Path('bar/foo'))
        raise AssertionError()
    except fs.InvalidPath:
        pass
    
def testClear():
    root = BuildBigSample()
    root.clear()
    eq_(root.dircount,0)
    eq_(root.filecount,0)

def test_delete():
    root = BuildBigSample()
    refdir = root.dirs[0]
    nextdir = root.dirs[1]
    assert root.dirs[0] is refdir
    refdir.delete()
    assert root.dirs[0] is nextdir
    eq_(root.dircount, SUBDIR_COUNT - 1)

def test_rename():
    root = BuildBigSample()
    refdir = root.AddDir('a')
    #refdir should have been added at the start
    assert root.dirs[0] is refdir
    eq_(refdir.name,'a')
    refdir.rename('z')
    #refdir should have moved to the end
    assert root.dirs[0] is not refdir
    assert root.dirs[-1] is refdir
    eq_(refdir.name,'z')

def test_move():
    root = TestDir(None,'root')
    refdir = TestDir(None,'foobar')
    reffile = refdir.AddFile('foobarfile')
    refsubdir = refdir.AddDir('bleh')
    refsubfile = refsubdir.AddFile('bleh.test')
    eq_(root.find_sub_file('foobarfile'),None)
    eq_(root.find_sub_dir('bleh'),None)
    eq_(refdir.find_sub_file('foobarfile'),reffile)
    eq_(refdir.find_sub_dir('bleh'),refsubdir)
    reffile.move(root)
    eq_(root.find_sub_file('foobarfile'),reffile)
    eq_(refdir.find_sub_file('foobarfile'),None)
    #move it back, and change it's name
    reffile.move(refdir,'blehfile')
    eq_(root.find_sub_file('blehfile'),None)
    eq_(refdir.find_sub_file('blehfile'),reffile)
    eq_(root.find_sub_file('foobarfile'),None)
    eq_(refdir.find_sub_file('foobarfile'),None)
    #move the subdir
    refsubdir.move(root)
    eq_(root.find_sub_dir('bleh'),refsubdir)
    eq_(refdir.find_sub_dir('bleh'),None)
    eq_(refsubfile.parent.path,('root','bleh'))
    #move it back with a different name
    refsubdir.move(refdir,'bleh2')
    eq_(root.find_sub_dir('bleh'),None)
    eq_(refdir.find_sub_dir('bleh'),None)
    eq_(root.find_sub_dir('bleh2'),None)
    eq_(refdir.find_sub_dir('bleh2'),refsubdir)
    eq_(refsubfile.parent.path,('foobar','bleh2'))

def test_move_file_conflict_with_directory_name():
    source = TestDir(None,'source')
    source_file = source.AddFile('foobar')
    dest = TestDir(None,'dest')
    dest_dir = dest.AddDir('foobar')
    assert_raises(fs.AlreadyExistsError, source_file.move, dest)
    assert source_file in source

def test_already_exists():
    ref = TestDir(None,'')
    ref.AddFile('foobar')
    assert_raises(fs.AlreadyExistsError, ref.AddFile, 'foobar')
    assert_raises(fs.AlreadyExistsError, ref.AddDir, 'foobar')

def test_move_dir_conflict():
    dir1 = TestDir(None,'')
    dir2 = TestDir(None,'')
    subdir = dir1.AddDir('foobar')
    dir2.AddFile('foobar')
    assert_raises(fs.AlreadyExistsError, subdir.move, dir2)
    assert 'foobar' in dir1
    assert 'foobar' in dir2

def test_auto_conflict():
    class FoobarManual(TestDir):
        def _resolve_conflict(self,offended,offender,conflicted_name):
            return 'foobar'
        
    
    ref = FoobarManual(None,'')
    ref.AddFile('foo')
    ref.AddFile('foo')
    assert 'foobar' in ref
    assert isinstance(ref[0], fs.File)
    assert isinstance(ref[1], fs.File)

def test_auto_conflict_move():
    class FoobarManual(TestDir):
        def _resolve_conflict(self,offended,offender,conflicted_name):
            return 'foobar'
        
    
    ref1 = FoobarManual(None,'')
    file1 = ref1.AddFile('foo')
    ref2 = FoobarManual(None,'')
    ref2.AddFile('foo')
    file1.move(ref2)
    assert 'foobar' in ref2

def test_file_delete_direct():
    root1 = TestDir(None,'')
    file1 = root1.AddFile('foobar')
    file1.delete()
    assert file1 not in root1

def test_file_move_direct():
    root1 = TestDir(None,'')
    file1 = root1.AddFile('foobar')
    root2 = TestDir(None,'')
    file1.move(root2)
    assert file1 in root2
    assert file1 not in root1

def test_file_rename_direct():
    root1 = TestDir(None,'')
    file1 = root1.AddFile('foo')
    assert 'foo' in root1
    file1.rename('bar')
    assert 'foo' not in root1
    assert 'bar' in root1

def test_clean_empty_dirs_simple():
    root = TestDir(None,'')
    root.AddDir('foobar')
    eq_(1, len(root))
    root.clean_empty_dirs()
    eq_(0, len(root))

def test_clean_empty_dirs_with_file_inside():
    root = TestDir(None,'')
    dir = root.AddDir('foobar')
    dir.AddFile('foobar')
    eq_(1, len(root))
    root.clean_empty_dirs()
    eq_(1, len(root))

def test_clean_empty_dirs_recursive():
    root = TestDir(None,'')
    dir1 = root.AddDir('foo')
    subfile = dir1.AddFile('foobar')
    dir2 = root.AddDir('bar')
    dir2.AddDir('foobar')
    eq_(2, len(root))
    root.clean_empty_dirs()
    eq_(1, len(root))
    subfile.delete()
    root.clean_empty_dirs()
    eq_(0, len(root))

def test_resolve_conflict_excpetion():
    # What happens is that I made a big mistake in _conflict_check, and when there is a conflict and
    # there is nothing in _resolve_conflict, the exception isn't raised properly
    foo = TestDir(None,'foo')
    foo.AddFile('bar')
    try:
        bar = File(None,'bar')
        foo.add_child(bar)
        raise AssertionError()
    except fs.AlreadyExistsError as e:
        eq_('bar', e.name)
        eq_('foo', e.parentname)

def test_resolve_conflict_on_rename():
    class FoobarManual(TestDir):
        def _resolve_conflict(self,offended,offender,conflicted_name):
            return 'foobar'
        
    
    ref = FoobarManual(None,'')
    ref.AddFile('foo')
    file = ref.AddFile('bar')
    dir = ref.AddDir('bleh')
    file.rename('foo')
    assert 'foobar' in ref
    file.rename('bar')
    assert 'foobar' not in ref
    dir.rename('foo')
    assert 'foobar' in ref
    dir.rename('bleh')
    assert 'foobar' not in ref
    file.name = 'foo'
    assert 'foobar' in ref
    file.name = 'bar'
    assert 'foobar' not in ref
    dir.name = 'foo'
    assert 'foobar' in ref
    dir.name = 'bleh'
    assert 'foobar' not in ref

def test_resolve_conflict_on_init():
    class FoobarManual(Directory):
        def _resolve_conflict(self,offended,offender,conflicted_name):
            return 'foobar'
        
    
    ref = FoobarManual(None,'')
    file1 = File(ref,'foo')
    file2 = File(ref,'foo')
    assert 'foobar' in ref
    file2.name = 'bar'
    assert 'foobar' not in ref
    dir = Directory(ref,'foo')
    assert 'foobar' in ref

def test_case_sensitive():
    root = Directory(None,'')
    root.case_sensitive = False
    f1 = File(root,'foo')
    try:
        f2 = File(root,'FoO')
        raise AssertionError()
    except fs.AlreadyExistsError:
        pass
    f2 = File(root,'bar')
    try:
        f2.name = 'FoO'
        raise AssertionError()
    except fs.AlreadyExistsError:
        pass
    #test that int access works
    assert root[0] is f1

def test_case_sensitive_in_subdir():
    root = Directory(None,'')
    root.case_sensitive = False
    new = root.new_directory('foobar')
    assert not new.case_sensitive
    root.case_sensitive = True
    assert new.case_sensitive

def test_case_sensitive_after_copy():
    ref = Directory(None,'')
    ref.case_sensitive = True
    ref.new_file('FOO')
    root = Directory(None,'')
    root.case_sensitive = False
    root.add_dir_copy(ref)
    assert not root[0].case_sensitive
    eq_('FOO', root[0]['foo'].name)

def test_new_directory():
    root = Directory(None,'')
    new = root.new_directory('foobar')
    eq_('foobar', new.name)
    eq_('foobar', root.dirs[0].name)

def test_new_file():
    root = Directory(None,'')
    new = root.new_file('foobar')
    eq_('foobar', new.name)
    eq_('foobar', root.files[0].name)

def test_copy():
    # Both add_dir_copy and add_file_copy are tested here
    root = BuildBigSample()
    refdir = TestDir(None,'foobar')
    refdir.AddFile('file1')
    refdir.AddFile('file2')
    refdir.AddFile('file3')
    foobar = root.add_dir_copy(refdir)
    addeddir = root.dirs[-1]
    assert addeddir is not refdir
    eq_(addeddir.name,refdir.name)
    eq_(addeddir.filecount,refdir.filecount)
    reffile = refdir.files[0]
    addedfile = addeddir.files[0]
    assert addedfile is not reffile
    eq_(addedfile.name,reffile.name)
    reffile = refdir.files[1]
    addedfile = addeddir.files[1]
    assert addedfile is not reffile
    eq_(addedfile.name,reffile.name)
    reffile = refdir.files[2]
    addedfile = addeddir.files[2]
    assert addedfile is not reffile
    eq_(addedfile.name,reffile.name)

def test_copy_file():
    test = Directory(None,'')
    root = Directory(None,'')
    ref = root.new_file('foo')
    ref._read_all_info()
    ref.size = 192
    test.add_file_copy(ref)
    copy = test[0]
    eq_(copy.name,'foo')
    eq_(copy.size,192)

def test_job_cancelled():
    #Start an add_dir_copy with a job param and cancel the job after a while.
    #The exception must go through, and the directory must NOT be added.
    test = Directory(None,'')
    root = Directory(None,'')
    for i in xrange(50):
        root.new_file('foo%d' % i)
    test.add_dir_copy(root,'dir1')
    eq_(1, len(test))
    eq_('dir1', test[0].name)
    mainjob = job.Job(1,lambda progress:progress < 30)
    assert_raises(job.JobCancelled, test.add_dir_copy, root, 'dir2', mainjob)
    eq_(1, len(test))
    eq_('dir1', test[0].name)

def test_add_dir_copy_already_exists():
    ref = TestDir(None,'test')
    root = Directory(None,'')
    root.add_dir_copy(ref,'foobar')
    assert_raises(fs.AlreadyExistsError, root.add_dir_copy, ref, 'foobar')

def test_original():
    root1 = TestDir(None,'')
    file1 = root1.AddFile('foobar')
    root2 = TestDir(None,'')
    root2.copy(root1)
    file2 = root2[0]
    root3 = TestDir(None,'')
    root3.copy(root2)
    file3 = root3[0]
    assert file3.copyof is file2
    assert file2.copyof is file1
    assert file3.original is file1

def test_original_with_dir():
    dir1 = TestDir(None,'')
    file1 = dir1.AddFile('foobar')
    dir2 = TestDir(None,'')
    dir3 = TestDir(None,'')
    dir2.copy(dir1)
    dir3.copy(dir2)
    assert dir1.original is dir1
    assert dir2.original is dir1
    assert dir3.original is dir1
    assert file1.original is file1
    assert dir2[0].original is file1
    assert dir3[0].original is file1

def test_original_not_being_a_Copy_instance():
    original = fs.Directory(None,'')
    copy = Directory(None,'')
    copy.copy(original)
    assert copy.original is original

def test_file_copy_direct():
    root = TestDir(None,'')
    file = root.AddFile('foo')
    file.size = 42
    copy = root.AddFile('bar')
    copy.copy(file)
    eq_(copy.size, 42)

def test_detach_copy():
    dir1 = TestDir(None,'')
    file1 = dir1.AddFile('foobar')
    dir2 = TestDir(None,'')
    dir3 = TestDir(None,'')
    dir2.copy(dir1)
    dir3.copy(dir2)
    w1 = weakref.ref(dir2)
    w2 = weakref.ref(dir2[0])
    w3 = weakref.ref(dir1)
    dir3.detach_copy()
    assert dir1.original is dir1
    assert dir2.original is dir1
    assert dir3.original is dir3
    assert file1.original is file1
    assert dir2[0].original is file1
    assert dir3[0].original is dir3[0]
    del dir2
    gc.collect()
    assert w1() is None
    assert w2() is None
    del dir1
    del file1
    gc.collect()
    assert w3() is None

def test_detach_copy_keep_all_original():
    dir1 = TestDir(None,'')
    file1 = dir1.AddFile('foobar')
    dir2 = TestDir(None,'')
    dir3 = TestDir(None,'')
    dir2.copy(dir1)
    dir3.copy(dir2)
    w1 = weakref.ref(dir2)
    w2 = weakref.ref(dir2[0])
    w3 = weakref.ref(dir1)
    dir3.detach_copy(True,True)
    assert dir1.original is dir1
    assert dir2.original is dir1
    assert dir3.original is dir1
    assert file1.original is file1
    assert dir2[0].original is file1
    assert dir3[0].original is file1
    assert dir2.copyof is dir1
    assert dir3.copyof is dir1
    assert dir2[0].copyof is file1
    assert dir3[0].copyof is file1
    del dir2
    gc.collect()
    assert w1() is None
    assert w2() is None
    del dir1
    gc.collect()
    assert w3() is not None

def test_detach_copy_keep_original_files():
    dir1 = TestDir(None,'')
    sub = dir1.AddDir('foo')
    file = sub.AddFile('bar')
    dir2 = TestDir(None,'')
    dir3 = TestDir(None,'')
    dir2.copy(dir1)
    dir3.copy(dir2)
    dir3.detach_copy(True,False)
    assert dir3.original is dir3
    assert dir3[0].original is dir3[0]
    assert dir3[0][0].original is file
    assert dir3.copyof is None
    assert dir3[0].copyof is None
    assert dir3[0][0].copyof is file

def test_detach_copy_keep_original_dirs():
    dir1 = TestDir(None,'')
    sub = dir1.AddDir('foo')
    file = sub.AddFile('bar')
    dir2 = TestDir(None,'')
    dir3 = TestDir(None,'')
    dir2.copy(dir1)
    dir3.copy(dir2)
    dir3.detach_copy(False,True)
    assert dir3.original is dir1
    assert dir3[0].original is sub
    assert dir3[0][0].original is dir3[0][0]
    assert dir3.copyof is dir1
    assert dir3[0].copyof is sub
    assert dir3[0][0].copyof is None

def test_add_file_copy_reads_info():
    @log_calls
    def fake_read_all_info(attrnames=None):
        pass
    f = File(None,'')
    f._read_all_info = fake_read_all_info
    d = Directory(None,'')
    d.add_file_copy(f)
    eq_(len(fake_read_all_info.calls), 1)

def test_file_against_file():
    ref = AutoResolve(None,'')
    file1 = File(ref,'foobar')
    file2 = File(ref,'foobar')
    assert '[000] foobar' in ref

def test_file_against_dir():
    ref = AutoResolve(None,'')
    dir = Directory(ref,'foobar')
    file = File(ref,'foobar')
    assert '[000] foobar' in ref

def test_dir_against_file():
    ref = AutoResolve(None,'')
    file = File(ref,'foobar')
    dir = Directory(ref,'foobar')
    assert '[000] foobar' in ref

def test_dir_against_dir_merge():
    @log_calls
    def on_should_merge(source, dest):
        return True
    
    ref = AutoResolve(None,'')
    ref.on_should_merge = on_should_merge
    dir1 = Directory(ref,'foobar')
    dir2 = Directory(ref,'foo')
    File(dir1,'foo')
    File(dir2,'foo')
    dir2.name = 'foobar'
    call = on_should_merge.calls[0]
    assert call['source'] is dir2
    assert call['dest'] is dir1
    eq_(1, len(ref))
    assert '[000] foobar' not in ref
    eq_(2, len(ref[0]))
    assert 'foo' in ref[0]
    assert '[000] foo' in ref[0]

def test_dir_against_dir_no_merge():
    @log_calls
    def on_should_merge(source, dest):
        return False
    
    ref = AutoResolve(None,'')
    ref.on_should_merge = on_should_merge
    dir1 = Directory(ref,'foobar')
    dir2 = Directory(ref,'foo')
    File(dir1,'foo')
    File(dir2,'foo')
    dir2.name = 'foobar'
    call = on_should_merge.calls[0]
    assert call['source'] is dir2
    assert call['dest'] is dir1
    assert '[000] foobar' in ref

def test_merge_event_called_by_subdir():
    @log_calls
    def on_should_merge(source, dest):
        return True
    
    ref = AutoResolve(None,'')
    ref.on_should_merge = on_should_merge
    dir = AutoResolve(ref,'subdir')
    dir1 = Directory(dir,'foobar')
    dir2 = Directory(dir,'foo')
    File(dir1,'foo')
    File(dir2,'foo')
    dir2.name = 'foobar'
    call = on_should_merge.calls[0]
    assert call['source'] is dir2
    assert call['dest'] is dir1
    assert '[000] foobar' not in dir
    eq_(2,len(dir[0]))
    assert 'foo' in dir[0]
    assert '[000] foo' in dir[0]

def test_conflict_list():
    ref = Directory(None,'')
    dir1 = Directory(ref,'foo')
    dir2 = Directory(ref,'bar')
    File(dir1,'foo')
    File(dir2,'foo')
    root = AutoResolve(None,'')
    root.copy(ref)
    f1 = File(root[0],'foo')
    f2 = File(root[1],'foo')
    eq_([],root.conflicts)
    eq_([f1],root[0].conflicts)
    eq_([f2],root[1].conflicts)
    eq_([f1,f2],root.allconflicts)
    f2.name = 'bar'
    eq_([f1],root.allconflicts)
    f1.name = 'bleh'
    eq_([],root.allconflicts)

def test_that_it_merges():
    root = AutoMerge(None,'')
    dir1 = Directory(root,'foo')
    dir2 = Directory(None,'foo')
    file1 = File(dir1,'bar1')
    file2 = File(dir2,'bar2')
    assert dir1 in root
    assert dir2 not in root
    assert file1 in dir1
    assert file2 in dir2
    dir2.move(root)
    assert dir1 in root
    assert dir2 not in root
    assert file1 in dir1
    assert file2 in dir1

