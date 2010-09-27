# Created By: Virgil Dupras
# Created On: 2004/12/22
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import time
import os
from random import randrange
import sys
from io import StringIO
import weakref
import gc

from hsutil.testutil import eq_

from hsutil.path import Path
from hsutil.testcase import TestCase

from .._fs import *

class TestDir(Directory):
    def AddDir(self,dirname):
        return self._create_sub_dir(dirname)
    
    def AddFile(self,filename):
        return self._create_sub_file(filename)
    

class TCDirectory(TestCase):
    def GenTestDir(self):
        root = TestDir(None,'root')
        root.AddDir('foo').AddFile('bar')
        root.AddDir('bleh').AddDir('bar')
        root.AddFile('foofile')
        root.AddFile('barfile')
        return root
    
    def testDirClass(self):
        #Test that the default behavior of _create_sub_dir is to create the same instance as self
        root = self.GenTestDir()
        self.assert_(isinstance(root[0],TestDir))
    
    def testDirName(self):
        root = self.GenTestDir()
        self.assertEqual(root.name,'root')
        self.assertEqual(root[0].name,'foo')
        self.assertEqual(root[1].name,'bleh')
        self.assertEqual(root[1][0].name,'bar')
    
    def testFileName(self):
        root = self.GenTestDir()
        self.assertEqual(root[2].name,'foofile')
        self.assertEqual(root[3].name,'barfile')
    
    def testParentDir(self):
        root = self.GenTestDir()
        self.assert_(root[0].parent is root)
        self.assert_(root[0][0].parent is root[0])
    
    def testParentList(self):
        root = self.GenTestDir()
        self.assertEqual([root], list(root[0].parents))
        self.assertEqual([root, root[0]], list(root[0][0].parents))
    
    def testSubDirCount(self):
        root = self.GenTestDir()
        self.assertEqual(2,root.dircount)
        self.assertEqual(0,root[0].dircount)
        self.assertEqual(1,root[1].dircount)
    
    def testSubFileCount(self):
        root = self.GenTestDir()
        self.assertEqual(2,root.filecount)
        self.assertEqual(1,root[0].filecount)
        self.assertEqual(0,root[1].filecount)
    
    def testfind_sub_dir(self):
        root = self.GenTestDir()
        self.assert_(root.find_sub_dir('foo') is root[0])
        self.assert_(root.find_sub_dir('foofile') is None)
        self.assert_(root.find_sub_dir('invalid') is None)
    
    def testfind_sub_file(self):
        root = self.GenTestDir()
        self.assert_(root.find_sub_file('foofile') is root[2])
        self.assert_(root.find_sub_file('foo') is None)
        self.assert_(root.find_sub_file('invalid') is None)
    
    def test_root(self):
        root = self.GenTestDir()
        self.assert_(root.root is root)
        self.assert_(root.dirs[0].root is root)
        self.assert_(root.dirs[0].dirs[0].root is root)
    
    def testAllDirs(self):
        root = self.GenTestDir()
        self.assertEqual(3,len(root.alldirs))
        self.assert_(root[0] in root.alldirs)
        self.assertEqual(set(root.alldirs), set(root.iteralldirs()))
    
    def testAllFiles(self):
        root = self.GenTestDir()
        self.assertEqual(3,len(root.allfiles))
        self.assert_(root[2] in root.allfiles)
        self.assertEqual(set(root.allfiles), set(root.iterallfiles()))
    
    def testStats(self):
        root = self.GenTestDir()
        self.assertEqual(root.get_stat('dircount'),3)
        self.assertEqual(root.get_stat('filecount'),3)
        self.assertEqual(root.get_stat('Size'),0)
        self.assertEqual(root.get_stat('extension',[]),[])
        root.AddFile('test.test')
        self.assertEqual(root.get_stat('extension'),['test'])
        self.assertEqual(root.get_stat('filecount'),4)
        bazdir = root.AddDir('baz')
        self.assertEqual(root.get_stat('extension'),['test'])
        f = bazdir.AddFile('baz.bleh')
        self.assertEqual(root.get_stat('extension'),['test','bleh'])
        f.parent = None
        self.assertEqual(root.get_stat('extension'),['test'])
    
    def test_already_exist_on_init(self):
        #Create a Directory that already exists in the parent
        #supplied as a parameter to the init func
        root = Directory(None,'root')
        Directory(root,'foobar')
        try:
            File(root,'foobar')
            self.fail()
        except AlreadyExistsError:
            pass
    
    def test_override_sort_key(self):
        #Override _sort_key for a function that would return the opposite order.
        class OverrideTest(TestDir):
            _sort_key = staticmethod(lambda x: -ord(x.name[0]))
        
        root = OverrideTest(None,'root')
        root.AddDir('a')
        root.AddDir('b')
        self.assertEqual('b',root.dirs[0].name)
        root.AddFile('c')
        root.AddFile('d')
        self.assertEqual('d',root.files[0].name)
    
    def test_is_container(self):
        root = TestDir(None,'foo')
        file = root.AddFile('bar')
        self.assertEqual(True,root.is_container)
        self.assertEqual(False,file.is_container)
    
    def test_child_sort_case_insensitive(self):
        root = TestDir(None,'root')
        root.AddDir('a')
        root.AddDir('B')
        self.assertEqual('a',root.dirs[0].name)
        root.AddFile('c')
        root.AddFile('D')
        self.assertEqual('c',root.files[0].name)
    
    def test_weakref(self):
        parent = Directory(None,'foo')
        w1 = weakref.ref(parent)
        w2 = weakref.ref(Directory(parent,'bar'))
        w3 = weakref.ref(File(parent[0],'bleh'))
        self.assert_(w1() is not None)
        self.assert_(w2() is not None)
        self.assert_(w3() is not None)
        del parent
        gc.collect()
        self.assert_(w1() is None)
        self.assert_(w2() is None)
        self.assert_(w3() is None)
    
    def test_alldirs_dont_go_further_if_child_is_not_container(self):
        #It may happen (like in the Bundle case) that a Node kind of lie about
        #its is_container status. Wheter it lies or not, if a Node says that is_container
        #is false, alldirs must NOT get it's subdirectories.
        class Liar(Directory):
            cls_is_container = False
        
        d = Directory(None,'')
        l = Liar(d,'liar')
        Directory(d,'foo')
        Directory(l,'bar')
        self.assertEqual(1,len(d.alldirs))
        self.assertEqual(set(d.alldirs) ,set(d.iteralldirs()))
    
    def test_allfiles_dont_go_further_if_child_is_not_container(self):
        #same thing as alldirs
        class Liar(Directory):
            cls_is_container = False
        
        d = Directory(None,'')
        l = Liar(d,'liar')
        File(d,'foo')
        File(l,'bar')
        self.assertEqual(2,len(d.allfiles)) #Liar is in fact counted as a file
        self.assertEqual(set(d.allfiles), set(d.iterallfiles()))
    

