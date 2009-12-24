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
from zope import interface, schema
from zojax.content.actions.interfaces import IAction
from zojax.portlet.interfaces import IPortletManagerConfiguration

from zojax.personal.tagging.interfaces import _


class IPersonalTagsPortletManager(IPortletManagerConfiguration):

    portletIds = schema.Tuple(
        title = _('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.actions',),
        required = True)


class IPersonalTagsPortlet(interface.Interface):

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    count = schema.Int(
        title = _(u'Tags count'),
        description = _('Number of tags in portlet.'),
        default = 20,
        required = True)
