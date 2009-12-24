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
from zope import interface, component
from zope.component import getAdapter
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.location import Location
from zope.security.interfaces import IPrincipal

from zojax.catalog.catalog import queryCatalog
from zojax.content.type.container import ContentContainer
from zojax.content.space.workspace import WorkspaceFactory
from zojax.personal.space.interfaces import \
    IPersonalSpace, IPersonalWorkspaceDescription
from zojax.security.utils import checkPermissionForPrincipal

from interfaces import _, IPersonalTagsWorkspace, IPersonalTagsWorkspaceFactory


class PersonalTagsWorkspace(Location):
    interface.implements(IPersonalTagsWorkspace)

    __name__ = 'tags'
    title = _('Tags')
    description = u''

    @property
    def space(self):
        return self.__parent__


class PersonalTagsWorkspaceFactory(object):
    component.adapts(IPersonalSpace)
    interface.implements(IPersonalTagsWorkspaceFactory)

    name = u'tags'
    title = _('Tags')
    description = _(u'Personal tags.')
    weight = 1000

    def __init__(self, space):
        self.space = space

    def get(self):
        view = PersonalTagsWorkspace()
        view.__parent__ = self.space
        return view

    install = get

    def uninstall(self):
        pass

    def isInstalled(self):
        return False

    def isAvailable(self):
        return True


class PersonalTagsWorkspaceDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'tags'
    title = _(u'Tags')
    description = u''

    def createTemp(self, context):
        view = PersonalTagsWorkspace()
        view.__parent__ = context
        return view
