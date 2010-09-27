# Created By: Virgil Dupras
# Created On: 2006/02/21
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hsutil.testutil import eq_

from hscommon import job

from ..stats import *

class BaseObject(object):
    intval = 1
    strval = 'foo'
    lstval = [1,2,3]
    tplval = property(lambda x:tuple(x.lstval))

def GenStats():
    st = StatsList()
    st.append(BaseObject())
    st.append(BaseObject())
    st.append(BaseObject())
    o = BaseObject()
    o.intval = 3
    o.strval = 'bar'
    o.lstval = [4,5,6]
    st.append(o)
    return st

def test_simple():
    st = GenStats()
    eq_(6, st.get_stat('intval'))
    eq_(['foo','bar'], st.get_stat('strval'))

def test_invalid():
    st = GenStats()
    eq_(0, st.get_stat('invalid'))

def test_partly_invalid():
    #If only a part of the items don't have the attr, make the stats with
    #only the valid items.
    st = GenStats()
    o = object()
    st.append(o)
    eq_(6, st.get_stat('intval'))

def test_one_item():
    st = StatsList()
    st.append(BaseObject())
    eq_(1, st.get_stat('intval'))
    eq_(['foo'], st.get_stat('strval'))

def test_remember():
    #Stats must remeber it's results to avoid useless re-calculation.
    #If _reset_stats is called, the buffer is flushed
    st = GenStats()
    eq_(6, st.get_stat('intval'))
    st.append(BaseObject())
    eq_(6, st.get_stat('intval'))
    st._reset_stats()
    eq_(7, st.get_stat('intval'))

def test_recursive():
    st = GenStats()
    st2 = StatsList()
    st2.append(BaseObject())
    st2.append(BaseObject())
    st2.append(BaseObject())
    o = BaseObject()
    o.intval = 3
    o.strval = 'bleh'
    st2.append(o)
    st.append(st2)
    eq_(12, st.get_stat('intval'))
    eq_(['foo','bar','bleh'], st.get_stat('strval'))
    eq_(0, st.get_stat('invalid'))

def test_is_stats_but_also_has_the_attr():
    #if a stat x is asked, and there is a Stats instance in the children,
    #and the children also has attr x, count the stat in
    st = GenStats()
    st2 = StatsList()
    st3 = StatsList()
    st.foobar = 3
    st2.foobar = 2
    st3.foobar = 1
    st.append(st2)
    st2.append(st3)
    eq_(6, st.get_stat('foobar'))

def test_long_int():
    st = StatsList()
    o = BaseObject()
    o.intval = 0xfffffffff
    st.append(o)
    o = BaseObject()
    o.intval = 0xfffffffff
    st.append(o)
    eq_(0xfffffffff*2,st.get_stat('intval'))

def test_cached_str_stat_in_substat():
    st = GenStats()
    st2 = GenStats()
    eq_(['foo','bar'], st2.get_stat('strval'))
    st.append(st2)
    eq_(['foo','bar'], st.get_stat('strval'))

def test_null_value():
    st = GenStats()
    eq_(0, st.get_stat('invalid'))
    eq_([], st.get_stat('invalid',[]))
    eq_('foobar', st.get_stat('invalid','foobar'))

def test_list_values():
    st = GenStats()
    eq_([1,2,3,1,2,3,1,2,3,4,5,6], st.get_stat('lstval'))

def test_tuple_values():
    st = GenStats()
    eq_((1,2,3,1,2,3,1,2,3,4,5,6), st.get_stat('tplval'))

def test_dont_let_parent_reuse_child_dict():
    root = StatsList()
    st1 = StatsList()
    st2 = StatsList()
    o1 = BaseObject()
    o2 = BaseObject()
    o2.strval = 'bar'
    st1.append(o1)
    st2.append(o2)
    root.append(st1)
    root.append(st2)
    eq_(['foo','bar'], root.get_stat('strval'))
    eq_(['foo'], st1.get_stat('strval'))
    eq_(['bar'], st2.get_stat('strval'))

def test_recursively_remember():
    #if a parent stat object has been resetted, but not its child,
    #don't make the child recalculate their stats.
    st = GenStats()
    st2 = GenStats()
    st.append(st2)
    eq_(12, st.get_stat('intval'))
    st2.append(BaseObject())
    st._reset_stats()
    eq_(12, st.get_stat('intval'))

def test_int_stats_with_none():
    st = GenStats()
    o = BaseObject()
    o.intval = 'foo'
    st.append(o)
    eq_(6, st.get_stat('intval'))

def test_zero_values():
    st = StatsList()
    o = BaseObject()
    o.strval = ''
    o.intval = 0
    st.append(o)
    eq_([], st.get_stat('strval',[]))

def test_reset_stats_return_value():
    #Returns True if there were stats to reset, and False if the stats were already empty.
    st = GenStats()
    st.get_stat('intval')
    assert st._reset_stats()
    assert not st._reset_stats()

def test_reset_stats_on_an_uninitialized_Stats_object():
    st = Stats()
    assert not st._reset_stats()

def test_cache_value_even_if_empty():
    st = GenStats()
    st.get_stat('foobar')
    assert st._reset_stats()
