# Created By: Virgil Dupras
# Created On: 2006/10/06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os.path as op
import os
import shutil

from hsfs.phys import music
from hscommon.path import Path
from jobprogress.job import Job, JobCancelled
from hscommon.testutil import eq_

from ..testutil import testdata
from .. import manualfs
from .music import *

class TestRoot_children:
    def test_new_directories_are_Volume(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        assert type(v) is Volume
    
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        f = root.new_file('file')
        assert type(f) is File

class TestVolume_children:
    def test_new_directories_are_music_Directory(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        assert type(d) is Directory
    
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        f = v.new_file('file')
        assert type(f) is File

class TestDirectory_children:
    def test_new_files_are_music_File(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        f = d.new_file('file')
        assert type(f) is File
    

class TestVolume_initial_path:
    def test_initial_path(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        result = v.initial_path
        eq_(p,result)
        assert isinstance(result,Path)
    
    def test_initial_path_persistence(self, tmpdir):
        p = Path(('foo','bar'))
        dbpath = str(tmpdir.join('fs.db'))
        root = Root(dbpath, threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        root.con.close()
        root = Root(dbpath, threaded=False)
        v = root[0]
        eq_(p,v.initial_path)
    
    def test_keep_initial_path_cache(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        p = v.initial_path
        assert v.initial_path is p
    
    def test_invalidate_cache_on_set(self):
        p = Path(('foo','bar'))
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = p
        eq_(p,v.initial_path)
        p = Path(('foo','baz'))
        v.initial_path = p
        eq_(p,v.initial_path)
    
    def test_initial_value(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        eq_(Path(''),v.initial_path)
    

class TestVolume_vol_type:
    def test_vol_type(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.vol_type = VOLTYPE_FIXED
        eq_(VOLTYPE_FIXED,v.vol_type)
    
    def test_vol_type_persistence(self, tmpdir):
        dbpath = str(tmpdir.join('fs.db'))
        root = Root(dbpath, threaded=False)
        v = root.new_directory('foo')
        v.vol_type = VOLTYPE_FIXED
        root = Root(dbpath, threaded=False)
        v = root[0]
        eq_(VOLTYPE_FIXED,v.vol_type)
    
    def test_initial_value(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        eq_(VOLTYPE_FIXED,v.vol_type)
    

class TestVolume_physical_path:
    def test_on_fixed_drive(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        v.initial_path = Path(('foo','bar'))
        eq_(v.initial_path,v.physical_path)
    

class TestDirectory_physical_path:
    def test_typical(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        v.initial_path = Path(('initial','path'))
        eq_(('','foo','bar'),d.path)
        eq_(('initial','path','bar'),d.physical_path)
    

class TestFile_physical_path:
    def test_typical(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('bar')
        f = d.new_file('baz')
        v.initial_path = Path(('initial','path'))
        eq_(('','foo','bar','baz'),f.path)
        eq_(('initial','path','bar','baz'),f.physical_path)
    

class Testadd_volume:
    def _get_ref_dir(self):
        ref = manualfs.Directory(None,'initial')
        ref.new_directory('dir')
        ref.new_file('file')    
        return ref    
    
    def test_typical(self):
        root = Root(threaded=False)
        ref = self._get_ref_dir()
        v = root.add_volume(ref,'volume_name',42)
        assert v in root
        eq_('volume_name',v.name)
        eq_(1,v.dircount)
        eq_(1,v.filecount)
        eq_(42,v.vol_type)
        eq_('initial',v.initial_path)
    
    def test_job_cancel(self):
        j = Job(1, lambda progress: False) # Will cancel right away
        ref = self._get_ref_dir()
        root = Root(threaded=False)
        try:
            root.add_volume(ref, 'volume_name', 42, j)
        except JobCancelled:
            pass # This is expected
        # Nothing should have been added
        eq_(0, len(root))
    

class TestVolume_Update:
    def test_that_ref_is_automatically_created(self, tmpdir):
        ogg_dir = testdata.filepath('ogg')
        ref_dir = str(tmpdir.join('ref_dir'))
        shutil.copytree(ogg_dir, ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'the_volume',VOLTYPE_FIXED)
        eq_(2,v.filecount)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.ogg'))
        v.update()
        eq_(3,v.filecount)
    
    def test_that_the_ref_create_is_a_music_dir(self, tmpdir):
        ogg_dir = testdata.filepath('ogg')
        ref_dir = str(tmpdir.join('ref_dir'))
        shutil.copytree(ogg_dir, ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'the_volume',VOLTYPE_FIXED)
        eq_(2,v.filecount)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.foo'))
        v.update()
        eq_(2,v.filecount)
    
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
    

class TestRoot_update_volumes:
    def test_only_update_fixed_volumes(self, tmpdir):
        ogg_dir = testdata.filepath('ogg')
        ref_dir = str(tmpdir.join('ref_dir'))
        shutil.copytree(ogg_dir, ref_dir)
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        vf = root.add_volume(ref,'fixed',VOLTYPE_FIXED)
        vc = root.add_volume(ref,'cdrom',VOLTYPE_CDROM)
        shutil.copy(op.join(ref_dir,'test1.ogg'),op.join(ref_dir,'test3.ogg'))
        root.update_volumes()
        eq_(3,vf.filecount)
        eq_(2,vc.filecount)
    

class TestJobs:
    def setup_method(self, method):
        def callback(progress):
            self.log.append(progress)
            return True
        
        self.log = []
        self.job = Job(1,callback)
    
    def do_test_log(self):
        eq_(0,self.log[0])
        eq_(100,self.log[-1])
    
    def test_Volume_Update(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        ref = manualfs.Directory(None,'')
        ref.new_file('foo')
        v.update(ref,job=self.job)
        self.do_test_log()
    
    def test_Root_update_volumes(self):
        root = Root(threaded=False)
        ref_dir = testdata.filepath('ogg')
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
    

class Testparent_volume:
    def test_from_volume(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        assert v.parent_volume is v
    
    def test_from_directory(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('foo')
        assert d.parent_volume is v
    
    def test_from_file(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        d = v.new_directory('foo')
        f = d.new_file('foo')
        assert f.parent_volume is v
    

class Testbuffer_path:
    def test_initial_value(self):
        root = Root(threaded=False)
        eq_(Path(()),root.buffer_path)
    
    def test_cdrom_volume_path(self):
        root = Root(threaded=False)
        v = root.new_directory('foo')
        root.buffer_path = Path('buffer')
        v.vol_type = VOLTYPE_CDROM
        eq_(Path(('buffer','foo')),v.physical_path)
    

class Testvolume_path_mode:
    def setup_method(self, method):
        self.root = Root(threaded=False)
        self.v = self.root.new_directory('vol')
        self.v.initial_path = Path('initial')
        self.f = self.v.new_file('file')
    
    def test_mode_normal(self):
        self.v.mode = MODE_NORMAL
        eq_(('','vol','file'),self.f.path)
    
    def test_mode_physical(self):
        self.v.mode = MODE_PHYSICAL
        eq_(('initial','file'),self.f.path)
    
    def test_mode_token(self):
        self.v.mode = MODE_TOKEN
        eq_(('!vol','file'),self.f.path)
    
    def test_default(self):
        eq_(MODE_NORMAL,self.v.mode)
    
    def test_invalidate_path(self):
        self.f.path
        self.v.mode = MODE_PHYSICAL
        eq_(('initial','file'),self.f.path)
    

class TestFileAttrs:
    def test_has_music_attrs(self):
        ref_dir = testdata.filepath('ogg')
        ref = music.Directory(None,ref_dir)
        root = Root(threaded=False)
        v = root.add_volume(ref,'foo',VOLTYPE_FIXED)
        f = v['test1.ogg']
        eq_('Astro',f.title)
    

class Testvolume_is_available:
    def setup_method(self, method):
        self.root = Root(threaded=False)
        self.v = self.root.new_directory('vol')
    
    def test_true(self):
        self.v.initial_path = testdata.filepath('') #it always exists
        assert self.v.is_available
    
    def test_false(self):
        self.v.initial_path = Path('/does/not/exist')
        assert not self.v.is_available
    
    def test_removable(self, tmpdir):
        # if the volume is removable, is_available is true when the disc is in place
        self.v.vol_type = VOLTYPE_CDROM
        rootpath = str(tmpdir)
        self.root.buffer_path = Path(rootpath)
        # create a directory with self.v.name as a name to emulate the insertion of the CD in /Volumes
        os.mkdir(op.join(rootpath, self.v.name))
        self.v.initial_path = Path('/does/not/exist') # physical_path should be read
        assert self.v.is_available
    
