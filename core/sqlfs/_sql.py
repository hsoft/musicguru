# Created By: Virgil Dupras
# Created On: 2006/10/03
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sqlite3 as sqlite
import time
from weakref import WeakValueDictionary

import hsfs as fs
from hscommon.job import nulljob, JobCancelled
from hsutil.misc import tryint
from hsutil.str import multi_replace
import hscommon.sqlite

(NODE_TYPE_DIR,
NODE_TYPE_FILE) = list(range(2))

(ATTR_TYPE_INT,
ATTR_TYPE_STR,
ATTR_TYPE_BINARY) = list(range(3))

def db_to_value(value_type,value):
    if value_type == ATTR_TYPE_INT:
        return tryint(value)
    if value_type == ATTR_TYPE_BINARY:
        divided = [value[i:i+2] for i in range(0,len(value),2)]
        return ''.join([chr(int(hex_repr,16)) for hex_repr in divided])
    return value

def value_to_db(value):
    value_type = get_value_type(value)
    if value_type == ATTR_TYPE_INT:
        value = str(value)
    elif value_type == ATTR_TYPE_BINARY:
        value = ''.join(['%02x' % ord(char) for char in value])
    else:
        if isinstance(value,str):
            value = multi_replace(value,['\n','\r'],'')
        else:
            value = str(value)
    return value

def get_value_type(value):
    if isinstance(value, (int, float)):
        return ATTR_TYPE_INT
    try:
        if not isinstance(value, str):
            if isinstance(value, bytes):
                return value.decode('utf-8')
            else:
                return str(value)
        return ATTR_TYPE_STR
    except UnicodeDecodeError:
        return ATTR_TYPE_BINARY

class Node(object):
    """Base class for File, Directory and Root.
    
    This handles all things common to File, Directory and Root, such as _get_attrs and _set_attrs.
    """
    def _get_attr(self, key):
        #Unlike _set_attr, the overhead of using _get_attrs would be bigger here, the whole set of 
        #attrs would be fetched, just to pick one value.
        sql = "select type,value from attrs where parent = ? and name = ?"
        result = self.con.execute(sql,(self.id,key))
        try:
            value_type, value = result.fetchall()[0]
            return db_to_value(value_type,value)
        except IndexError:
            raise KeyError("Attr '%s' does not exists for id %d" % (key,self.id))
    
    def _get_attrs(self):
        """Returns a dict of all attrs in the db corresponding to self.id
        """
        result = {}
        sql = "select name,type,value from attrs where parent = ?"
        cur = self.con.execute(sql,(self.id,))
        return ((key, db_to_value(value_type, value)) for key, value_type, value in cur)
    
    def _set_attr(self, key, value, commit=True):
        sql = "insert or replace into attrs(parent,name,type,value) values(?,?,?,?)"
        to_insert = (self.id, key, get_value_type(value), value_to_db(value))
        self.con.execute(sql, to_insert)
        if commit:
            self.con.commit()
    
    def _set_attrs(self, attrs, commit=True):
        """Sets attrs in the db to 'attrs' with a 'parent' value of self.id.
        
        All values already in the db for self.id are deleted before the insertion of the new 
        values.
        """
        for key, value in list(attrs.items()):
            self._set_attr(key, value, False)
        if commit:
            self.con.commit()
    
    def delete(self, commit=True):
        """Removes self from the db, recursively.
        """
        for node in self[:]:
            node.delete(False)
        sql = "delete from nodes where rowid = ?"
        self.con.execute(sql,(self.id,))
        sql = "delete from attrs where parent = ?"
        self.con.execute(sql,(self.id,))
        if commit:
            self.con.commit()
        if self.parent is not None:
            del self.parent._id_cache[self.id]
            self.parent = None
    

class File(fs.File, Node):
    """A SQL stored representation of a file.
    """
    def _read_info(self, field):
        super(File, self)._read_info(field)
        for key, value in self._get_attrs():
            setattr(self, key, value)

