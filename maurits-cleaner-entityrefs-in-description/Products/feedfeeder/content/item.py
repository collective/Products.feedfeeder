# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import *
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from zope import interface

from Products.feedfeeder.interfaces.item import IFeedItem
from Products.feedfeeder.config import PROJECTNAME

copied_fields = {}
copied_fields['text'] = ATDocument.schema['text'].copy()
copied_fields['text'].required = 0
schema = Schema((

    StringField(
        name='feedItemAuthor',
        widget=StringWidget(
            label='Feeditemauthor',
            label_msgid='feedfeeder_label_feedItemAuthor',
            i18n_domain='feedfeeder',
        )
    ),

    DateTimeField(
        name='feedItemUpdated',
        default=DateTime('2000/01/01'),
        widget=CalendarWidget(
            label='Feeditemupdated',
            label_msgid='feedfeeder_label_feedItemUpdated',
            i18n_domain='feedfeeder',
        )
    ),

    copied_fields['text'],
    StringField(
        name='link',
        widget=StringWidget(
            label='Link',
            label_msgid='feedfeeder_label_link',
            i18n_domain='feedfeeder',
        )
    ),

    ComputedField(
        name='objectids',
        widget=ComputedWidget(
            label='Object Ids',
            label_msgid='feedfeeder_label_objectids',
            i18n_domain='feedfeeder',
        )
    ),

    ComputedField(
        name='hasBody',
        widget=ComputedWidget(
            label='Has body text',
            label_msgid='feedfeeder_label_hasbody',
            i18n_domain='feedfeeder',
        )
    ),

    StringField(
        name='feedTitle',
        widget=StringWidget(
            label='Feed Title',
            label_msgid='feedfeeder_label_feedTitle',
            i18n_domain='feedfeeder',
        )
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

    # This name appears in the 'add' box
    archetype_name = 'Feed Item'

    meta_type = 'FeedFeederItem'
    portal_type = 'FeedFeederItem'
    allowed_content_types = ['File']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'FeedFeederItem.gif'
    immediate_view = 'feed-item.html'
    default_view = 'feed-item.html'
    suppl_views = ()
    typeDescription = "Feed Item"
    typeDescMsgId = 'description_edit_feedfeederitem'


    actions = (


       {'action': "string:${object_url}/feed-item.html",
        'category': "object",
        'id': 'view',
        'name': 'view',
        'permissions': ("View", ),
        'condition': 'python:1',
       },


    )

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
                comment='Automatic transition triggered by FeedFolder')
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
