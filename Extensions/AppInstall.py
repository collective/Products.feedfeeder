from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(site):
    out = StringIO()
    applyGenericSetupProfile(site, out)
    add_indexes(site, out)


def applyGenericSetupProfile(site, out):
    """Just apply our own extension profile.
    """

    setup_tool = getToolByName(site, 'portal_setup')
    setup_tool.setImportContext('profile-feedfeeder:default')
    print >> out, "Applying the generic setup profile for feedfeeder..."
    setup_tool.runAllImportSteps(purge_old=False)
    try:
        setup_tool.setImportContext('profile-CMFPlone:plone')
    except KeyError:
        # Plone 3.0 has a different profile name
        setup_tool.setImportContext('profile-Products.CMFPlone:plone')
    print >> out, "Applied the generic setup profile for feedfeeder"


def add_indexes(site, out):
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
        print >> out, 'Added DateIndex for %s.' % idx
