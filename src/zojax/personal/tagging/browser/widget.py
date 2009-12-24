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
from zope import interface, schema, component
from zope.component import getUtility
from zope.security.proxy import removeSecurityProxy
from zope.app.component.hooks import getSite

from z3c.form import converter
from z3c.form.browser import text
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget

from zojax.personal.tagging.field import IPersonalTagsField
from zojax.personal.tagging.interfaces import IPersonalTags
from interfaces import IPersonalTagsWidget


class PersonalTagsWidget(text.TextWidget):
    interface.implements(IPersonalTagsWidget)

    klass = u'z-widget-personal-tags'

    def popularTags(self):
        engine = IPersonalTags(self.request.principal).engine

        idx = 1
        tags = []
        for weight, tag in engine.getTagCloud(True):
            tags.append(tag)
            if idx == 10:
                break
            idx += 1

        return tags


class PersonalTagsWidgetConverter(converter.BaseDataConverter):
    component.adapts(IPersonalTagsField, PersonalTagsWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        return u', '.join(value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        res = []
        for tag in (v for v in (v.strip() for v in value.split(',')) if v):
            if tag not in res:
                res.append(tag)
        return tuple(res)


@interface.implementer(IFieldWidget)
@component.adapter(IPersonalTagsField, IFormLayer)
def PersonalTagsFieldWidget(field, request):
    return FieldWidget(field, PersonalTagsWidget(request))
