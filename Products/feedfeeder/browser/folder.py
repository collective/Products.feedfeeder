from zope import interface
from zope import component
from zope import annotation

import transaction

from z3c.form import interfaces
from z3c.form import form
from z3c.form import field
from z3c.form import widget
from z3c.form.browser import textarea

from plone.app.z3cform.layout import wrap_form

from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from Products.feedfeeder.interfaces import folder as folder_ifaces
from Products.feedfeeder.interfaces import consumer
from Products.feedfeeder import folder

class LinesWidget(textarea.TextAreaWidget):
    interface.implements(interfaces.IDataConverter)

    def toWidgetValue(self, value):
        return '\n'.join(value or [])

    def toFieldValue(self, raw):
        return self.field._type(
            self.field.value_type.fromUnicode(item)
            for item in raw.split('\n'))

def LinesFieldWidget(field, request):
    """IFieldWidget factory for TextWidget."""
    return widget.FieldWidget(field, LinesWidget(request))

class FolderFeedsForm(form.EditForm):
    """Specify syndication feeds from which to populate a folder
    """
    label = u"Folder Feeds"

    fields = field.Fields(folder_ifaces.IFolderFeedsForm)
    fields['feedURLs'].widgetFactory = LinesFieldWidget

    def applyChanges(self, *args, **kw):
        """Mark the folder as an IFeedFolder if ther are feedURLs"""
        result = super(FolderFeedsForm, self).applyChanges(
            *args, **kw)
        context = aq_inner(self.context)

        interface.noLongerProvides(context, folder_ifaces.IFeedFolder)

        annotations = annotation.IAnnotations(context)
        factory = folder.FolderFeeds
        key = factory.__module__ + '.' + factory.__name__
        if key in annotations:
            if folder_ifaces.IFolderFeedsForm(context).feedURLs:
                interface.alsoProvides(
                    context, folder_ifaces.IFeedFolder)

        context.reindexObject(idxs=['object_provides'])
    
        return result

FolderFeedsFormWrapped = wrap_form(FolderFeedsForm)

class UpdateAllFeedFolders(object):

    def __call__(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        feed_consumer = component.getUtility(consumer.IFeedConsumer)
        for brain in catalog(
            hasFeedURLs=True,
            path='/'.join(context.getPhysicalPath())):
            folder = brain.getObject()
            feed_consumer.retrieveFeedItems(folder)
            # Commit after every folder reduce chances of a write
            # conflict with other requests
            transaction.commit()
