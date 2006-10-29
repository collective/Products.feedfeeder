# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.config import *
from Products.CMFCore.utils import getToolByName

##code-section module-header #fill in your manual code here
##/code-section module-header

MESSAGE_PRIORITIES = DisplayList((
        ('high', 'High Priority'),
            ('normal', 'Normal Priority'),
            ('low', 'Low Priority'),
            ))


schema = Schema((

    LinesField(
        name='feeds',
        widget=LinesWidget(
            label='Feeds',
            label_msgid='feedfeeder_label_feeds',
            i18n_domain='feedfeeder',
        )
    ),

    LinesField(
        default='low',
        name='workflow_state',
        vocabulary='getWorkflowStates',
        widget=SelectionWidget(
            format='select',
            label='Default workflow state on import',
            label_msgid='feedfeeder_label_feeds',
            i18n_domain='feedfeeder',

        )
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FeedfeederFolder_schema = ATBTreeFolder.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

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
    #content_icon = 'FeedfeederFolder.gif'
    immediate_view = 'feed-folder.html'
    default_view = 'feed-folder.html'
    suppl_views = ()
    typeDescription = "Feed Folder"
    typeDescMsgId = 'description_edit_feedfeederfolder'


    actions =  (


       {'action': "string:${object_url}/update_feed_items",
        'category': "object_buttons",
        'id': 'update_feed_items',
        'name': 'Update Feed Items',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:$object_url/feed-folder.html",
        'category': "object",
        'id': 'view',
        'name': 'view',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = FeedfeederFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Methods from Interface IFeedsContainer

    security.declarePublic('getItem')

    def getWorkflowStates(self):
        #import pdb; pdb.set_trace()

        wf_tool = getToolByName(self,'portal_workflow')
        wf = wf_tool.getChainForPortalType('FeedFeederItem')
        #states = wf_tool[wf].states.objectIds()

        #display_states = []
        #for state in states:
        #    dstate = []
        #    dstate.append(state.getId())
        #    dstate.append(state.getTitle())
        #    display_states.append(dstate)

        #return DisplayList(display_states)
        return DisplayList([('value','name')])

    def getInitialState(self):
        return 'low'
        

    def getItem(self,id):
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
    def replaceItem(self,id):
        """
        """
        self.manage_delObjects([id])
        return self.addItem(id)

    security.declarePublic('addItem')
    def addItem(self, id):
        """
        """
        self.invokeFactory('FeedFeederItem', id)
        return self[id]


registerType(FeedfeederFolder, PROJECTNAME)
# end of class FeedfeederFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



