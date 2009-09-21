# -*- coding: utf-8 -*-
#
# Base TestCase for feedfeeder
#

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

ZopeTestCase.installProduct('feedfeeder')

testcase = PloneTestCase.PloneTestCase

PloneTestCase.setupPloneSite(products=['feedfeeder'])


class MainTestCase(testcase):
    """Base TestCase for feedfeeder."""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MainTestCase))
    return suite
