# -*- coding: utf-8 -*-
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) 
#

from Testing import ZopeTestCase
from Products.feedfeeder.tests.MainTestCase import MainTestCase

# Import the tested classes


class testDocIntegrationTests(MainTestCase):
    """Test-cases for class(es) ."""

    ##code-section class-header_testDocIntegrationTests #fill in your manual code here
    ##/code-section class-header_testDocIntegrationTests

    def afterSetUp(self):
        """
        """
        pass
    # Manually created methods


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    ##code-section test-suite-in-between #fill in your manual code here
##/code-section test-suite-in-between


    return TestSuite((
        ZopeDocFileSuite('testDocIntegrationTests.txt',
                         package='Products.feedfeeder.doc',
                         test_class=testDocIntegrationTests),
    ))

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


