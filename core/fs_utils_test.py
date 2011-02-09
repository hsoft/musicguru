# Created By: Virgil Dupras
# Created On: 2005/09/08
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os
import os.path as op
from io import StringIO
import sys
import weakref
import gc
import shutil

from hscommon.testutil import eq_
import hsfs.music
from hsfs import phys
from hsfs.tests.phys_test import create_fake_fs, create_unicode_test_dir
from hscommon.path import Path
from jobprogress.job import Job

from . import manualfs
from .fs_utils import *
from .sqlfs.music import Root, VOLTYPE_CDROM

class TestDir(manualfs.Directory):
    def AddDir(self,dirname):
        return TestDir(self,dirname)

    def AddFile(self,filename):
        return self._create_sub_file(filename)

class TestSmartMove:
    def test_simple(self):
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        foobar_from = merge_from.AddFile('foobar_from')
        foobar_into = merge_into.AddFile('foobar_into')
        smart_move([foobar_from],merge_into)
        eq_(2,len(merge_into))
        eq_('foobar_into',merge_into[0].name)
        eq_('foobar_from',merge_into[1].name)
    
    def test_conflict(self):
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        foobar_from = merge_from.AddFile('foobar')
        foobar_into = merge_into.AddFile('foobar')
        smart_move([foobar_from],merge_into)
        eq_(2,len(merge_into))
        eq_('foobar',merge_into[0].name)
        eq_('[000] foobar',merge_into[1].name)
    
    def test_double_conflict(self):
        # If a file named '[000] foobar' goes into a directory where there is already a '[000] foobar'
        # file, the new name must be '[001] foobar', not '[000] [000] foobar'!
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        merge_from.AddFile('foobar')
        merge_from.AddFile('[000] foobar')
        merge_into.AddFile('foobar')
        merge_into.AddFile('[000] foobar')
        smart_move(merge_from.files,merge_into)
        eq_(4,len(merge_into))
        eq_('foobar',merge_into[0].name)
        eq_('[000] foobar',merge_into[1].name)
        eq_('[001] foobar',merge_into[2].name)
        eq_('[002] foobar',merge_into[3].name)
    
    def test_dont_allow_merge(self):
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        foobar_from = merge_from.AddDir('foobar')
        foobar_into = merge_into.AddDir('foobar')
        foobar_from.AddFile('foobar')
        foobar_into.AddFile('foobar')
        smart_move(merge_from,merge_into,False)
        eq_(2,len(merge_into))
        eq_('foobar',merge_into[0].name)
        eq_('[000] foobar',merge_into[1].name)
        eq_('foobar',merge_into[0][0].name)
        eq_('foobar',merge_into[1][0].name)
    
    def test_allow_merge(self):
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        foobar_from = merge_from.AddDir('foobar')
        foobar_into = merge_into.AddDir('foobar')
        foobar_from.AddFile('foobar')
        foobar_into.AddFile('foobar')
        smart_move(merge_from,merge_into,True)
        eq_(1,len(merge_into))
        eq_('foobar',merge_into[0].name)
        eq_('foobar',merge_into[0][0].name)
        eq_('[000] foobar',merge_into[0][1].name)
        
    def test_item_in_dest(self):
        merge_from = TestDir(None,'merge_from')
        foobar_from = merge_from.AddFile('foobar')
        smart_move([foobar_from],merge_from)
        eq_(1,len(merge_from))
        eq_('foobar',merge_from[0].name)
        
    def test_merge_2nd_level(self):
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        foobar_from = merge_from.AddDir('foo').AddDir('bar')
        foobar_into = merge_into.AddDir('foo').AddDir('bar')
        foobar_from.AddFile('foobar')
        foobar_into.AddFile('foobar')
        smart_move(merge_from,merge_into,True)
        eq_(1,len(merge_into))
        eq_('foo',merge_into[0].name)
        eq_(1,len(merge_into[0]))
        eq_('bar',merge_into[0][0].name)
        eq_(2,len(merge_into[0][0]))
        eq_('foobar',merge_into[0][0][0].name)
        eq_('[000] foobar',merge_into[0][0][1].name)

    def test_dont_move_children(self):
        # If items contain both an item and its parent, dont move the item (only the parent must be moved)
        merge_from = TestDir(None,'merge_from')
        merge_into = TestDir(None,'merge_into')
        subdir = merge_from.AddDir('subdir')
        subfile = subdir.AddFile('subfile')
        smart_move([subdir, subfile], merge_into)
        assert subfile not in merge_into
        assert subfile in subdir
    

