# -*- coding: utf-8 -*-

from zope import interface
from zope.app.event import interfaces as evtifaces

class IFeedItem(interface.Interface):
    """
    """

    def addEnclosure(id):
       """Add an enclosure.
       """

class IFeedItemConsumedEvent(evtifaces.IObjectModifiedEvent):
    """Intended to be fired after a new feed item has been successfully
    consumed.
    """
