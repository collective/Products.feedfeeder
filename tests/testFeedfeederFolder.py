# -*- coding: utf-8 -*-
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) FeedfeederFolder
#

from Testing import ZopeTestCase
from Products.feedfeeder.config import *
from Products.feedfeeder.tests.MainTestCase import MainTestCase

# Import the tested classes
from Products.feedfeeder.content.folder import FeedfeederFolder

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testFeedfeederFolder(MainTestCase):
    """Test-cases for class(es) FeedfeederFolder."""

    ##code-section class-header_testFeedfeederFolder #fill in your manual code here
    ##/code-section class-header_testFeedfeederFolder

    def afterSetUp(self):
        pass

    # from class FeedfeederFolder:
    def test_update_feed_items(self):
        pass

    # from class FeedfeederFolder:
    def test_view(self):
        pass

    # Manually created methods

    def test_addRetrievedFeedItem(self):
        pass

    def test_downloadEntries(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testFeedfeederFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


