# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import (
    CalendarWidget, ComputedField, ComputedWidget, DateTimeField,
    ObjectField, Schema, StringField, StringWidget, registerType)

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from zope import interface

from Products.feedfeeder.interfaces.item import IFeedItem
from Products.feedfeeder.config import PROJECTNAME

from Products.feedfeeder import _


copied_fields = {}
copied_fields['text'] = ATDocument.schema['text'].copy()
copied_fields['text'].required = 0
schema = Schema((

    StringField(
        name='feedItemAuthor',
        widget=StringWidget(
            label=_('feedfeeder_label_feedItemAuthor', default='Feeditemauthor'),
        )
    ),

    DateTimeField(
        name='feedItemUpdated',
        default=DateTime('2000/01/01'),
        widget=CalendarWidget(
            label=_('feedfeeder_label_feedItemUpdated', 'Feeditemupdated'),
        )
    ),

    copied_fields['text'],
    StringField(
        name='link',
        widget=StringWidget(
            label=_('feedfeeder_label_link', default='Link'),
        )
    ),

    ComputedField(
        name='objectids',
        widget=ComputedWidget(
            label=_('feedfeeder_label_objectids', default='Object Ids'),
        )
    ),

    ComputedField(
        name='hasBody',
        widget=ComputedWidget(
            label=_('feedfeeder_label_hasbody', default='Has body text'),
        )
    ),

    StringField(
        name='feedTitle',
        widget=StringWidget(
            label=_('feedfeeder_label_feedTitle', default='Feed Title'),
        )
    ),
    ObjectField(
        name='objectInfo',
#        read_permission=ManagePortal,
#        write_permission=ManagePortal,
        widget=StringWidget(
            visible={'view': 'invisible',
                     'edit': 'invisible'},
        ),
        default={},
    ),

),
)

FeedFeederItem_schema = getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()


class FeedFeederItem(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    # zope3 interfaces
    interface.implements(IFeedItem)

    _at_rename_after_creation = True

    schema = FeedFeederItem_schema

    security.declarePublic('addEnclosure')

    def addEnclosure(self, id):
        """
        """
        self.invokeFactory('File', id)
        self.reindexObject()
        transition = self.getDefaultTransition()
        if transition != '':
            wf_tool = getToolByName(self, 'portal_workflow')
            # The default transition should be valid for a
            # FeedFolderItem, but our File might not have the same
            # transitions available.  So check this.
            transitions = wf_tool.getTransitionsFor(self[id])
            transition_ids = [trans['id'] for trans in transitions]
            if transition in transition_ids:
                wf_tool.doActionFor(self[id], transition,
                comment=_('Automatic transition triggered by FeedFolder'))
        return self[id]

    security.declarePublic('remote_url')

    def remote_url(self):
        """Compatibility method that makes working with link checkers
        easier.
        """
        return self.getLink()

    security.declarePublic('getObjectids')

    def getObjectids(self):
        """Return the ids of enclosed objects.
        """
        return self.objectIds()

    security.declarePublic('getHasBody')

    def getHasBody(self):
        """Return True if the object has body text.
        """
        if bool(self.getText()):
            return 1
        return 0

    def _get_feed_tags(self):
        """Get the tags from the feed item.

        tags/keywords/categories

        We store this in the _feed_tags attribute.  Old items may not
        have this yet, so we protect against AttributeErrors by
        specifying a getter and setter as wrapper around that
        attribute.  We return an empty list when the attribute is not
        there.

        This is not hooked up yet, but this way the tags are available
        for whoever wants to integrate them in third party products.
        """
        if base_hasattr(self, '_feed_tags'):
            return getattr(self, '_feed_tags')
        return []

    def _set_feed_tags(self, value):
        """Get the tags from the feed item.

        tags/keywords/categories
        """
        if not value:
            self._feed_tags = []
        elif isinstance(value, list):
            self._feed_tags = value
        elif isinstance(value, tuple):
            self._feed_tags = list(value)
        elif isinstance(value, basestring):
            self._feed_tags = [value]
        else:
            raise ValueError("expected list, tuple or basestring, got %s",
                             type(value))

    feed_tags = property(_get_feed_tags, _set_feed_tags)


registerType(FeedFeederItem, PROJECTNAME)
