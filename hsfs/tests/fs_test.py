# Created By: Virgil Dupras
# Created On: 2004/12/22
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os
import sys
from io import StringIO
import weakref
import gc

import pytest
from hscommon.testutil import eq_
from hscommon.path import Path

from .._fs import *

class TestDir(Directory):
    def AddDir(self,dirname):
        return self._create_sub_dir(dirname)
    
    def AddFile(self,filename):
        return self._create_sub_file(filename)
    

class TestDirectory:
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
        assert isinstance(root[0],TestDir)
    
    def testDirName(self):
        root = self.GenTestDir()
        eq_(root.name,'root')
        eq_(root[0].name,'foo')
        eq_(root[1].name,'bleh')
        eq_(root[1][0].name,'bar')
    
    def testFileName(self):
        root = self.GenTestDir()
        eq_(root[2].name,'foofile')
        eq_(root[3].name,'barfile')
    
    def testParentDir(self):
        root = self.GenTestDir()
        assert root[0].parent is root
        assert root[0][0].parent is root[0]
    
    def testParentList(self):
        root = self.GenTestDir()
        eq_([root], list(root[0].parents))
        eq_([root, root[0]], list(root[0][0].parents))
    
    def testSubDirCount(self):
        root = self.GenTestDir()
        eq_(2,root.dircount)
        eq_(0,root[0].dircount)
        eq_(1,root[1].dircount)
    
    def testSubFileCount(self):
        root = self.GenTestDir()
        eq_(2,root.filecount)
        eq_(1,root[0].filecount)
        eq_(0,root[1].filecount)
    
    def testfind_sub_dir(self):
        root = self.GenTestDir()
        assert root.find_sub_dir('foo') is root[0]
        assert root.find_sub_dir('foofile') is None
        assert root.find_sub_dir('invalid') is None
    
    def testfind_sub_file(self):
        root = self.GenTestDir()
        assert root.find_sub_file('foofile') is root[2]
        assert root.find_sub_file('foo') is None
        assert root.find_sub_file('invalid') is None
    
    def test_root(self):
        root = self.GenTestDir()
        assert root.root is root
        assert root.dirs[0].root is root
        assert root.dirs[0].dirs[0].root is root
    
    def testAllDirs(self):
        root = self.GenTestDir()
        eq_(3,len(root.alldirs))
        assert root[0] in root.alldirs
        eq_(set(root.alldirs), set(root.iteralldirs()))
    
    def testAllFiles(self):
        root = self.GenTestDir()
        eq_(3,len(root.allfiles))
        assert root[2] in root.allfiles
        eq_(set(root.allfiles), set(root.iterallfiles()))
    
    def testStats(self):
        root = self.GenTestDir()
        eq_(root.get_stat('dircount'),3)
        eq_(root.get_stat('filecount'),3)
        eq_(root.get_stat('Size'),0)
        eq_(root.get_stat('extension',[]),[])
        root.AddFile('test.test')
        eq_(root.get_stat('extension'),['test'])
        eq_(root.get_stat('filecount'),4)
        bazdir = root.AddDir('baz')
        eq_(root.get_stat('extension'),['test'])
        f = bazdir.AddFile('baz.bleh')
        eq_(root.get_stat('extension'),['test','bleh'])
        f.parent = None
        eq_(root.get_stat('extension'),['test'])
    
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
        eq_('b',root.dirs[0].name)
        root.AddFile('c')
        root.AddFile('d')
        eq_('d',root.files[0].name)
    
    def test_is_container(self):
        root = TestDir(None,'foo')
        file = root.AddFile('bar')
        eq_(True,root.is_container)
        eq_(False,file.is_container)
    
    def test_child_sort_case_insensitive(self):
        root = TestDir(None,'root')
        root.AddDir('a')
        root.AddDir('B')
        eq_('a',root.dirs[0].name)
        root.AddFile('c')
        root.AddFile('D')
        eq_('c',root.files[0].name)
    
    def test_weakref(self):
        parent = Directory(None,'foo')
        w1 = weakref.ref(parent)
        w2 = weakref.ref(Directory(parent,'bar'))
        w3 = weakref.ref(File(parent[0],'bleh'))
        assert w1() is not None
        assert w2() is not None
        assert w3() is not None
        del parent
        gc.collect()
        assert w1() is None
        assert w2() is None
        assert w3() is None
    
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
        eq_(1,len(d.alldirs))
        eq_(set(d.alldirs) ,set(d.iteralldirs()))
    
    def test_allfiles_dont_go_further_if_child_is_not_container(self):
        #same thing as alldirs
        class Liar(Directory):
            cls_is_container = False
        
        d = Directory(None,'')
        l = Liar(d,'liar')
        File(d,'foo')
        File(l,'bar')
        eq_(2,len(d.allfiles)) #Liar is in fact counted as a file
        eq_(set(d.allfiles), set(d.iterallfiles()))
    

