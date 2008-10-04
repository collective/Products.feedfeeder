# -*- coding: utf-8 -*-
import unittest
from Products.feedfeeder.tests.MainTestCase import MainTestCase
from Products.PloneTestCase.layer import PloneSite


def test_suite():
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    suite = ZopeDocFileSuite('feedfeeder-integration.txt',
                             package='Products.feedfeeder.doc',
                             test_class=MainTestCase)
    suite.layer = PloneSite

    return unittest.TestSuite((suite, ))
