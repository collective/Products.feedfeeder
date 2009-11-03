"""Tests which use collective.testcaselayer"""

import unittest
from zope.testing import doctest

from Testing import ZopeTestCase
from Products.PloneTestCase import ptc

from collective.testcaselayer import ptc as tcl_ptc

from Products.feedfeeder.tests import MainTestCase
MainTestCase # pyflakes

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    layer_suite = ZopeTestCase.FunctionalDocFileSuite(
        'portal_types.txt',
        package='Products.feedfeeder.doc',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    layer_suite.layer = tcl_ptc.ptc_layer
    return unittest.TestSuite([layer_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

