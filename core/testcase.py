# Created By: Virgil Dupras
# Created On: 2009-06-11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import py.path
from hscommon.testcase import TestCase as TestCaseBase
from hscommon.path import Path

class TestCase(TestCaseBase):
    def tearDown(self):
        if hasattr(self, '_created_directories'):
            self.global_teardown()
    
    def tmpdir(self, *args, **kwargs):
        if not hasattr(self, '_created_directories'):
            self.global_setup()
        return TestCaseBase.tmpdir(self, *args, **kwargs)
    
    def mock(self, *args, **kwargs):
        if not hasattr(self, '_created_directories'):
            self.global_setup()
        return TestCaseBase.mock(self, *args, **kwargs)
    
    @property
    def datadirpath(self):
        return py.path.local(str(Path(__file__)[:-1] + 'testdata'))
