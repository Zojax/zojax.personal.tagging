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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds

from zojax.catalog.interfaces import ICatalog
from zojax.tagging.index import TagIndex

from zojax.personal.tagging.interfaces import IPersonalTags


class PersonalTags(object):

    def update(self):
        super(PersonalTags, self).update()

        ids = getUtility(IIntIds)
        engine = IPersonalTags(self.getPrincipal()).engine

        tags = []
        for weight, tag in engine.getTagCloud():
            tags.append({'tag': tag, 'weight': weight+100})

        self.tags = tags

        request = self.request
        if 'tag' in request:
            tag = request.get('tag', '').strip()

            if tag:
                ctool = getUtility(ICatalog)

                self.showContent = True
                self.contents = ctool.searchResults(
                    personalTags={'any_of': (tag,)},
                    sort_on='modified', sort_order='reverse',
                    indexes={'personalTags':TagIndex(engine)})

    def getPrincipal(self):
        return self.request.principal


class PersonalTagsWorkspace(PersonalTags):

    def update(self):
        super(PersonalTagsWorkspace, self).update()

        self.prefs = IPersonalTags(self.request.principal)

    def getPrincipal(self):
        return self.__parent__.principal
