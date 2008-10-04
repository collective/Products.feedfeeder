from Products.CMFCore.utils import getToolByName
# Check for Plone 3.0 or above
try:
    from Products.CMFPlone.migrations import v3_0
    v3_0 # pyflakes
except ImportError:
    PLONE30 = 0
else:
    PLONE30 = 1


def add_indexes(site, logger):
    """Add indexes.

    I have *had* it with catalog.xml for indexes.  If we have to add
    some code here to reindex our indexes after catalog.xml has been
    imported, we might as well add some code instead to only add them
    when they are not there yet.

    """
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()

    idx = "getFeedItemUpdated"
    if idx not in indexes:
        # Setting index_naive_time_as_local to True does not seem
        # possible with the 'extra' argument to addIndex, but True is
        # the default, so we are happy.
        catalog.addIndex(idx, 'DateIndex')
        logger.info('Added DateIndex for %s.' % idx)


def createFeedUpdatedCriterion(site, logger):
    """Make getFeedItemUpdated field a criterion for Smart Folders.

    This is for backwards compatibility with Plone 2.5 as in 3.0 this
    can be done with profiles/default/portal_atct.xml
    """
    if PLONE30:
        # Plone 3 does this in portal_atct.xml
        return
    logger.info('Adding smart folder metadata and index.')
    fieldname = 'getFeedItemUpdated'
    friendlyName = 'FeedItem Updated'
    description = 'Date that the FeedItem was last updated.'
    enabled = True
    criteria = ('ATFriendlyDateCriteria', 'ATDateRangeCriterion')

    smart_folder_tool = getToolByName(site, 'portal_atct')
    smart_folder_tool.addIndex(fieldname, friendlyName, description,
                               enabled, criteria)
    smart_folder_tool.addMetadata(fieldname, friendlyName, description,
                                  enabled)


def importVarious(context):
    # Only run step if a flag file is present
    if context.readDataFile('feedfeeder_various.txt') is None:
        return
    logger = context.getLogger('feedfeeder')
    site = context.getSite()
    add_indexes(site, logger)
    createFeedUpdatedCriterion(site, logger)
    logger.info('feedfeeder_various step imported')
