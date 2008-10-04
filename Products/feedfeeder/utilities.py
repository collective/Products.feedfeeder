# -*- coding: utf-8 -*-
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

from Products.feedfeeder.interfaces.container import IFeedsContainer
from Products.feedfeeder.interfaces.contenthandler import \
    IFeedItemContentHandler
from Products.feedfeeder.events import FeedItemConsumedEvent
from Products.feedfeeder.interfaces.consumer import IFeedConsumer

RE_FILENAME = re.compile('filename *= *(.*)')


class FeedConsumer:
    """
    """
    # zope3 interfaces
    interface.implements(IFeedConsumer)

    def retrieveFeedItems(self, container):
        feedContainer = IFeedsContainer(container)
        for url in feedContainer.getFeeds():
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

    def _retrieveSingleFeed(self, feedContainer, url):
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
            try:
                sig = md5.new(entry.id)
            except AttributeError:
                """ sometimes,
                gruik rss providers send items without guid element """
                sig = md5.new(entry.link)
            id = sig.hexdigest()

            updated = entry.get('updated')
            published = entry.get('published')

            if updated == '':
                # property may be blank if never item has never
                # been updated -- use published date
                updated = published

            if updated is None:
                continue

            updated = DateTime(updated)

            prev = feedContainer.getItem(id)

            if prev is None:
                # Completely new item, add it.
                addItem = feedContainer.addItem
            elif updated > prev.getFeedItemUpdated():
                # Refreshed item, replace it.
                addItem = feedContainer.replaceItem
            else:
                # Not new, not refreshed: let it be, laddy.
                continue

            obj = addItem(id)

            linkDict = getattr(entry, 'link', None)
            if linkDict:
                # Hey, that's not a dict at all; at least not in my test.
                #link = linkDict['href']
                link = linkDict
            else:
                linkDict = getattr(entry, 'links', [{'href': ''}])[0]
                link = linkDict['href']

            if published is not None:
                published = DateTime(published)
                obj.setEffectiveDate(published)
            obj.update(id=id,
                       title=getattr(entry, 'title', ''),
                       description=getattr(entry, 'summary', ''),
                       feedItemAuthor=getattr(entry, 'author', ''),
                       feedItemUpdated=updated,
                       link=link,
                       feedTitle=parsed['feed'].get('title', ''),
                       )
            if hasattr(entry, 'content'):
                content = entry.content[0]
                if content['type'] in ('text/xhtml', 'application/xhtml+xml'):
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
                            obj.update(text=content['value'])
                        else:
                            handler.apply(top)
                            # Grab the first non-<dl> node and treat
                            # that as the content.
                            actualContent = None
                            for node in top.childNodes:
                                if node.nodeName == 'div':
                                    actualContent = node.toxml()
                                    obj.update(text=actualContent)
                                    break
                    else:
                        obj.update(text=content['value'])
                else:
                    obj.update(text=content['value'])

            if hasattr(entry, 'links'):
                enclosures = [x for x in entry.links if x.rel == 'enclosure']
                real_enclosures = [x for x in enclosures if
                                   not self.isHTMLEnclosure(x)]

                for link in real_enclosures:
                    enclosureSig = md5.new(link.href)
                    enclosureId = enclosureSig.hexdigest()
                    enclosure = obj.addEnclosure(enclosureId)
                    enclosure.update(title=enclosureId)
                    updateWithRemoteFile(enclosure, link)
                    if enclosure.Title() != enclosure.getId():
                        self.tryRenamingEnclosure(enclosure, obj)
                    # At this moment in time, the
                    # rename-after-creation magic might have changed
                    # the ID of the file. So we recatalog the object.
                    obj.reindexObject()

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