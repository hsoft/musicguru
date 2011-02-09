# Created By: Virgil Dupras
# Created On: 2011-02-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

# Stuff that used to be in hsutil and that is not generic enough to end up in hscommon

import re

from hscommon import io
from hscommon.util import delete_if_empty

def clean_empty_dirs(path, deleteself=False, files_to_delete=[]):
    """Recursively delete empty dirs in directory. 'directory' is deleted only
    if empty and 'deleteself' is True.
    Returns the list of delete paths.
    files_to_delete: The name is clear enough. However, files in
        this list will ONLY be deleted if it makes the directory deletable
        thereafter (In other words, if the directory contains files not in the
        list, NO file will be deleted)
    """
    result = []
    subdirs = [name for name in io.listdir(path) if io.isdir(path + name)]
    for subdir in subdirs:
        result.extend(clean_empty_dirs(path + subdir, True, files_to_delete))
    if deleteself and delete_if_empty(path, files_to_delete):
        result.append(str(path))
    return result

re_process_tokens = re.compile('\%[\w:\s]*\%',re.IGNORECASE)

def process_tokens(s, handlers, data=None):
    """Process a token filled (%token%) string using handlers.
    
    s is a string containing tokens. Tokens are words between two
    percent (%) signs. They can optionally contain parameters, which are
    defined with :, like %token:param:other_param%.
    
    handlers is a dictionnary of strings mapped to callable. the string
    represent a supported token name, and the callable must return a string
    that will replace the token. If the callabale returns None, or doesn't
    have the number of parameters matching with the number of params
    present in the token, the token will be substitued by '(none)'
    
    if handlers is a callable instead of a dictionnary, it means that
    the user wants only a single handler. in this case, the token name will be
    passed as the first parameter. if there is a data, data will be the second
    param, and then will follow the sub params.
    
    if data is not None, every handler will receive it as their first
    parameter. Don't forget to think about it when writing your handlers!
    """
    def replace(match):
        result = None
        expression = match.string[match.start()+1:match.end()-1].lower()
        token = expression.split(':')[0]
        params = expression.split(':')[1:]
        if data is not None:
            params.insert(0,data)
        if hasattr(handlers, '__call__'):
            params.insert(0,token)
            handler = handlers
        else:
            handler = handlers.get(token,None)
        if hasattr(handler, '__call__'):
            try:
                result = handler(*params)
            except TypeError:
                pass
        if result is None:
            result = ''
        result = result.replace('\n', ' ').replace('\0', ' ').strip()
        if result == '':
            result = '(none)'
        return result
    
    return re_process_tokens.sub(replace, s)
