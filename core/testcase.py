# Created By: Virgil Dupras
# Created On: 2009-06-11
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from hsutil.testcase import TestCase as TestCaseBase
from hsutil.path import Path

class TestCase(TestCaseBase):
    def tearDown(self):
        if hasattr(self, '_created_directories'):
            self.global_teardown()
    
    @classmethod
    def datadirpath(cls):
        return Path(__file__)[:-1] + 'testdata'
    
    def tmpdir(self, *args, **kwargs):
        if not hasattr(self, '_created_directories'):
            self.global_setup()
        return TestCaseBase.tmpdir(self, *args, **kwargs)
    
    def mock(self, *args, **kwargs):
        if not hasattr(self, '_created_directories'):
            self.global_setup()
        return TestCaseBase.mock(self, *args, **kwargs)
