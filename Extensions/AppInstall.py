from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(site):
    out = StringIO()
    applyGenericSetupProfile(site, out)


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
