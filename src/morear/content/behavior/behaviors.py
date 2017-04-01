# -*- coding: utf-8 -*-
from morear.content import _
# from plone.autoform import directives
from plone.supermodel import directives
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapts
from zope.interface import alsoProvides, implements
from zope.interface import provider
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.interfaces import IDexterityContent
#from plone.directives import dexterity
from plone.app.textfield import RichText
from plone.app.content.interfaces import INameFromTitle
from plone.namedfile.field import NamedBlobImage
from DateTime import DateTime
import random
#from plone.directives import form


class IBigImage(model.Schema):
    """ Add bigImage_* field """

    model.fieldset(
        'bigImage',
        label=_(u"bigImage"),
        fields=['bigImage_1', 'bigImage_2']
    )

    bigImage_1 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page."),
        required=False,
    )

    bigImage_2 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page."),
        required=False,
    )


class IContentMedia(model.Schema):
    """ Add content media field """

    model.fieldset(
        'contentMedia',
        label=_(u"contentMedia"),
        fields=['mainImage', 'aboveText', 'image_1', 'image_2', 'image_3', 'youtube', 'belowText']
    )

    mainImage = NamedBlobImage(
        title=_(u"Main Image"),
        required=False,
    )

    aboveText = RichText(
        title=_(u'Above Text'),
        required=False,
    )

    image_1 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    image_2 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    youtube = schema.TextLine(
        title=(u'Youtube URL'),
        required=False,
    )

    belowText = RichText(
        title=_(u'Below Text'),
        required=False,
    )


alsoProvides(IBigImage, IFormFieldProvider)
alsoProvides(IContentMedia, IFormFieldProvider)


def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class BigImage(object):
    implements(IBigImage)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    bigImage_1 = context_property("bigImage_1")
    bigImage_2 = context_property("bigImage_2")


class ContentMedia(object):
    implements(IContentMedia)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    mainImage = context_property("mainImage")
    aboveText = context_property("aboveText")
    image_1 = context_property("image_1")
    image_2 = context_property("image_2")
    image_3 = context_property("image_3")
    youtube = context_property("youtube")
    belowText = context_property("belowText")


class INamedFromTimeStamp(INameFromTitle):
    """ Marker/Form interface for namedFromTimeStamp
    """


class NamedFromTimeStamp(object):
    """ Adapter for NamedFromTimeStamp
    """
    implements(INamedFromTimeStamp)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    @property
    def title(self):
        timeString = '%s%s' % (DateTime().strftime("%Y%m%d%H%M"), random.randint(100000, 999999))
        return timeString
