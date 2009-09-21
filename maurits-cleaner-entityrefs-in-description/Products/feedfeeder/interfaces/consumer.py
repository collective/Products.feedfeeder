# -*- coding: utf-8 -*-
from zope import interface


class IFeedConsumer(interface.Interface):
    """
    """

    def retrieveFeedItems(container):
        """Get new/updated feed items."""
