# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATFolder
from Products.feedfeeder.interfaces.item import IFeedItem
from Products.feedfeeder.config import *
from Products.CMFCore.utils import getToolByName

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.document import ATDocument
from DateTime import DateTime

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['text'] = ATDocument.schema['text'].copy()
copied_fields['text'].required = 0
schema = Schema((

    StringField(
        name='feedItemAuthor',
        index="FieldIndex:brains",
        widget=StringWidget(
            label='Feeditemauthor',
            label_msgid='feedfeeder_label_feedItemAuthor',
            i18n_domain='feedfeeder',
        )
    ),

    DateTimeField(
        name='feedItemUpdated',
        default=DateTime('2000/01/01'),
        index="DateIndex:brains",
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

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FeedFeederItem_schema = getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

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


    actions =  (


       {'action': "string:${object_url}/feed-item.html",
        'category': "object",
        'id': 'view',
        'name': 'view',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = FeedFeederItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Methods from Interface IFeedItem

    security.declarePublic('addEnclosure')
    def addEnclosure(self,id):
        """
        """
        self.invokeFactory('File', id)
        transition = self.getDefaultTransition()
        if transition != '':
            wf_tool = getToolByName(self,'portal_workflow')
            wf_tool.doActionFor(self[id], transition,
                comment='Automatic transition triggered by FeedFolder')
        return self[id]

    # Manually created methods

    security.declarePublic('remote_url')
    def remote_url(self):
        """Compatibility method that makes working with link checkers
        easier.
        """

        return self.getLink()
    ##/code-section class-header


registerType(FeedFeederItem, PROJECTNAME)
# end of class FeedFeederItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



