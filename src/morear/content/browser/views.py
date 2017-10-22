# -*- coding: utf-8 -*-
from morear.content import _
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
import urllib2

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




class OrderDetailInfo(BrowserView):

    template = ViewPageTemplateFile("template/order_detail_info.pt")

    def execSql(self, execStr):
        self.conn = ENGINE.connect() # DB連線
        execResult = self.conn.execute(execStr)
        self.conn.close()
        return execResult.fetchall()

    def getParameter(self, parameterNo):
        self.paraName = {'logoColorL': 'Logo樣式(左)', 'surfaceR': '面板顏色/樣式(右)', 'laserPriceR': '刻字價格(右)',
            'upDownL': '客製面板圖案/下上(左)', 'laserTextR': '刻字(右)', 'urgentCasePrice': '急件價格', 'cusImgL': '客製面板圖案(左)',
            'urgentCase': '急件', 'laserTextL': '刻字(左)', 'upDownR': '客製面板圖案/下上(右)', 'message': 'message', 'laserPriceL': '刻字價格(左)',
            'logoColorR': 'Logo樣式(右)', 'surfaceL': '面板顏色/樣式(左)', 'lineLength': '耳機線材', 'rotateL': '客製面板圖案/旋轉角度(左)',
            'logoColorPriceR': 'Logo樣式價格(右)', 'zoomR': '客製面板圖案/縮放%(右)', 'leftRightL': '客製面板圖案/左右(左)',
            'leftRightR': '客製面板圖案/下上(右)', 'zoomL': '客製面板圖案/縮放%(左)', 'logoColorPriceL': 'Logo樣式價格(左)',
            'rotateR': '客製面板圖案/旋轉角度(右)', 'linePrice': '耳機線材價格', 'shell3D': '主體顏色', 'productName': '產品名稱',
            'surfacePrice': '面板顏色/樣式價格', 'discount': '折扣', 'outBoxText': '外箱文字(廢棄)', 'extSer': '特殊需求',
            'shell3DPrice': '主體顏色價格', 'service_person': '服務人員', 'cusImgR': '客製面板圖案(右)', 'pType': '產品類型', 'totalSum': '總價',
            'basePrice': '商品定價', 'action': '行動(廢棄)', 'sNumber': '序號',
            # 以下耳塞專用參數
            'ep_colorRPrice': '耳塞顏色價格(右)', 'ep_material': '耳塞材質', 'ep_materialPrice': '耳塞材質價格',
            'ep_typeNoPrice': '耳塞濾音器型號價格', 'ep_colorR': '耳塞顏色(右)', 'ep_typeNo': '耳塞濾音器型號',
            'ep_colorPrice': '耳塞顏色價格(合計)', 'ep_colorL': '耳塞顏色(左)', 'earplugsAmount': '耳塞數量(廢棄)',
            'ep_colorLPrice': '耳塞顏色價格',}

        execStr = "SELECT parameter\
                   FROM parameter\
                   WHERE id = %s" % parameterNo
        return self.execSql(execStr)[0]

    def getOrderItem(self, orderId):
        self.orderItemList = [_(u'p_UID'), _(u'qty'), _(u'unitPrice'), _(u'parameterNo'), _(u'sNumber')]

        execStr = "SELECT p_UID, qty, unitPrice, parameterNo, sNumber\
                   FROM orderItem WHERE orderId = '%s'" % orderId
        return self.execSql(execStr)

    def getOrderInfo(self, orderId):
        self.orderInfoList = [_(u'userId'), _(u'b_email'), _(u'orderId'), _(u'b_name'), _(u'b_city'), _(u'b_addr'), _(u'b_phone'),
            _(u'pickupType'), _(u'pickupTime'), _(u'r_name'), _(u'r_email'), _(u'r_city'), _(u'r_addr'), _(u'r_phone'),
            _(u'i_2list'), _(u'i_invoiceNo'), _(u'i_city'), _(u'i_addr'), _(u'pickupStoreUID'), _(u'ecpayNo'), _(u'createDate')]

        execStr = "SELECT userId, b_email, orderId, b_name, b_city, b_addr, b_phone,\
                          pickupType, pickupTime, r_name, r_email, r_city, r_addr, r_phone,\
                          i_2list, i_invoiceNo, i_city, i_addr, pickupStoreUID, ecpayNo, createDate\
                   FROM orderInfo WHERE orderId = '%s'" % orderId
        return self.execSql(execStr)[0]

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        execStr = "SELECT userId, orderId FROM orderInfo WHERE 1 ORDER BY createDate DESC"
        self.results = self.execSql(execStr)

        return self.template()


class OrderListingView(BrowserView):

    template = ViewPageTemplateFile("template/order_listing_view.pt")

    def getOrderItems(self, orderId):
        self.conn = ENGINE.connect() # DB連線

        execStr = "SELECT p_UID, qty FROM orderItem WHERE orderId = '%s'" % orderId
        execResult = self.conn.execute(execStr)
        self.conn.close()
        return execResult.fetchall()

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        self.conn = ENGINE.connect() # DB連線

        execStr = "SELECT userId, orderId FROM orderInfo WHERE 1 ORDER BY createDate DESC"
        execResult = self.conn.execute(execStr)
        self.results = execResult.fetchall()
        self.conn.close()

        return self.template()


