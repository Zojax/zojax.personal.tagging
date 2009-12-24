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
from zope import interface, schema
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds

from zojax.layoutform import button, Fields, PageletForm
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.personal.tagging.interfaces import IPersonalTags, _


class ITagsForm(interface.Interface):

    tags = schema.TextLine(
        title = _(u'Tags'),
        description = _(u'Enter your tags.'),
        required = False)


class ModifyTagsForm(PageletForm):

    fields = Fields(ITagsForm)

    def getContent(self):
        prefs = IPersonalTags(self.request.principal)
        tags = prefs.getTags(
            getUtility(IIntIds).queryId(removeAllProxies(self.context)))
        return {'tags': ', '.join(tags)}

    @button.buttonAndHandler(_(u'Save'))
    def handleSave(self, action):
        data, errors = self.extractData()

        tags = [t.strip() for t in data['tags'].split(',')]

        prefs = IPersonalTags(self.request.principal)
        prefs.setTags(
            getUtility(IIntIds).queryId(removeAllProxies(self.context)), tags)

        IStatusMessage(self.request).add(_(u'Tags have been changed.'))
        self.redirect('./')
