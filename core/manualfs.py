# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2004-12-27
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import hsfs as fs
from hscommon import job
from hsutil.misc import nonone
from hsutil.conflict import get_conflicted_name, is_conflicted

class _CopyOf(object):
    #--- Public
    
    def copy(self, refnode):
        self.copyof = refnode
    
    def detach_copy(self, keep_original_files=False, keep_original_dirs=False):
        if self.is_container:
            keep = keep_original_dirs
        else:
            keep = keep_original_files
        if keep:
            self.copyof = self.original
        else:
            self.copyof = None
        for child in self:
            child.detach_copy(keep_original_files,keep_original_dirs)
    
    #--- Properties
    
    copyof = None
    
    @property
    def original(self):
        if hasattr(self.copyof, 'original'):
            return self.copyof.original
        else:
            return nonone(self.copyof, self)
    

class Node(fs.Node):
    #--- Override
    
    def __init__(self, parent=None, name=''):
        try:
            super(Node, self).__init__(parent,name)
        except fs.AlreadyExistsError:
            newname = parent._resolve_conflict(parent[name], self, name)
            if newname:
                if isinstance(newname, basestring):
                    super(Node, self).__init__(parent, newname)
            else:
                raise
    
    def _set_name(self, newname):
        try:
            super(Node, self)._set_name(newname)
        except fs.AlreadyExistsError:
            newname = self.parent._resolve_conflict(self.parent[newname], self, newname)
            if newname:
                if isinstance(newname, basestring):
                    super(Node, self)._set_name(newname)
            else:
                raise
    
    #--- Public
    def delete(self):
        self.parent = None
    
    def move(self, dest, newname=None):
        dest.add_child(self, newname)
    
    def rename(self, newname):
        self.name = newname
    

class File(fs.File, Node, _CopyOf):
    #--- Public
    def copy(self, reffile):
        super(File,self).copy(reffile)
        for attrname in reffile.INITIAL_INFO:
            if attrname in reffile.__dict__:
                setattr(self, attrname, getattr(reffile, attrname))
        self.INITIAL_INFO = reffile.INITIAL_INFO
    

class Directory(fs.Directory, Node, _CopyOf):
    """A Directory that you can manipulate at will
    
    This is the opposite of auto.Directory. When you subclass this, you have
    to manually add/delete/move everything.
    
    Littles notes:
    
    You might notice that some AlreadyExistsError are raised in this unit.
    You might think "hey, fs.Directory covers all possible occurance of
    AlreadyExistsError, why do you duplicate code here?" It is true that
    fs.Directory takes care of all this. However, if you look at the code
    after the raise (in this unit), you will see that , first, it is only in
    move. And what's special about move funcs is that you can change the
    name as you move. And to do this, you must delete the child from
    it's former parent before you add it in it's new parent. If you don't
    check for conflict *before* and there's is a conflict occuring, you're
    left with a parent less child.
    """
    #--- Class Attributes
    cls_file_class = File
    
    #--- Overrides
    def __init__(self, parent=None, dirname=''):
        if isinstance(parent, Directory):
            self.__case_sensitive = parent.case_sensitive
        else:
            self.__case_sensitive = True
        self._attrs_to_read = None
        super(Directory, self).__init__(parent, dirname)
    
    def _do_hash(self, value):
        if (not self.case_sensitive) and isinstance(value, basestring):
            return value.lower()
        else:
            return value
    
    #--- Protected
    def _conflict_check(self, name, node):
        if name in self:
            newname = self._resolve_conflict(self[name], node, name)
            if newname:
                return newname
            else:
                raise fs.AlreadyExistsError(name, self)
        else:
            return name
    
    def _resolve_conflict(self, offended, offender, conflicted_name): # Virtual
        """Override this to automatically resolve a name conflict instead
        of raising an AlreadyExistsError. If you return something else than
        None or '', there will be a second try to add name. There is no
        third try. if the result of ResolveConflict is also conflictual,
        an error will be raised. You can also return a True value that is not
        a string, and it will cancel the exception raise, but not make a second
        try.
        """
    
    #--- Public
    def add_child(self, child, newname=None):
        if child in self:
            return child
        if not newname:
            newname = child.name
        newname = self._conflict_check(newname, child)
        if not isinstance(newname, basestring):
            return child #Just don't perform the add, _resolve_conflict has taken 
                         #care of everything
        child.parent = None
        child.name = newname
        child.parent = self
        if isinstance(child, Directory):
            child.case_sensitive = self.case_sensitive
        return child
    
    def add_dir_copy(self, refdir, newname='', job=job.nulljob):
        if not newname:
            newname = refdir.name
        result = self._create_sub_dir(newname, False)
        result.copy(refdir, job)
        self.add_child(result)
        return result
    
    def add_file_copy(self, reffile, newname=''):
        if not newname:
            newname = reffile.name
        reffile._read_all_info(self._attrs_to_read)
        result = self._create_sub_file(newname, False)
        result.copy(reffile)
        self.add_child(result)
        return result
    
    def add_path(self, path):
        """
        Creates the first item of path (a tuple), and calls _AddPath in this new
        directory. If the directory already exists, uses this directory.
        Returns the added (or found) directory.
        """
        if not path:
            return self
        else:
            try:
                founddir = self[path[0]]
                if not isinstance(founddir, Directory):
                    raise fs.InvalidPath(founddir)
            except KeyError:
                founddir = self._create_sub_dir(path[0])
            return founddir.add_path(path[1:])
    
    def clean_empty_dirs(self):
        for directory in self.dirs:
            directory.clean_empty_dirs()
        to_delete = (d for d in self.dirs if not len(d))
        for directory in to_delete:
            directory.delete()
    
    def copy(self, refdir, job=job.nulljob):
        super(Directory, self).copy(refdir)
        filecount = refdir.filecount
        dircount  = refdir.dircount
        if filecount > 0:
            job = job.start_subjob(dircount + 1)
            job.start_job(filecount)
        else:
            job = job.start_subjob(dircount)
        for myfile in refdir.files:
            self.add_file_copy(myfile)
            job.add_progress()
        for directory in refdir.dirs:
            self.add_dir_copy(directory, '', job)
    
    def new_directory(self, name):
        return self._create_sub_dir(name)
    
    def new_file(self, name):
        return self._create_sub_file(name)
    
    #--- Properties
    @property
    def case_sensitive(self):
        return self.__case_sensitive
    
    @case_sensitive.setter
    def case_sensitive(self, value):
        if value != self.__case_sensitive:
            self.__case_sensitive = value
            self._rebuild_hashes()
            for subdir in self:
                if isinstance(subdir, Directory):
                    subdir.case_sensitive = value
    

class AutoResolve(Directory):
    #---Override
    def _resolve_conflict(self, offended, offender, conflicted_name):
        if offended.is_container and offender.is_container:
            should_merge = self.on_should_merge(offender, offended)
            if should_merge:
                # There's a circular reference problem
                from .fs_utils import smart_move
                smart_move(offender, offended)
                offender.delete()
                return True
        return get_conflicted_name(self, conflicted_name)
    
    #---Events
    def on_should_merge(self, source, dest):
        if (self.parent is not None) and hasattr(self.parent, 'on_should_merge'):
            return self.parent.on_should_merge(source, dest)
    
    #---Properties
    @property
    def allconflicts(self):
        return self.get_stat('conflicts', [])
    
    @property
    def conflicts(self):
        return [y for y in self.files if is_conflicted(y.name)]
    

class AutoMerge(AutoResolve):
    def on_should_merge(self, source, dest):
        return True
    
