# Created By: Virgil Dupras
# Created On: 2004/12/07
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import hashlib
import time
import logging

from hsutil.misc import nonone
from hsutil import io
from .. import _fs as fs, auto

MTIME_COOLDOWN = 1 # 1 second minimum cooldown between GetMTime() calls

class InvalidDestinationError(fs.FSError):
    """A copy/move operation has been called, but the destination is invalid."""
    cls_message = "'{name}' is an invalid destination for this operation."

class OperationError(fs.FSError):
    """A copy/move/delete operation has been called, but the checkup after the 
    operation shows that it didn't work."""
    cls_message = "Operation on '{name}' failed."

class Node(object):
    def _do_get_mtime(self):
        # This function is called quite often. The goal here is to only actually call os.stat() once
        # a second at most, unless we made a modification from *here*. That's why _EndOperation()
        # resets the counter.
        last_mtime_time = getattr(self, '_last_mtime_time', 0)
        if time.time() - last_mtime_time < MTIME_COOLDOWN:
            return self._last_mtime_value
        try:
            self._last_mtime_time = time.time()
            self._last_mtime_value = io.stat(self.path).st_mtime
        except OSError:
            self._last_mtime_value = 1
        return self._last_mtime_value
    
    def _do_copy(self, src, dest):
        raise NotImplementedError()
    
    def copy(self, dest, newname='', force=False):
        if not isinstance(dest, Directory):
            raise InvalidDestinationError(dest)
        if newname == '':
            newname = self.path[-1]
        if (not force) and (newname in dest):
            raise fs.AlreadyExistsError(self, dest)
        try:
            self._do_copy(self.path, dest.path + newname)
        except EnvironmentError:
            raise OperationError(self)
        dest._do_update()
        if newname in dest:
            return dest[newname]
        else:
            raise OperationError(self)
    
    def _do_delete(self, path):
        raise NotImplementedError()
    
    def delete(self):
        oldparent = self.parent
        self._do_delete(self.path)
        oldparent._do_update()
        if self in oldparent:
            raise OperationError(self)
    
    def move(self, dest, newname='', force=False):
        if not isinstance(dest, Directory):
            raise InvalidDestinationError(dest)
        oldparent = self.parent
        if newname == '':
            newname = self.path[-1]
        if newname in dest:
            if force:
                dest[newname].delete()
            else:
                raise fs.AlreadyExistsError(self,dest)
        #We want to keep the same instance, thus we move self manually
        old_path = self.path
        old_parent = self.parent
        self.parent = None
        self.name = newname
        self.parent = dest
        try:
            io.move(old_path, dest.path + newname)
        except EnvironmentError:
            self.parent = old_parent
            raise OperationError(self)
        oldparent._do_update()
        dest._do_update()
        return self
    
    @auto.hold_parent_update
    def rename(self, newname):
        if newname in self.parent:
            raise fs.AlreadyExistsError(self, newname)
        oldpath = self.path
        newpath = self.path[:-1] + newname
        try:
            io.rename(oldpath, newpath)
            self.name = newname
        except OSError:
            raise OperationError(self)
    

class File(fs.File, Node):
    #---Override
    def _get_mtime(self):
        return self._do_get_mtime()
    
    def _read_info(self, field):
        super(File, self)._read_info(field)
        if field in ('size', 'ctime', 'mtime'):
            stats = io.stat(self.path)
            self.size = nonone(stats.st_size, 0)
            self.ctime = nonone(stats.st_ctime, 0)
            self.mtime = nonone(stats.st_mtime, 0)
        elif field == 'md5partial':
            try:
                fp = io.open(self.path, 'rb')
                offset = self._md5partial_offset
                size = self._md5partial_size
                fp.seek(offset)
                partialdata = fp.read(size)
                md5 = hashlib.md5(partialdata)
                self.md5partial = md5.digest()
                fp.close()
            except Exception:
                pass
        elif field == 'md5':
            try:
                fp = io.open(self.path, 'rb')
                filedata = fp.read()
                md5 = hashlib.md5(filedata)
                self.md5 = md5.digest()
                fp.close()
            except Exception:
                pass
    
    def _do_copy(self, src, dest):
        io.copy(src, dest)
    
    def _do_delete(self, path):
        io.remove(path)
    
class Directory(auto.Directory, Node):
    #---Class
    cls_file_class = File
    #---Override
    def _get_mtime(self):
        return self._do_get_mtime()
    
    def _fetch_subitems(self):
        try:
            items = io.listdir(self.path)
            bogus_names = [name for name in items if not isinstance(name, str)]
            if bogus_names:
                logging.warning("Encountered files with the wrong encoding: %r", bogus_names)
                items = (name for name in items if isinstance(name, str))                
            items = (name for name in items if not io.islink(self.path + name))
            subdirs = []
            subfiles = []
            for name in items:
                if io.isdir(self.path + name):
                    subdirs.append(name)
                else:
                    subfiles.append(name)
            return (subdirs, subfiles)
        except OSError:
            if self.parent is not None:
                return ([], [])
            else:
                raise fs.InvalidPath(self)
    
    def _do_copy(self, src, dest):
        io.copytree(src, dest, True)
    
    def _do_delete(self, path):
        io.rmtree(path)
    
