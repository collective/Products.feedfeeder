from zope import interface
from zope.lifecycleevent import IObjectModifiedEvent


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
