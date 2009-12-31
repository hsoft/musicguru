# Created By: Virgil Dupras
# Created On: 2006/10/03
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import sqlite3 as sqlite
import os.path as op
import time
import weakref

from nose.tools import eq_

import hsfs as fs
from .. import manualfs
from hsutil.job import Job, JobCancelled
from hsutil.testcase import TestCase

from ._sql import *

INFO_SAMPLE = {
    'foo': 'bar',
    'baz': 42,
    'int_in_str': '42',
    'long': 42L
}

class FakeFile(manualfs.File):
    def _read_all_info(self, attrnames=None):
        super(FakeFile, self)._read_all_info(attrnames)
        self.root.callcount += 1        
    
    def _read_info(self, field):
        if field == 'mtime':
            self.mtime = 42
        elif field == 'md5':
            self.md5 = self.name
    

def getref():
    ref = manualfs.Directory()
    ref.cls_file_class = FakeFile
    ref.callcount = 0
    d1 = ref.new_directory('sub1')
    d2 = ref.new_directory('sub2')
    d1.cls_file_class = FakeFile
    d2.cls_file_class = FakeFile
    f1 = ref.new_file('file1')
    f2 = d1.new_file('file2')
    f3 = d2.new_file('file3')
    return ref

class TCDirectory(TestCase):
    def test_new_directory(self):
        root = Root(threaded=False)
        d = root.new_directory('bar')
        self.assertEqual('bar',d.name)
        self.assert_(root is d.parent)
        self.assert_(d in root)
        self.assert_(root[0] is d)
        self.assert_(root.dirs[0] is d)
    
    def test_persistence(self):
        p = self.tmpdir()
        dbpath = op.join(p,'fs.db')
        root = Root(dbpath, 'root', threaded=False)
        root.new_directory('bar')
        root.con.close()
        root = Root(dbpath, 'root', threaded=False)
        self.assertEqual('bar',root[0].name)
    
    def test_two_subdir_levels(self):
        root = Root(threaded=False)
        d1 = root.new_directory('foo')
        d2 = d1.new_directory('bar')
        self.assert_(root[0][0] is d2)
        self.assertEqual('bar',d2.name)
    
    def test_escaping(self):
        root = Root(threaded=False)
        try:
            d1 = root.new_directory('foo\'bar')
            self.assertEqual('foo\'bar',d1.name)
        except sqlite.OperationalError:
            self.fail()
    
    def test_new_file(self):
        root = Root(threaded=False)
        d = root.new_directory('subdir')
        root.new_file('foo')
        file = d.new_file('bar')
        self.assertEqual('foo',root.files[0].name)
        self.assertEqual('bar',root.dirs[0].files[0].name)
        self.assert_(isinstance(file,File))
    
    def test_name_collisions(self):
        root = Root(threaded=False)
        root.new_directory('foo')
        self.assertRaises(fs.AlreadyExistsError,root.new_directory,'foo')
        self.assertRaises(fs.AlreadyExistsError,root.new_file,'foo')
    
    def test_unicode(self):
        root = Root(threaded=False)
        d = root.new_directory(u'foo\u00e9')
        self.assertEqual(u'foo\u00e9',d.name)
    

class TCFile(TestCase):
    def test_escaping(self):
        root = Root(threaded=False)
        try:
            f = root.new_file('foo\'bar')
            self.assertEqual('foo\'bar',f.name)
        except sqlite.OperationalError:
            self.fail()
    

