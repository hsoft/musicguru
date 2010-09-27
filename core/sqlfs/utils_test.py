# Created By: Virgil Dupras
# Created On: 2006/10/07
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from ..testcase import TestCase
from ._sql import *
from .utils import *

def getref():
    root = Root(threaded=False)
    f1 = root.new_file('f1')
    f2 = root.new_file('f2')
    f3 = root.new_file('f3')
    f4 = root.new_file('f4')
    f1._set_attr('foo','bar')
    f2._set_attr('foo','bar')
    f3._set_attr('foo','baz')
    f4._set_attr('foo','bleh')
    f1._set_attr('int',1)
    f2._set_attr('int',2)
    f3._set_attr('int',3)
    f4._set_attr('int',4)
    return root

class TCattr_values_of_nodes(TestCase):
    def test_with_node_ids(self):
        root = getref()
        self.assertEqual(['bar','baz','bleh'],attr_values_of_nodes(root.con,'foo',[file.id for file in root.files]).fetchall())
    
    def test_get_only_asked_attr_name(self):
        root = getref()
        root['f1']._set_attr('bar','unwanted')
        self.assertEqual(['bar','baz','bleh'],attr_values_of_nodes(root.con,'foo',[file.id for file in root.files]).fetchall())
    
    def test_dont_include_empty_values(self):
        root = getref()
        root['f1']._set_attr('foo','')
        self.assertEqual(['bar','baz','bleh'],attr_values_of_nodes(root.con,'foo',[file.id for file in root.files]).fetchall())
    
    def test_all_values_if_ids_is_None(self):
        root = getref()
        self.assertEqual(['bar','baz','bleh'],attr_values_of_nodes(root.con,'foo').fetchall())
    
    def test_no_value_if_ids_are_empty(self):
        root = getref()
        self.assertEqual([],attr_values_of_nodes(root.con,'foo',[]).fetchall())
    
    def test_sorted(self):
        root = getref()
        root['f3']._set_attr('foo','aaa')
        root['f4']._set_attr('foo','AAB')
        self.assertEqual(['aaa','AAB','bar'],attr_values_of_nodes(root.con,'foo').fetchall())
    

class TCattr_sum_of_nodes(TestCase):
    def test_ids_is_None(self):
        root = getref()
        self.assertEqual(10,attr_sum_of_nodes(root.con,'int'))
    
    def test_with_node_ids(self):
        root = getref()
        self.assertEqual(4,attr_sum_of_nodes(root.con,'int',[root['f1'].id,root['f3'].id]))
    
    def test_with_no_result_row(self):
        root = getref()
        self.assertEqual(0,attr_sum_of_nodes(root.con,'int',[42]))
    

class TCnodes_of_attr_values(TestCase):
    def test_typical(self):
        root = getref()
        values = ['bar','bleh']
        result = nodes_of_attr_values(root.con,'foo',values)
        self.assertEqual(3,len(result))
        result = result.fetchall()
        self.assert_(root['f1'].id)
        self.assert_(root['f2'].id)
        self.assert_(root['f4'].id)
    
    def test_sql_escape(self):
        root = getref()
        nodes_of_attr_values(root.con,'foo',['foo\'bar'])
    
    def test_return_nothing_if_there_is_no_values(self):
        root = Root(threaded=False)
        f1 = root.new_file('f1')
        f1._set_attr('foo','')
        self.assertEqual([],nodes_of_attr_values(root.con,'foo',[]))
    
