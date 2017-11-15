# -*- coding: utf-8 -*-
from morear.content import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form
from zope import schema


class IMorearSetting(Form.Schema):

    """ Basic setting for Morear """
    faqCat = schema.Text(
        title=_(u"Faq Categories Setting"),
        required=True,
    )


class MorearSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IMorearSetting

MorearSettingControlPanelView = layout.wrap_form(MorearSettingControlPanelForm, ControlPanelFormWrapper)
MorearSettingControlPanelView.label = _(u"Morear Setting")
