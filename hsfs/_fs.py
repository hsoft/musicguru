# Created By: Virgil Dupras
# Created On: 2004/12/06
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import logging

from hscommon.path import Path
from hscommon.util import get_file_ext

from . import tree
from .stats import Stats

#---Exceptions------------------------------------------------------------------
class FSError(Exception):
    cls_message = "An error has occured on '{name}' in '{parent}'"
    def __init__(self, fsobject, parent=None, message=None):
        if not message:
            message = self.cls_message
        if isinstance(fsobject, str):
            self.name = fsobject
        elif isinstance(fsobject, Node):
            self.name = fsobject.name
            if parent is None:
                parent = fsobject.parent
        else:
            self.name = ''
        if isinstance(parent, str):
            self.parentname = parent
        elif isinstance(parent, Directory):
            self.parentname = parent.name
        else:
            self.parentname = ''
        Exception.__init__(self, message.format(name=self.name, parent=self.parentname))
    

class AlreadyExistsError(FSError):
    "The directory or file name we're trying to add already exists"
    cls_message = "'{name}' already exists in '{parent}'"

class InvalidPath(FSError):
    "The path of self is invalid, and cannot be worked with."
    cls_message = "'{name}' is invalid."

#---Classes---------------------------------------------------------------------
class Node(tree.HashedTree):
    """Base class for both Files and Directories.
    
    This the the base class for files and directories. It basically takes care
    of path stuff.
    """
    cls_is_container = True
    #---Override
    def __init__(self, parent, value):
        try:
            self.__path = None
            super(Node, self).__init__(parent, value)
        except tree.HashCollisionError:
            raise AlreadyExistsError(self, parent)
    
    def _do_before_add(self, child):
        try:
            child._invalidate_path()
            super(Node, self)._do_before_add(child)
        except tree.HashCollisionError:
            raise AlreadyExistsError(child, self)
    
    #---Protected
    def _build_path(self):
        return self.parent.path + (self.value, ) if self.parent is not None else Path((self.value, ))
    
    def _invalidate_path(self, recursive=True):
        self.__path = None
        if recursive:
            for child in self:
                child._invalidate_path()
    
    def _set_name(self, newname):
        try:
            if not newname:
                return
            self._invalidate_path()
            self.value = newname
        except tree.HashCollisionError:
            raise AlreadyExistsError(newname, self.parent)
    
    #---Public
    def find_path(self, path):
        if not path:
            return self
        try:
            found = self[path[0]]
            return found.find_path(path[1:])
        except KeyError:
            return
    
    #---Properties
    @property
    def is_container(self):
        return self.cls_is_container
    
    @property
    def name(self):
        return self.value
    
    @name.setter
    def name(self, value):
        self._set_name(value)
    
    @property
    def path(self):
        if self.__path is None:
            self.__path = self._build_path()
        return self.__path
    

class File(Node):
    cls_is_container = False
    INITIAL_INFO = {
        'size': 0,
        'ctime': 0,
        'mtime': 0,
        'md5': '',
        'md5partial': '',
    }
    
    def __init__(self, parent, filename):
        #This offset is where we should start reading the file to get a partial md5
        #For audio file, it should be where audio data starts
        self._md5partial_offset = 0x4000 #16Kb
        self._md5partial_size   = 0x4000 #16Kb
        super(File, self).__init__(parent, filename)
    
    def __getattr__(self, attrname):
        # Only called when attr is not there
        if attrname in self.INITIAL_INFO:
            try:
                self._read_info(attrname)
            except Exception as e:
                logging.warning("An error '%s' was raised while decoding '%s'", e, repr(self.path))
            try:
                return self.__dict__[attrname]
            except KeyError:
                return self.INITIAL_INFO[attrname]
        raise AttributeError()
    
    #---Protected
    def _do_after_value_change(self, newvalue): #Override
        super(File, self)._do_after_value_change(newvalue)
        if self.parent is not None:
            self.parent._sortedfiles = None
            self.parent._reset_stats()
    
    def _read_info(self, field):
        pass
    
    def _invalidate_info(self):
        for attrname in self.INITIAL_INFO:
            if attrname in self.__dict__:
                delattr(self, attrname)
    
    #---Protected
    def _read_all_info(self, attrnames=None):
        """Cache all possible info.
        
        If `attrnames` is not None, caches only attrnames.
        """
        if attrnames is None:
            attrnames = list(self.INITIAL_INFO.keys())
        for attrname in attrnames:
            if attrname not in self.__dict__:
                self._read_info(attrname)
    
    #---Properties
    @property
    def extension(self):
        return get_file_ext(self.name)
    

class Directory(Node, Stats):
    #---Class attributes
    cls_file_class = File
    cls_dir_class = None
    
    #---Magic functions
    def __init__(self, parent=None, dirname=''):
        self._sorteddirs = None
        self._sortedfiles = None
        super(Directory, self).__init__(parent, dirname)
    
    #---Private
    def __child_moved(self, child):
        if child.is_container:
            self._sorteddirs = None
        else:
            self._sortedfiles = None
        self._reset_stats()
    
    #---Overrides
    def _do_after_add(self, child):
        super(Directory, self)._do_after_add(child)
        self.__child_moved(child)
    
    def _do_after_value_change(self, newvalue):
        super(Directory, self)._do_after_value_change(newvalue)
        if self.parent is not None:
            self.parent._sorteddirs = None
            self.parent._reset_stats()
    
    def _do_after_remove(self, child):
        super(Directory, self)._do_after_remove(child)
        self.__child_moved(child)
    
    def _reset_stats(self):
        result = super(Directory, self)._reset_stats()
        if result and (self.parent is not None):
            self.parent._reset_stats()
    
    #---Virtual
    _sort_key = staticmethod(lambda x: x.name.lower())
    
    def _create_sub_dir(self, name, with_parent=True):
        parent = self if with_parent else None
        if self.cls_dir_class is not None:
            return self.cls_dir_class(parent, name)
        else:
            return self.__class__(parent, name)
    
    def _create_sub_file(self, name, with_parent=True):
        parent = self if with_parent else None
        return self.cls_file_class(parent, name)
    
    #---Public
    def find_sub_dir(self, name):
        """
        Find the sub directory with the name dirname. This function doesn't
        recurse and only return a directory if dirname is found immediately in
        self.
        """
        try:
            result = self[name]
            if result.is_container:
                return result
        except KeyError:
            pass
    
    def find_sub_file(self, name):
        """
        find_sub_dir, but for files
        """
        try:
            result = self[name]
            if not result.is_container:
                return result
        except KeyError:
            pass
    
    def iteralldirs(self):
        return self.iterall(lambda x: x.is_container)
    
    def iterallfiles(self):
        for child in self:
            if child.is_container:
                for subchild in child.iterallfiles():
                    yield subchild
            else:
                yield child
    
    #---Properties
    @property
    def alldirs(self):
        return list(self.iteralldirs())
    
    @property
    def allfiles(self):
        return list(self.iterallfiles())
    
    @property
    def dirs(self):
        if self._sorteddirs is None:
            self._sorteddirs = [child for child in self if child.is_container]
            self._sorteddirs.sort(key=self._sort_key)
        return self._sorteddirs[:]
    
    @property
    def files(self):
        if self._sortedfiles is None:
            self._sortedfiles = [child for child in self if not child.is_container]
            self._sortedfiles.sort(key=self._sort_key)
        return self._sortedfiles[:]
    
    @property
    def dircount(self):
        return len(self.dirs)
    
    @property
    def filecount(self):
        return len(self.files)
    
