# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.CMFCore.utils import getToolByName

from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.config import PROJECTNAME
from Products.feedfeeder import _

schema = Schema((

    LinesField(
        name='feeds',
        widget=LinesWidget(
            label=_('feedfeeder_label_feeds', default='Feeds')
        )
    ),

    BooleanField(
        name='redirect',
        widget=BooleanWidget(
            description=_("help_redirect", default="If checked the feed item will be automatically redirected if you don't have the edit permission."),
            label=_('label_redirect', default='Automatic redirect of feed items')
        )
    ),

    StringField(
        name='defaultTransition',
        vocabulary='getAvailableTransitions',
        widget=SelectionWidget(
            format='select',
            description=_('help_default_transition', default="When updating this feed's item the transition selected below will be performed."),
            label=_('label_default_transition', default='Default transition'),
        )
    ),

),
)

FeedfeederFolder_schema = ATBTreeFolder.schema.copy() + \
    schema.copy()


class FeedfeederFolder(ATBTreeFolder):
    """
      Verify class test
      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IFeedsContainer, FeedfeederFolder)
      True
    """
    security = ClassSecurityInfo()
    # zope3 interfaces
    interface.implements(IFeedsContainer)

    _at_rename_after_creation = True

    schema = FeedfeederFolder_schema

    def getAvailableTransitions(self):
        # Create a temporary object so we can ask what transitions are
        # available for it.
        id = 'temp_zest_temp'
        self.invokeFactory('FeedFeederItem', id)
        wf_tool = getToolByName(self, 'portal_workflow')
        transitions = wf_tool.getTransitionsFor(self[id])
        display_trans = [('', _('Keep initial state')), ]
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
                comment=_('Automatic transition triggered by FeedFolder'))
        return self[id]

    security.declarePublic('getFeedFolder')

    def getFeedFolder(self):
        return self


registerType(FeedfeederFolder, PROJECTNAME)
# end of class FeedfeederFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer
