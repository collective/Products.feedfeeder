from Products.CMFCore.utils import getToolByName

# The default profile id of your package:
PROFILE_ID = 'profile-Products.feedfeeder:default'
# The profile id for the registry.  Done because on Plone 4.1 you get
# an ImportError when trying to store a value for
# plone.app.querystring.
REGISTRY_PROFILE_ID = 'profile-Products.feedfeeder:registry'


def update_types(context):
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')


def update_actions(context):
    context.runImportStepFromProfile(PROFILE_ID, 'actions')


def update_rolemap(context):
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')


def update_registry(context):
    # context could be portal_setup or the Plone Site.
    portal_setup = getToolByName(context, 'portal_setup')
    try:
        portal_setup.runImportStepFromProfile(
            REGISTRY_PROFILE_ID, 'plone.app.registry')
    except (ValueError, ImportError):
        # Probably Plone 4.0, which has no plone.app.registry, or
        # Plone 4.1, which has no plone.app.querystring.  None of
        # these two actually needs the registry settings in that case.
        pass


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
    update_registry(site)
    logger.info('feedfeeder_various step imported')