class TCAttr_multiple(TestCase):
    def test_attrs(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attrs(INFO_SAMPLE)
        result = f._get_attrs()
        self.assertEqual(INFO_SAMPLE, dict(result))
    
    def test_attrs_persistence(self):
        p = self.tmpdir()
        dbpath = op.join(p,'fs.db')
        root = Root(dbpath, threaded=False)
        f = root.new_file('foobar')
        f._set_attrs(INFO_SAMPLE)
        root.con.close()
        root = Root(dbpath, threaded=False)
        f = root[0]
        result = f._get_attrs()
        self.assertEqual(INFO_SAMPLE, dict(result))
    
    def test_set_attrs_twice(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attrs(INFO_SAMPLE)
        f._set_attrs(INFO_SAMPLE)
        sql = "select count(*) from attrs"
        result = f.con.execute(sql)
        self.assertEqual(len(INFO_SAMPLE), result.fetchall()[0][0])
    
    def test_dir_attrs(self):
        #This test is just to verify that the _get_attrs _set_attrs func are at the Node level.
        #Tests in File are assumed.
        root = Root(threaded=False)
        subdir = root.new_directory('foobar')
        subdir._set_attrs(INFO_SAMPLE)
        result = subdir._get_attrs()
        self.assertEqual(INFO_SAMPLE, dict(result))
    
    def test_escaping(self):
        #Hey, this test nver failed because of my use of 'cur.executemany'
        root = Root(threaded=False)
        d = {'foo': 'foo\'bar'}
        f = root.new_file('foobar')
        try:
            f._set_attrs(d)
        except sqlite.OperationalError:
            self.fail()
    

class TCAttr_single(TestCase):
    def test_str(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo','bar')
        self.assertEqual('bar',f._get_attr('foo'))
    
    def test_int(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo',42)
        self.assertEqual(42,f._get_attr('foo'))
    
    def test_str_int(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo','42')
        self.assertEqual('42',f._get_attr('foo'))
    
    def test_set_same_attr_twice(self):
        #When that happens, we don't want two rows in the db, we want an update to happen.
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo',1)
        f._set_attr('foo',2)
        self.assertEqual(2,f._get_attr('foo'))
        result = root.con.execute("select * from attrs")
        self.assertEqual(1, len(result.fetchall()))
    
    def test_escaping(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        try:
            f._set_attr('foo','foo\'bar')
        except sqlite.OperationalError:
            self.fail()
    
    def test_raise_key_error_if_not_exists(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        self.assertRaises(KeyError,f._get_attr,'foo')
    
    def test_unicode(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo',u'foo\u00e9')
        self.assertEqual(u'foo\u00e9',f._get_attr('foo'))
    
    def test_binary(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo','\x0e\xff')
        self.assertEqual('\x0e\xff',f._get_attr('foo'))
    
    def test_replace_newline_and_cr(self):
        root = Root(threaded=False)
        f = root.new_file('foobar')
        f._set_attr('foo','foo\rbar\n')
        self.assertEqual('foobar',f._get_attr('foo'))
    

class TC_delete(TestCase):
    def test_that_objects_are_gone(self):
        root = Root(threaded=False)
        f = root.new_file('file')
        d = root.new_directory('dir')
        f.delete()
        self.assertEqual(1,len(root))
        d.delete()
        self.assertEqual(0,len(root))
    
    def test_transaction_is_commited(self):
        p = self.tmpdir()
        dbpath = op.join(p,'fs.db')
        root = Root(dbpath, threaded=False)
        f = root.new_file('file')
        f.delete()
        root.con.close()
        root = Root(dbpath, threaded=False)
        result = root.con.execute("select * from nodes")
        self.assertEqual(0, len(result.fetchall()))
    
    def test_also_delete_attrs(self):
        root = Root(threaded=False)
        f = root.new_file('file')
        d = root.new_directory('dir')
        f._set_attrs(INFO_SAMPLE)
        d._set_attrs(INFO_SAMPLE)
        f.delete()
        d.delete()
        result = root.con.execute("select * from attrs")
        self.assertEqual(0, len(result.fetchall()))
    
    def test_delete_dir_then_add_file_with_same_name(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        d.delete()
        result = root.new_file('foo')
        self.assert_(isinstance(result,File))
    
    def test_that_delete_is_recursive(self):
        root = Root(threaded=False)
        d1 = root.new_directory('dir1')
        d2 = root.new_directory('dir2')
        sd1 = d1.new_directory('dir')
        sd1.new_file('file1')
        sd1.new_file('file2')
        d1.delete()
        result = root.con.execute("select * from nodes")
        self.assertEqual(1, len(result.fetchall())) #Only d2 should be left
    

class TCUpdate_initial(TestCase):
    #Only test the first call of Update on a Directory
    def test_that_dirs_and_files_are_added(self):
        root = Root(threaded=False)
        root.update(getref())
        self.assert_('sub1' in root)
        self.assert_('sub2' in root)
        self.assert_('file1' in root)
        self.assert_('file2' in root['sub1'])
        self.assert_('file3' in root['sub2'])
    
    def test_that_attrs_are_set(self):
        root = Root(threaded=False)
        ref = getref()
        for f in ref.allfiles:
            f._read_all_info()
            f.md5 = f.name
        root.update(ref)
        self.assertEqual('file1',root['file1'].md5)
        self.assertEqual('file2',root['sub1']['file2'].md5)
        self.assertEqual('file3',root['sub2']['file3'].md5)
    
    def test_that_attrs_are_set_with_persistence(self):
        p = self.tmpdir()
        dbpath = op.join(p,'fs.db')
        root = Root(dbpath, threaded=False)
        ref = getref()
        for f in ref.allfiles:
            f._read_all_info()
            f.md5 = f.name
        root.update(ref)
        root.con.close()
        root = Root(dbpath, threaded=False)
        self.assertEqual('file1',root['file1'].md5)
        self.assertEqual('file2',root['sub1']['file2'].md5)
        self.assertEqual('file3',root['sub2']['file3'].md5)
    
    def test_update_files_with_higher_mtime(self):
        root = Root(threaded=False)
        ref = getref()
        for f in ref.allfiles:
            f._read_all_info()
            f.md5 = f.name
        root.update(ref)
        ref['file1'].md5 = 'changed'
        ref['sub1']['file2'].md5 = 'changed'
        ref['sub1']['file2'].mtime = time.time() + 1
        root.update(ref)
        self.assertEqual('file1',root['file1'].md5)
        self.assertEqual('changed',root['sub1']['file2'].md5)
    
    def test_only_read_selected_attrs(self):
        root = Root(threaded=False)
        assert root._attrs_to_read is None
        root._attrs_to_read = ['mtime']
        root.update(getref())
        f = root.allfiles[0]
        eq_(f.md5, '') # md5 has not been read
    
    def test_cancel(self):
        def callback(progress):
            self.log.append(progress)
            return len(self.log) < 5
        
        self.log = []
        job = Job(1,callback)
        root = Root(threaded=False)
        ref = getref()
        try:
            root.update(ref,job=job)
            self.fail("Should have cancelled")
        except JobCancelled:
            pass
        self.assertEqual(0,len(root))
    

class TCUpdate_subsequent(TestCase):
    #Test what happens when Update is called a second time.
    def setUp(self):
        def FakeReadAllInfo(instance,sections=None):
            self.callcount += 1
            self.oldread(instance,sections)
        
        self.callcount = 0
        self.oldread = manualfs.File._read_all_info
        manualfs.File._read_all_info = FakeReadAllInfo
        root = Root(threaded=False)
        ref = getref()
        root.update(ref)
        self.root = root
        self.ref = ref
        
    def tearDown(self):
        manualfs.File._read_all_info = self.oldread
    
    def test_files_were_added(self):
        root,ref = self.root,self.ref
        ref.new_file('file4')
        root.update(ref)
        self.assertEqual(2,root.filecount)
    
    def test_always_update_zero_mtime_nodes(self):
        #We always want attrs to be read when a sql file mtime is zero, event if the ref mtime
        # is also zero.
        root,ref = self.root,self.ref
        reffile = ref.new_file('file4')
        reffile.mtime #read info
        reffile.mtime = 0
        reffile.size = 42
        root.update(ref)
        self.assertEqual(2,root.filecount)
        file4 = root['file4']
        self.assertEqual(42,file4.size)
    
    def test_files_were_removed(self):
        root,ref = self.root,self.ref
        ref.files[0].delete()
        ref.dirs[0].files[0].delete()
        root.update(ref)
        self.assertEqual(1,len(root.allfiles))
    
    def test_dirs_were_added(self):
        root,ref = self.root,self.ref
        ref.new_directory('sub3')
        root.update(ref)
        self.assertEqual(3,root.dircount)
    
    def test_dirs_were_removed(self):
        root,ref = self.root,self.ref
        ref.dirs[0].delete()
        root.update(ref)
        self.assertEqual(1,root.dircount)
    
    def test_file_removed_and_added_as_dir(self):
        root,ref = self.root,self.ref
        ref['file1'].delete()
        ref.new_directory('file1')
        root.update(ref)
        self.assertEqual(3,root.dircount)
        self.assertEqual(0,root.filecount)
    
    def test_dir_removed_and_added_as_file(self):
        root,ref = self.root,self.ref
        ref['sub1'].delete()
        ref.new_file('sub1')
        root.update(ref)
        self.assertEqual(1,root.dircount)
        self.assertEqual(2,root.filecount)
    
    def test_file_removed_and_added_as_dir(self):
        root,ref = self.root,self.ref
        ref['file1'].delete()
        ref.new_directory('file1')
        root.update(ref)
        self.assertEqual(3,root.dircount)
        self.assertEqual(0,root.filecount)
    

class TCJobs(TestCase):
    def test_Update(self):
        def callback(progress):
            self.log.append(progress)
            return True
        
        self.log = []
        job = Job(1,callback)
        root = Root(threaded=False)
        ref = getref()
        root.update(ref,job=job)
        self.assertEqual(0,self.log[0])
        self.assertEqual(100,self.log[-1])
    

class TCfind_node_of_id(TestCase):
    def test_id_is_self(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        self.assert_(root.find_node_of_id(root.id) is root)
    
    def test_find_id_not_in_self(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        self.assert_(root.find_node_of_id(42) is None)
    
    def test_find_id_in_children(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        self.assert_(root.find_node_of_id(d.id) is d)
    
    def test_id_cache_is_weakref(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        w = weakref.ref(d)
        root.find_node_of_id(d.id)
        d.delete()
        root[:] #Perform the actual delete
        del d
        self.assert_(w() is None)
    
    def test_check_cache_validity(self):
        #Ok, the cache is weakref. But what if something else keeps the object alive?
        #The cache would return an erronous value.
        root = Root(threaded=False)
        d = root.new_directory('foo')
        root.find_node_of_id(d.id)
        d.delete()
        self.assert_(root.find_node_of_id(d.id) is None)
    
    def test_node_was_deleted_and_a_new_node_was_created_with_the_same_id(self):
        root = Root(threaded=False)
        d1 = root.new_directory('foo')
        root.find_node_of_id(d1.id)
        d1.delete()
        root[:] #Remove d1 instance from root
        d2 = root.new_directory('foo') #Should have same id as d1
        self.assert_(root.find_node_of_id(d2.id) is d2)
    
    def test_two_levels_deep(self):
        root = Root(threaded=False)
        d = root.new_directory('foo')
        f = d.new_file('bar')
        self.assert_(root.find_node_of_id(f.id) is f)
    