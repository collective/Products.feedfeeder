from zope import interface
from zope import schema
from zope.schema import vocabulary

from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

class IFeedFolder(interface.Interface):
    """A folder for which feedURLs have been set
    """

def AddableTypesVocab(context):
    context = getattr(context, '__parent__', context)
    if not hasattr(context, 'allowedContentTypes'):
        return vocabulary.SimpleVocabulary(())
    return vocabulary.SimpleVocabulary([
        vocabulary.SimpleTerm(
            type_info.getId(), title=type_info.Title())
        for type_info in context.allowedContentTypes()])

def TransitionsVocab(context):
    wft = getToolByName(context, 'portal_workflow')
    wf_ids = set()
    trans_titles = set() 
    terms = {}
    for type_info in context.allowedContentTypes():
        for wf_id in wft.getChainFor(type_info.getId()):
            if wf_id in wf_ids:
                continue
            wf_ids.add(wf_id)
        
            wf = wft.getWorkflowById(wf_id)
            for trans in wf.transitions.objectValues():
                title = u'%s (%s)' % (
                    trans.actbox_name or trans.title, wf.title)
                path = '/'.join(trans.getPhysicalPath())
                terms[title] = vocabulary.SimpleTerm(
                    path, title=title)
    return vocabulary.SimpleVocabulary(
        [term for title, term in sorted(terms.iteritems())])

class IFolderFeedsForm(interface.Interface):
    """Specify syndication feeds from which to populate a folder
    """

    feedURLs = schema.List(
        title=u'Feed URLs',
        required=False,
        value_type=schema.ASCIILine())
    itemType = schema.Choice(
        title=u'Item Type',
        required=False,
        vocabulary='AddableTypesVocab')
    itemTransitions = schema.List(
        title=u'Item Workflow Transitions',
        required=False,
        value_type=schema.Choice(vocabulary='TransitionsVocab'))

    @interface.invariant
    def areTransitionsValidForType(context):
        wft = getToolByName(context.__context__, 'portal_workflow')
        transitions = {}
        errors = set()
        for wf in wft.getWorkflowsFor(context.itemType):
            for trans in wf.transitions.objectValues():
                transitions['/'.join(trans.getPhysicalPath())] = wf
        for item_trans in context.itemTransitions:
            if item_trans not in transitions:
                errors.add(item_trans)

        if errors:
            titles = []
            for trans_path in errors:
                trans = context.__context__.restrictedTraverse(
                    trans_path)
                wf = aq_parent(aq_parent(trans))
                titles.append(u'%s (%s)' % (
                    trans.actbox_name or trans.title, wf.title))
            raise interface.Invalid(
                ("The following transitions are invalid for the '%s' "
                 "content type: %s") % (
                    context.itemType, ', '.join(
                        "'%s'" % title for title in titles)))
