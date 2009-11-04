from zope import interface
from zope import component

from Products.feedfeeder.interfaces import folder
from Products.feedfeeder.interfaces.consumer import IFeedConsumer


class IUpdateFeedItems(interface.Interface):

    def update():
        pass


class IsFeedContainer(object):
    """A view that can only be looked up on feed folders"""

class UpdateFeedItems(object):
    """A view for updating the feed items in a feed folder.
    """

    interface.implements(IUpdateFeedItems)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        consumer = component.getUtility(IFeedConsumer)
        consumer.retrieveFeedItems(self.context)

    def __call__(self):
        self.update()
        self.request.response.redirect(
            self.context.absolute_url()
            +"?portal_status_message=Feed+items+updated")
