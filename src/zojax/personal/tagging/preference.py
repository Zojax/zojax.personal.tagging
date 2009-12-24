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
"""

$Id$
"""
from rwproperty import getproperty, setproperty

from zope import interface
from zope.security.interfaces import IPrincipal
from zope.security.proxy import removeSecurityProxy
from zope.component import getUtility, adapts
from zope.app.intid.interfaces import IIntIds

from zojax.content.tagging.interfaces import IContentTaggable

from interfaces import IPersonalTags, IPersonalTagsConfiglet, IContentPersonalTags, \
                       IPersonalTaggable


class BasePersonalTags(object):

    @property
    def engine(self):
        return getUtility(IPersonalTagsConfiglet).getEngine(self.__principal__.id)

    def getTags(self, oid):
        configlet = getUtility(IPersonalTagsConfiglet)
        return configlet.getTags(self.__principal__.id, oid)

    def setTags(self, oid, tags):
        configlet = getUtility(IPersonalTagsConfiglet)
        configlet.setTags(self.__principal__.id, oid, tags)

    def removeTags(self, oid):
        configlet = getUtility(IPersonalTagsConfiglet)
        configlet.removeTags(self.__principal__.id, oid)


class PersonalTags(BasePersonalTags):
    interface.implements(IPersonalTags)


class ContentPersonalTags(BasePersonalTags):
    adapts(IContentTaggable, IPrincipal)
    interface.implements(IContentPersonalTags)

    def __init__(self, context, principal):
        self.context, self.__principal__ = context, principal
        self.id = getUtility(IIntIds).getId(removeSecurityProxy(context))

    @getproperty
    def tags(self):
        return self.getTags(self.id)

    @setproperty
    def tags(self, tags):
        self.setTags(self.id, tags)