class TCFSNode(TestCase):
    def setUp(self):
        self.global_setup()
    
    def tearDown(self):
        self.global_teardown()
    
    def test_rename_exception(self):
        root = TestDir(None,'root')
        foo = root.AddFile('foo')
        bar = root.AddFile('bar')
        try:
            bar.name = 'foo'
            self.fail()
        except AlreadyExistsError as e:
            self.assertEqual('foo',e.name)
    
    def test_is_container(self):
        class NodeSubclass(Node):
            tc = self
            cls_is_container = property(lambda x: x.tc.container)
        
        self.container = False
        node = NodeSubclass(None,'foobar')
        self.assertEqual(False,node.is_container)
        self.container = True
        self.assertEqual(True,node.is_container)
    
    def test_Path(self):
        self.mock(os, 'sep', '/')
        root = TestDir(None,'root')
        root.AddDir('foo').AddFile('bar')
        self.assertEqual('root',str(root.path))
        self.assertEqual('root/foo',str(root[0].path))
        self.assertEqual('root/foo/bar',str(root[0][0].path))
    
    def test_path_with_slash_in_name(self):
        self.mock(os, 'sep', '/')
        ref = TestDir(None,'/foo/bar')
        self.assertEqual(('','foo','bar'),ref.path)
        file = ref.AddFile('bleh')
        self.assertEqual(('','foo','bar','bleh'),file.path)
    
    def test_path_with_empty_name(self):
        ref = TestDir(None,'')
        self.assertEqual(('',),ref.path)
        self.assertEqual('/',str(ref.path))
    
    def test_path_change(self):
        root = TestDir(None,'root')
        foo = root.AddDir('foo')
        bar = foo.AddFile('bar')
        self.assertEqual(('root','foo','bar'),bar.path)
        bar.parent = root
        self.assertEqual(('root','bar'),bar.path)
        bar.name = 'bleh'
        self.assertEqual(('root','bleh'),bar.path)
        root.name = 'foobar'
        self.assertEqual(('foobar','bleh'),bar.path)
    
    def test_set_empty_name(self):
        foo = TestDir(None,'foo')
        bar = foo.AddFile('bar')
        foo.name = ''
        self.assertEqual('foo',foo.name)
        bar.name = ''
        self.assertEqual('bar',bar.name)
    
    def test_weakref(self):
        import weakref
        parent = Node(None,'foo')
        Node(parent,'bar')
        w = weakref.ref(parent)
        del parent
        gc.collect()
        self.assert_(w() is None)
    
    def test_path_invalidation_on_parent_change(self):
        p1 = Node(None,'p1')
        p2 = Node(None,'p2')
        c = Node(p1,'c')
        self.assertEqual(('p1','c'),c.path)
        c.parent = p2
        self.assertEqual(('p2','c'),c.path)
    
    def test_invalidate_path_recursive(self):
        n1 = Node(None,'n1')
        n2 = Node(n1,'n2')
        n2.path
        n1._invalidate_path() #recursive by default
        self.assert_(n1._Node__path is None)
        self.assert_(n2._Node__path is None)
        n2.path
        n1._invalidate_path(False) #Non-recursive
        self.assert_(n1._Node__path is None)
        self.assert_(n2._Node__path is not None)
    
    def test_find_path(self):
        n = Node(None,'')
        foo = Node(n,'foo')
        bar = Node(foo,'bar')
        self.assert_(n.find_path(Path('foo')) is foo)
        self.assert_(n.find_path(Path('bar')) is None)
        self.assert_(n.find_path(Path(())) is n)
        self.assert_(n.find_path(Path(('foo','bar'))) is bar)
    
    def test_find_path_with_empty_names(self):
        n = Node(None, '')
        n2 = Node(n, '')
        self.assert_(n.find_path(Path(())) is n)
    
    def test_build_path(self):
        """fs.Node subclasses can override _build_path() to have a different path than the default
        one
        """
        class MyNode(Node):
            def _build_path(self):
                return Path('foo/bar')
            
        node = MyNode(None, '')
        self.assertEqual(node.path, ('foo', 'bar'))
            
    
    

