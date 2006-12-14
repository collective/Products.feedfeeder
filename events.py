# -*- coding: utf-8 -*-

from zope import interface
from zope.app.event import objectevent
from Products.feedfeeder.interfaces import item as itemifaces

class FeedItemConsumedEvent(objectevent.ObjectModifiedEvent):
    """Fired when a feed item has been successfully consumed.
    """

    interface.implements(itemifaces.IFeedItemConsumedEvent)
