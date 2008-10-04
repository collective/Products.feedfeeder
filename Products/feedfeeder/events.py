# -*- coding: utf-8 -*-

from zope import interface
try:
    from zope.lifecycleevent import ObjectModifiedEvent
    ObjectModifiedEvent # pyflakes
except ImportError:
    # BBB for Zope 2.9
    from zope.app.event.objectevent import ObjectModifiedEvent
from Products.feedfeeder.interfaces import item as itemifaces


class FeedItemConsumedEvent(ObjectModifiedEvent):
    """Fired when a feed item has been successfully consumed.
    """

    interface.implements(itemifaces.IFeedItemConsumedEvent)
