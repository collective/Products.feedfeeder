# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.CMFCore.utils import getToolByName

from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.config import PROJECTNAME

schema = Schema((

    LinesField(
        name='feeds',
        widget=LinesWidget(
            label='Feeds',
            label_msgid='feedfeeder_label_feeds',
            i18n_domain='feedfeeder',
        )
    ),

    StringField(
        name='defaultTransition',
        vocabulary='getAvailableTransitions',
        widget=SelectionWidget(
            format='select',
            description="When updating this feed's item the transition selected below will be performed.",
            description_msgid="help_default_transition",
            label='Default transition',
            label_msgid='label_default_transition',
            i18n_domain='feedfeeder',
        )
    ),
),
)

FeedfeederFolder_schema = ATBTreeFolder.schema.copy() + \
    schema.copy()


class FeedfeederFolder(ATBTreeFolder):
    """
    """
    security = ClassSecurityInfo()
    # zope3 interfaces
    interface.implements(IFeedsContainer)

    # This name appears in the 'add' box
    archetype_name = 'Feed Folder'

    meta_type = 'FeedfeederFolder'
    portal_type = 'FeedfeederFolder'
    allowed_content_types = ['FeedFeederItem']
    filter_content_types = 1
    global_allow = 1
    content_icon = 'feed_icon.gif'
    immediate_view = 'feed-folder.html'
    default_view = 'feed-folder.html'
    suppl_views = ()
    typeDescription = "Feed Folder"
    typeDescMsgId = 'description_edit_feedfeederfolder'


    actions = (

       {'action': "string:${object_url}/update_feed_items",
        'category': "object_buttons",
        'id': 'update_feed_items',
        'name': 'Update Feed Items',
        'permissions': ("View", ),
        'condition': 'python:1',
       },

       {'action': "string:$object_url/feed-folder.html",
        'category': "object",
        'id': 'view',
        'name': 'view',
        'permissions': ("View", ),
        'condition': 'python:1',
       },

    )

    _at_rename_after_creation = True

    schema = FeedfeederFolder_schema

    def getAvailableTransitions(self):
        # Create a temporary object so we can ask what transitions are
        # available for it.
        id = 'temp_zest_temp'
        self.invokeFactory('FeedFeederItem', id)
        wf_tool = getToolByName(self, 'portal_workflow')
        transitions = wf_tool.getTransitionsFor(self[id])
        display_trans = [('', 'Keep initial state'), ]
        for trans in transitions:
            display_trans.append((trans['id'], trans['name']))
        # Unindex and remove the temporary object
        self[id].unindexObject()
        self._delOb(id)
        return DisplayList(display_trans)

    security.declarePublic('getItem')

    def getItem(self, id):
        """
        """
        if id in self.objectIds():
            return self[id]
        return None

    security.declarePublic('getFeeds')

    def getFeeds(self):
        """
        """
        return self.feeds

    security.declarePublic('replaceItem')

    def replaceItem(self, id):
        """
        """
        self.manage_delObjects([id])
        return self.addItem(id)

    security.declarePublic('addItem')

    def addItem(self, id):
        """
        """
        self.invokeFactory('FeedFeederItem', id)
        transition = self.getDefaultTransition()
        if transition != '':
            wf_tool = getToolByName(self, 'portal_workflow')
            wf_tool.doActionFor(self[id], transition,
                comment='Automatic transition triggered by FeedFolder')
        return self[id]


registerType(FeedfeederFolder, PROJECTNAME)
# end of class FeedfeederFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer
