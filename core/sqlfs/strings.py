# Created By: Virgil Dupras
# Created On: 2006/10/11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sqlite3 as sqlite

class Buffer(object):
    """Store strings in a SQLite db without duplicating them.
    
    The commits are *NOT* assumed by this class. You have to do them externally. This is to have
    optimal performances
    """
    def __init__(self,con):
        def fill():
            cur = con.execute("select rowid,value from strings")
            for rowid,value in cur:
                self.__str_to_row[value] = rowid
                self.__row_to_str[rowid] = value
        
        self.con = con
        self.__str_to_row = {}
        self.__row_to_str = {}
        try:
            fill()
        except sqlite.OperationalError:
            self.con.execute("create table strings(value TEXT)")
            fill()
    
    def row_of_string(self,s):
        try:
            return self.__str_to_row[s]
        except KeyError:
            self.con.execute("insert into strings(value) values(?)",(s,))
            rowid = len(self.__str_to_row) + 1
            self.__str_to_row[s] = rowid
            self.__row_to_str[rowid] = s
            return rowid
    
    def string_of_row(self,row):
        try:
            return self.__row_to_str[row]
        except KeyError:
            raise IndexError
    
