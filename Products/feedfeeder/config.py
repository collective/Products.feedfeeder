# -*- coding: utf-8 -*-

# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. This will be included
# in this file if found.

from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = "feedfeeder"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add" % PROJECTNAME
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

STYLESHEETS = []
JAVASCRIPTS = []
