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
from ..event.member_event import OperatorDB


logger = logging.getLogger('morear.content')
LIMIT=20
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
# create_engine 內的字串，之後要改到 registry 讀取
ENGINE = create_engine('mysql+mysqldb://morear:morear@localhost/morear?charset=utf8', echo=True)


class Member_Contact_Mana(BrowserView):

    template = ViewPageTemplateFile("template/member_contact_mana.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        userId = api.user.get_current().getId()
        conn = ENGINE.connect()
        execStr = "select commonStore, commonReceive from member where userId = '%s'" % userId # commonReceive, fail, not use.
        execScript = conn.execute(execStr)
        execResult = execScript.fetchall()

        # 轉置矩陣
        commonStore, commonReceive = map(tuple, zip(*execResult))
        self.storeBrain = None
        if commonStore[0]:
            self.storeBrain = api.content.find(context=portal, UID=json.loads(commonStore[0]))

        execStr = "select name, city, addr, phone from receiveInfo where userId = '%s'" % userId # commonReceive, fail, not use.
        execScript = conn.execute(execStr)
        self.receiveList = execScript.fetchall()

        conn.close()
        return self.template()


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
            userId = request.form.get('member_id')
            userPwd = request.form.get('member_pwd')
            conn = ENGINE.connect()
            execStr = "select password from member where userId = '%s'" % userId
            query = conn.execute(execStr)
            result = query.fetchall()

            # 登入失敗:f, 成功:s
            if not result:
                request.response.redirect('%s/members/@@member_login_menu?r=f' % portal.absolute_url())
                return

            pwd = result[0][0]
            if userPwd == pwd:
                # 登入成功
                self.context.acl_users.session._setupSession(userId.encode("utf-8"), self.context.REQUEST.RESPONSE)
                request.response.redirect(portal.absolute_url())
                userObject = api.user.get(userid=userId)
                notify(UserLoggedInEvent(userObject))
            else:
                request.response.redirect('%s/members/@@member_login_menu?r=f' % portal.absolute_url())
            conn.close()
            return
        else:
            request.response.redirect('%s/members/@@member_login_menu?r=f' % portal.absolute_url())
            return

        return


class Member_Logout(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        # 清除cookie使登出
        request.response.setCookie('__ac', '')
        request.response.redirect(portal.absolute_url())
        return


class Member_Registry(BrowserView):

    template = ViewPageTemplateFile("template/member_registry.pt")

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


class Member_Update(Member_Registry):

    template = ViewPageTemplateFile("template/member_update.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        self.user = api.user.get_current()
        self.userId = self.user.getId()

        conn = ENGINE.connect() # DB連線

        if not request.form or request.form.has_key('u'): # 條件未上
            sqlStr = "select tel, address from `member` where userId = '%s'" % self.userId
            execResult = conn.execute(sqlStr)
            self.userInfo = execResult.fetchall()[0]
#            import pdb; pdb.set_trace()
            return self.template()
        else:
            fullname = request.form.get('fullname')
            tel = request.form.get('telNo')
            address = request.form.get('address')
            sqlStr = "update member set fullname = '%s', tel = '%s', address = '%s' where userId = '%s'" % (fullname, tel, address, self.userId)
            conn.execute(sqlStr)
            conn.close()
            self.user.setProperties({'fullname': fullname})
            request.response.redirect('%s/members/@@member_update?u' % portal.absolute_url())
            return

        conn.close()


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

