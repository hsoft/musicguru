# Created By: Virgil Dupras
# Created On: 2006/10/11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sqlite3 as sqlite
import os.path as op

from ..testcase import TestCase
from .strings import *

class TCEmptyBuffer(TestCase):
    def setUp(self):
        con = sqlite.connect(':memory:')
        self.buf = Buffer(con)
    
    def test_add_some_strings(self):
        self.assertEqual(1,self.buf.row_of_string('foo'))
        self.assertEqual(2,self.buf.row_of_string('bar'))
    
    def test_ask_for_str_of_row(self):
        self.buf.row_of_string('foo')
        self.buf.row_of_string('bar')
        self.assertEqual('foo',self.buf.string_of_row(1))
        self.assertEqual('bar',self.buf.string_of_row(2))
        self.assertRaises(IndexError,self.buf.string_of_row,3)
    
    def test_row_of_existing_str(self):
        self.assertEqual(1,self.buf.row_of_string('foo'))
        self.assertEqual(1,self.buf.row_of_string('foo'))
    

class TCReloadedBuffer(TestCase):
    def setUp(self):
        super(TCReloadedBuffer,self).setUp()
        p = self.tmpdir()
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
        self.buf = Buffer(con)
    
    def tearDown(self):
        self.buf.con.close()
        super(TCReloadedBuffer,self).tearDown()
    
    def test_ask_for_rows(self):
        self.assertEqual(2,self.buf.row_of_string('bar'))
    
