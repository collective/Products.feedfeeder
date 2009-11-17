# -*- coding: utf-8 -*-
import logging
from xml.dom import minidom
import md5
import os
import re
import tempfile
import urllib2

import feedparser
from DateTime import DateTime
from zope import component
from zope import event
from zope import interface

from plone.i18n.normalizer.interfaces import IURLNormalizer

from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from Products.feedfeeder.interfaces.contenthandler import \
    IFeedItemContentHandler
from Products.feedfeeder.events import FeedItemConsumedEvent
from Products.feedfeeder.interfaces.consumer import IFeedConsumer
from Products.feedfeeder.extendeddatetime import extendedDateTime
from Products.feedfeeder.interfaces import folder as folder_ifaces
from Products.feedfeeder.interfaces import item as item_ifaces

RE_FILENAME = re.compile('filename *= *(.*)')
logger = logging.getLogger("feedfeeder")

import formatter
import htmllib
from StringIO import StringIO

# Unifiable list taken from http://www.aaronsw.com/2002/html2text.py
unifiable = {
    'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"', 'nbsp': ' ',
    'rarr': '->', 'larr': '<-', 'middot': '*', 'copy': '(C)',
    'mdash': '--', 'ndash': '-', 'oelig': 'oe', 'aelig': 'ae',
    'agrave': 'a', 'aacute': 'a', 'acirc': 'a', 'atilde': 'a', 'auml': 'a',
    'aring': 'a',
    'egrave': 'e', 'eacute': 'e', 'ecirc': 'e', 'euml': 'e',
    'igrave': 'i', 'iacute': 'i', 'icirc': 'i', 'iuml': 'i',
    'ograve': 'o', 'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
    'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
    }


class SimpleHTMLParser(htmllib.HTMLParser):

    def handle_entityref(self, name):
        logger.warn("Parsing entity %r", name)
        value = unifiable.get(name)
        self.formatter.add_literal_data(value)
        logger.warn("Parsed as value %r", value)


def convert_summary(input):
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


def update_text(obj, text, mimetype=None):
    field = obj.getField('text')
    if mimetype in field.getAllowedContentTypes(obj):
        obj.setText(text, mimetype=mimetype)
        obj.reindexObject()
    else:
        # update does a reindexObject automatically
        obj.update(text=text)


