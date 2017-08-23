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


class UpdateCart(BrowserView):

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


    def parameterToDB(self, parameter):
        """  parameter 直接寫入資料庫， return content id ==> SELECT LAST_INSERT_ID(); """


        ins = self.parameter.insert()
#        import pdb; pdb.set_trace()
        ins = ins.values(date=DATETIME().strftime('%Y/%m/%d'), parameter=json.dumps(parameter))
        try:
            execSql = self.conn.execute(ins)
            insertedId = int(execSql.lastrowid)
        except:
            pass

        return insertedId


    def addItem(self, cookies, cart, request): # 只做新增
        response = request.response

        pType = request.form.get('pType')
        if pType == 'normal':
            uid = request.form.get('uid')
        else:
            uid = request.form.get('productName')

        item = api.content.find(context = self.portal, UID = uid)[0]
        qty = 1 # 只做新增

        if pType != 'normal': # 客製品
            price = request.form['totalSum']
            total = price * qty
            parameter = request.form
            parameter = self.parameterToDB(parameter)

            cartData = {
                uid: {
                    'qty': qty,
                    'price': price,
                    'total': total,
                    'parameter': parameter,
                }
            }

            if not cart or cart == 'null':
                response.setCookie('cart', json.dumps([cartData]), expires=(DATETIME()+1).strftime('%c'))
                return '商品已加入購物車'
            else:
                cart = json.loads(cart)
                cart.append(cartData)
                response.setCookie('cart', json.dumps(cart), expires=(DATETIME()+1).strftime('%c'))
                return '商品已加入購物車'

            return '客製品已加入購物車'

        price = item.getObject().basePrice
        total = price * qty

        cartData = {
            uid: {
                'qty': qty,
                'price': price,
                'total': total,
            }
        }

        if not cart or cart == 'null':
            response.setCookie('cart', json.dumps([cartData]), expires=(DATETIME()+1).strftime('%c'))
            return '商品已加入購物車'
        else:
           cart = json.loads(cart)
           if uid in ''.join(str(cart)):
               return '商品已存在購物車'
           else:
               cart.append(cartData)
               response.setCookie('cart', json.dumps(cart), expires=(DATETIME()+1).strftime('%c'))
               return '商品已加入購物車'


    def delItem(self): #TODO
        """  """


    def updateItem(self): #TODO
        """  """


    def __call__(self):
        self.portal = api.portal.get()
        request = self.request
        self.getDB()
        self.conn = ENGINE.connect() # DB連線

        cookies = request.cookies
        cart = cookies.get('cart', None)
        action = request.form.get('action', None)

        if action == 'add':
            resultStr = self.addItem(cookies, cart, request)
        else:
            return

        self.conn.close()
        return resultStr


# 記得vm.rotateR, vm.rotateL 要*3.6
        import pdb; pdb.set_trace()

        orderInfo = {}
        orderInfo['UID'] = request.form.get('productName')
        orderInfo['qty'] = 1
        orderInfo['totalSum'] = request.form.get('totalSum', 1000000)

        payment_info = {
            'MerchantTradeNo': merchantTradeNo,
            'ItemName': itemName,
            'TradeDesc': '%s, Total: $%s' % (itemDescription, totalAmount),
            'TotalAmount': totalAmount,
            'ChoosePayment': 'ALL',
            'PaymentType': 'aio',
            'EncryptType': 1,
            'PaymentInfoURL': paymentInfoURL,
            'ClientBackURL': '%s?MerchantTradeNo=%s&LogisticsType=%s&LogisticsSubType=%s' %
                (clientBackURL, merchantTradeNo, request.form.get('LogisticsType', 'cvs'), request.form.get('LogisticsSubType', 'UNIMART')),  #可以使用 get 帶參數
            'ReturnURL': api.portal.get_registry_record('%s.returnURL' % prefixString),
            'MerchantTradeDate': DateTime().strftime('%Y/%m/%d %H:%M:%S'),
            'MerchantID': api.portal.get_registry_record('%s.merchantID' % prefixString),
        }


        response.setCookie('itemInCart', '{}')
        return 'DONE'

class SetFeatured(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        request = self.request

        if not request.form.get('uid'):
            return
        brain = api.content.find(context=portal, UID=request.form['uid'])
        try:
            item = brain[0].getObject()
        except:return

        if request.form.has_key('checked'):
            if request.form.get('checked') == 'true':
                item.featured = True
            else:
                item.featured = False
            notify(ObjectModifiedEvent(item))
            item.reindexObject()
        elif request.form.has_key('headWeight'):
            item.headWeight = int(request.form.get('headWeight', 10))
            notify(ObjectModifiedEvent(item))
            item.reindexObject()
        transaction.commit()
        return


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
        portal = api.portal.get()

        self.headphoneList = api.content.find(context=portal, Type='Product', pType='headphone')
        self.earplugs = api.content.find(context=portal, Type='Product', pType='earplugs')

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
            searchCond['SearchableText'] = keyword

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


class DeleteObj(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#        import pdb; pdb.set_trace()
        uid = request.form.get('uid')
        if not uid:
            return

        obj = api.content.find(UID=uid)[0].getObject()
        api.content.delete(obj=obj)
