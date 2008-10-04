# -*- coding: utf-8 -*-
from zope import interface


class IFeedfeederFolderView(interface.Interface):
    """View of a FeedfeederFolder"""

    def item_list():
        """List of items"""
