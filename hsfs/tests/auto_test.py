# Created By: Virgil Dupras
# Created On: 2006/06/29
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.testcase import TestCase

from .. import _fs as fs, auto

class FakeAutoDir(auto.Directory):
    def __init__(self, parent=None, name=''):
        super(FakeAutoDir, self).__init__(parent, name)
        self.fakeddirs = []
        self.fakedfiles = []
        self.fakedmtime = 0
        self.mtime_call_count = 0
        self.subitems_call_count = 0
    
    def _fetch_subitems(self):
        self.subitems_call_count += 1
        return (self.fakeddirs, self.fakedfiles)
    
    def _get_mtime(self):
        self.mtime_call_count += 1
        return self.fakedmtime
    

class TCDirectory(TestCase):
    def test_in_test_doesnt_create_children(self):
        #A simple test to see if a Directory contains a name
        #such as "'foo' in dir" should just call the Fetch 
        #functions.
        d = FakeAutoDir()
        d._do_update = lambda: self.fail("_do_update has been called")
        d.fakedmtime = 1 #Invalidate the current content
        self.assert_('foo' not in d)
    
    def test_in_test_doesnt_call_fetch_if_mtime_hasnt_changed(self):
        #However, if the directory already cached all its content, we
        #want to use this instead of Fetch for the in test.
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        d._do_update()
        d.fakedfiles = ['foo','bar']
        self.assert_('foo' in d)
        self.assert_('bar' not in d)
    
    def test_len_call_do_create_children(self):
        #Same thing for "len" as for "in".
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        self.assertEqual(1,len(d))
        self.assertEqual(1,fs.Directory.__len__(d))
    
    def test_len_doesnt_call_fetch_if_mtime_hasnt_changed(self):
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        d._do_update()
        d.fakedfiles = ['foo','bar']
        self.assertEqual(1,len(d))
    
    def test_dircount_do_create_children(self):
        d = FakeAutoDir()
        d.fakeddirs = ['foo']
        d.fakedmtime = 1
        self.assertEqual(1,d.dircount)
        self.assertEqual(1,fs.Directory.__len__(d))
    
    def test_dircount_doesnt_call_fetch_if_mtime_hasnt_changed(self):
        d = FakeAutoDir()
        d.fakeddirs = ['foo']
        d.fakedmtime = 1
        d._do_update()
        d.fakeddirs = ['foo','bar']
        self.assertEqual(1,d.dircount)
    
    def test_filecount_do_create_children(self):
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        self.assertEqual(1,d.filecount)
        self.assertEqual(1,fs.Directory.__len__(d))
    
    def test_filecount_doesnt_call_fetch_if_mtime_hasnt_changed(self):
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        d._do_update()
        d.fakedfiles = ['foo','bar']
        self.assertEqual(1,d.filecount)
    
    def test_normalized_fetches_before_comparison_in_do_update(self):
        d = FakeAutoDir()
        d.fakedfiles = ['fooe\u0301']
        d.fakeddirs = ['bare\u0301']
        d.fakedmtime = 1
        subfile = d.files[0]
        subdir = d.dirs[0]
        d._do_update()
        self.assert_(d.files[0] is subfile)
        self.assert_(d.dirs[0] is subdir)
    
    def test_files_prop_checks_for_update(self):
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        d.files
        d.fakedfiles = ['foo','bar']
        d.fakedmtime = 2
        self.assertEqual(2,len(d.files))
    
    def test_dirs_prop_checks_for_update(self):
        d = FakeAutoDir()
        d.fakeddirs = ['foo']
        d.fakedmtime = 1
        d.dirs
        d.fakeddirs = ['foo','bar']
        d.fakedmtime = 2
        self.assertEqual(2,len(d.dirs))
    
    def test_remove_file_and_add_dir_of_the_same_name_in_do_update(self):
        # Previously, we wanted in this case to remove the old 'foo' dir and add a 'foo' file, 
        # but now we want the instance of whatever was there. This is because in dupeguru, when
        # an update was performed, all instances of bundle type (they are Directory, but act as a file)
        # were lost and that caused problem.
        d = FakeAutoDir()
        d.fakedfiles = ['foo']
        d.fakedmtime = 1
        len(d)
        mydir = d[0]
        d.fakedfiles = []
        d.fakeddirs = ['foo']
        d.fakedmtime = 2
        self.assertEqual(len(d), 1)
        self.assert_(mydir in d)
    
    def test_adjust_name_from_normalization_form_if_needed(self):
        # if for some reason the name of a node has a different normalization form than the name
        # in _getSubItems(), automatically adjust that name and keep the same instance in there.
        root = FakeAutoDir()
        root.fakeddirs = ['foo\u00e9']
        root.fakedfiles = ['bar\u00e9']
        root.fakedmtime = 1
        d = root.dirs[0]
        f = root.files[0]
        root.fakeddirs = ['fooe\u0301']
        root.fakedfiles = ['bare\u0301']
        root.fakedmtime = 2
        len(root)
        self.assert_(d.parent is root)
        self.assertEqual('fooe\u0301', d.name)
        self.assert_(f.parent is root)
        self.assertEqual('bare\u0301', f.name)
        root.fakeddirs = ['foo\u00e9']
        root.fakedfiles = ['bar\u00e9']
        root.fakedmtime = 3
        len(root)
        self.assert_(d.parent is root)
        self.assertEqual('foo\u00e9', d.name)
        self.assert_(f.parent is root)
        self.assertEqual('bar\u00e9', f.name)
    
    def test_force_update(self):
        d = FakeAutoDir()
        d.fakedmtime = 1
        len(d)
        d.fakedfiles = ['foo']
        d.force_update() #The mtime stays the same, but we force an update anyway.
        self.assertEqual(1,len(d.files))
    
    def test_force_update_is_recursive(self):
        d1 = FakeAutoDir()
        d1.fakedmtime = 1
        d1.fakeddirs = ['foo']
        d2 = d1['foo']
        d2.fakedmtime = 1
        d2.fakeddirs = ['foo']
        d3 = d2['foo']
        d3.fakedmtime = 1
        len(d3)
        d3.fakedfiles = ['foo']
        d1.force_update()
        self.assertEqual(len(d3.files), 1)
    
    def test_force_update_fetch_subdirs_lazily_after(self):
        #What happened here is that the recursive loop called "dirs", which called "Update"
        #Of course, we don't want that to happen.
        d = FakeAutoDir()
        d.fakedmtime = 1
        d._do_update = lambda: self.fail("We shouldn't update on force_update()")
        d.force_update()
    
    def test_force_update_also_forces_file_updates(self):
        # force_update also clears the file's info
        d = FakeAutoDir()
        d.fakedmtime = 1
        d.fakedfiles = ['foo']
        f = d.files[0]
        # We could go through a whole big mechanism that subclasses File and override read_info and
        # all, but let's rely on the protected _info dict... simpler.
        f.size = 42
        d.force_update()
        assert 'size' not in f.__dict__
    