class TestFSNode:
    def test_rename_exception(self):
        root = TestDir(None,'root')
        foo = root.AddFile('foo')
        bar = root.AddFile('bar')
        try:
            bar.name = 'foo'
            self.fail()
        except AlreadyExistsError as e:
            eq_('foo',e.name)
    
    def test_is_container(self):
        class NodeSubclass(Node):
            tc = self
            cls_is_container = property(lambda x: x.tc.container)
        
        self.container = False
        node = NodeSubclass(None,'foobar')
        eq_(False,node.is_container)
        self.container = True
        eq_(True,node.is_container)
    
    def test_Path(self, monkeypatch):
        monkeypatch.setattr(os, 'sep', '/')
        root = TestDir(None,'root')
        root.AddDir('foo').AddFile('bar')
        eq_('root',str(root.path))
        eq_('root/foo',str(root[0].path))
        eq_('root/foo/bar',str(root[0][0].path))
    
    def test_path_with_slash_in_name(self, monkeypatch):
        monkeypatch.setattr(os, 'sep', '/')
        ref = TestDir(None,'/foo/bar')
        eq_(('','foo','bar'),ref.path)
        file = ref.AddFile('bleh')
        eq_(('','foo','bar','bleh'),file.path)
    
    def test_path_with_empty_name(self):
        ref = TestDir(None,'')
        eq_(('',),ref.path)
        eq_('/',str(ref.path))
    
    def test_path_change(self):
        root = TestDir(None,'root')
        foo = root.AddDir('foo')
        bar = foo.AddFile('bar')
        eq_(('root','foo','bar'),bar.path)
        bar.parent = root
        eq_(('root','bar'),bar.path)
        bar.name = 'bleh'
        eq_(('root','bleh'),bar.path)
        root.name = 'foobar'
        eq_(('foobar','bleh'),bar.path)
    
    def test_set_empty_name(self):
        foo = TestDir(None,'foo')
        bar = foo.AddFile('bar')
        foo.name = ''
        eq_('foo',foo.name)
        bar.name = ''
        eq_('bar',bar.name)
    
    def test_weakref(self):
        import weakref
        parent = Node(None,'foo')
        Node(parent,'bar')
        w = weakref.ref(parent)
        del parent
        gc.collect()
        assert w() is None
    
    def test_path_invalidation_on_parent_change(self):
        p1 = Node(None,'p1')
        p2 = Node(None,'p2')
        c = Node(p1,'c')
        eq_(('p1','c'),c.path)
        c.parent = p2
        eq_(('p2','c'),c.path)
    
    def test_invalidate_path_recursive(self):
        n1 = Node(None,'n1')
        n2 = Node(n1,'n2')
        n2.path
        n1._invalidate_path() #recursive by default
        assert n1._Node__path is None
        assert n2._Node__path is None
        n2.path
        n1._invalidate_path(False) #Non-recursive
        assert n1._Node__path is None
        assert n2._Node__path is not None
    
    def test_find_path(self):
        n = Node(None,'')
        foo = Node(n,'foo')
        bar = Node(foo,'bar')
        assert n.find_path(Path('foo')) is foo
        assert n.find_path(Path('bar')) is None
        assert n.find_path(Path(())) is n
        assert n.find_path(Path(('foo','bar'))) is bar
    
    def test_find_path_with_empty_names(self):
        n = Node(None, '')
        n2 = Node(n, '')
        assert n.find_path(Path(())) is n
    
    def test_build_path(self):
        """fs.Node subclasses can override _build_path() to have a different path than the default
        one
        """
        class MyNode(Node):
            def _build_path(self):
                return Path('foo/bar')
            
        node = MyNode(None, '')
        eq_(node.path, ('foo', 'bar'))
            
    
    

class TestFile:
    def pytest_funcarg__dosetup(self, request):
        monkeypatch = request.getfuncargvalue('monkeypatch')
        monkeypatch.setattr(sys, 'stdout', StringIO())
    
    def test_ctime(self, dosetup):
        f = File(None,'foobar')
        eq_(0,f.ctime)
    
    def test_mtime(self, dosetup):
        f = File(None,'foobar')
        eq_(0,f.mtime)
    
    def test_read_all_info(self, dosetup):
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
    
    @pytest.mark.xfail # There's some weird stuff going on with capture that I still have to figure out...
    def test_exception_is_raised_while_reading(self, dosetup, capsys):
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
        out, err = capsys.readouterr()
        assert "hello!\xe9" in err
    
    def test_default_info_is_only_set_for_requested_section(self, dosetup):
        f = File(None,'')
        f.size
        assert 'md5' not in f.__dict__
    
