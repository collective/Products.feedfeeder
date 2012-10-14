from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implements


class IFeedItemView(Interface):
    """ """

    def redirect_url():
        """ Returns empty string or the url to be redirected, depending on
            the configuration of the feed folder.

            Returns an empty string if redirect is not enabled or if
            you have modify permissions
        """

    def parent():
        """ Returns the feed item parent """

    def checkEditPermission():
        """ Returns if you have the edit permission"""

    def show_doc_byline():
        """ Returns whether the document byline should be shown or not."""


class FeedItemView(BrowserView):
    """
      Verify class test
      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IFeedItemView, FeedItemView)
      True

      Fake objects
      ------------
      >>> fake_request = {}
      >>> class FakeFolder(object):
      ...     def __init__(self, redirect):
      ...         self.redirect = redirect
      ...     def getRedirect(self):
      ...         return self.redirect
      >>> class FakeItem(object):
      ...     def __init__(self, redirect):
      ...         self.folder = FakeFolder(redirect)
      ...     def getObjectInfo(self):
      ...         return {'link':'http://somewhere'}
      ...     def getFeedFolder(self):
      ...         return self.folder
      >>> class FakeFeedItemView(FeedItemView):
      ...     def checkEditPermission(self):
      ...         return True

      Test redirects
      --------------
      Item with a folder with redirect enabled
      >>> item1 = FakeItem(True)
      >>> view1 = FakeFeedItemView(item1, fake_request)
      >>> bool(view1.redirect_url())
      False

      Item with a folder with redirect not enabled
      >>> item2 = FakeItem(False)
      >>> view2 = FakeFeedItemView(item2, fake_request)
      >>> bool(view2.redirect_url())
      False

      Test redirects with no edit permissions
      ---------------------------------------
      >>> class FakeFeedItemView(FeedItemView):
      ...     def checkEditPermission(self):
      ...         return False

      Item with a folder with redirect enabled
      >>> item1 = FakeItem(True)
      >>> view1 = FakeFeedItemView(item1, fake_request)
      >>> view1.redirect_url()
      'http://somewhere'

      Item with a folder with redirect not enabled
      >>> item2 = FakeItem(False)
      >>> view2 = FakeFeedItemView(item2, fake_request)
      >>> bool(view2.redirect_url())
      False
    """
    implements(IFeedItemView)

    def __call__(self):
        redirect_url = self.redirect_url()
        if redirect_url:
            return self.request.response.redirect(redirect_url)
        # Render our template as set in the zcml.
        return self.index()

    def redirect_url(self):
        object_info = self.context.getObjectInfo()
        parent = self.parent()
        if parent.getRedirect() and not self.checkEditPermission():
            return object_info.get('link')
        else:
            return ''

    def parent(self):
        return self.context.getFeedFolder()

    def checkEditPermission(self):
        """ Returns if you have the edit permission"""
        membership = getMultiAdapter((self.context, self.request),
                                     name=u'plone_tools').membership()
        return membership.checkPermission(
            'Modify portal content', self.context)

    def show_doc_byline(self):
        """ Returns whether the document byline should be shown or not."""
        plone_tools = getMultiAdapter((self.context, self.request),
                                      name='plone_tools')
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        properties = plone_tools.properties()
        site_properties = getattr(properties, 'site_properties')
        anonymous = portal_state.anonymous()
        allowAnonymousViewAbout = site_properties.getProperty(
            'allowAnonymousViewAbout', True)
        return not anonymous or allowAnonymousViewAbout