class GetPartner(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#        import pdb; pdb.set_trace()
        if request.form.has_key('city'):
#            import pdb; pdb.set_trace()
            return urllib2.urlopen('http://210.68.106.227/cities/available').read()

        if request.form.has_key('cityId'):
            cityId = request.form.get('cityId')
            return urllib2.urlopen('http://210.68.106.227/cities/%s/districts/available' % cityId).read()

        if request.form.has_key('districtId'):
            districtId = request.form.get('districtId')
            return urllib2.urlopen('http://210.68.106.227/stores?districtId=%s' % districtId).read()

#        import pdb; pdb.set_trace()


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

        conn = ENGINE.connect() # DB連線
        execStr = "INSERT INTO parameter (date, parameter) VALUES ('%s', '%s')" % (DATETIME().strftime('%Y/%m/%d'), json.dumps(parameter))
        conn.execute(execStr)
        # 取得寫入 id
        execStr = "SELECT LAST_INSERT_ID()"
        insertedId = conn.execute(execStr).fetchone()[0]

        conn.close()
        import pdb; pdb.set_trace()

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


class Download_View(BrowserView):

    template = ViewPageTemplateFile("template/download_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        self.items = context.getChildNodes()
        self.categories = []
#        import pdb; pdb.set_trace()
        for item in self.items:
            subject = item.subject
            if subject:
                for cat in subject:
                    if cat not in self.categories:
                        self.categories.append(cat)

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

        self.items = context.getChildNodes()
        self.categories = []
#        import pdb; pdb.set_trace()
        for item in self.items:
            subject = item.subject
            if subject:
                for cat in subject:
                    if cat not in self.categories:
                        self.categories.append(cat)

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


class ReShowOptionView(BrowserView):

    template = ViewPageTemplateFile("template/re_show_option_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        self.headphoneList = api.content.find(context=portal, Type='Product', pType='headphone')
        self.earplugs = api.content.find(context=portal, Type='Product', pType='earplugs')

        orderId = request.form.get('oid', None)
        parameterNo = request.form.get('para', None)

        if orderId is None or parameterNo is None:
            request.response.redirect(portal.absolute_url())
            return

        conn = ENGINE.connect()
        execStr = "SELECT parameter FROM parameter WHERE id = %s" % parameterNo
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()[0][0]
#        import pdb; pdb.set_trace()
        self.parameter = json.loads(execResult)

        conn.close()
        return self.template()


class NewsListingView(BrowserView):

    template = ViewPageTemplateFile("template/news_listing_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class MusicmanListingView(NewsListingView):

    template = ViewPageTemplateFile("template/musicman_listing_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        portal = api.portal.get()

        return self.template()


class LinksListingView(BrowserView):

    template = ViewPageTemplateFile("template/links_listing_view.pt")

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
        self.brain = []
#        import pdb; pdb.set_trace()
        if self.keyword.strip():
            self.brain = api.content.find(portal=portal, SearchableText=self.keyword.strip())

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


class AddCommonStore(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        operatorDB = OperatorDB()
        operatorDB.getDB()
        conn = ENGINE.connect() # DB連線

        user = api.user.get_current()
        userId = user.getId()

        # 取讀 commonStore
        sqlStr = "select commonStore from member where userId = '%s'" % userId
        execute = conn.execute(sqlStr)
        result = execute.fetchall()[0][0]
        storeUID = request.form.get('storeUID')

        if result is None:
            commonStore = json.dumps([storeUID])
            sqlStr = "update member set commonStore = '%s' where userId = '%s'" % (commonStore, userId)
        elif storeUID not in result:
            result = json.loads(result)
            result.append(storeUID)
            result = json.dumps(result)
            sqlStr = "update member set commonStore = '%s' where userId = '%s'" % (result, userId)
        conn.execute(sqlStr)

#        import pdb; pdb.set_trace()
        conn.close()


class DelCommonStore(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        uid = request.form.get('uid')
        if not uid:
            request.response.redirect(portal.absolute_url())
            return

        userId = api.user.get_current().getId()

        conn = ENGINE.connect()
        execStr = 'select commonStore from member where userId = "%s"' % userId
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()
        result = json.loads(execResult[0][0])
#        import pdb; pdb.set_trace()
        if uid in result:
            result.remove(uid)
            wInStr = json.dumps(result)
            execStr = "update member set commonStore = '%s' where userId = '%s'" % (wInStr, userId)
            conn.execute(execStr)
        conn.close()


class AddReceive(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        user = api.user.get_current()
        userId = user.getId()

        conn = ENGINE.connect() # DB連線

        name = request.form.get('name')
        city = request.form.get('city')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        email = request.form.get('email')

        execStr = "INSERT INTO receiveInfo(userId, name, city, addr, phone, email) \
                   VALUES ('%s','%s','%s','%s','%s', '%s')" % \
                   (userId, name, city, addr, phone, email)
        execSql = conn.execute(execStr)

        conn.close()


class DelReceive(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        user = api.user.get_current()
        userId = user.getId()

        conn = ENGINE.connect() # DB連線

        name = request.form.get('name')
        city = request.form.get('city')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        email = request.form.get('email')

#        import pdb;pdb.set_trace()
        execStr = "DELETE FROM receiveInfo WHERE userId = '%s' and name = '%s' and city = '%s' and addr = '%s' and phone = '%s' and email = '%s'" % \
                  (userId, name, city, addr, phone, email)
        execSql = conn.execute(execStr)


class Site_Map(BrowserView):

    template = ViewPageTemplateFile("template/site_map.pt")

    def __call__(self):
        return self.template()
