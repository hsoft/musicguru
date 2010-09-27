# Created By: Virgil Dupras
# Created On: 2005/03/23
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import weakref
import gc

from hsutil.testutil import eq_

from hsutil.decorators import log_calls

from ..tree import *

def test_tree_creation():
    # Just create an instance and verify it's attributes.
    t = Tree()
    eq_(t.parent,None)
    eq_(list(t.parents), [])
    eq_(len(t),0)
    eq_(t.root,t)
    assert t not in t
    assert None not in t

def test_tree_add():
    # Create a tree, add a couple of child, test if everything is right.
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t)
    t3 = Tree(t)
    t11 = Tree(t1)
    t12 = Tree(t1)
    t31 = Tree(t3)
    t311 = Tree(t31)
    eq_(len(t),3)
    eq_(len(t1),2)
    eq_(len(t11),0)
    eq_(len(t12),0)
    eq_(len(t2),0)
    eq_(len(t3),1)
    eq_(len(t31),1)
    eq_(len(t311),0)
    eq_(list(t311.parents), [t,t3,t31])
    eq_(t311.root,t)
    eq_(t1.parent,t)
    assert t311 not in t
    assert t311 not in t3
    assert t311 in t31
    assert not t311 in t311
    assert t2 in t
    eq_(t[0],t1)
    eq_(t[1],t2)
    eq_(t[2],t3)
    eq_(t[-1],t3)
    eq_(t1[0],t11)
    try:
        bleh = t1[2]
        raise AssertionError()
    except IndexError:pass
    try:
        t[0] = t2
        raise AssertionError()
    except InvalidActionError:pass

def test_set_parent():
    # Create a tree, add a couple of child, play with 'parent'.
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t)
    t3 = Tree(t)
    t11 = Tree(t1)
    t12 = Tree(t1)
    t31 = Tree(t3)
    t311 = Tree(t31)
    ref = Tree()
    eq_(t1.parent,t)
    eq_(list(t11.parents), [t,t1])
    eq_(list(t311.parents), [t,t3,t31])
    t1.parent = ref
    eq_(t1.parent,ref)
    eq_(list(t11.parents), [ref,t1])
    eq_(list(t311.parents), [t,t3,t31])
    eq_(len(t),2)
    t3.parent = None
    eq_(list(t311.parents), [t3,t31])
    eq_(len(t),1)
    t3.parent = t1
    eq_(list(t311.parents), [ref,t1,t3,t31])
    eq_(len(t1),3)
    t.parent = ref
    eq_(len(ref),2)
    eq_(list(t2.parents), [ref,t])
    eq_(t1.parent,ref)
    eq_(t.parent,ref)
    eq_(ref.parent,None)
    eq_(t311.root,ref)
    assert t2 not in ref
    assert t in ref
    assert t311 not in ref

def test_parent_recursion():
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t1)
    try:
        t.parent = t
        raise AssertionError()
    except ParentRecursionError:
        pass
    try:
        t.parent = t2
        raise AssertionError()
    except ParentRecursionError:
        pass

def test_tree_del():
    # Create a tree, add a couple of child, delete them.
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t)
    t3 = Tree(t)
    t11 = Tree(t1)
    t12 = Tree(t1)
    t31 = Tree(t3)
    t311 = Tree(t31)
    del t[0]
    assert t2 in t
    assert t12 in t1
    assert t1 not in t
    assert t12 not in t
    eq_(len(t),2)
    eq_(t[0],t2)
    eq_(t1.parent,None)
    eq_(list(t12.parents), [t1])

def test_that_tree_is_freed():
    t = Tree()
    w = weakref.ref(t)
    assert w() is t
    del t
    assert w() is None

def test_that_tree_and_child_are_freed():
    t = Tree()
    c = Tree(t)
    wt = weakref.ref(t)
    wc = weakref.ref(c)
    assert wt() is t
    assert wc() is c
    del t
    del c
    gc.collect()
    assert wt() is None
    assert wc() is None

def test_clear():
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t)
    t.clear()
    eq_(len(t),0)
    assert t1.parent is None
    assert t2.parent is None

def test_that_remove_events_are_called_on_clear():
    @log_calls
    def fake_after(child):
        pass
    @log_calls
    def fake_before(child):
        pass
    t = Tree()
    Tree(t)
    Tree(t)
    t._do_after_remove = fake_after
    t._do_before_remove = fake_before
    t.clear()
    eq_(len(fake_after.calls), 2)
    eq_(len(fake_before.calls), 2)

def test_iterall():
    t = Tree()
    i = t.iterall()
    assert iter(i) is i
    eq_([],list(i))
    t1 = Tree(t)
    t2 = Tree(t)
    i = t.iterall()
    eq_([t1,t2],list(i))
    t11 = Tree(t1)
    i = t.iterall()
    eq_([t1,t11,t2],list(i))

def test_iterall_with_filter():
    t = Tree()
    t1 = Tree(t)
    t2 = Tree(t)
    t11 = Tree(t1)
    t111 = Tree(t11)
    t21 = Tree(t2)
    i = t.iterall(lambda x: x is not t11)
    #when a filter exclude an object, all its children must be filtered out, even if they don't
    #match the filter
    eq_([t1,t2,t21], list(i))

