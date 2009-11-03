from zope import interface

from z3c.form import interfaces
from z3c.form import form
from z3c.form import field
from z3c.form import widget
from z3c.form.browser import textarea

from plone.app.z3cform.layout import wrap_form

from Products.feedfeeder.interfaces import folder

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

    fields = field.Fields(folder.IFolderFeedsForm)
    fields['feedURLs'].widgetFactory = LinesFieldWidget

FolderFeedsFormWrapped = wrap_form(FolderFeedsForm)
