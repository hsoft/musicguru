# Created By: Virgil Dupras
# Created On: 2006/10/11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sqlite3 as sqlite
import os.path as op

from pytest import raises
from hscommon.testutil import eq_
from .strings import *

class TestEmptyBuffer:
    def setup_method(self, method):
        con = sqlite.connect(':memory:')
        self.buf = Buffer(con)
    
    def test_add_some_strings(self):
        eq_(1,self.buf.row_of_string('foo'))
        eq_(2,self.buf.row_of_string('bar'))
    
    def test_ask_for_str_of_row(self):
        self.buf.row_of_string('foo')
        self.buf.row_of_string('bar')
        eq_('foo',self.buf.string_of_row(1))
        eq_('bar',self.buf.string_of_row(2))
        with raises(IndexError):
            self.buf.string_of_row(3)
    
    def test_row_of_existing_str(self):
        eq_(1,self.buf.row_of_string('foo'))
        eq_(1,self.buf.row_of_string('foo'))
    

    
def test_ask_for_rows(tmpdir):
    p = str(tmpdir)
    dbpath = op.join(p,'strings.db')
    con = sqlite.connect(dbpath)
    buf = Buffer(con)
    buf.row_of_string('foo')
    buf.row_of_string('bar')
    buf.row_of_string('baz')
    buf.row_of_string('bleh')
    del buf
    con.commit()
    con.close()
    del con
    con = sqlite.connect(dbpath)
    cur = con.execute("select * from strings")
    buf = Buffer(con)
    try:
        eq_(buf.row_of_string('bar'), 2)
    finally:
        buf.con.close()