def test_dont_trigger__iter__or__getitem__on_setparent():
    # The call of __iter__ during __InvalidateParentListCache() creates all kinds of problems
    # for the subclasses
    class MyTree(Tree):
        dontcall = False
        def __iter__(self):
            if self.dontcall:
                raise Exception()
            return super(MyTree, self).__iter__()
        
    
    t = MyTree()
    t1 = MyTree(t)
    list(t1.parents)
    t1.dontcall = True
    try:
        t1.parent = None
    except Exception:
        raise AssertionError()

def test_hashtree_creation():
    # Just create an instance and verify it's attributes.
    t = HashedTree(None,'bleh')
    eq_(t.parent,None)
    eq_(list(t.parents), [])
    eq_(len(t),0)
    eq_(t.root,t)
    assert t not in t
    assert None not in t
    eq_(t.value,'bleh')

def test_hashedtree_add():
    # Create a tree, add a couple of child, test if everything is right.
    t = HashedTree(None,'t')
    t1 = HashedTree(t,'t1')
    t2 = HashedTree(t,'t2')
    t3 = HashedTree(t,'t3')
    t11 = HashedTree(t1,'t11')
    t12 = HashedTree(t1,'t12')
    t31 = HashedTree(t3,'t31')
    t311 = HashedTree(t31,'t311')
    eq_(t['t1'],t1)
    try:
        t['t31']
        raise AssertionError()
    except KeyError:
        pass
    eq_(t['t3']['t31']['t311'],t311)
    assert 't1' in t
    assert 't12' in t1
    assert 't12' not in t
    assert 'bleh' not in t

def test_hashedtree_del():
    # Create a tree, add a couple of child, delete them.
    t = HashedTree(None,'t')
    t1 = HashedTree(t,'t1')
    t2 = HashedTree(t,'t2')
    t3 = HashedTree(t,'t3')
    t11 = HashedTree(t1,'t11')
    t12 = HashedTree(t1,'t12')
    t31 = HashedTree(t3,'t31')
    t311 = HashedTree(t31,'t311')
    del t['t1']
    assert t2 in t
    assert 't2' in t
    assert t12 in t1
    assert 't12' in t1
    assert t1 not in t
    assert 't1' not in t
    assert t12 not in t
    assert 't12' not in t
    eq_(len(t),2)
    eq_(t[0],t2)
    eq_(t['t2'],t2)
    try:
        eq_(t['t1'],t2)
        raise AssertionError()
    except KeyError:pass
    eq_(t1.parent,None)
    eq_(list(t12.parents), [t1])

def test_change_hash():
    # Create a tree, add a couple of child, change hashes.
    t = HashedTree(None,'t')
    t1 = HashedTree(t,'t1')
    t2 = HashedTree(t,'t2')
    t3 = HashedTree(t,'t3')
    t11 = HashedTree(t1,'t11')
    t12 = HashedTree(t1,'t12')
    t31 = HashedTree(t3,'t31')
    t311 = HashedTree(t31,'t311')
    eq_(t['t1'],t1)
    try:
        t['foobar']
        raise AssertionError()
    except KeyError:pass
    t1.value = 'foobar'
    eq_(t['foobar'],t1)
    try:
        t['t1']
        raise AssertionError()
    except KeyError:pass
    try:
        t1.value = 't2'
        raise AssertionError()
    except HashCollisionError:
        pass

def test_uppercase():
    # Create a subclass of HashedTree that overrides _do_hash to see if everything works well.
    class Special(HashedTree):
        def _do_hash(self,value):
            return value.upper()
    
    t = Special(None,'t')
    t1 = Special(t,'t1')
    t2 = Special(t,'t2')
    t3 = Special(t,'t3')
    t11 = Special(t1,'t11')
    t12 = Special(t1,'t12')
    t31 = Special(t3,'t31')
    t311 = Special(t31,'t311')
    assert t3 in t
    assert t311 not in t
    assert 't1' in t
    assert 'T1' in t
    assert 'BLEH' not in t
    assert t['t1']['t12'] is t12
    assert t['T1']['T12'] is t12
    t._do_hash = lambda value: value
    t._rebuild_hashes()
    assert 't3' in t
    assert 't1' in t
    assert 'T1' not in t

def test_hash_change():
    class Special(HashedTree):
        def _do_hash(self,value):
            return value.upper()
    t1 = HashedTree(None,'')
    t2 = Special(None,'')
    child = HashedTree(t1,'foobar')
    assert t1['foobar'] is child
    child.parent = t2
    assert t2['FOOBAR'] is child

def test_rebuild_hashes_with_uppercase():
    #The problem happens on _do_after_remove that happens because child.parent
    #is set to None when ignorecollision is True.
    def do_hash(value):
        return value.upper()
    
    t = HashedTree(None,'')
    t1 = HashedTree(t,'foobar')
    t2 = HashedTree(t,'FOOBAR')
    t3 = HashedTree(t,'FooBar')
    t._do_hash = do_hash
    t._rebuild_hashes()
    eq_(1,len(t))
    assert t['foobar'] is not None
