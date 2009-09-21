# -*- coding: utf-8 -*-
import unittest
from zope.testing import doctestunit


def test_suite():
    return unittest.TestSuite((
        doctestunit.DocFileSuite('feedconsuming.txt',
                                 package='Products.feedfeeder.doc'),
        doctestunit.DocFileSuite('extendeddatetime.txt',
                                 package='Products.feedfeeder.doc'),
        ))
