# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from morear.content import _
from zope import schema
from zope.interface import Interface
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import invariant, Invalid
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class IMorearContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IProduct(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )


class WrongImageSize(Invalid):
    __doc__ = _(u"Get a wrong image size.")


class ICover(Interface):

    @invariant
    def validateImageSize(data):
        for i in range(10):
            imageObj = getattr(data, 'mainSlide_%s' % str(i+1))
            if hasattr(imageObj, 'getImageSize'):
                if imageObj.getImageSize() != (1280, 680):
                    raise WrongImageSize(_(u"Wrong image size, Please check Main Slider Image size, must be 1280x680 px."))

        for i in range(6):
            imageObj = getattr(data, 'moreDesignImage_%s' % str(i+1))
            if hasattr(imageObj, 'getImageSize'):
                if imageObj.getImageSize() != (640, 270):
                    raise WrongImageSize(_(u"Wrong image size, Please check More Design Image size, must be 640x270 px."))

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    model.fieldset(
        'mainSlide',
        label=_(u"mainSlide"),
        description=_(u"Must be select image size at 1280x680."),
        fields=['mainSlide_1', 'mainUrl_1',
                'mainSlide_2', 'mainUrl_2',
                'mainSlide_3', 'mainUrl_3',
                'mainSlide_4', 'mainUrl_4',
                'mainSlide_5', 'mainUrl_5',
                'mainSlide_6', 'mainUrl_6',
                'mainSlide_7', 'mainUrl_7',
                'mainSlide_8', 'mainUrl_8',
                'mainSlide_9', 'mainUrl_9',
                'mainSlide_10', 'mainUrl_10',]
    )

    mainSlide_1 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=True,
    )

    mainUrl_1 = schema.URI(
        title=_(u"Main Slider URL"),
        required=True,
    )

    mainSlide_2 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_2 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_3 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_3 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_4 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_4 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_5 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_5 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_6 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_6 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_7 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_7 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_8 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_8 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_9 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_9 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    mainSlide_10 = NamedBlobImage(
        title=_(u"Main Slide"),
        required=False,
    )

    mainUrl_10 = schema.URI(
        title=_(u"Main Slider URL"),
        required=False,
    )

    model.fieldset(
        'whatsNew',
        label=_(u"whatsNEW"),
        fields=['whatsNew_title', 'whatsNew_text', 'whatsNew_URI','whatsNew_bigImage', 'whatsNew_smallImage']
    )

    whatsNew_title = schema.TextLine(
        title=_(u"What's New title."),
        required=True,
    )

    whatsNew_text = schema.Text(
        title=_(u"What's New Text."),
        required=True,
    )

    whatsNew_URI = schema.URI(
        title=_(u"What's New URI."),
        required=True,
    )

    whatsNew_bigImage = NamedBlobImage(
        title=_(u"What's New Big Image, 800X400"),
        required=True,
    )

    whatsNew_smallImage = NamedBlobImage(
        title=_(u"What's New Small Image, 411X153."),
        required=False,
    )

    model.fieldset(
        'moreDesign',
        label=_(u"moreDesign"),
        description=_(u"Must be select image size at 640x270."),
        fields=['moreDesignImage_1', 'moreDesignUrl_1',
                'moreDesignImage_2', 'moreDesignUrl_2',
                'moreDesignImage_3', 'moreDesignUrl_3',
                'moreDesignImage_4', 'moreDesignUrl_4',
                'moreDesignImage_5', 'moreDesignUrl_5',
                'moreDesignImage_6', 'moreDesignUrl_6',]
    )

    moreDesignImage_1 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_1 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    moreDesignImage_2 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_2 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    moreDesignImage_3 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_3 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    moreDesignImage_4 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_4 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    moreDesignImage_5 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_5 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    moreDesignImage_6 = NamedBlobImage(
        title=_(u"More Design Image"),
        required=True,
    )

    moreDesignUrl_6 = schema.URI(
        title=_(u"More Design URL"),
        required=True,
    )

    """
    moreDesign = schema.Text(
        title=_(u'More Design, UIDs'),
        required=True,
    ) """



    model.fieldset(
        'moreFeast',
        label=_(u"More Feast Text"),
        fields=['moreFeast_text', 'spotifyEmbed']
    )

    moreFeast_text = schema.Text(
        title=_("More Feast Text"),
        required=True,
    )

    spotifyEmbed = schema.Text(
        title=_(u"Spotify Embeded Code"),
        required=True,
    )


faq_category = SimpleVocabulary(
    [SimpleTerm(value=u'Customize', title=_(u'Customize')),
     SimpleTerm(value=u'Shipping', title=_(u'Shipping'))]
    )


class IFaq(Interface):

    title = schema.TextLine(
        title=_(u'Question'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    category = schema.Choice(
        title=_(u'Category'),
        vocabulary=faq_category,
        default=u'Customize',
        required=True,
    )


class IDocWithBigImage(Interface):

    title = schema.TextLine(
        title=_(u'Document With Big Image'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )
