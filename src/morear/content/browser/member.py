# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone.utils import safe_unicode
import logging
import transaction
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.PlonePAS.events import UserLoggedInEvent, UserInitialLoginInEvent
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


class Member_Reg_Accept_Form(BrowserView):

    template = ViewPageTemplateFile("template/member_reg_accept_form.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if not api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        return self.template()


class Member_LoginMenu(BrowserView):

    template = ViewPageTemplateFile("template/member_login_menu.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if not api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        return self.template()


class Member_Login(BrowserView):

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


class Member_Logout(BrowserView):

#    template = ViewPageTemplateFile("template/member_logout.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class Member_Registry(BrowserView):

    template = ViewPageTemplateFile("template/member_registry.pt")

    def getDB(self): #移到event.py，這裏應用用不到了
        self.metadata = MetaData(ENGINE)
        self.member = Table(
            'member', self.metadata,
            Column('id', INTEGER, primary_key=True, autoincrement=True),
            Column('userId', String(20), unique=True),
            Column('userName', String(50)),
            Column('password', String(50)), # 明碼，以後考慮改 hash256
            Column('birthday', Date),
            Column('tel', String(10)),
            Column('address', Text),
            Column('commonStore', Text), # 5組，存店的uid [uid, uid....]
            Column('commonReceive', Text), # 10組，存 收件人/地址/電話 [(name, addr, tel).....]
            Column('registry_time', DateTime), # 註冊時間
            Column('last_time', DateTime), # 最後修改時間
            mysql_engine='InnoDB',
            mysql_charset='utf8',
            use_unicode=True,
        )
        self.metadata.create_all()


    def registryAccount(self, request):
        userId = request.form.get('userid')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        agreePromote = request.form.get('agree_promote', False)
        birthday = request.form.get('bday')
        telNo = request.form.get('telNo')
        address = request.form.get('address')

        if not (userId and username and password and email):
            return False

        if api.user.get(userid=userId): # 若 not None, 表示已存在
            return False

        user = api.user.create(email=email, username=userId, roles=('Member',), properties={'fullname':username,})

#        import pdb; pdb.set_trace() ## 還沒寫進sql
        return user
#        self.getDB() #移到event.py，這裏應用用不到了


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if not api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        if request.form:
            user = self.registryAccount(request)
            if user:
                context.acl_users.session._setupSession(user.id, context.REQUEST.RESPONSE)
                request.response.redirect(portal.absolute_url())
                # notify event hander
                notify(UserLoggedInEvent(user))

            request.response.redirect(portal.absolute_url())

        return self.template()


class Member_Exist(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        userId = request.form.get('u', None)
        if not userId:
            return None
        if api.user.get(userid=userId):
            return 'true'
        else:
            return 'false'



class Member_03(BrowserView):

    template = ViewPageTemplateFile("template/member_03.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class Member_04(BrowserView):

    template = ViewPageTemplateFile("template/member_04.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()