class Directory(fs.Directory,Node):
    """A SQL stored representation of a directory.
    """
    cls_file_class = File
    def __new_item(self, node_type, name, commit=True):
        #raises fs.AlreadyExistsError
        if node_type == NODE_TYPE_FILE:
            result = self._create_sub_file(name)
        else:
            result = self._create_sub_dir(name)
            result._id_cache = self._id_cache
        sql = "insert into nodes(parent,type,name) values(?,?,?)"
        cur = self.con.execute(sql, (self.id, node_type, name))
        result.id = cur.lastrowid
        result.con = self.con
        self._id_cache[result.id] = result
        if commit:
            self.con.commit()
        return result
    
    def _load_from_db(self):
        sql = "select rowid,name,type from nodes where parent = ?"
        cur = self.con.execute(sql, (self.id, ))
        for row, name, type in cur:
            if type == NODE_TYPE_FILE:
                new = self._create_sub_file(name)
            else:
                new = self._create_sub_dir(name)
                new._id_cache = self._id_cache
            new.id = row
            new.con = self.con
            self._id_cache[new.id] = new
        for dir in self.dirs:
            dir._load_from_db()
    
    def new_directory(self, name, commit=True):
        """Adds a new directory to self and return it.
        
        if commit is false, the transaction isn't commited to sqlite.
        """
        return self.__new_item(NODE_TYPE_DIR, name, commit)
    
    def new_file(self,name,commit=True):
        """Adds a new file to self and return it.
        
        if commit is false, the transaction isn't commited to sqlite.
        """
        return self.__new_item(NODE_TYPE_FILE, name, commit)
    
    def update(self, ref, commit=True, job=nulljob):
        """Updates self according to ref, recursively.
        
        Removes all files/dirs not in ref, and add all files/dirs not in self
        if commit is false, the transaction isn't commited to sqlite.
        """
        try:
            jobcount = ref.dircount + 1
            job = job.start_subjob(jobcount)
            job.start_job(ref.filecount)
            [d.delete() for d in self.dirs if ref.find_sub_dir(d.name) is None]
            mtime = getattr(self, 'mtime', 0) # Root doesn't have mtime
            # If a Directory mtime didn't change, it means no file changed.
            # (subdir could have changed though)
            if (mtime == 0) or (mtime > ref.mtime): 
                [f.delete() for f in self.files if ref.find_sub_file(f.name) is None]
                for reffile in ref.files:
                    job.add_progress()
                    try:
                        new = self[reffile.name]
                    except KeyError:
                        new = self.new_file(reffile.name, commit=False)
                    new_mtime = float(new.mtime) # in old databases, mtime is stored as string 
                    if (new_mtime == 0) or (reffile.mtime > new_mtime):
                        attrnames = self.root._attrs_to_read
                        if attrnames is None:
                            attrnames = list(reffile.INITIAL_INFO.keys())
                        attrs = {}
                        for attrname in attrnames:
                            try:
                                attrs[attrname] = getattr(reffile, attrname)
                            except AttributeError: # just ignore it
                                pass
                        new._set_attrs(attrs, False)
                        new._invalidate_info()
            for refdir in ref.dirs:
                try:
                    new = self[refdir.name]
                except KeyError:
                    new = self.new_directory(refdir.name, commit=False)
                new.update(refdir, commit=False, job=job)
                job.set_progress(100)
            if commit:
                self.con.commit()
        except JobCancelled:
            self.con.rollback()
            self.clear()
            self._load_from_db()
            raise
    

class Root(Directory):
    cls_dir_class = Directory
    def __init__(self, dbname=':memory:', dirname='', threaded=True):
        super(Root,self).__init__(None,dirname)
        if threaded:
            self.con = hscommon.sqlite.ThreadedConn(dbname, False)
        else:
            self.con = sqlite.connect(dbname)
        self.id = 0
        self._attrs_to_read = None
        self._id_cache = WeakValueDictionary()
        self._id_cache[0] = self
        try:
            cur = self.con.execute("select * from nodes where 1=2")
        except sqlite.OperationalError:
            self.__create_tables()
        self._load_from_db()
    
    def __create_tables(self):
        sqls = [
            'create table nodes(parent INT,type INT,name TEXT);',
            'create table attrs(parent INT,name TEXT,type INT,value TEXT);',
            'create index idx_node_parent on nodes(parent);',
            'create index idx_node_name on nodes(name);',
            'create index idx_attr_parent on attrs(parent);',
            'create index idx_attr_name on attrs(name);',
            'create unique index idx_node_unique on nodes(parent,name);',
            'create unique index idx_attr_unique on attrs(parent,name);'
        ]
        for sql in sqls:
            self.con.execute(sql)
    
    def find_node_of_id(self,id):
        return self._id_cache.get(id)
    
