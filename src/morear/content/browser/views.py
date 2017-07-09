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


class ProductOptionView(BrowserView):

    template = ViewPageTemplateFile("template/product_option_view.pt")

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


class LocationView(BrowserView):

    template = ViewPageTemplateFile("template/location_view.pt")

    def getCitys(self):
        portal = api.portal.get()
        brain = api.content.find(context=portal, Type='Location')
        citys = []
        for item in brain:
            if item.city not in citys:
                citys.append(item.city)
        return citys


    def __call__(self):
        context = self.context
        request = self.request

        return self.template()


class LocationListingView(LocationView):

    template = ViewPageTemplateFile("template/location_listing_view.pt")


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        catalog = portal.portal_catalog

        searchCond = {'Type': 'Location'}
        city = safe_unicode(request.form.get('city', None))
        if city and safe_unicode('請選擇') not in city:
            searchCond['city'] = city

        district = safe_unicode(request.form.get('dist', None))
        if district and safe_unicode('請選擇') not in district:
            searchCond['district'] = district

        weekendService = request.form.get('weekend', '')
        if '假日' in weekendService: # 只找平日營業
            searchCond['weekendService'] = True

        keyword = safe_unicode(request.form.get('keyword', None))
        if keyword:
            searchCond['SearchableText': keyword]

        self.brain = catalog(searchCond)
        return self.template()


class GetDist(BrowserView):

    def getDists(self, city):
        portal = api.portal.get()
        brain = api.content.find(context=portal, Type='Location', city=city)
        dists = []
        for item in brain:
            if item.district not in dists:
                dists.append(item.district)
        return dists


    def __call__(self):

        request = self.request
        portal = api.portal.get()

        city = safe_unicode(request.get('city', None))
        if city is None or safe_unicode('請選擇') in city:
            return ['--請選擇區域--']
        else:
            return self.getDists(city)


class SearchResultView(BrowserView):

    template = ViewPageTemplateFile("template/search_result_view.pt")

    def __call__(self):
        request = self.request
        portal = api.portal.get()

        self.keyword = request.form.get('keyword', '')
        self.brain = api.content.find(portal=portal, SearchableText=self.keyword)

        return self.template()

