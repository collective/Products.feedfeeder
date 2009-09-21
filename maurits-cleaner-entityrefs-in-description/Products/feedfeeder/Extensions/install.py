from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(site):
    out = StringIO()
    applyGenericSetupProfile(site, out)


def applyGenericSetupProfile(site, out):
    """Just apply our own extension profile.
    """

    our_profile = 'profile-Products.feedfeeder:default'
    setup_tool = getToolByName(site, 'portal_setup')
    print >> out, "Applying the generic setup profile for feedfeeder..."
    try:
        setup_tool.runAllImportStepsFromProfile(our_profile)
    except AttributeError:
        # BBB for Plone 2.5
        setup_tool.setImportContext(our_profile)
        setup_tool.runAllImportSteps(purge_old=False)
        setup_tool.setImportContext('profile-CMFPlone:plone')
    print >> out, "Applied the generic setup profile for feedfeeder"