class FeedConsumer:
    """
    """
    # zope3 interfaces
    interface.implements(IFeedConsumer)

    def retrieveFeedItems(self, container):
        feedContainer = folder_ifaces.IFolderFeeds(container)
        for url in feedContainer.feedURLs:
            self._retrieveSingleFeed(feedContainer, url)

    def tryRenamingEnclosure(self, enclosure, feeditem):
        newId = enclosure.Title()
        for x in range(1, 10):
            if newId not in feeditem.objectIds():
                try:
                    feeditem.manage_renameObject(enclosure.getId(),
                                            newId)
                    break
                except:
                    pass
            newId = '%i_%s' % (x, enclosure.Title())

    def addItem(self, feedsContainer, id):
        """
        """
        container = feedsContainer.__parent__
        item = container[
            container.invokeFactory(feedsContainer.itemType, id)]
        interface.alsoProvides(item, item_ifaces.IFeedItem)
        wf_tool = getToolByName(container, 'portal_workflow')
        for transition in feedsContainer.itemTransitions:
            wf_tool.doActionFor(
                item, transition.rsplit('/', 1)[-1], comment=
                'Automatic transition triggered by FeedFolder')
        return item

    def replaceItem(self, feedsContainer, id):
        """
        """
        container = feedsContainer.__parent__
        container.manage_delObjects([id])
        return self.addItem(feedsContainer, id)

    def addEnclosure(self, feedsContainer, item, id):
        """
        """
        container = item
        is_folder = item.restrictedTraverse(
            '@@plone_context_state').is_structural_folder()
        if not is_folder:
            container = aq_parent(item)

        enclosure = container[container.invokeFactory('File', id)]

        wf_tool = getToolByName(item, 'portal_workflow')
        for transition in feedsContainer.enclosureTransitions:
            wf_tool.doActionFor(
                enclosure, transition.rsplit('/', 1)[-1],
                comment='Automatic transition triggered by FeedFolder')

        if not is_folder:
            related = item.getField('relatedItems')
            if related is not None:
                item.addReference(enclosure, related.relationship)

        return enclosure

    def _retrieveSingleFeed(self, feedContainer, url):
        container = feedContainer.__parent__
        # feedparser doesn't understand proper file: url's
        if url.startswith('file://'):
            url = url[7:]
            if not os.path.exists(url):
                raise IOError("Couldn't locate %r" % url)
        # urllib does not support the 'feed' scheme -- replace with 'http'
        if url.startswith('feed://'):
            url = url.replace('feed://', 'http://', 1)
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            linkDict = getattr(entry, 'link', None)
            title = getattr(entry, 'title', '')
            id = getattr(entry, 'id', linkDict or title)
            if not id:
                logger.warn((
                    "Skipping the following entry since no id, link "
                    "or title can be found: %r") % entry)
                continue
            id = md5.new(id).hexdigest()

            updated = entry.get('updated')
            published = entry.get('published')

            if not updated:
                # property may be blank if item has never
                # been updated -- use published date
                updated = published

            if updated:
                try:
                    updated = extendedDateTime(updated)
                except DateTime.SyntaxError:
                    logger.warn("SyntaxError while parsing %r as DateTime for "
                                "the 'updated' field of entry %s",
                                updated, getattr(entry, 'title', ''))
                    continue

            prev = feedContainer.__parent__.get(id)
            if prev is None:
                # Completely new item, add it.
                obj = self.addItem(feedContainer, id)
            elif updated is None:
                logger.warn("No updated or published date known. "
                            "Not updating previously added entry.")
                continue
            elif updated > prev.modified():
                # Refreshed item, replace it.
                obj = self.replaceItem(feedContainer, id)
            else:
                # Not new, not refreshed: let it be, laddy.
                continue

            if linkDict:
                # Hey, that's not a dict at all; at least not in my test.
                #link = linkDict['href']
                link = linkDict
            else:
                linkDict = getattr(entry, 'links', [{'href': ''}])[0]
                link = linkDict['href']

            if not updated:
                updated = DateTime()
            if published is not None:
                try:
                    published = extendedDateTime(published)
                except DateTime.SyntaxError:
                    logger.warn("SyntaxError while parsing %r as DateTime for "
                                "the 'published' field of entry %s",
                                published, getattr(entry, 'title', ''))
                    continue
                obj.setEffectiveDate(published)

            summary = getattr(entry, 'summary', '')
            logger.debug("1 summary: %r" % summary)
            summary = convert_summary(summary)
            logger.debug("2 summary: %r" % summary)

            # Tags cannot be handled by the update method AFAIK,
            # because it is not an Archetypes field.
            feed_tags = [x.get('term') for x in entry.get('tags', [])]
            obj.update(id=id,
                       title=title,
                       description=summary,
                       creators=[getattr(entry, 'author', '')],
                       remoteURL=link,
                       subject=feed_tags,
                       eventUrl=link,
                       eventType=feed_tags)
            if hasattr(entry, 'content'):
                content = entry.content[0]
                ctype=content.get('type') # sometimes no type on linux prsr.
                if ctype in ('text/xhtml', 'application/xhtml+xml'):
                    # Warning: minidom.parseString needs a byte
                    # string, not a unicode one, so we need to
                    # encode it first.
                    # http://evanjones.ca/python-utf8.html
                    try:
                        doc = minidom.parseString(
                            content['value'].encode('utf-8'))
                    except:
                        # Might be an ExpatError, but that is
                        # somewhere in a .so file, so we cannot
                        # specifically catch only that error.
                        continue
                    if len(doc.childNodes) > 0 and \
                            doc.firstChild.hasAttributes():
                        handler = None
                        top = doc.firstChild
                        cls = top.getAttribute('class')
                        if cls:
                            handler = component.queryAdapter(
                                obj, IFeedItemContentHandler, name=cls)
                        if handler is None:
                            handler = component.queryAdapter(
                                obj, IFeedItemContentHandler)

                        if handler is None:
                            update_text(obj, content['value'], mimetype=ctype)
                        else:
                            handler.apply(top)
                            # Grab the first non-<dl> node and treat
                            # that as the content.
                            actualContent = None
                            for node in top.childNodes:
                                if node.nodeName == 'div':
                                    actualContent = node.toxml()
                                    update_text(obj, actualContent,
                                                mimetype=ctype)
                                    break
                    else:
                        update_text(obj, content['value'], mimetype=ctype)
                else:
                    update_text(obj, content['value'], mimetype=ctype)

            if hasattr(entry, 'links'):
                enclosures = [x for x in entry.links if x.rel == 'enclosure']
                real_enclosures = [x for x in enclosures if
                                   not self.isHTMLEnclosure(x)]

                for link in real_enclosures:
                    enclosureSig = md5.new(link.href)
                    enclosureId = enclosureSig.hexdigest()
                    enclosure = self.addEnclosure(
                        feedContainer, obj, enclosureId)
                    enclosure.update(title=enclosureId)
                    updateWithRemoteFile(enclosure, link)
                    if enclosure.Title() != enclosure.getId():
                        self.tryRenamingEnclosure(enclosure, obj)
                    # At this moment in time, the
                    # rename-after-creation magic might have changed
                    # the ID of the file. So we recatalog the object.
                    obj.reindexObject()


            # the modification date is updated on
            # reindexObject(idxs=[]) so set the modification date on
            # the way out
            obj.setModificationDate(updated)
            obj.reindexObject(idxs=['modification_date'])

            if obj is not None:
                event.notify(FeedItemConsumedEvent(obj))

    def isHTMLEnclosure(self, enclosure):
        return enclosure.type == u'text/html'


def updateWithRemoteFile(obj, link):
    file = tempfile.TemporaryFile('w+b')
    try:
        remote = urllib2.urlopen(link.href.encode('utf-8'))
        info = remote.info()
        filename = None
        if link.href.startswith('file:'):
            pos = link.href.rfind('/')
            if pos > -1:
                filename = link.href[pos+1:]
            else:
                filename = link.href[5:]

        disp = info.get('Content-Disposition', None)
        if disp is not None:
            m = RE_FILENAME.search(disp)
            if m is not None:
                filename = m.group(1).strip()

        if filename is not None:
            obj.update(title=filename)

        max = 2048
        sz = max
        while sz == max:
            buffer = remote.read(max)
            sz = len(buffer)
            if sz > 0:
                file.write(buffer)

        file.flush()
        file.seek(0)
        obj.update_data(file, link.type)
        file.close()
    except urllib2.URLError, e:
        # well, if we cannot retrieve the data, the file object will
        # remain empty
        pass
    except  OSError, e:
        # well, if we cannot retrieve the data, the file object will
        # remain empty
        pass
