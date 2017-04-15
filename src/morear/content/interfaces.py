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


class IProduct(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )


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
        fields=['mainSlideUIDs',]
    )

    mainSlideUIDs = schema.Text(
        title=_(u'Main Slider UIDs.'),
        required=True,
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
        fields=['moreDesign',]
    )

    moreDesign = schema.Text(
        title=_(u'More Design, UIDs'),
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


class IFaq(Interface):

    title = schema.TextLine(
        title=_(u'Question'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )
