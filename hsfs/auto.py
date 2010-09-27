# Created By: Virgil Dupras
# Created On: 2005/01/05
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from unicodedata import normalize
import logging

from hsutil.misc import flatten
from . import _fs as fs

def hold_update(method):
    ''' Holds updates during the execution of a auto directory method.
    
        One of the problems with the auto paradigm is that sometimes you're in the middle of an
        operation (let's say rename) and then an update happens right when you're in the middle of 
        it, effectively messing up your directory. What you want to do is to hold your update until
        the operation is over.
    '''
    def wrapper(self, *args, **kwargs):
        self._begin_operation()
        try:
            result = method(self, *args, **kwargs)
        finally:
            self._end_operation()
        return result
    
    return wrapper

def hold_parent_update(method):
    ''' Holds updates during the execution of a auto directory children method.
    
        Same as hold_update, but it calls begin/end on the parent instead of on self.
    '''
    def wrapper(self, *args, **kwargs):
        if self.parent is None:
            return method(self, *args, **kwargs)
        self.parent._begin_operation()
        try:
            result = method(self, *args, **kwargs)
        finally:
            self.parent._end_operation()
        return result
    
    return wrapper

class Directory(fs.Directory):
    #---Overrides
    def __init__(self, parent=None, dirname=''):
        self._lastupdate = 0
        self.__updating = False
        super(Directory, self).__init__(parent, dirname)
    
    def __contains__(self, node):
        if isinstance(node, str) and self.__needs_update():
            return node in flatten(self._fetch_subitems())
        else:
            return super(Directory, self).__contains__(node)

    def __getitem__(self, key):
        self.__update_if_needed()
        return super(Directory, self).__getitem__(key)

    def __iter__(self):
        self.__update_if_needed()
        return super(Directory, self).__iter__()

    def __len__(self):
        self.__update_if_needed()
        return super(Directory, self).__len__()
    
    def _invalidate_path(self, recursive=True):
        # We must not auto generate children on InvalidatePath because it would make the whole auto 
        # thing pointless (Every children would be created as soon as the first child is added to 
        # the root)
        super(Directory, self)._invalidate_path(False)
        if recursive:
            for child in super(Directory, self).__iter__():
                child._invalidate_path()
    
    #---Private
    def __needs_update(self):
        return (not self.__updating) and (self._get_mtime() > self._lastupdate)
    
    def __update_if_needed(self):
        if self.__needs_update():
            self.__updating = True
            self._do_update()
            self.__updating = False
    
    #---Virtual
    def _fetch_subitems(self):
        ''' Returns a list of subitems in the format ([subdirs], [subfiles])
        '''
        return ([], [])
    
    # Return the last modification time this is used to know if we must refresh
    def _get_mtime(self):
        return 0
    
    #---Protected
    def _do_update(self):
        subdirs, subfiles = self._fetch_subitems()
        ref_names = subdirs + subfiles
        # purge items from elements for which the name is not in ref_names
        to_purge = ((item, item.name) for item in self[:] if item.name not in ref_names)
        for item, name in to_purge:
            if isinstance(name, str):
                # Check if the NFD/NFC versions of the name are there
                nfd_name = normalize('NFD', name)
                if nfd_name in ref_names:
                    item.name = nfd_name
                    continue
                nfc_name = normalize('NFC', name)
                if nfc_name in ref_names:
                    item.name = nfc_name
                    continue
            logging.debug('Purged %s' % repr(item.path))
            item.parent = None # Not in ref_names, purge.
        for d in subdirs:
            if d not in self:
                self._create_sub_dir(d)
        for f in subfiles:
            if f not in self:
                self._create_sub_file(f)
        self._lastupdate = self._get_mtime()
    
    def _begin_operation(self):
        self.__updating = True
    
    def _end_operation(self):
        self.__updating = False
    
    #---Public
    @hold_update
    def force_update(self):
        # One might wonder "Why not just clear the tree?" That's because we might be holding up to
        # a subtree's instance, and that subtree instance has to be updated as well.
        self._lastupdate = 0
        for f in self.files:
            f._invalidate_info()
        for d in self.dirs:
            d.force_update()
    
    #---Properties
    @property
    def dirs(self):
        self.__update_if_needed()
        return super(Directory, self).dirs
    
    @property
    def files(self):
        self.__update_if_needed()
        return super(Directory, self).files
    
