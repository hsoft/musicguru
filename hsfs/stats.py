# Created By: Virgil Dupras
# Created On: 2006/02/21
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hsutil.misc import nonone

def do_add(x, y):
    if isinstance(x, (int, list, tuple)):
        try:
            return x + y
        except TypeError:
            return x
    if isinstance(x, dict):
        result = x
    else:
        result = {x: 1}
    if not isinstance(y, dict):
        y = {y: 1}
    for key, value in y.items():
        try:
            result[key] += value
        except KeyError:
            result[key] = value
    return result

def do_get_substats(item, attr):
    result = item._get_stat(attr)
    if isinstance(result, dict):
        result = result.copy()
    return result

class Stats(object):
    """Stats is intended to be a mixin class, and it should be mixed with a
    container class. To use it, call get_stat(arg). This will go through self,
    and look for <arg> attributes among items, and will return stats about it.
    If Stats contains other Stats instances, the stats will be recursive.
    if arg returns an int value, the result will be an int value. if arg returns
    a string, the result will be a list, ordered by occurance (the more occurance
    of str, the lower the index)
    """
    #---Protected
    def _get_stat(self, stat):
        """ Returns either None, int or dict.
        """
        try:
            if stat in self.__stats:
                return self.__stats[stat]
        except AttributeError:
            self.__stats = {}
        values = [getattr(child, stat, None) for child in self if not isinstance(child, Stats)]
        values += [do_get_substats(child, stat) for child in self if isinstance(child, Stats)]       
        if hasattr(self, stat):
            values.insert(0, getattr(self, stat))
        values = [_f for _f in values if _f]
        if values:
            result = values[0]
            for value in values[1:]:
                result = do_add(result, value)
            if isinstance(result, str):
                result = {result: 1}
        else:
            result = None
        self.__stats[stat] = result
        return result
    
    def _reset_stats(self):
        try:
            if not self.__stats:
                return False
            self.__stats = {}
            return True
        except AttributeError:
            return False
    
    #---Public
    def get_stat(self, stat, null_value=0):
        """ Returns the aggregated value of the 'stat' attribute of all self's children.
            
            Returns either int or [str] (sorted by occurence). 
            If the result is None, null_value is returned.
        """
        result = self._get_stat(stat)
        if isinstance(result, dict):
            result = sorted(list(result.keys()), key=result.__getitem__, reverse=True)
        return nonone(result, null_value)
    

class StatsList(Stats, list):
    pass
