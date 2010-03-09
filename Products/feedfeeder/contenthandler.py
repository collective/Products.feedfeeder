# -*- coding: utf-8 -*-

import logging
import formatter
from StringIO import StringIO

from persistent.dict import PersistentDict
from zope import interface
from zope import component
try:
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.annotation.interfaces import IAnnotations
    IAttributeAnnotatable, IAnnotations # pyflakes
except ImportError:
    from zope.app.annotation.interfaces import IAttributeAnnotatable
    from zope.app.annotation.interfaces import IAnnotations

from DateTime import DateTime

from Products.Archetypes import interfaces as at_ifaces

from Products.feedfeeder.interfaces.contenthandler import \
    IFeedItemContentHandler
from Products.feedfeeder.extendeddatetime import extendedDateTime
from Products.feedfeeder.utilities import SimpleHTMLParser

logger = logging.getLogger("feedfeeder")

class StandardContentHandler(object):
    interface.implements(IFeedItemContentHandler)
    component.adapts(at_ifaces.IBaseObject)
    
    def __init__(self, context):
        self.context = context

    def apply(self, entry, contentNode):
        self.update(entry, contentNode)
        self.context.update(**self.fields)

    def update(self, entry, contentNode):
        self.fields = fields = {}
        
        fields['title'] = getattr(entry, 'title', '')

        updated = entry.get('updated')
        published = entry.get('published')
        if not updated:
            updated = DateTime()
        if published is not None:
            try:
                published = extendedDateTime(published)
            except DateTime.SyntaxError:
                logger.warn("SyntaxError while parsing %r as DateTime for "
                            "the 'published' field of entry %s",
                            published, getattr(entry, 'title', ''))
            else:
                fields['effectiveDate'] = published

        linkDict = getattr(entry, 'link', None)
        if linkDict:
            # Hey, that's not a dict at all; at least not in my test.
            #link = linkDict['href']
            link = linkDict
        else:
            linkDict = getattr(entry, 'links', [{'href': ''}])[0]
            link = linkDict['href']
        fields['remoteUrl'] = fields['eventUrl'] = link

        summary = getattr(entry, 'summary', '')
        logger.debug("1 summary: %r" % summary)
        fields['description'] = self.convert_summary(summary)
        logger.debug("2 summary: %r" % summary)

        # Tags cannot be handled by the update method AFAIK,
        # because it is not an Archetypes field.
        fields['subject'] = fields['eventType'] = [
            x.get('term') for x in entry.get('tags', [])]

        fields['creators'] =[getattr(entry, 'author', '')]

        self.update_text(entry, contentNode)
    
    def convert_summary(self, input):
        out = StringIO()
        writer = formatter.DumbWriter(out)
        parser = SimpleHTMLParser(formatter.AbstractFormatter(writer))
        parser.feed(input)
        try:
            value = out.getvalue()
        except UnicodeDecodeError:
            logger.warn("UnicodeDecodeError while converting summary. "
                        "Falling back to original input.")
            value = input
        out.close()
        return value

    def update_text(self, entry, contentNode):
        if not hasattr(entry, 'content'):
            return
        
        obj = self.context
        content = entry.content[0]
        ctype = content.get('type')

        text = content['value']
        mimetype = ctype

        if contentNode is not None:
            # Grab the first non-<dl> node and treat
            # that as the content.
            top = contentNode.firstChild
            actualContent = None
            for node in top.childNodes:
                if node.nodeName == 'div':
                    text = node.toxml()

        field = obj.getField('text')
        if field is None:
            return
        
        if mimetype in field.getAllowedContentTypes(obj):
            obj.setText(text, mimetype=mimetype)
        else:
            obj.setText(text)

class AnnotationContentHandler(StandardContentHandler):
    """A content handler that parses definition list entries to apply
    zope3 style annotations to the context.
    """

    ANNO_KEY = 'feedfeeder.metadata'

    def _extractText(self, node):
        s = node.toxml().strip()
        s = s[len(node.nodeName)+2:-1*(len(node.nodeName)+3)]
        return s

    def update_text(self, entry, contentNode):
        top = contentNode.firstChild
        
        if not IAttributeAnnotatable.providedBy(self.context):
            directly = interface.directlyProvidedBy(self.context)
            interface.directlyProvides(self.context,
                                            directly + IAttributeAnnotatable)
        annotations = IAnnotations(self.context)
        metadata = annotations.get(self.ANNO_KEY, None)
        if metadata is None:
            metadata = PersistentDict()
            annotations[self.ANNO_KEY] = metadata

        for dl_el in top.childNodes:
            if dl_el.nodeName != 'dl':
                continue

            term = None
            for el in dl_el.childNodes:
                if el.nodeName == 'dt':
                    term = self._extractText(el)
                elif el.nodeName == 'dd':
                    definition = self._extractText(el)
                    metadata[term] = definition

        text = None
        for node in top.childNodes:
            if node.nodeName == 'div':
                text = node.toxml()

        obj = self.context
        field = obj.getField('text')
        if field is None:
            return
                
        content = entry.content[0]
        mimetype = content.get('type')
        if mimetype in field.getAllowedContentTypes(obj):
            obj.setText(text, mimetype=mimetype)
        else:
            obj.setText(text)
