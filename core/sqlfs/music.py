# Created By: Virgil Dupras
# Created On: 2006/10/06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from . import _sql as sql

import hsfs as fs
import hsfs.music
from hsfs.phys import music
from hscommon import io
from hscommon.path import Path
from jobprogress.job import nulljob, JobCancelled

class Node:
    @property
    def parent_volume(self):
        if self.parent is not None:
            return self.parent.parent_volume
    
    @property
    def physical_path(self):
         return self.parent.physical_path + self.name
    

class File(sql.File, Node, hsfs.music._File):
    pass

class Directory(sql.Directory, Node):
    cls_file_class = File

(VOLTYPE_CDROM,
VOLTYPE_FIXED) = list(range(2))

(MODE_NORMAL,
MODE_PHYSICAL,
MODE_TOKEN) = list(range(3))

class Volume(Directory):
    cls_dir_class = Directory
    def __init__(self, parent, name):
        super(Volume, self).__init__(parent, name)
        self.__initial_path = None
        self.__mode = MODE_NORMAL
    
    #---Protected
    def _build_path(self): #Override
        if self.mode == MODE_PHYSICAL:
            return self.physical_path
        elif self.mode == MODE_TOKEN:
            return ('!%s' % self.name, )
        else:
            return super(Volume, self)._build_path()
    
    #---Public
    def update(self, ref=None, job=nulljob):
        if ref is None:
            ref = music.Directory(None, str(self.initial_path))
        try:
            super(Volume, self).update(ref, job=job)
        except fs.InvalidPath:
            pass
    
    #---Properties
    @property
    def initial_path(self):
        if self.__initial_path is None:
            try:
                value = self._get_attr('initial_path')
            except KeyError:
                value = ''
            self.__initial_path = Path(value)
        return self.__initial_path
    
    @initial_path.setter
    def initial_path(self, value):
        self._set_attr('initial_path', str(value))
        self.__initial_path = None
    
    @property
    def is_available(self):
        return io.exists(self.physical_path)
    
    @property
    def is_removable(self):
        return self.vol_type == VOLTYPE_CDROM
    
    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, value):
        self.__mode = value
        self._invalidate_path()
    
    @property
    def parent_volume(self):
        return self
    
    @property
    def physical_path(self):
        if self.vol_type == VOLTYPE_CDROM:
            return self.parent.buffer_path + self.name
        else:
            return self.initial_path
    
    @property
    def vol_type(self):
        try:
            return self._get_attr('vol_type')
        except KeyError:
            return VOLTYPE_FIXED
    
    @vol_type.setter
    def vol_type(self, value):
        self._set_attr('vol_type',value)
    

class Root(sql.Root):
    cls_dir_class = Volume
    cls_file_class = File
    
    def __init__(self, dbname=':memory:', dirname='', threaded=True):
        super(Root, self).__init__(dbname, dirname, threaded=threaded)
        self._attrs_to_read = ['audiosize', 'size', 'ctime', 'mtime', 'duration', 'bitrate', 'samplerate', 'title', 
            'artist', 'album', 'genre', 'year', 'track', 'comment']
    
    def add_volume(self, ref, volume_name, volume_type, job=nulljob):
        result = self.new_directory(volume_name)
        try:
            result.update(ref, job)
        except JobCancelled:
            # If add_volume is cancelled, we don't want a half updated volume added.
            # We want nothing added.
            result.delete()
            raise
        result.vol_type = volume_type
        result.initial_path = ref.path
        return result
    
    def update_volumes(self,job=nulljob):
        updatable = [volume for volume in self if volume.vol_type == VOLTYPE_FIXED]
        job = job.start_subjob(len(updatable))
        for volume in updatable:
            volume.update(job=job)
    
    buffer_path = Path(())
