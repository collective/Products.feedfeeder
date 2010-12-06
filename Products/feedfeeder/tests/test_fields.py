from Products.feedfeeder.tests.MainTestCase import MainTestCase


class TestFields(MainTestCase):
    """ """
    def afterSetUp(self):
        self.loginAsPortalOwner()

        feedfolder_id = self.folder.invokeFactory('FeedfeederFolder', 'feedfolder')

        self.feedfolder = getattr(self.folder, feedfolder_id)
#        self.feedfolder.invokeFactor

    def test_redirect_field(self):
        """ Does exists the redirect field?  """
        self.assertTrue(getattr(self.feedfolder, 'getRedirect'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFields))
    return suite


