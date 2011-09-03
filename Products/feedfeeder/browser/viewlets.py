from plone.app.layout.viewlets.content import DocumentBylineViewlet


class FeedFeederBylineViewlet(DocumentBylineViewlet):

    def creator(self):
        return self.context.getFeedItemAuthor()
