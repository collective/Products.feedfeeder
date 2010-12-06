from zope.interface import Interface
from zope.interface import implements 

from Products.Five import BrowserView

from zope.pagetemplate.pagetemplatefile import PageTemplateFile

class IFeedItemView(Interface):
    """ """

    def redirect_url():
        """ Returns empty string or the url to be redirected, depending on
            the configuration of the feed folder
        """

    def parent():
        """ Returns the feed item parent """


class FeedItemView(BrowserView):
    """ 
      Verify class test
      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IFeedItemView, FeedItemView)
      True

      >>> fake_requets = {}
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

      Test redirects
      --------------
      Item with a folder with redirect enabled
      >>> item1 = FakeItem(True)
      >>> view1 = FeedItemView(item1, fake_requets)
      >>> view1.redirect_url()
      'http://somewhere'

      Item with a folder with redirect not enabled
      >>> item2 = FakeItem(False)
      >>> view2 = FeedItemView(item2, fake_requets)
      >>> bool(view2.redirect_url())
      False

    """
    implements(IFeedItemView)

    __call__ = PageTemplateFile('feed-item.pt')


    def redirect_url(self):
        object_info = self.context.getObjectInfo()
        parent = self.parent()
        if parent.getRedirect():
            return object_info.get('link')
        else:
            return ''

    def parent(self):
        return self.context.getFeedFolder()