class TestGetNewName:
    #The GetNewName functionnality has been moved to the RestructureView.
    #Moving all these tests individually would be too long. What I'll do
    #is that I'll create an interface here that will call restructuredirectory
    #and return what GetNewName would have returned.
    def Gen(self,attrs):
        dir = manualfs.Directory(None, 'foo')
        result = hsfs.music._File(dir,'bar.mp3')
        result._read_all_info()
        for key, value in list(attrs.items()):
            setattr(result, key, value)
        return result

    def MockGetNewName(self,file,model,whitespaces = WS_DONT_TOUCH):
        dir = manualfs.Directory(None, 'foo')
        dir.add_child(file)
        result = RestructureDirectory(dir,model,whitespaces)
        myfile = result.allfiles[0]
        return str(myfile.path[1:]) #remove leading /

    def test_simple(self):
        #That all values that can be supplied as an argument in the model.
        eq_('bar.mp3',self.MockGetNewName(self.Gen({}),'%oldfilename%'))
        eq_('foo_artist.mp3',self.MockGetNewName(self.Gen({'artist':'foo_artist'}),'%artist%'))
        eq_('foo_album.mp3',self.MockGetNewName(self.Gen({'album':'foo_album'}),'%album%'))
        eq_('2005.mp3',self.MockGetNewName(self.Gen({'year':2005}),'%year%'))
        eq_('foo_genre.mp3',self.MockGetNewName(self.Gen({'genre':'foo_genre'}),'%genre%'))
        eq_('09.mp3',self.MockGetNewName(self.Gen({'track':9}),'%track%'))
        eq_('foo_title.mp3',self.MockGetNewName(self.Gen({'title':'foo_title'}),'%title%'))
        eq_('foo.mp3',self.MockGetNewName(self.Gen({}),'%oldpath%'))

    def test_combined(self):
        #Try a couple of combinations.
        attrs = {
            'artist':'foo_artist',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            'genre':'foo_genre',
            }
        model = '%artist%/%album%/%track% - %artist% - %title%'
        expected = op.join('foo_artist','foo_album','09 - foo_artist - foo_title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))
        model = '%artist%/%album%/%track% - %title%'
        expected = op.join('foo_artist','foo_album','09 - foo_title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))
        model = '%genre%/%artist%/[%year%]%album%/%track% - %title%'
        expected = op.join('foo_genre','foo_artist','[2005]foo_album','09 - foo_title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))
        model = '%artist%/%album% - %track% - %title%'
        expected = op.join('foo_artist','foo_album - 09 - foo_title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))

    def test_invalid(self):
        attrs = {
            'artist':'foo_artist',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            }
        model = '%artist%/%album%/%track% - %artist% - %invalid%'
        expected = op.join('foo_artist','foo_album','09 - foo_artist - (none).mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))
        model = '%genre%/%album%/%track% - %artist% - %invalid%' #no genre in attrs
        expected = op.join('(none)','foo_album','09 - foo_artist - (none).mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model))

    def test_whitespace(self):
        attrs = {
            'artist':'foo_artist',
            'album' :'foo album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            }
        model = '%artist%/%album%/%track% - %artist% - %title%'
        expected = op.join('foo artist','foo album','09 - foo artist - foo title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model,WS_UNDERSCORES_TO_SPACES))
        expected = op.join('foo_artist','foo_album','09 - foo_artist - foo_title.mp3')
        eq_(expected,self.MockGetNewName(self.Gen(attrs),model,WS_SPACES_TO_UNDERSCORES))

    def test_no_extension(self):
        myfile = self.Gen({})
        myfile.name = 'foobar'
        eq_('foobar',self.MockGetNewName(myfile,'%oldfilename%'))

class TestRestructureDirectory:
    def Gen(self,attrs,parent,name):
        result = hsfs.music._File(parent,name + '.mp3')
        result._read_all_info()
        for key, value in list(attrs.items()):
            setattr(result, key, value)
        return result
    
    def test_main(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {
            'artist':'foo_artist',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            'genre':'foo_genre',
            }
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%artist%/%album%/%track% - %artist% - %title%')
        eq_(1,len(result))
        eq_('foo_artist',result[0].name)
        eq_(1,len(result[0]))
        eq_('foo_album',result[0][0].name)
        eq_(1,len(result[0][0]))
        eq_('09 - foo_artist - foo_title.mp3',result[0][0][0].name)
    
    def test_conflict(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {
            'artist':'foo_artist',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            'genre':'foo_genre',
            }
        self.Gen(attrs,dir,'foobar1')
        self.Gen(attrs,dir,'foobar2')
        result = RestructureDirectory(dir,'%artist%/%album%/%track% - %artist% - %title%')
        eq_(1,len(result))
        eq_('foo_artist',result[0].name)
        eq_(1,len(result[0]))
        eq_('foo_album',result[0][0].name)
        eq_(2,len(result[0][0]))
        eq_('09 - foo_artist - foo_title.mp3',result[0][0][0].name)
        eq_('[000] 09 - foo_artist - foo_title.mp3',result[0][0][1].name)
    
    def test_slash_in_tokens(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {
            'artist':'foo/artist',
            'album' :'foo\\album',
            'track' :9,
            'year'  :2005,
            'title':'foo/title',
            'genre':'foo/genre',
            }
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%artist%/%album%/%track% - %artist% - %title%')
        eq_(1,len(result))
        eq_('foo artist',result[0].name)
        eq_(1,len(result[0]))
        eq_('foo album',result[0][0].name)
        eq_(1,len(result[0][0]))
        eq_('09 - foo artist - foo title.mp3',result[0][0][0].name)
    
    def test_groups(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist%')
        eq_('E-L.mp3',result[0].name)
    
    def test_groups_lower(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'zoo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emp:lower%')
        eq_('p-z.mp3',result[0].name)
    
    def test_groups_on_exact_step(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'roo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emr:lower%')
        eq_('r-z.mp3',result[0].name)
    
    def test_groups_on_step_plus_one(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'soo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emr:lower%')
        eq_('r-z.mp3',result[0].name)
    
    def test_groups_on_step_minus_one(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'qoo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emr:lower%')
        eq_('m-q.mp3',result[0].name)
    
    def test_groups_genre(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'genre':'soo_genre',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:genre:emr:lower%')
        eq_('r-z.mp3',result[0].name)
    
    def test_groups_out_of_range(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'(oo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emr:lower%')
        eq_('a-d.mp3',result[0].name)
    
    def test_groups_empty(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%group:artist:emr:lower%')
        eq_('a-d.mp3',result[0].name)
    
    def test_firstletter_normal(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%firstletter:artist%')
        eq_('F.mp3',result[0].name)
    
    def test_firstletter_album(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'album':'goo_album',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%firstletter:album%')
        eq_('G.mp3',result[0].name)
    
    def test_firstletter_no_attr(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%firstletter:album%')
        eq_('(none).mp3',result[0].name)
    
    def test_firstletter_empty_attr(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%firstletter:artist%')
        eq_('(none).mp3',result[0].name)
    
    def test_firstletter_lower(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist',}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%firstletter:artist:lower%')
        eq_('f.mp3',result[0].name)
    
    def test_forbidden_chars(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {
            'artist':'foo/\\artist',
            'album' :'foo:*album',
            'title':'foo|?title',
            'genre':'foo<>genre',
            }
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%genre%/%album%/%artist% - %title%')
        eq_(1,len(result))
        eq_('foo  genre',result[0].name)
        eq_(1,len(result[0]))
        eq_('foo  album',result[0][0].name)
        eq_(1,len(result[0][0]))
        eq_('foo  artist - foo  title.mp3',result[0][0][0].name)
    
    def test_weakref(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {
            'artist':'foo_artist',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            'genre':'foo_genre',
            }
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%artist%/%album%/%track% - %artist% - %title%')
        copy = manualfs.Directory(None, '')
        copy.copy(result)
        w = weakref.ref(result)
        del result
        copy.detach_copy(True)
        gc.collect()
        assert w() is None
    
    def test_case_insensitive_option(self):
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist','title' :'t1'}
        file1 = self.Gen(attrs,dir,'foobar1')
        attrs = {'artist':'FOO_ARTIST','title' :'t2'}
        file2 = self.Gen(attrs,dir,'foobar2')
        result = RestructureDirectory(dir,'%artist%/%title%',case_sensitive=False)
        eq_(1,len(result))
        eq_(2,len(result.allfiles))
    
    def test_dont_rename_empty_tags(self):
        dir = manualfs.Directory(None, '')
        subdir = dir.new_directory('subdir')
        attrs = {
            'artist':'',
            'album' :'foo_album',
            'track' :9,
            'year'  :2005,
            'title':'foo_title',
            'genre':'foo_genre',
            }
        file = self.Gen(attrs,subdir,'foobar')
        result = RestructureDirectory(dir,'%artist%/%album%/%track% - %artist% - %title%',rename_empty_tag=False)
        eq_(1,len(result))
        eq_('(not renamed)',result[0].name)
        eq_(1,len(result[0]))
        eq_('subdir',result[0][0].name)
        eq_(1,len(result[0][0]))
        eq_('foobar.mp3',result[0][0][0].name)
    
    def test_backslashes_are_counted_as_slashes(self):
        #What happened here is that models containing backslashes could make 
        #the result not to create a directory when it should.
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist','title' :'t1'}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%artist%\\%title%')
        assert isinstance(result[0], manualfs.Directory)
    
    def test_job(self):
        def do_progress(progress):
            self.progress = progress
            return True
        
        self.progress = 0
        j = Job(1,do_progress)
        dir = manualfs.Directory(None, 'root')
        attrs = {'artist':'foo_artist','title' :'t1'}
        file = self.Gen(attrs,dir,'foobar')
        result = RestructureDirectory(dir,'%artist%\\%title%',parent_job=j)
        eq_(100,self.progress)
    

class TestSplit:
    def Gen(self,specs):
        #specs is a list of files you want to add to your virtual directory
        #Every item in specs must be a tuple like this:
        #(filename,size)
        #if filename is none, 'foobar_xxx' will be the filename, where xxx is a sequencial number
        result = TestDir(None,'')
        seq = 0
        for spec in specs:
            filename = spec[0]
            if not filename:
                filename = 'foobar_%d' % seq
                seq += 1
            file = result.AddFile(filename)
            file._read_all_info()
            file.size = spec[1]
        return result
    
    _one_byte = (None,1)
    
    def test_simple_one_chunk(self):
        #A test that should return only one chunk
        ref = self.Gen([self._one_byte,self._one_byte])
        splitter = Split(ref,'CD %sequence%',700 * 1024 * 1024)
        eq_(1,len(splitter))
        assert ref[0].name in splitter[0]
        assert ref[1].name in splitter[0]
    
    def test_simple_two_chunk(self):
        #A test that should return two chunks with one file in each
        ref = self.Gen([self._one_byte,self._one_byte])
        splitter = Split(ref,'CD %sequence%',1)
        eq_(2,len(splitter))
        assert ref[0].name in splitter[0]
        assert ref[1].name in splitter[1]
    
    def test_file_too_big_for_chunk(self):
        #Test a case where a file would be too big even to fit alone in a
        #single chunk. In this case, a chunk is created especially for this
        #file, and no other file will be added to it. It will be up to the
        #user of the Split to warn deal with these chunks appropriately.
        ref = self.Gen([self._one_byte,(None,2),self._one_byte])
        splitter = Split(ref,'CD %sequence%',2)
        eq_(3,len(splitter))
        assert ref[0].name in splitter[0]
        assert ref[1].name in splitter[1]
        assert ref[2].name in splitter[2]
    
    def test_chunk_name_sequence(self):
        ref = self.Gen([self._one_byte,self._one_byte])
        splitter = Split(ref,'CD %sequence%',1)
        eq_('CD 1',splitter[0].name)
        eq_('CD 2',splitter[1].name)
    
    def test_chunk_name_item(self):
        ref = self.Gen([('abc',1),('def',1)])
        splitter = Split(ref,'CD %item:first% - %item:last%',2)
        eq_('CD abc - def',splitter[0].name)
    
    def test_chunk_name_item_1st_letter(self):
        ref = self.Gen([('abc',1),('def',1)])
        splitter = Split(ref,'CD %item:first:1% - %item:last:1%',2)
        eq_('CD a - d',splitter[0].name)
    
    def test_chunk_name_item_2nd_letter(self):
        ref = self.Gen([('abc',1),('def',1)])
        splitter = Split(ref,'CD %item:first:2% - %item:last:2%',2)
        eq_('CD ab - de',splitter[0].name)

    def test_chunk_name_item_invalid_letter(self):
        ref = self.Gen([('abc',1),('def',1)])
        splitter = Split(ref,'CD %item:first:invalid% - %item:last:invalid%',2)
        eq_('CD abc - def',splitter[0].name)
    
    def test_invalid_model(self):
        ref = self.Gen([self._one_byte,self._one_byte])
        ref[0].artist = 'foobar_first'
        ref[1].artist = 'foobar_last'
        splitter = Split(ref,'CD %foobar% - %sequence:foobar:bleh% - %% - %artist% - %artist:foobar% - %artist:first:foobar% - %sequence%',2)
        eq_('CD (none) - (none) - (none) - (none) - (none) - (none) - 1',splitter[0].name)
    
    def test_chunk_name_formatted_sequence(self):
        ref = self.Gen([self._one_byte,self._one_byte])
        splitter = Split(ref,'CD %sequence:3%',1)
        eq_('CD 001',splitter[0].name)
        eq_('CD 002',splitter[1].name)
    
    def test_chunk_name_conflict(self):
        ref = self.Gen([('foobar1',1),('foobar2',1)])
        splitter = Split(ref,'CD %item:first:1% - %item:last:1%',1)
        eq_('CD f - f',splitter[0].name)
        eq_('[000] CD f - f',splitter[1].name)
    
    def test_that_structure_is_preserved(self):
        ref = self.Gen([self._one_byte,self._one_byte])
        dir1 = ref.AddDir('dir1')
        dir2 = ref.AddDir('dir2')
        ref.files[0].move(dir1)
        ref.files[0].move(dir2)
        splitter = Split(ref,'CD %sequence%',2)
        eq_(1,len(splitter))
        eq_(2,len(splitter[0]))
        eq_('dir1',splitter[0][0].name)
        eq_('dir2',splitter[0][1].name)
        eq_('foobar_0',splitter[0][0][0].name)
        eq_('foobar_1',splitter[0][1][0].name)
    
    def test_grouping(self):
        ref = self.Gen([self._one_byte,self._one_byte,self._one_byte])
        f1 = ref[0]
        f2 = ref[1]
        f3 = ref[2]
        d1 = ref.AddDir('a')
        d2 = ref.AddDir('b')
        f1.move(d1)
        f2.move(d2)
        f3.move(d2)
        splitter = Split(ref,'CD %sequence%',2)
        eq_(2,len(splitter))
        assert d1.name in splitter[0]
        assert d2.name in splitter[0]
        assert d2.name in splitter[1]
        assert f1.name in splitter[0][0]
        assert f2.name in splitter[0][1]
        assert f3.name in splitter[1][0]
        #now with grouping
        splitter = Split(ref,'CD %sequence%',2,1)
        eq_(2,len(splitter))
        assert d1.name in splitter[0]
        assert d2.name not in splitter[0]
        assert d2.name in splitter[1]
        assert f1.name in splitter[0][0]
        assert f2.name in splitter[1][0]
        assert f3.name in splitter[1][0]
    
    def test_group_too_large(self):
        #What happens here is that the grouping level is at one, but one of the level 1
        #directory is larger than the maximum capacity. What the splitter should do it to
        #progressively fall back to higher grouping level until it can fit something somewhere.
        #The result of this test should be:
        #CD 1/a/f1
        #CD 2/b/1/f1
        #CD 2/b/1/f3
        #CD 3/b/2/f4
        ref = self.Gen([self._one_byte,self._one_byte,self._one_byte,self._one_byte])
        f1 = ref[0]
        f2 = ref[1]
        f3 = ref[2]
        f4 = ref[3]
        d1 = ref.AddDir('a')
        d2 = ref.AddDir('b')
        d21 = d2.AddDir('1')
        d22 = d2.AddDir('2')
        f1.move(d1)
        f2.move(d21)
        f3.move(d21)
        f4.move(d22)
        splitter = Split(ref,'CD %sequence%',2,1)
        #There should be 3 cds, one with 'a', one with 'b', and another one with 'b'
        eq_(3,len(splitter))
        assert d1.name in splitter[0]
        assert d2.name not in splitter[0]
        assert d2.name in splitter[1]
        assert d2.name in splitter[2]
        assert d21.name in splitter[1][0]
        assert d22.name in splitter[2][0]
        assert f1.name in splitter[0][0]
        assert f2.name in splitter[1][0][0]
        assert f3.name in splitter[1][0][0]
        assert f4.name in splitter[2][0][0]
    
    def test_forbidden_chars(self):
        ref = self.Gen([('a|:<>',1),('b?\\/*',1)])
        splitter = Split(ref,'CD %item:first% - %item:last%',2)
        eq_('CD a - b',splitter[0].name)
    
    def test_file_that_is_higher_than_the_grouping_level(self):
        # if a file is in root of refdir when grouping level is 0, we want that
        # file at the root of its chunk in the splitted result.
        ref = manualfs.Directory(None, '')
        ref.new_file('foobar')
        splitted = Split(ref,'CD %sequence%',1,1)
        eq_('foobar',splitted[0][0].name)
    
    def test_file_too_large_dont_create_new_chunk_if_current_one_is_empty(self):
        ref = self.Gen([(None,2)])
        splitted = Split(ref,'foo',1)
        eq_(1,len(splitted))
    

class TestBatchOperation:
    def pytest_funcarg__dosetup(self, request):
        tmpdir = request.getfuncargvalue('tmpdir')
        self.rootpath = str(tmpdir)
        self.testpath = create_fake_fs(self.rootpath)
        ref = phys.Directory(None, self.testpath)
        copy = manualfs.Directory(None, '')
        copy.copy(ref)
        self.ref = ref
        self.copy = copy
    
    def test_main(self, dosetup):
        self.copy['file1.test'].name = 'foobar'
        self.copy['dir1'].name = 'foobar_dir'
        bo = BatchOperation(self.copy,self.testpath)
        bo.rename()
        ref = phys.Directory(None,self.testpath)
        assert 'foobar' in ref
        assert 'file1.test' not in ref
        assert 'foobar_dir' in ref
        assert 'file1.test' in ref['foobar_dir']
    
    def test_copy_has_a_name(self, dosetup):
        #The name of the root copy dir must not be included in the rename.
        self.copy.name = 'foobar'
        self.copy['file1.test'].name = 'foobar'
        bo = BatchOperation(self.copy,self.testpath)
        bo.rename()
        ref = phys.Directory(None,self.testpath)
        assert 'foobar' in ref
        assert 'file1.test' not in ref
    
    def test_copy_instead_of_move(self, dosetup):
        self.copy['file1.test'].name = 'foobar'
        self.copy['dir1'].name = 'foobar_dir'
        bo = BatchOperation(self.copy,self.testpath)
        bo.copy()
        ref = phys.Directory(None,self.testpath)
        assert 'foobar' in ref
        assert 'file1.test' in ref
        assert 'foobar_dir' in ref
        assert 'file1.test' in ref['foobar_dir']
        assert 'file1.test' in ref['dir1']
    
    def test_empty(self, dosetup):
        bo = BatchOperation(TestDir(None,''),'foobar')
        eq_([],bo.name_list)
    
    def test_simple(self, dosetup):
        ref = TestDir(None,'reference')
        ref.AddDir('dir').AddFile('subfile')
        ref.AddFile('file')
        copy = TestDir(None,'copy')
        copy.copy(ref)
        bo = BatchOperation(copy,Path('destination'))
        expected = [
            (Path(('reference','file')),Path(('destination','file'))),
            (Path(('reference','dir','subfile')),Path(('destination','dir','subfile'))),
        ]
        eq_(expected,bo.name_list)
    
    def test_source_same_as_dest(self, dosetup):
        ref = TestDir(None,'reference')
        ref.AddDir('dir').AddFile('subfile')
        ref.AddFile('file')
        copy = TestDir(None,'copy')
        copy.copy(ref)
        copy.files[0].rename('renamed')
        bo = BatchOperation(copy,Path('reference'))
        expected = [(Path(('reference','file')),Path(('reference','renamed')))]
        eq_(expected,bo.name_list)
    
    def test_renamed_as_list(self, dosetup):
        ref = TestDir(None,'reference')
        ref.AddDir('dir').AddFile('subfile')
        ref.AddFile('file')
        copy = TestDir(None,'copy')
        copy.copy(ref)
        bo = BatchOperation(copy.allfiles,Path('destination'))
        expected = [
            (Path(('reference','file')),Path(('destination','file'))),
            (Path(('reference','dir','subfile')),Path(('destination','dir','subfile'))),
        ]
        eq_(expected,bo.name_list)
    
    def test_cdrom_volume_name_list(self, dosetup):
        #ABOUT CD PROCESSING
        #
        #When the original song of a song in renamed is a children of a
        #mpl.Volume that has a VOLTYPE_CDROM vol_type, we must launch the
        #OnNeedCD event. That event will return either a path for the CD, from
        #which we will copy, '', or None.
        #
        #If it's a path, verify that all wanted files are there (re-launch a
        #OnNeedCD if not), and then copy the files to their destination
        #
        #If the reult is '', it means that the CD will be skipped.
        #
        #If the result is None, the operation is cancelled.
        #
        #ABOUT THIS TEST
        #
        #The actual copy (with CD prompting) will only happen on Copy or Rename.
        #meanwhile, BatchProcess has to build a name_list. Paths in name_list
        #that are from CDs will start with %cd:<cd name>%.
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(('','foobar')))
        eq_(3,len(bo.name_list))
        eq_(('!volume','fs','file1.test'),bo.name_list[0][0])
        eq_(('','foobar','fs','file1.test'),bo.name_list[0][1])
        eq_(('!volume','fs','file2.test'),bo.name_list[1][0])
        eq_(('','foobar','fs','file2.test'),bo.name_list[1][1])
        eq_(('!volume','fs','file3.test'),bo.name_list[2][0])
        eq_(('','foobar','fs','file3.test'),bo.name_list[2][1])
    
    def test_copy_tokenized_path(self, dosetup, tmpdir):
        def OnNeedCD(location):
            assert location is volume
            return Path(self.rootpath)
        
        copypath = str(tmpdir)
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(copypath))
        bo.OnNeedCD = OnNeedCD
        bo.copy()
        result = phys.Directory(None,copypath)
        eq_(1,len(result))
        eq_('fs',result[0].name)
    
    def test_with_job(self, dosetup):
        def update(progress,description=''):
            self.log.append(progress)
            return True
        
        self.copy['file1.test'].name = 'foobar'
        self.copy['dir1'].name = 'foobar_dir'
        bo = BatchOperation(self.copy,self.testpath)
        self.log = []
        job = Job(1,update)
        assert bo.copy(job)
        expected_log = [0, 0, 50, 100]
        eq_(expected_log,self.log)
    
    def test_OnNeedCD_returns_none(self, dosetup, tmpdir):
        def OnNeedCD(location):
            return
        
        copypath = str(tmpdir.join('copypath'))
        os.mkdir(copypath)
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(copypath))
        bo.OnNeedCD = OnNeedCD
        assert not bo.copy()
        result = phys.Directory(None,copypath)
        eq_(0,len(result))
    
    def test_with_job_cancel(self, dosetup):
        def update(progress,description=''):
            self.log.append(progress)
            return progress < 50
        
        self.copy['file1.test'].name = 'foobar'
        self.copy['dir1'].name = 'foobar_dir'
        bo = BatchOperation(self.copy,self.testpath)
        self.log = []
        job = Job(1,update)
        assert not bo.rename(job)
        expected_log = [0, 0, 50]
        eq_(expected_log,self.log)
    
    def test_with_ioerror(self, dosetup):
        #When not copying from CDs, operation throwing IOError should just
        #skip the operation and go to the next file.
        fake_file = manualfs.File(self.copy, 'fake_file')
        fake_original_dir = manualfs.Directory(None,'')
        fake_original_file = manualfs.File(fake_original_dir, 'fake_file')
        fake_file.copy(fake_original_file)
        bo = BatchOperation(self.copy,self.testpath)
        assert bo.copy()
    
    def test_with_ioerror_cd(self, dosetup, tmpdir):
        #When copying from CDs, operation throwing IOError should call OnNeedCD
        #until the file is found or the whole operation is cancelled.
        def OnNeedCD(location):
            self.need_cd_calls += 1
            if self.need_cd_calls == 3:
                return
            assert location is volume
            return self.rootpath
        
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        dir.new_file('fake')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(str(tmpdir)))
        self.need_cd_calls = 0
        bo.OnNeedCD = OnNeedCD
        assert not bo.copy()
        eq_(3,self.need_cd_calls)
    
    def test_cd_copy_with_job(self, dosetup, tmpdir):
        def OnNeedCD(location):
            assert location is volume
            return Path(self.rootpath)
        
        def update(progress,description=''):
            self.log.append(progress)
            return True
        
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(str(tmpdir)))
        bo.OnNeedCD = OnNeedCD
        self.log = []
        job = Job(1,update)
        assert bo.copy(job)
        expected_log = [0, 0, 33, 66, 100]
        eq_(expected_log,self.log)
    
    def test_cd_copy_OnNeedCD_returns_string(self, dosetup, tmpdir):
        #When OnNeedCD returns a string instead of a path, BO must work properly.
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        dir = volume.new_directory('fs')
        dir.new_file('file1.test')
        dir.new_file('file2.test')
        dir.new_file('file3.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(str(tmpdir)))
        bo.OnNeedCD = lambda location: self.rootpath
        assert bo.copy()
    
    def test_cd_move(self, dosetup, tmpdir):
        #When it's cd operation, we should ALWAYS copy.
        def OnNeedCD(location):
            assert location is volume
            return Path(self.testpath)
        
        root = Root(threaded=False)
        volume = root.new_directory('volume')
        volume.vol_type = VOLTYPE_CDROM
        volume.new_file('file1.test')
        renamed = manualfs.Directory(None, '')
        renamed.copy(volume)
        bo = BatchOperation(renamed,Path(str(tmpdir)))
        bo.OnNeedCD = OnNeedCD
        assert bo.rename()
        assert op.exists(op.join(self.testpath,'file1.test'))
    
    def test_rename_conflicts(self, dosetup):
        copy = self.copy
        file1 = copy['file1.test']
        file2 = copy['file2.test']
        file1.name = 'foobar'
        file2.name = 'file1.test'
        file1.name = 'file2.test'
        #There will be a conflict during the rename
        bo = BatchOperation(copy,Path(self.testpath))
        bo.rename()
        ref = phys.Directory(None,self.testpath)
        eq_(2,ref['file1.test'].size)
        eq_(1,ref['file2.test'].size)
    
    def test_rename_unresolved_conflict(self, dosetup, tmpdir):
        copypath = str(tmpdir.join('copypath'))
        shutil.copytree(self.testpath, copypath)
        bo = BatchOperation(self.copy,Path(copypath))
        #every file will be in conflict, but the conflict will not be resolved.
        bo.rename()
        tmpdir = phys.Directory(None,self.testpath)
        assert 'file1.test' in tmpdir
    
    def test_ProcessNormalList_catches_OSError_and_issue_warning(self, dosetup, tmpdir, monkeypatch):
        def FakeMove(_, __):
            raise OSError()
        
        monkeypatch.setattr(shutil, 'move', FakeMove)
        monkeypatch.setattr(sys, 'stdout', StringIO())
        assert sys.stdout.tell() == 0
        bo = BatchOperation(self.copy, Path('foo'))
        rootpath = Path(str(tmpdir))
        source = rootpath + 'zerofile'
        dest = rootpath + 'foo_zero'
        open(str(source), 'w').close() # He want the file to exist so the move call is made.
        try:
            bo._BatchOperation__ProcessNormalList([(source, dest)], False)
        except OSError:
            self.fail()
        assert sys.stdout.tell() > 0
    

class TestBatchOperation_unicode:
    # Path instances should only be "rendered" as unicode(), not str()
    def pytest_funcarg__dosetup(self, request):
        monkeypatch = request.getfuncargvalue('monkeypatch')
        tmpdir = request.getfuncargvalue('tmpdir')
        monkeypatch.setattr(sys, 'getfilesystemencoding', lambda: 'ascii') # force a failure on any non-ascii char
        testpath = Path(str(tmpdir))
        create_unicode_test_dir(testpath)
        sourcedir = phys.Directory(None, str(testpath))
        copy = manualfs.Directory(None, '')
        copy.copy(sourcedir)
        destpath = Path(str(tmpdir))
        self.sourcedircopy = copy
        self.destpath = destpath
        
    def test_copy(self, dosetup):
        bo = BatchOperation(self.sourcedircopy, self.destpath)
        try:
            bo.copy()
        except UnicodeEncodeError:
            self.fail()
    
    def test_rename(self, dosetup):
        bo = BatchOperation(self.sourcedircopy, self.destpath)
        try:
            bo.rename()
        except UnicodeEncodeError:
            self.fail()
    
    def test_warning(self, dosetup, monkeypatch):
        def FakeMove(_, __):
            raise OSError()
        
        monkeypatch.setattr(shutil, 'move', FakeMove)
        monkeypatch.setattr(sys, 'stdout', StringIO())
        bo = BatchOperation(self.sourcedircopy, self.destpath)
        try:
            bo.rename()
        except UnicodeEncodeError:
            self.fail()
    

class TestFSBuffer:
    def test_empty(self):
        buf = Buffer(5)
        eq_(5,buf.size)
        eq_([],buf.DoBufferingFor(''))
        eq_([],buf.content)
        eq_(0,buf.space_taken)
        eq_(5,buf.space_left)
    
    def test_one_dest(self):
        #buf only has one dest, so the process is quite straightforward.
        #Copy all sources on DoBufferingFor, and remove them all on PurgeBufferOf.
        buf = Buffer(3)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',1),
            (file3,'source2','dest1',1),
        )
        buf.AddFiles(files)
        eq_(0,buf.space_taken)
        eq_(3,buf.space_left)
        expected = [(file1,'source1','dest1',1),(file2,'source2','dest1',1),(file3,'source2','dest1',1)]
        eq_(expected,buf.DoBufferingFor('dest1'))
        eq_(expected,buf.content)
        eq_(3,buf.space_taken)
        eq_(0,buf.space_left)
        eq_(expected,buf.PurgeBufferOf('dest1'))
        eq_([],buf.content)
        eq_(0,buf.space_taken)
        eq_(3,buf.space_left)
    
    def test_get_sources_get_destinations(self):
        buf = Buffer(3)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',1),
            (file3,'source2','dest2',1),
        )
        expected = ['source1','source2']
        eq_(expected,buf.GetSources(files))
        expected = ['dest1','dest2']
        eq_(expected,buf.GetDestinations(files))
    
    def test_two_dest_enough_space(self):
        #Here, we have 2 dests, and enough space to hold every files. Thus,
        #all files are copied on the first DoBufferingFor, but only files for
        #dest1 are removed in the purge. Then, no files are copied on the
        #second buffering, and the remaining file is removed on the second
        #purge.
        buf = Buffer(3)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',1),
            (file3,'source2','dest2',1),
        )
        buf.AddFiles(files)
        expected = [(file1,'source1','dest1',1),(file2,'source2','dest1',1),(file3,'source2','dest2',1)]
        eq_(expected,buf.DoBufferingFor('dest1'))
        eq_(expected,buf.content)
        expected = [(file1,'source1','dest1',1),(file2,'source2','dest1',1)]
        eq_(expected,buf.PurgeBufferOf('dest1'))
        expected = [(file3,'source2','dest2',1)]
        eq_(expected,buf.content)
        eq_([],buf.DoBufferingFor('dest2'))
        eq_(expected,buf.content)
        eq_(expected,buf.PurgeBufferOf('dest2'))
        eq_([],buf.content)
    
    def test_two_dest_not_enough_space(self):
        #Here, we have 2 dests, and notenough space to hold every files. Thus,
        #only 2 files are copied on the first DoBufferingFor, and are both removed
        #on purge. Then, the last one is copied on the 2nd buffering, and removed
        #on the 2nd purge.
        buf = Buffer(2)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',1),
            (file3,'source2','dest2',1),
        )
        buf.AddFiles(files)
        expected = [(file1,'source1','dest1',1),(file2,'source2','dest1',1)]
        eq_(expected,buf.DoBufferingFor('dest1'))
        eq_(expected,buf.content)
        eq_(expected,buf.PurgeBufferOf('dest1'))
        expected = [(file3,'source2','dest2',1)]
        eq_([],buf.content)
        eq_(expected,buf.DoBufferingFor('dest2'))
        eq_(expected,buf.content)
        eq_(expected,buf.PurgeBufferOf('dest2'))
        eq_([],buf.content)
    
    def test_get_bytes_required(self):
        buf = Buffer(2)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',2),
            (file3,'source2','dest2',1),
        )
        buf.AddFiles(files)
        eq_(3,buf.GetMinimumBytesRequired())
        eq_(4,buf.GetMaximumBytesRequired())
    
    def test_set_size(self):
        buf = Buffer(5)
        file1 = 'foobar/file1'
        file2 = 'foobar/file2'
        file3 = 'foobar/file3'
        files = (
            (file1,'source1','dest1',1),
            (file2,'source2','dest1',2),
            (file3,'source2','dest2',1),
        )
        buf.AddFiles(files)
        buf.DoBufferingFor('dest1')
        eq_(5,buf.size)
        eq_(4,buf.space_taken)
        eq_(1,buf.space_left)
        buf.size = 10
        eq_(10,buf.size)
        eq_(4,buf.space_taken)
        eq_(6,buf.space_left)
    
