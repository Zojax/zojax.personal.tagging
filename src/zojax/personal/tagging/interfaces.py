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
from zope.i18nmessageid import MessageFactory

from zojax.content.tagging.interfaces import IContentTaggable, IContentTags
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory

from field import PersonalTagsField

_ = MessageFactory('zojax.personal.tagging')


class IPersonalTaggable(IContentTaggable):
    """Marker interface for taggable object by user."""


class IPersonalTags(interface.Interface):
    """Personal tags"""

    engine = interface.Attribute('Tagging engine')

    def getTags(oid):
        """Return tags for oid."""

    def setTags(oid, tags):
        """Set tags for oid."""


class IContentPersonalTags(IContentTags):
    """ content personal tags """

    tags = PersonalTagsField(
        title = _('Personal tags'),
        description = _('Think of a tag as a simple category name. You can categorize your documents, files, and blog posts with any word or words that makes sense.'),
        required = False)


class IPersonalTagsConfiglet(interface.Interface):
    """Personal tags configlet """

    useGlobalTags = schema.Bool(title=_(u'Use global tags as personal'),
                                          description=_(u'If checked global tags '
                                                        'will be used to store '
                                                        'personal tags when editing'),
                                          default=True)


class IPersonalTagsWorkspace(IWorkspace):
    """ tags workspace """


class IPersonalTagsWorkspaceFactory(IWorkspaceFactory):
    """ tags workspace factory """
