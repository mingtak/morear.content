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
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


driverType = SimpleVocabulary(
    [SimpleTerm(value=u'One Driver', title=_(u'One Driver')),
     SimpleTerm(value=u'Two Driver', title=_(u'Two Driver'))]
    )


class IParameterSet(model.Schema):
    """ Add product's parameter set """

    model.fieldset(
        'headphone',
        label=_(u""),
        fields=['bgImage_left', 'bgImage_right', 'driver', 'lineLength', 'lineColor', 'shell3D',
                'surfaceColorR', 'surfaceColorL', 'logoColor']
    )

    lineColor = RelationList(
        title=_(u"Line Color"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaImage'),),
        required=False,
    )

    shell3D = RelationList(
        title=_(u"3D Print Shell"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaImage'),),
        required=False,
    )

    bgImage_left = NamedBlobImage(
        title=_(u'Background Image, Left'),
        required=False,
    )

    bgImage_right = NamedBlobImage(
        title=_(u'Background Image, Right'),
        required=False,
    )

    driver = schema.Choice(
        title=_(u'Driver'),
        vocabulary=driverType,
        required=False,
    )

    lineLength = RelationList(
        title=_(u"Line Length"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaText'),),
        required=False,
    )

    surfaceColorR = RelationList(
        title=_(u"Surface Color, Right"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaImage'),),
        required=False,
    )

    surfaceColorL = RelationList(
        title=_(u"Surface Color, Left"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaImage'),),
        required=False,
    )

    logoColor = RelationList(
        title=_(u"Logo Color"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='ParaImage'),),
        required=False,
    )


alsoProvides(IParameterSet, IFormFieldProvider)


def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class ParameterSet(object):
    implements(IParameterSet)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    bgImage_left = context_property("bgImage_left")
    bgImage_right = context_property("bgImage_right")
    driver = context_property("driver")
    lineLength = context_property("lineLength")
    surfaceColorR = context_property("surfaceColorR")
    surfaceColorL = context_property("surfaceColorL")
    lineColor = context_property("lineColor")
    shell3D = context_property("shell3D")
    logoColor = context_property("logoColor")
