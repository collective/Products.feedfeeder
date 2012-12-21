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
    setup_tool.runAllImportStepsFromProfile(our_profile)
    print >> out, "Applied the generic setup profile for feedfeeder"
