# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from morear.content.interfaces import IFaq


@indexer(IFaq)
def faq_category_indexer(obj):
    return obj.category
