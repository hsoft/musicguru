# Created By: Virgil Dupras
# Created On: 2006/10/06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os.path as op
import os
import shutil

from nose.tools import nottest

import hsaudiotag.testcase
from hsutil.testcase import TestCase
from hsfs.phys import music
from hsutil.path import Path
from hscommon.job import Job, JobCancelled

from .. import manualfs
from .music import *

class TCRoot_children(TestCase):
    def test_new_directories_are_Volume(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        self.assert_(type(v) is Volume)
    
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        f = root.new_file('file')
        self.assert_(type(f) is File)

class TCVolume_children(TestCase):
    def test_new_directories_are_music_Directory(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        self.assert_(type(d) is Directory)
    
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        f = v.new_file('file')
        self.assert_(type(f) is File)

class TCDirectory_children(TestCase):
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        f = d.new_file('file')
        self.assert_(type(f) is File)
    

class TCVolume_initial_path(TestCase):
    def test_initial_path(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        result = v.initial_path
        self.assertEqual(p,result)
        self.assert_(isinstance(result,Path))
    
    def test_initial_path_persistence(self):
        p = Path(('foo','bar'))
        dbpath = op.join(self.tmpdir(),'fs.db')
        root = Root(dbpath, threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        root.con.close()
        root = Root(dbpath, threaded=False)
        v = root[0]
        self.assertEqual(p,v.initial_path)
    
    def test_keep_initial_path_cache(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        p = v.initial_path
        self.assert_(v.initial_path is p)
    
    def test_invalidate_cache_on_set(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        self.assertEqual(p,v.initial_path)
        p = Path(('foo','baz'))
        v.initial_path = p
        self.assertEqual(p,v.initial_path)
    
    def test_initial_value(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        self.assertEqual(Path(''),v.initial_path)
    

class TCVolume_vol_type(TestCase):
    def test_vol_type(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.vol_type = VOLTYPE_FIXED
        self.assertEqual(VOLTYPE_FIXED,v.vol_type)
    
    def test_vol_type_persistence(self):
        dbpath = op.join(self.tmpdir(),'fs.db')
        root = Root(dbpath, threaded=False)
        v = root.new_directory('foo')
        v.vol_type = VOLTYPE_FIXED
        root = Root(dbpath, threaded=False)
        v = root[0]
        self.assertEqual(VOLTYPE_FIXED,v.vol_type)
    
    def test_initial_value(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        self.assertEqual(VOLTYPE_FIXED,v.vol_type)
    

class TCVolume_physical_path(TestCase):
    def test_on_fixed_drive(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = Path(('foo','bar'))
        self.assertEqual(v.initial_path,v.physical_path)
    

class TCDirectory_physical_path(TestCase):
    def test_typical(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        v.initial_path = Path(('initial','path'))
        self.assertEqual(('','foo','bar'),d.path)
        self.assertEqual(('initial','path','bar'),d.physical_path)
    

class TCFile_physical_path(TestCase):
    def test_typical(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        f = d.new_file('baz')
        v.initial_path = Path(('initial','path'))
        self.assertEqual(('','foo','bar','baz'),f.path)
        self.assertEqual(('initial','path','bar','baz'),f.physical_path)
    

class TCadd_volume(TestCase):
    def _get_ref_dir(self):
        ref = manualfs.Directory(None,'initial')
        ref.new_directory('dir')
        ref.new_file('file')    
        return ref    
    
    def test_typical(self):
        root = Root(threaded=False)
        ref = self._get_ref_dir()
        v = root.add_volume(ref,'volume_name',42)
        self.assert_(v in root)
        self.assertEqual('volume_name',v.name)
        self.assertEqual(1,v.dircount)
        self.assertEqual(1,v.filecount)
        self.assertEqual(42,v.vol_type)
        self.assertEqual('initial',v.initial_path)
    
    def test_job_cancel(self):
        j = Job(1, lambda progress: False) # Will cancel right away
        ref = self._get_ref_dir()
        root = Root(threaded=False)
        try:
            root.add_volume(ref, 'volume_name', 42, j)
        except JobCancelled:
            pass # This is expected
        # Nothing should have been added
        self.assertEqual(0, len(root))
    

class TCVolume_Update(TestCase):
    def test_that_ref_is_automatically_created(self):
        ref_dir = hsaudiotag.testcase.TestCase.filepath('ogg')
        ref_dir = self.tmpdir(ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'the_volume',VOLTYPE_FIXED)
        self.assertEqual(2,v.filecount)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.ogg'))
        v.update()
        self.assertEqual(3,v.filecount)
    
    def test_that_the_ref_create_is_a_music_dir(self):
        ref_dir = hsaudiotag.testcase.TestCase.filepath('ogg')
        ref_dir = self.tmpdir(ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'the_volume',VOLTYPE_FIXED)
        self.assertEqual(2,v.filecount)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.foo'))
        v.update()
        self.assertEqual(2,v.filecount)
    
    def test_gracefully_handle_invalid_path(self):
        # Sometimes, the volume is from an external drive and that drive is not plugged in.
        # In this case, we just want to ignore the error and just not update that volume.
        root = Root(threaded=False)
        volume = root.new_directory('foobar')
        volume.vol_type = VOLTYPE_FIXED
        volume.initial_path = '/does/not/exist'
        try:
            volume.update()
        except hs.fs.InvalidPath:
            self.fail()
    

class TCRoot_update_volumes(TestCase):
    def test_only_update_fixed_volumes(self):
        ref_dir = hsaudiotag.testcase.TestCase.filepath('ogg')
        ref_dir = self.tmpdir(ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        vf = root.add_volume(ref,'fixed',VOLTYPE_FIXED)
        vc = root.add_volume(ref,'cdrom',VOLTYPE_CDROM)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.ogg'))
        root.update_volumes()
        self.assertEqual(3,vf.filecount)
        self.assertEqual(2,vc.filecount)
    

class TCJobs(TestCase):
    def setUp(self):
        def callback(progress):
            self.log.append(progress)
            return True
        
        self.log = []
        self.job = Job(1,callback)
    
    @nottest
    def do_test_log(self):
        self.assertEqual(0,self.log[0])
        self.assertEqual(100,self.log[-1])
    
    def test_Volume_Update(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        ref = manualfs.Directory(None,'')
        ref.new_file('foo')
        v.update(ref,job=self.job)
        self.do_test_log()
    
    def test_Root_update_volumes(self):
        root = Root(threaded=False)
        ref_dir = hsaudiotag.testcase.TestCase.filepath('ogg')
        v = root.new_directory('foo')
        v.initial_path = Path(ref_dir)
        v.vol_type = VOLTYPE_FIXED
        root.update_volumes(job=self.job)
        self.do_test_log()
    
    def test_Root_add_volume(self):
        root = Root(threaded=False)
        ref = manualfs.Directory(None,'')
        ref.new_file('foo')
        root.add_volume(ref,'foo',1,job=self.job)
        self.do_test_log()
    

class TCparent_volume(TestCase):
    def test_from_volume(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        self.assert_(v.parent_volume is v)
    
    def test_from_directory(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('foo')
        self.assert_(d.parent_volume is v)
    
    def test_from_file(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('foo')
        f = d.new_file('foo')
        self.assert_(f.parent_volume is v)
    

class TCbuffer_path(TestCase):
    def test_initial_value(self):
        root = Root(threaded=False)
        self.assertEqual(Path(()),root.buffer_path)
    
    def test_cdrom_volume_path(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        root.buffer_path = Path('buffer')
        v.vol_type = VOLTYPE_CDROM
        self.assertEqual(Path(('buffer','foo')),v.physical_path)
    

class TCvolume_path_mode(TestCase):
    def setUp(self):
        self.root = Root(threaded=False)
        self.v = self.root.new_directory('vol')
        self.v.initial_path = Path('initial')
        self.f = self.v.new_file('file')
    
    def test_mode_normal(self):
        self.v.mode = MODE_NORMAL
        self.assertEqual(('','vol','file'),self.f.path)
    
    def test_mode_physical(self):
        self.v.mode = MODE_PHYSICAL
        self.assertEqual(('initial','file'),self.f.path)
    
    def test_mode_token(self):
        self.v.mode = MODE_TOKEN
        self.assertEqual(('!vol','file'),self.f.path)
    
    def test_default(self):
        self.assertEqual(MODE_NORMAL,self.v.mode)
    
    def test_invalidate_path(self):
        self.f.path
        self.v.mode = MODE_PHYSICAL
        self.assertEqual(('initial','file'),self.f.path)
    

class TCFileAttrs(TestCase):
    def test_has_music_attrs(self):
        ref_dir = hsaudiotag.testcase.TestCase.filepath('ogg')
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'foo',VOLTYPE_FIXED)
        f = v['test1.ogg']
        self.assertEqual('Astro',f.title)
    

class TCvolume_is_available(TestCase):
    def setUp(self):
        self.root = Root(threaded=False)
        self.v = self.root.new_directory('vol')
    
    def test_true(self):
        self.v.initial_path = TestCase.filepath('') #it always exists
        self.assertTrue(self.v.is_available)
    
    def test_false(self):
        self.v.initial_path = Path('/does/not/exist')
        self.assertFalse(self.v.is_available)
    
    def test_removable(self):
        # if the volume is removable, is_available is true when the disc is in place
        self.v.vol_type = VOLTYPE_CDROM
        rootpath = self.tmpdir()
        self.root.buffer_path = Path(rootpath)
        # create a directory with self.v.name as a name to emulate the insertion of the CD in /Volumes
        os.mkdir(op.join(rootpath, self.v.name))
        self.v.initial_path = Path('/does/not/exist') # physical_path should be read
        self.assertTrue(self.v.is_available)
    
