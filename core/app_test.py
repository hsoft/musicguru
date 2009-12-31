# Created By: Virgil Dupras
# Created On: 2007-10-12
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from hsutil.path import Path
from hsutil.testcase import TestCase

from .app_cocoa import MusicGuru
from .sqlfs.music import Root, VOLTYPE_CDROM

class TCApp_GetLocationData(TestCase):
    def test_values(self):
        root = Root(threaded=False)
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
    