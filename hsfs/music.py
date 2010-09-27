# Created By: Virgil Dupras
# Created On: 2004/12/13
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from . import _fs as fs

class _File(fs.File):
    INITIAL_INFO = fs.File.INITIAL_INFO.copy()
    INITIAL_INFO.update({
        'audiosize': 0,
        'bitrate'  : 0,
        'duration' : 0,
        'samplerate':0,
        'artist'  : '',
        'album'   : '',
        'title'   : '',
        'genre'   : '',
        'comment' : '',
        'year'    : '',
        'track'   : 0,
    })
