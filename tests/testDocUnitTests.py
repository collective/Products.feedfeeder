# -*- coding: utf-8 -*-
##code-section module-header #fill in your manual code here
import unittest
from zope import component
from zope.component import testing
from zope.testing import doctestunit
##/code-section module-header



class testDocUnitTests:
    """
    """

    ##code-section class-header_testDocUnitTests #fill in your manual code here
    ##/code-section class-header_testDocUnitTests


    def testDummy(self):
        self.failIf(True)


    def afterSetUp(self):
        """
        """
        pass

##code-section module-footer #fill in your manual code here
def setUp(test):
    testing.setUp(test)

def tearDown(test):
    testing.tearDown(test)

def test_suite():
    return unittest.TestSuite((
        doctestunit.DocFileSuite('feedconsuming.txt',
                                 package='Products.feedfeeder.doc',
                                 setUp=setUp,
                                 tearDown=testing.tearDown),
        ))
##/code-section module-footer


