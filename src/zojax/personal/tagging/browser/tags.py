##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
from zope.app.security.interfaces import IUnauthenticatedPrincipal
"""

$Id$
"""
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds

from zojax.personal.tagging.interfaces import IPersonalTags



class UserTags(object):

    oid = None
    tags = None

    def update(self):
        super(UserTags, self).update()

        prefs = IPersonalTags(self.request.principal)
        self.oid = getUtility(IIntIds).queryId(removeAllProxies(self.context))
        if self.oid:
            self.tags = prefs.getTags(self.oid)

    def isAvailable(self):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return False
        if self.oid is None:
            return False
        else:
            return True
