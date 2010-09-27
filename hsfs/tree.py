# Created By: Virgil Dupras
# Created On: 2005/03/23
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license



class ParentRecursionError(Exception):
    """The parent is being set so there would be an infinite loop in GetParentList"""

class InvalidActionError(Exception):
    """This action is not allowed in a Tree"""

class HashCollisionError(Exception):
    """The child's hash is already present in the parent"""

class Tree(object):
    """A super basic tree. The goal of this class is to never break its integrity. A Tree instance 
    will always be in self.parent.__children. 'self in self.parent' will always return true unless 
    parent is None. A Tree instance will not be in another's tree instance beside it's parent.
    Setting a tree parent will properly perform the necessary move to keep integrity intact. All 
    container magic functions are implemented.
    """
    #---Base Overrides
    def __init__(self, parent=None):
        self.__parent = None
        self.__children = []
        self.parent = parent # This will automatically add self to parent
    
    def __contains__(self, item):
        try:
            return self is item.parent
        except AttributeError:
            return False
    
    def __delitem__(self, key):
        if isinstance(key, slice):
            for child in self[key]:
                child.parent = None
        else:
            self[key].parent = None
    
    def __getitem__(self, key):
        return self.__children[key]
    
    def __iter__(self):
        return iter(self.__children)
    
    def __len__(self):
        return len(self.__children)
    
    def __setitem__(self, key, value):
        raise InvalidActionError()
    
    #---Virtual
    def _do_after_add(self, child):
        pass
    
    def _do_after_remove(self, child):
        pass
    
    def _do_before_add(self, child):
        pass
    
    def _do_before_remove(self, child):
        pass
    
    #---Public
    def clear(self):
        for child in self[:]: #We must copy self's content because a modification could occur.
            child.parent = None
    
    def iterall(self, filter_func=None):
        to_yield = filter(filter_func, self) if filter_func is not None else self
        for child in to_yield:
            yield child
            for subchild in child.iterall(filter_func):
                yield subchild
    
    #---Properties
    @property
    def parent(self):
        return self.__parent
    
    @parent.setter
    def parent(self, newparent):
        # Why does this function look so messy:
        # Because what we want to achieve here is to dispatch the BeforeAdd/Remove
        # events before self.parent is being changed, but we also want to
        # dispatch AfterAdd/Remove after self.parent has been changed.
        # Additionally, we want to be able to cancel BOTH remove and add, in
        # EITHER BeforeAdd or BeforeRemove.
        oldparent = self.parent
        if newparent is oldparent:
            return
        if (newparent is not None) and ((newparent is self) or (self in newparent.parents)):
            raise ParentRecursionError()
        if newparent is not None:
            newparent._do_before_add(self)
        if oldparent is not None:
            oldparent._do_before_remove(self)
        if newparent is not None:
            newparent.__children.append(self)
        if oldparent is not None:
            oldparent.__children.remove(self) 
        self.__parent = newparent
        if oldparent is not None:
            oldparent._do_after_remove(self)
        if newparent is not None:
            newparent._do_after_add(self)
    
    @property
    def parents(self):
        parent = self.parent
        if parent is not None:
            for grandparent in parent.parents:
                yield grandparent
            yield parent
    
    @property
    def root(self):
        return self.parent.root if self.parent is not None else self
    

class HashedTree(Tree):
    """A Tree that indexes it's children by their hash value. Avoid by all
    means to use integer or tuple hashes because it might mess with __delitems__
    and __getitem__.
    """
    #---Base Overrides
    def __init__(self, parent, value):
        """'parent' is the parent tree, 'value' is the value to use to calculate
        the hash.
        """
        self.__dict = {}
        self.__value = value
        self.__hash = parent._do_hash(value) if parent is not None else self._do_hash(value)
        super(HashedTree, self).__init__(parent)
    
    def __contains__(self, item):
        """IMPORTANT: if item is a Tree, it calls Tree.__contains__.
        Otherwise, it looks for a hash of item.
        """
        if isinstance(item, Tree):
            return Tree.__contains__(self, item)
        else:
            return self._do_hash(item) in self.__dict
    
    def __getitem__(self, key):
        """key can be a tuple. If it is, __getitem__ will go down the children.
        """
        if isinstance(key, slice):
            return Tree.__getitem__(self, key)
        elif isinstance(key, int):
            return self.__dict.get(self._do_hash(key), Tree.__getitem__(self, key))
        else:
            return self.__dict[self._do_hash(key)]
    
    #---Private
    def __update_hash(self):
        if self.parent is not None:
            self.__hash = self.parent._do_hash(self.__value)
        else:
            self.__hash = self._do_hash(self.__value)
    
    #---Protected
    def _do_hash(self, value):
        return value
    
    def _rebuild_hashes(self):
        """Call this if you changed your _do_hash function.
        """
        self.__dict = None
        newdict = {}
        for child in self[:]: #We must copy self's content because a modification could occur.
            child.__update_hash()
            if child.__hash in newdict:
                child.parent = None
            else:
                newdict[child.__hash] = child
        self.__dict = newdict
    
    #---Override
    def _do_after_add(self, child):
        child.__update_hash()
        self.__dict[child.__hash] = child
    
    def _do_after_remove(self, child):
        if self.__dict:
            del self.__dict[child.__hash]
    
    def _do_before_add(self, child):
        if child.__value in self:
            raise HashCollisionError()
    
    #---Virtual
    def _do_after_value_change(self, newvalue):
        pass
    
    def _do_before_value_change(self, newvalue):
        pass
    
    #---Properties
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value == self.__value:
            return
        if (self.parent is not None) and (value in self.parent):
            raise HashCollisionError()
        self._do_before_value_change(value)
        old = self.__hash
        self.__value = value
        self.__update_hash()
        if self.parent is not None:
            del self.parent.__dict[old]
            self.parent.__dict[self.__hash] = self
        self._do_after_value_change(value)
    
