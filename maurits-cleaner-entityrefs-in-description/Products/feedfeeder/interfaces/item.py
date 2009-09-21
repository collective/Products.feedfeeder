# -*- coding: utf-8 -*-

from zope import interface
try:
    from zope.lifecycleevent import IObjectModifiedEvent
except ImportError:
    # BBB for Zope 2.9
    from zope.app.event.interfaces import IObjectModifiedEvent


class IFeedItem(interface.Interface):
    """
    """

    def addEnclosure(id):
        """Add an enclosure.
        """


class IFeedItemConsumedEvent(IObjectModifiedEvent):
    """Intended to be fired after a new feed item has been successfully
    consumed.
    """
