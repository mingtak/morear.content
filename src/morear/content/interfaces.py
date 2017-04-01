# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from morear.content import _
from zope import schema
from zope.interface import Interface
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IMorearContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICover(Interface):

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
        fields=['mainSlideUIDs',
                'mainSlide_1', 'mainSlideURI_1',
                'mainSlide_2', 'mainSlideURI_2',
                'mainSlide_3', 'mainSlideURI_3',]
    )

    mainSlideUIDs = schema.Text(
        title=_(u'Main Slider UIDs.'),
        required=True,
    )

    mainSlide_1 = NamedBlobImage(
        title=_(u"Main Slider, 1280X680"),
        required=True,
    )

    mainSlideURI_1 = schema.URI(
        title=_(u"Main Slide URI."),
        required=True,
    )

    mainSlide_2 = NamedBlobImage(
        title=_(u"Main Slider, 1280X680"),
        required=False,
    )

    mainSlideURI_2 = schema.URI(
        title=_(u"Main Slide URI."),
        required=False,
    )

    mainSlide_3 = NamedBlobImage(
        title=_(u"Main Slider, 1280X680"),
        required=False,
    )

    mainSlideURI_3 = schema.URI(
        title=_(u"Main Slide URI."),
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
        fields=['moreDesign',
                'moreDesignImage_1', 'moreDesignURI_1',
                'moreDesignImage_2', 'moreDesignURI_2',
                'moreDesignImage_3', 'moreDesignURI_3',
                'moreDesignImage_4', 'moreDesignURI_4',
                'moreDesignImage_5', 'moreDesignURI_5',
                'moreDesignImage_6', 'moreDesignURI_6',]
    )

    moreDesign = schema.Text(
        title=_(u'More Design, UIDs'),
        required=True,
    )

    moreDesignImage_1 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_1 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    moreDesignImage_2 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_2 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    moreDesignImage_3 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_3 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    moreDesignImage_4 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_4 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    moreDesignImage_5 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_5 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    moreDesignImage_6 = NamedBlobImage(
        title=_(u"More Design Image, 640X269."),
        required=True,
    )

    moreDesignURI_6 = schema.URI(
        title=_(u"More Design URI."),
        required=True,
    )

    model.fieldset(
        'moreFeast',
        label=_(u"More Feast Text"),
        fields=['moreFeast_text']
    )

    moreFeast_text = schema.Text(
        title=_("More Feast Text"),
        required=True,
    )
