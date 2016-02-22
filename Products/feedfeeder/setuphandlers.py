from Products.CMFCore.utils import getToolByName

# The default profile id of your package:
PROFILE_ID = 'profile-Products.feedfeeder:default'


def update_types(context):
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')


def update_actions(context):
    context.runImportStepFromProfile(PROFILE_ID, 'actions')


def update_rolemap(context):
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')


def update_registry(context):
    # context could be portal_setup or the Plone Site.
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(
        PROFILE_ID, 'plone.app.registry')


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


def importVarious(context):
    # Only run step if a flag file is present
    if context.readDataFile('feedfeeder_various.txt') is None:
        return
    logger = context.getLogger('feedfeeder')
    site = context.getSite()
    add_indexes(site, logger)
    logger.info('feedfeeder_various step imported')
