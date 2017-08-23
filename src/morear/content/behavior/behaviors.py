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
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from DateTime import DateTime
import random
from plone.directives import form


class IMusicMan(model.Schema):
    """ Add Music Man behavior """

    model.fieldset(
        'musicman',
        label=_(u"musicman / recommend"),
        fields=['mmTitle', 'mmInfo', 'mmImage', 'mmAudio', ]
    )

    mmTitle = schema.TextLine(
        title=_(u"Music Man Title"),
        required=False,
    )

    mmInfo = schema.Text(
        title=_(u"Music Man Infomation"),
        required=False,
    )

    mmImage = NamedBlobImage(
        title=_(u"Music Man Image"),
        required=False,
    )

    mmAudio = NamedBlobFile(
        title=_(u"Music Man Audio"),
        description=_(u"Audio file format: *.mp3"),
        required=False,
    )


class IFeatured(model.Schema):
    """ Add featured field """

    form.mode(featured='hidden')
    featured = schema.Bool(
        title=_(u"Featured"),
        description=_(u"Checked it for featured."),
        default=False,
        required=False,
    )

#    form.mode(headWeight='hidden')
    headWeight = schema.Int(
        title=_(u"Head Weight"),
        description=_(u"Please set Head Weight value, default:10."),
        default=10,
        required=True,
    )


class IKeyword(model.Schema):
    """ Add Keyword field """

    keyword = schema.TextLine(
        title=_(u'Keyword'),
        description=_(u"keyword, split with common."),
        required=False,
    )


class IBigImage(model.Schema):
    """ Add bigImage_* field """

    model.fieldset(
        'bigImage',
        label=_(u"bigImage"),
        fields=['bigImage_1', 'bigImage_2', 'bigImage_3','bigImage_4', 'bigImage_5', ]
    )

    bigImage_1 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page. Size:1900 X 950"),
        required=False,
    )

    bigImage_2 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page. Size:1900 X 950"),
        required=False,
    )

    bigImage_3 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page. Size:1900 X 950"),
        required=False,
    )

    bigImage_4 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page. Size:1900 X 950"),
        required=False,
    )

    bigImage_5 = NamedBlobImage(
        title=_(u"Big Image"),
        description=_(u"Big image for page. Size:1900 X 950"),
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
        description=_(u"Size: 600 X 450"),
        required=False,
    )

    aboveText = RichText(
        title=_(u'Above Text'),
        required=False,
    )

    image_1 = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Size: 600 X 450"),
        required=False,
    )

    image_2 = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Size: 600 X 450"),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"Size: 600 X 450"),
        required=False,
    )

    youtube = schema.TextLine(
        title=_(u'Youtube URL'),
        required=False,
    )

    belowText = RichText(
        title=_(u'Below Text'),
        required=False,
    )


alsoProvides(IBigImage, IFormFieldProvider)
alsoProvides(IContentMedia, IFormFieldProvider)
alsoProvides(IKeyword, IFormFieldProvider)
alsoProvides(IFeatured, IFormFieldProvider)
alsoProvides(IMusicMan, IFormFieldProvider)


def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class MusicMan(object):
    implements(IMusicMan)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    mmTitle = context_property("mmTitle")
    mmInfo = context_property("mmInfo")
    mmImage = context_property("mmImage")
    mmAudio = context_property("mmAudio")


class Keyword(object):
    implements(IKeyword)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    keyword = context_property("keyword")


class BigImage(object):
    implements(IBigImage)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    bigImage_1 = context_property("bigImage_1")
    bigImage_2 = context_property("bigImage_2")
    bigImage_3 = context_property("bigImage_3")
    bigImage_4 = context_property("bigImage_4")
    bigImage_5 = context_property("bigImage_5")


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


class Featured(object):
    implements(IFeatured)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    featured = context_property("featured")
    headWeight = context_property("headWeight")


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
