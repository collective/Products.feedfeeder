# -*- coding: utf-8 -*-

# Product configuration.
#
# The contents of this module is imported into __init__.py, the
# workflow configuration and every content type module.

from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = "feedfeeder"
AddContent = "feedfeeder: Add"
UpdateFeed = "feedfeeder: Update feed"
UpdateAllFeeds = "feedfeeder: Update all feeds"

DEFAULT_ADD_CONTENT_PERMISSION = AddContent
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

MAXSIZE = 10000  # in kb

product_globals = globals()
