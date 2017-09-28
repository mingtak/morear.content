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
#from ..event.member_event import OperatorDB


logger = logging.getLogger('morear.content')
LIMIT=20
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
# create_engine 內的字串，之後要改到 registry 讀取
ENGINE = create_engine('mysql+mysqldb://morear:morear@localhost/morear?charset=utf8', echo=True)


class Shopping_Client_Back_Url(BrowserView):

    template = ViewPageTemplateFile("template/shopping_client_back_url.pt")

    def __call__(self):
        self.portal = api.portal.get()
        context = self.context
        request = self.request

        self.is_anonymous = api.user.is_anonymous()
        if self.is_anonymous:
            request.response.redirect(self.portal.absolute_url())
            return

        self.userId = api.user.get_current().getId()
        self.orderId = request.form.get('orderId')
        request.response.setCookie('cart', json.dumps([]), path='/')
        return self.template()


class Shopping_Cart_Step2_Payment(BrowserView):

    template = ViewPageTemplateFile("template/shopping_cart_step2_payment.pt")

    def __call__(self):
        self.portal = api.portal.get()
        context = self.context
        request = self.request

        self.is_anonymous = api.user.is_anonymous()
        if self.is_anonymous:
            request.response.redirect(self.portal.absolute_url())
            return

        self.user = api.user.get_current()
        userId = self.user.getId()

        conn = ENGINE.connect() # DB連線

        # 取得帳號資料
        execStr = "select fullname, tel, city, address from member where userId = '%s'" % userId
#        import pdb; pdb.set_trace()
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()[0]
        self.user_info = execResult

        # 取得常用取貨門市
        execStr = "select commonStore from member where userId = '%s'" % userId
        execSql = conn.execute(execStr)
        commonStore = execSql.fetchall()[0][0]
        if commonStore is None:
            self.brain = []
        else:
            commonStore = json.loads(commonStore)
            self.brain = api.content.find(context=self.portal, Type="Location", UID=commonStore)

        execStr = "select id, name, city, addr, phone, email from receiveInfo where userId = '%s'" % userId
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()
        self.receiveList = []
        if execResult:
            self.receiveList = execResult

        conn.close()
        return self.template()


class Shopping_Cart_Step2(BrowserView):

    template = ViewPageTemplateFile("template/shopping_cart_step2.pt")

    def __call__(self):
        self.portal = api.portal.get()
        context = self.context
        request = self.request

        self.is_anonymous = api.user.is_anonymous()

        return self.template()


class Shopping_Cart(BrowserView):

    template = ViewPageTemplateFile("template/shopping_cart.pt")

    def getDB(self):
        self.metadata = MetaData(ENGINE)
        self.parameter = Table(
            'parameter', self.metadata,
            Column('id', INTEGER, primary_key=True, autoincrement=True),
            Column('date', Date),
            Column('parameter', MEDIUMTEXT), # 參數
            mysql_engine='InnoDB',
            mysql_charset='utf8',
            use_unicode=True,
        )
        self.metadata.create_all()


    def __call__(self):
        self.portal = api.portal.get()
        request = self.request
        self.getDB()
        self.conn = ENGINE.connect() # DB連線

        self.totalPrice = 0
        cookies = request.cookies
        self.cart = cookies.get('cart', None)
        if self.cart:
            self.cart = json.loads(self.cart)
            for item in self.cart:
#                import pdb;pdb.set_trace()
                self.totalPrice += int(item.values()[0].get('total', 0))
        else:
            self.cart = {}

#        import pdb; pdb.set_trace()
        self.conn.close()
        return self.template()