class FakeAtomicParent(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.called_begin = False
        self.called_end = False
    
    def _begin_operation(self):
        self.called_begin = True
    
    def _end_operation(self):
        self.called_end = True
    
    @auto.hold_update
    def some_atomic_operation(self):
        return 43

class FakeAtomicChild(object):
    def __init__(self, parent):
        self.parent = parent
    
    @auto.hold_parent_update
    def some_atomic_operation(self):
        return 42
    

class TCHoldUpdate(TestCase):
    def test_main(self):
        parent = FakeAtomicParent()
        self.assertEqual(43, parent.some_atomic_operation())
        self.assert_(parent.called_begin)
        self.assert_(parent.called_end)
    
    def test_raises_exception(self):
        class FakeAtomicParentError(FakeAtomicParent):
            @auto.hold_update
            def some_atomic_operation(self):
                raise Exception()
            
        
        parent = FakeAtomicParentError()
        try:
            parent.some_atomic_operation()
            self.fail() #We must still raise it
        except Exception:
            pass
        # Make sure that we call _EndOperation
        self.assert_(parent.called_begin)
        self.assert_(parent.called_end)
    
    def test_no_parent(self):
        parent = FakeAtomicParent()
        self.assertEqual(43, parent.some_atomic_operation())
        self.assert_(parent.called_begin)
        self.assert_(parent.called_end)
    

class TCHoldParentUpdate(TestCase):
    def test_main(self):
        parent = FakeAtomicParent()
        child = FakeAtomicChild(parent)
        self.assertEqual(42, child.some_atomic_operation())
        self.assert_(parent.called_begin)
        self.assert_(parent.called_end)
    
    def test_raises_exception(self):
        class FakeAtomicChildError(FakeAtomicParent):
            @auto.hold_parent_update
            def some_atomic_operation(self):
                raise Exception()
            
        
        parent = FakeAtomicParent()
        child = FakeAtomicChildError(parent)
        try:
            child.some_atomic_operation()
            self.fail() #We must still raise it
        except Exception:
            pass
        # Make sure that we call _EndOperation
        self.assert_(parent.called_begin)
        self.assert_(parent.called_end)
    
    def test_no_parent(self):
        child = FakeAtomicChild(None)
        self.assertEqual(42, child.some_atomic_operation()) # We shouldn't get an exception here.
    
