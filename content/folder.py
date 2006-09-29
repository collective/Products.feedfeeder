from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='feeds',
        widget=LinesWidget(
            label='Feeds',
            label_msgid='feedfeeder_label_feeds',
            i18n_domain='feedfeeder',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FeedfeederFolder_schema = getattr(ATBTreeFolder, 'schema', Schema(())).copy() + \
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
    allowed_content_types = ['FeedFeederItem'] + list(getattr(ATBTreeFolder, 'allowed_content_types', []))
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

    security.declarePublic('getFeeds')
    def getFeeds(self):
        """
        """
        return self.feeds

    security.declarePublic('addItem')
    def addItem(self, id):
        """
        """
        self.invokeFactory('FeedFeederItem', id)
        return self[id]

    security.declarePublic('replaceItem')
    def replaceItem(self,id):
        """
        """
        self.manage_delObjects([id])
        return self.addItem(id)

    security.declarePublic('getItem')
    def getItem(self,id):
        """
        """
        if id in self.objectIds():
            return self[id]
        return None


registerType(FeedfeederFolder, PROJECTNAME)
# end of class FeedfeederFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



