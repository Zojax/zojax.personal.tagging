##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os.path
import unittest, doctest
from zope import interface, event
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.app.testing import setup, functional
from zope.app.testing.functional import ZCMLLayer
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import setSite
from zope.app.security.interfaces import IAuthentication

from zojax.ownership.interfaces import IOwnership
from zojax.catalog.catalog import ICatalog, Catalog
from zojax.personal.space.manager import \
    PersonalSpaceManager, IPersonalSpaceManager

from content import Content1, Content2

personalTaggingLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'personalTaggingLayer', allow_teardown=True)


def FunctionalDocFileSuite(*paths, **kw):
    layer = personalTaggingLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # people
        root['people'] = PersonalSpaceManager()
        sm.registerUtility(root['people'], IPersonalSpaceManager)

        user = sm.getUtility(IAuthentication).getPrincipal('zope.mgr')
        root['people'].assignPersonalSpace(user)

        user = sm.getUtility(IAuthentication).getPrincipal('zope.user1')
        root['people'].assignPersonalSpace(user)

        user = sm.getUtility(IAuthentication).getPrincipal('zope.user2')
        root['people'].assignPersonalSpace(user)

        # default content
        content = Content1()
        event.notify(ObjectCreatedEvent(content))
        IOwnership(content).ownerId = 'zope.user1'
        root['content11'] = content

        content = Content1()
        event.notify(ObjectCreatedEvent(content))
        IOwnership(content).ownerId = 'zope.user1'
        root['content12'] = content

        content = Content2()
        event.notify(ObjectCreatedEvent(content))
        IOwnership(content).ownerId = 'zope.user2'
        root['content21'] = content

        content = Content2()
        event.notify(ObjectCreatedEvent(content))
        IOwnership(content).ownerId = 'zope.user2'
        root['content22'] = content

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite

def test_suite():
    test = FunctionalDocFileSuite(
        "tests.txt")

    return unittest.TestSuite((test,))
