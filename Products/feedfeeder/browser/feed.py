import logging

from zope import interface
from zope import component

from Products.feedfeeder.interfaces.consumer import IFeedConsumer
from Products.feedfeeder.interfaces.container import IFeedsContainer

from Products.statusmessages.interfaces import IStatusMessage

from Products.feedfeeder import _

import transaction
import DateTime
import zExceptions

logger = logging.getLogger("feedfeeder")


class IUpdateFeedItems(interface.Interface):

    def update():
        pass


class IsFeedContainer(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_feedcontainer(self):
        return IFeedsContainer.providedBy(self.context)


class UpdateFeedItems(object):
    """A view for updating the feed items in a feed folder.
    """

    interface.implements(IUpdateFeedItems)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        consumer = component.getUtility(IFeedConsumer)
        consumer.retrieveFeedItems(self.context)

    def __call__(self):
        self.update()
        message = _('Feed items updated')
        messages = IStatusMessage(self.request, alternate=None)
        if messages is not None:
            messages.addStatusMessage(message, 'info')
        self.request.response.redirect(self.context.absolute_url())


class FeedFolderView(object):
    """A view for feed folders.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def items(self):
        """Return all feed items.

        Currently implemented as a generator since there could
        theoretically be tens of thousands of items.
        """

        listing = self.context.getFolderContents
        results = listing({'sort_on': 'getFeedItemUpdated',
                           'sort_order': 'descending',
                           'portal_type': 'FeedFeederItem'})
        if not results and self.context.portal_type == 'Topic':
            # Use the queryCatalog of the Topic itself.
            results = self.context.queryCatalog(
                portal_type='FeedFeederItem')
        for index, x in enumerate(results):
            content_url = x.getURL()
            item = dict(updated_date=x.getFeedItemUpdated,
                        url=content_url,
                        content_url=content_url,
                        title=x.Title,
                        summary=x.Description,
                        author=x.getFeedItemAuthor,
                        has_text=x.getHasBody,
                        target_link=x.getLink,
                        )
            self.extraDecoration(item, x)
            enclosures = x.getObjectids

            if (enclosures and enclosures is not None and
                    len(enclosures) == 1):
                # only one enclosure? return item title but return link
                # to sole enclosure, unless there is some body text.
                if not int(x.getHasBody):
                    item['url'] = item['url'] + '/' + enclosures[0]
            yield item

    def extraDecoration(self, item, brain):
        pass

    def item_list(self):
        return [x for x in self.items]

    def __call__(self, *args, **kwargs):
        return self.index(template_id='feed-folder.html')


class MegaUpdate(object):
    """ Update all feed folders on the site.

    This is intended to be called using HTTP command-line client
    or a clock server.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def updateAll(self):
        """
        """

        logger.info("Beginning feed update process")

        updated = 0
        errors = 0
        context = self.context.aq_inner

        brains = context.portal_catalog(portal_type="FeedfeederFolder")

        logger.info("Found %d feed folders" % len(list(brains)))

        for brain in brains:
            folder = brain.getObject()
            logger.debug("Updating folder:" + str(folder))
            update_view = folder.unrestrictedTraverse("@@update_feed_items")
            try:
                update_view.update()
                updated += 1
            except Exception, e:
                # Don't allow a single bad feed to crash us.
                logger.error("Feed raised exception:" + str(folder))
                logger.exception(e)
                errors += 1

        msg = "Updated %d feed folders, %d errors" % (updated, errors)
        logger.info(msg)

        return msg

    def __call__(self):
        return self.updateAll()


class MegaClean(object):
    """ Clean-up old feed items by deleting them on the site.

    This is intended to be called using HTTP command-line client
    or a clock server.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def clean(self, days, transaction_threshold=100):
        """Perform the clean-up by looking old objects and deleting them.

        Example: /planets/@@feed-mega-cleanup?days=30

        Commit ZODB transaction for every N objects to that commit
        buffer does not grow too long (timewise, memory wise).

        Source:
        http://opensourcehacker.com/2011/08/28/automatically-removing-old-items-from-a-plone-site/

        @param days: if item has been created before than this many
          days ago it is deleted

        @param transaction_threshold: How often we commit - for every nth item

        """
        context = self.context.aq_inner
        count = 0
        # DateTime deltas are days as floating points
        end = DateTime.DateTime() - days
        start = DateTime.DateTime(2000, 1, 1)
        date_range_query = {'query': (start, end), 'range': 'min:max'}
        logger.info("Beginning feed clean up for items older than {0} "
                    "({1} days)".format(end, days))
        items = context.portal_catalog.queryCatalog(
            {"portal_type": "FeedFeederItem",
             "getFeedItemUpdated": date_range_query,
             "sort_on": "getFeedItemUpdated"
             })
        for b in items:
            count += 1
            obj = b.getObject()
            logger.info("Deleting: %s %s", obj.absolute_url(),
                        obj.getFeedItemUpdated())
            obj.aq_parent.manage_delObjects([obj.getId()])
            if count % transaction_threshold == 0:
                # Prevent transaction becoming too large (memory buffer)
                # by committing now and then
                logger.info("Committing transaction")
                transaction.commit()
        msg = "{0} items removed.".format(count)
        logger.info(msg)
        return msg

    def __call__(self):
        days = self.request.form.get("days", None)
        if not days:
            raise zExceptions.InternalError(
                "Bad input. Please give days=90 as HTTP GET query parameter")
        days = int(days)
        return self.clean(days)