class TCFile(TestCase):
    def setUp(self):
        self.global_setup()
        self.mock(sys, 'stdout', StringIO())
    
    def tearDown(self):
        self.global_teardown()
    
    def test_ctime(self):
        f = File(None,'foobar')
        self.assertEqual(0,f.ctime)
    
    def test_mtime(self):
        f = File(None,'foobar')
        self.assertEqual(0,f.mtime)
    
    def test_read_all_info(self):
        class FakeFile(File):
            INITIAL_INFO = {'foo': '', 'bar': '', 'baz': ''}
            def _read_info(self, field):
                if field == 'foo':
                    self.foo = 'foo'
                if field in ('bar', 'baz'):
                    self.bar = 'bar'
                    self.baz = 'baz'
            
        
        f = FakeFile(None,'')
        f._read_all_info()
        assert 'foo' in f.__dict__
        assert 'bar' in f.__dict__
        assert 'baz' in f.__dict__
        f = FakeFile(None,'')
        f._read_all_info(attrnames=['foo'])
        assert 'foo' in f.__dict__
        assert 'bar' not in f.__dict__
        assert 'baz' not in f.__dict__
    
    def test_exception_is_raised_while_reading(self):
        # When an exception is raised while reading info, a warning is issued and the defaults are set
        def FakeReadInfo(field):
            raise Exception("hello!\xe9")
        
        f = File(None,'')
        f._read_info = FakeReadInfo
        eq_(f.size, 0) # no UnicodeEncodeError
        eq_(f.mtime, 0)
        eq_(f.ctime, 0)
        eq_(f.md5, '')
        eq_(f.md5partial, '')
        self.logged.seek(0)
        assert "hello!\xe9" in self.logged.read()
    
    def test_default_info_is_only_set_for_requested_section(self):
        f = File(None,'')
        f.size
        assert 'md5' not in f.__dict__
    
