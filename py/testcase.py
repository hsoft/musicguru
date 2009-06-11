#!/usr/bin/env python
# Unit Name: musicguru.testcase
# Created By: Virgil Dupras
# Created On: 2009-06-11
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

from hsutil.testcase import TestCase as TestCaseBase
from hsutil.path import Path

class TestCase(TestCaseBase):
    @classmethod
    def datadirpath(cls):
        return Path(__file__)[:-1] + 'testdata'
    
