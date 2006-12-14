# -*- coding: utf-8 -*-
import os
import sys
import unittest
from Testing import ZopeTestCase
from Products.feedfeeder.tests.MainTestCase import MainTestCase

try:
    from Products.PloneTestCase.layer import PloneSite as test_layer
except:
    test_layer = None

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

def test_suite():
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    suite = ZopeDocFileSuite('feedfeeder-integration.txt',
                             package='Products.feedfeeder.doc',
                             test_class=MainTestCase)
    if test_layer is not None:
        suite.layer = test_layer

    return unittest.TestSuite((suite,))

if __name__ == '__main__':
    framework()


