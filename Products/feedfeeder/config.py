# -*- coding: utf-8 -*-

# Product configuration.
#
# The contents of this module is imported into __init__.py, the
# workflow configuration and every content type module.

from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = "feedfeeder"

DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add" % PROJECTNAME
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

product_globals = globals()
