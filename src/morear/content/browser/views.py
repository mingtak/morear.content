# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone.utils import safe_unicode
import logging

logger = logging.getLogger('morear.content')
LIMIT=20


class TransState(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#        import pdb; pdb.set_trace()
        uid = request.form.get('uid')
        if not uid:
            return

        obj = api.content.find(UID=uid)[0].getObject()
        state = api.content.get_state(obj=obj)
        if state == 'published':
            api.content.transition(obj=obj, transition='reject')
        else:
            api.content.transition(obj=obj, transition='publish')


class DocWithBigImageView(BrowserView):

    template = ViewPageTemplateFile("template/doc_with_big_image_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class FaqView(BrowserView):

    template = ViewPageTemplateFile("template/faq_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class FaqListingView(BrowserView):

    template = ViewPageTemplateFile("template/faq_listing_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class ProductListingView(BrowserView):

    template = ViewPageTemplateFile("template/product_listing_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class CoverView(BrowserView):

    template = ViewPageTemplateFile("template/cover_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class ProductView(BrowserView):

    template = ViewPageTemplateFile("template/product_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class NewsListingView(BrowserView):

    template = ViewPageTemplateFile("template/news_listing_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class IsAdmin(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            return 'False'
        current = api.user.get_current()
        roles = api.user.get_roles(user=current)
#        import pdb; pdb.set_trace()
        if 'Manager' in roles or 'Site Administrator' in roles:
            return 'True'
        else:
            return 'False'

