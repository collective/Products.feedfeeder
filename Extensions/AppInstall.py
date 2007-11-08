from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(portal):
    """Just apply our own extension profile.
    """
    out = StringIO()

    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-feedfeeder:default')
    print >> out, "Applying the generic setup profile for feedfeeder..."
    setup_tool.runAllImportSteps(purge_old=False)
    try:
        setup_tool.setImportContext('profile-CMFPlone:plone')
    except KeyError:
        # Plone 3.0 has a different profile name
        setup_tool.setImportContext('profile-Products.CMFPlone:plone')
    print >> out, "Applied the generic setup profile for feedfeeder"

