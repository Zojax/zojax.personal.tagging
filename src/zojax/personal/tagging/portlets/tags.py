##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
from zope import interface
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite

from zojax.content.space.utils import getSpace
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.tagging.interfaces import IPersonalTags


class PersonalTagsPortlet(object):

    engine = None
    siteUrl = None

    def listTags(self):
        idx = 0
        tags = []
        engine = removeSecurityProxy(self.engine)
        for weight, tag in engine.getTagCloud(True):
            weight = weight+100.0
            tags.append({'tag': tag, 'weight': '%0.2f'%weight, 'wvalue': weight})
            if idx == self.count:
                break
            idx += 1

        return tags

    def isAvailable(self):
        return self.engine is not None

    def update(self):
        space = getSpace(self.context)
        if IPersonalSpace.providedBy(space):
            principal = space.principal
        else:
            principal = self.request.principal
        try:
            self.engine = IPersonalTags(principal).engine
        except (TypeError, AttributeError):
            return
        self.siteUrl = absoluteURL(getSite(), self.request)
        super(PersonalTagsPortlet, self).update()


class PersonalTagsPortletView(object):

    def getcls(self, value):
        return value < 135 and 'tag-small' or None
