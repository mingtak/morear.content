# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from morear.content.interfaces import IFaq, ILocation, IProduct


@indexer(IFaq)
def faq_category_indexer(obj):
    return obj.category


@indexer(ILocation)
def city_indexer(obj):
    return obj.city


@indexer(ILocation)
def district_indexer(obj):
    return obj.district


@indexer(ILocation)
def weekendService_indexer(obj):
    return obj.weekendService


@indexer(IProduct)
def pType_indexer(obj):
    return obj.pType
