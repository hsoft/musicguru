#!/usr/bin/env python
# Unit Name: hs.cocoa
# Created By: Virgil Dupras
# Created On: 2007-10-12
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

import unittest

from hs.path import Path
from hs.testcase import TestCase

from musicguru.app import MusicGuru
from musicguru.sqlfs.music import Root, VOLTYPE_CDROM

class TCApp_GetLocationData(TestCase):
    def test_values(self):
        root = Root()
        root.buffer_path = Path('/does/not/exist')
        loc = root.new_directory('foo')
        loc.vol_type = VOLTYPE_CDROM
        # Let's fake its stats
        loc._Stats__stats = {'size': int(3.5 * 1024 * 1024 * 1024), 'filecount': 42}
        app = MusicGuru()
        expected = ['foo', 42, '3.50', True, False, unicode(Path('/does/not/exist/foo'))]
        result = app.GetLocationData(loc)
        self.assertEqual(expected, result)
        # The path supplied must be a unicode string, it is going through the pyobjc bridge
        self.assert_(isinstance(result[5], unicode))
    

if __name__ == '__main__':
    unittest.main()