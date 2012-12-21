from zope import interface
from zope.lifecycleevent import ObjectModifiedEvent

from Products.feedfeeder.interfaces import item as itemifaces


class FeedItemConsumedEvent(ObjectModifiedEvent):
    """Fired when a feed item has been successfully consumed.
    """

    interface.implements(itemifaces.IFeedItemConsumedEvent)
