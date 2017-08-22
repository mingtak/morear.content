# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone.utils import safe_unicode
import logging
import transaction
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import json
import random
import urllib, urllib2

from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, String,\
                       ForeignKey, Boolean, Text, Date, DateTime, JSON, BLOB
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import Integer as INTEGER # 名稱衝突，改取別名
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

from DateTime import DateTime as DATETIME # 名稱衝突，改取別名


logger = logging.getLogger('morear.content')
LIMIT=20
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
# create_engine 內的字串，之後要改到 registry 讀取
ENGINE = create_engine('mysql+mysqldb://morear:morear@localhost/morear?charset=utf8', echo=True)


class MemberLoginMenu(BrowserView):

    template = ViewPageTemplateFile("template/member_login_menu.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class MemberLogin(BrowserView):

#    template = ViewPageTemplateFile("template/member_login.pt")
#測試用 reCAPTCHA key pair
# site key: 6LdUty0UAAAAAK6vEfDiBKeVRQskYebwOyGvO3oI
# secret key: 6LdUty0UAAAAAMSKideRk_b6LYpwH0CRVnJnrXqc


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = urllib.urlencode({
            'secret': '6LdUty0UAAAAAMSKideRk_b6LYpwH0CRVnJnrXqc',
            'response': request.form.get('g-recaptcha-response'),
        })
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        recaptResult = response.read()

        if json.loads(recaptResult).get('success'):
            """ TODO: 檢查密碼 """
            userId = request.form.get('member_id')
            userPwd = request.form.get('member_pwd')

        else:
            return '驗證失敗'
        request.response.redirect(portal.absolute_url())

#        import pdb; pdb.set_trace()

        return


class MemberLogout(BrowserView):

#    template = ViewPageTemplateFile("template/member_logout.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class Member03(BrowserView):

    template = ViewPageTemplateFile("template/member_03.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class Member04(BrowserView):

    template = ViewPageTemplateFile("template/member_04.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()

