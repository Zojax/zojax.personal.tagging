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
from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOSet, OOBTree
from zope import interface, component
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.authentication.utils import getPrincipal
from zojax.controlpanel.configlet import Configlet
from zojax.tagging.engine import TaggingEngine
from zojax.content.tagging.interfaces import IContentTaggable, IContentTags

from interfaces import IPersonalTagsConfiglet, IContentPersonalTags, \
                       IPersonalTaggable


class PersonalTagsConfiglet(Configlet):

    @property
    def tags(self):
        tags = self.data.get('tags')
        if tags is None:
            tags = OOBTree()
            self.data['tags'] = tags

        return tags

    @property
    def oids(self):
        oids = self.data.get('oids')
        if oids is None:
            oids = OOBTree()
            self.data['oids'] = oids

        return oids

    @property
    def engines(self):
        engines = self.data.get('engines')
        if engines is None:
            engines = OOBTree()
            self.data['engines'] = engines

        return engines

    def removeObject(self, oid):
        pass

    def removePrincipal(self, pid):
        pass

    def getTags(self, pid, oid):
        data = self.tags.get(pid)
        if data:
            return data.get(oid, ())
        else:
            return ()

    def setTags(self, pid, oid, tags):
        self.removeTags(pid, oid)

        if not tags:
            return

        t = []
        for tag in tags:
            tag = tag.lower().strip()
            if tag:
                t.append(tag)
        if not t:
            return

        tags = t

        pdata = self.tags.get(pid)
        if pdata is None:
            pdata = IOBTree()
            self.tags[pid] = pdata

        oids = pdata.get(oid)
        if oids is None:
            oids = OOSet()
            pdata[oid] = oids

        oids.update(tags)

        # insert oid -> pid reference
        oids = self.oids.get(oid)
        if oids is None:
            oids = OOSet()
            self.oids[oid] = oids

        oids.insert(pid)

        #update tagging engine
        engine = self.getEngine(pid)
        try:
            engine.update(oid, tags)
        except:
            engine.clear()
            engine.update(oid, tags)

    def removeTags(self, pid, oid):
        data = self.tags.get(pid)
        if data is not None and oid in data:
            del data[oid]

        data = self.oids.get(oid)
        if data is not None and pid in data:
            data.remove(pid)

        #update tagging engine
        engine = self.getEngine(pid)
        engine.remove(oid)

    def getEngine(self, pid):
        engine = self.engines.get(pid)
        if engine is None:
            engine = TaggingEngine()
            self.engines[pid] = engine

        return engine

    def isAvailable(self):
        return False


@component.adapter(IContentTaggable, IObjectModifiedEvent)
def taggableModified(ob, event):
    if component.getUtility(IPersonalTagsConfiglet).useGlobalTags:
        tags = IContentTags(ob).tags
        principal = getPrincipal()
        if principal is not None:
            component.getMultiAdapter((ob, principal), IContentPersonalTags).tags = tags
