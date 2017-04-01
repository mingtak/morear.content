# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

LIMIT = 10


class CustomInfoInHeader(base.ViewletBase):
    """  """
