# -*- coding: utf-8 -*-
#
# Base TestCase for feedfeeder
#

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.feedfeeder.config import PRODUCT_DEPENDENCIES
from Products.feedfeeder.config import DEPENDENCIES

PRODUCT_DEPENDENCIES.append('feedfeeder')

# Install all (product-) dependencies
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('feedfeeder')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('feedfeeder')

testcase = PloneTestCase.PloneTestCase

PloneTestCase.setupPloneSite(products=PRODUCTS)


class MainTestCase(testcase):
    """Base TestCase for feedfeeder."""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MainTestCase))
    return suite
