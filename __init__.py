# -*- coding: utf-8 -*-

# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

from zLOG import LOG, INFO, DEBUG

LOG('feedfeeder', DEBUG, 'Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

from Globals import package_home
from Products.CMFCore import utils as cmfutils
from Products.CMFCore import permissions
from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

import os, os.path

from Products.feedfeeder.config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/feedfeeder',
                                    product_globals)

##code-section custom-init-head #fill in your manual code here
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry
import Products.CMFPlone.interfaces
##/code-section custom-init-head


def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration
    import content
    import interfaces

    import utilities
    import contenthandler

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for feedfeeder installed'

    ##code-section custom-init-bottom #fill in your manual code here
    profile_registry.registerProfile(
        name='default',
        title='Feedfeeder',
        description='Profile for Feedfeeder',
        path='profiles/default',
        product='feedfeeder',
        profile_type=EXTENSION,
        for_=Products.CMFPlone.interfaces.IPloneSiteRoot)
    ##/code-section custom-init-bottom

