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
import string

from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, String,\
                       ForeignKey, Boolean, Text, Date, DateTime, JSON, BLOB
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import Integer as INTEGER # 名稱衝突，改取別名
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

from DateTime import DateTime as DATETIME # 名稱衝突，改取別名
from ..event.member_event import OperatorDB
from morear.content import DBSTR, RECAPTCHA_SECRET, RECAPTCHA_URL


logger = logging.getLogger('morear.content')
LIMIT=20
BASEMODEL = declarative_base()
ENGINE = create_engine(DBSTR, echo=True)


class Member_Forget_Pwd(BrowserView):

    template = ViewPageTemplateFile("template/member_forget_pwd.pt")

    def modifyPwd(self, hash):
        context = self.context
        request = self.request
        portal = api.portal.get()

        conn = ENGINE.connect()
        execStr = "SELECT userId FROM forgetpwd WHERE hash = '%s'" % hash
        execResult = conn.execute(execStr)
        result = execResult.fetchall()

        execStr = "DELETE FROM forgetpwd WHERE hash = '%s'" % hash
        conn.execute(execStr)

        conn.close()
        userId = result[0][0]
        context.acl_users.session._setupSession(userId.encode("utf-8"), request.response)
        request.response.redirect('%s/members/@@member_modify_pwd' % portal.absolute_url())
        return

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        hash = request.form.get('hash', None)
        if hash:
            try:
                self.modifyPwd(hash)
            except:
                request.response.redirect(portal.absolute_url())
            return

        gRespon = request.form.get('g-recaptcha-response', None)
        if gRespon is None:
            return self.template()

        email = request.form.get('email')
        if not email:
            return request.response.redirect(portal.absolute_url())

        url = RECAPTCHA_URL
        data = urllib.urlencode({
            'secret': RECAPTCHA_SECRET,
            'response': request.form.get('g-recaptcha-response'),
        })
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        recaptResult = response.read()

        if not json.loads(recaptResult).get('success'):
            return 'false'

        conn = ENGINE.connect()
        users = api.user.get_users()
        for user in users:
            userId = user.getProperty('id')
            if userId.startswith('gg') or userId.startswith('fb'):
                continue
            if email == user.getProperty('email'):
                hash = ''.join(random.choice(string.uppercase + string.lowercase + string.digits) for _ in range(60))
                requestTime = DATETIME().strftime('%Y/%m/%d %H:%M:%S')
                url = '%s/members/@@member_forget_pwd?hash=%s' % (portal.absolute_url(), hash)
                execStr = "INSERT INTO forgetpwd(userId, hash, request_time) VALUES ('%s','%s','%s')" % (userId, hash, requestTime)
                conn.execute(execStr)
                api.portal.send_email(
                    recipient=email,
                    sender="me@morear.tw",
                    subject="%s 您好，Morear 系統通知:變更密碼設定" % userId,
                    body='%s 您好，剛才由系統發出忘記並重新設定密碼請求，如非您本人提出，請忽略本信件並刪除，若要重新設定密碼，請點擊以下連結: %s' % \
                          (userId, url),
                )

        conn.close()
        return 'true'


class Member_Modify_Pwd(BrowserView):

    template = ViewPageTemplateFile("template/member_modify_pwd.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect(portal.absolute_url())
            return

        if not request.form.get('g-recaptcha-response', False):
            return self.template()

        url = RECAPTCHA_URL
        data = urllib.urlencode({
            'secret': RECAPTCHA_SECRET,
            'response': request.form.get('g-recaptcha-response'),
        })
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        recaptResult = response.read()

        if json.loads(recaptResult).get('success'):
            password = request.form.get('password')
            user = api.user.get_current()
            userId = user.getId()
            nowStr = DATETIME().strftime('%Y/%m/%d %H:%M:%S')

            conn = ENGINE.connect()
            execStr = "UPDATE member SET `password` = '%s', `last_update` = '%s' WHERE userId = '%s'" % (password, nowStr, userId)
            conn.execute(execStr)

            user.setSecurityProfile(password=password)

        return self.template()


class Member_Order_List(BrowserView):

    template = ViewPageTemplateFile("template/member_order_list.pt")

    def getOrder(self, orderNumber):
        conn = ENGINE.connect()
        execStr = "SELECT orderId, p_UID, qty, unitPrice, parameterNo, sNumber FROM orderItem WHERE orderId = '%s'" % orderNumber
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()
        conn.close()
        return execResult


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        if api.user.is_anonymous():
            request.response.redirect('%s/members/@@member_login_menu' % portal.absolute_url())
            return

        userId = api.user.get_current().getId()
        conn = ENGINE.connect()
        execStr = "SELECT orderInfo.orderId, orderInfo.createDate, orderItem.p_UID, orderItem.qty, orderItem.unitPrice\
                   FROM orderInfo, orderItem\
                   WHERE orderInfo.orderId = orderItem.orderId\
                   AND userId = '%s'\
                   ORDER BY orderInfo.createDate DESC" % userId
        execSql = conn.execute(execStr)
        execResult = execSql.fetchall()
        conn.close()

        self.orders = []
        self.items = {}
        self.orderInfo = {}
        for item in execResult:
            if item[0] not in self.orders:
                self.orders.append(item[0])
            if not self.items.has_key(item[0]):
                self.items[item[0]] = []
                self.orderInfo[item[0]]= {'itemNames': '', 'total': 0}
            itemTitle = api.content.find(context=portal, UID=item[2])[0].Title
            self.items[item[0]].append({'date': item[1],
                                        'p_uid': item[2],
                                        'itemTitle': itemTitle,
                                        'qty': item[3],
                                        'unitPrice': item[4],
                                        'subTotal': item[3] * item[4],
                                       })

            self.orderInfo[item[0]]['itemNames'] += ' %s /' % itemTitle
            self.orderInfo[item[0]]['total'] += item[3] * item[4]

        logger.info(self.orders)
        logger.info(self.items)
        logger.info(self.orderInfo)
        return self.template()


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

        execStr = "select name, city, addr, phone, email from receiveInfo where userId = '%s'" % userId # commonReceive, fail, not use.
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

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        url = RECAPTCHA_URL
        data = urllib.urlencode({
            'secret': RECAPTCHA_SECRET,
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
                request.response.redirect('%s?auth' % portal.absolute_url())
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
        city = request.form.get('city')
        address = request.form.get('address')

        if not (userId and username and password and email):
            return False

        if api.user.get(userid=userId): # 若 not None, 表示已存在
            return False

        user = api.user.create(email=email, username=userId, roles=('Member',), properties={'fullname':username,})
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
        self.userEmail = self.user.getProperty('email')

        conn = ENGINE.connect() # DB連線

        if not request.form or request.form.has_key('u'):
            sqlStr = "select tel, city, address from `member` where userId = '%s'" % self.userId
            execResult = conn.execute(sqlStr)
            self.userInfo = execResult.fetchall()[0]
            return self.template()
        else:
            fullname = request.form.get('fullname')
            tel = request.form.get('telNo')
            city = request.form.get('city')
            address = request.form.get('address')
            sqlStr = "update member set fullname = '%s', tel = '%s', city = '%s', address = '%s' where userId = '%s'" %\
                     (fullname, tel, city, address, self.userId)
            conn.execute(sqlStr)
            conn.close()

            # email
            email = request.form.get('email_info')
            self.user.setProperties({'fullname': fullname, 'email': email})

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

        return self.template()


class Member_04(BrowserView):

    template = ViewPageTemplateFile("template/member_04.pt")

    def __call__(self):
        context = self.context
        request = self.request

        return self.template()

