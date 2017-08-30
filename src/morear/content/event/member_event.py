# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode

from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, String,\
                       ForeignKey, Boolean, Text, Date, DateTime, JSON, BLOB
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import Integer as INTEGER # 名稱衝突，改取別名
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

from Products.CMFPlone.utils import safe_unicode
from DateTime import DateTime as DATETIME # 名稱衝突，改取別名
import json
import random
import logging
from plone import api
import transaction

logger = logging.getLogger('morear.content')
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
# create_engine 內的字串，之後要改到 registry 讀取
ENGINE = create_engine('mysql+mysqldb://morear:morear@localhost/morear?charset=utf8', echo=True)


class OperatorDB:
    def memberDataToDB(self, conn, userData):
        """  Member Data 直接寫入資料庫  """
        ins = self.member.insert()
    #    import pdb; pdb.set_trace()
        ins = ins.values(
            registry_time=DATETIME().strftime('%Y/%m/%d %H:%M:%S'),
            last_update=DATETIME().strftime('%Y/%m/%d %H:%M:%S'),
            userId=userData.get('userid'),
            fullname=userData.get('username'),
            password=userData.get('password'),
            birthday=userData.get('bday'),
            tel=userData.get('telNo'),
            address=userData.get('address'),
            agree_promote=userData.get('agree_promote'),
        )

        try:
            execSql = conn.execute(ins)
            insertedId = int(execSql.lastrowid)
            logger.info('insert：%s' % insertedId)
        except:
            import pdb; pdb.set_trace()
            logger.error('Has a Wrong!!!')

        return


    def getDB(self):
        self.metadata = MetaData(ENGINE)
        self.member = Table(
            'member', self.metadata,
            Column('id', INTEGER, primary_key=True, autoincrement=True),
            Column('userId', String(20), unique=True),
            Column('fullname', String(50)),
            Column('password', String(50)), # 明碼，以後考慮改 hash256
            Column('birthday', Date),
            Column('tel', String(10)),
            Column('address', Text),
            Column('agree_promote', Boolean), # 行銷同意確認
            Column('commonStore', Text), # 5組，存店的uid [uid, uid....]
            Column('commonReceive', Text), # 10組，存 收件人/地址/電話 [(name, addr, tel).....]
            Column('registry_time', DateTime), # 註冊時間
            Column('last_update', DateTime), # 最後修改時間
            mysql_engine='InnoDB',
            mysql_charset='utf8',
            use_unicode=True,
        )
        self.metadata.create_all()


def userCreated(event):
    user = event.principal
    portal = api.portal.get()
    userData = portal.REQUEST.form

    operatorDB = OperatorDB()

    operatorDB.getDB()
    conn = ENGINE.connect() # DB連線

    operatorDB.memberDataToDB(conn, userData)

    conn.close()
#    import pdb; pdb.set_trace()


