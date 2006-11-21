from zope import interface
from zope import component
from Products.feedfeeder.interfaces.consumer import IFeedConsumer

class IUpdateFeedItems(interface.Interface):
    def update(): pass

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
        self.request.response.redirect(self.context.absolute_url()
                                       +"?portal_status_message=Feed+items+updated")
class FeedFolderView(object):
    """A view for feed folders.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def items(self):
        """All feed items.  Currently implemented as a generator since
        there could theoretically be tens of thousands of items.
        """
        
        listing = self.context.getFolderContents
        results = listing({'sort_on': 'getFeedItemUpdated', 
                           'sort_order': 'descending',
                           'portal_type': 'FeedFeederItem'})
        if not results and self.context.portal_type == 'Topic':
            # Use the queryCatalog of the Topic itself.
            results = self.context.queryCatalog({'portal_type': 'FeedFeederItem'})
        for index, x in enumerate(results):
            item = dict(updated_date = x.getFeedItemUpdated,
                        url = x.getURL(),
                        title = x.Title,
                        summary = x.Description,
                        author = x.getFeedItemAuthor,
                        )
            obj = x.getObject()
            # We need to see if this is really needed.
            # Yes, this is really needed:
            # x.getURL gets the url of the item in Zope and we need
            # the url of the original item, which isn't in the brain.
            # A test for this has now been added.
            url = obj.remote_url()
            if url:
                item['url'] = url
            self.extraDecoration(item, obj)
            enclosures = obj.getFolderContents()

            if (not obj.getText()) and len(enclosures) == 1:
                # only one enclosure? return item title but return link
                # to sole enclosure
                enclosure = enclosures[0]
                enc = dict(item)
                enc['url'] = enclosure.getURL()
                yield enc
            else:
                yield item

    def extraDecoration(self, item, obj):
        pass

    def item_list(self):
        return [x for x in self.items]

    def __call__(self, *args, **kwargs):
        return self.index(template_id='feed-folder.html')
