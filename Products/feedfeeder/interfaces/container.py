# -*- coding: utf-8 -*-
from zope import interface


class IFeedsContainer(interface.Interface):
    """Container for feeds"""

    def getFeeds():
        """
        """

    def addItem(id):
        """
        """

    def replaceItem(id):
        """
        """

    def getItem(id):
        """
        """
