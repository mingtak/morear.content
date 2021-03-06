# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('morear.content')

# mysql參數
DBSTR = 'mysql+mysqldb://morear:morear@localhost/morear?charset=utf8'

# google recaptcha 參數
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'
RECAPTCHA_SECRET = '6LdUty0UAAAAAMSKideRk_b6LYpwH0CRVnJnrXqc'

# 耳機參數 i18n
_(u'logoColorL')
_(u'surfaceR')
_(u'laserPriceR')
_(u'upDownL')
_(u'laserTextR')
_(u'urgentCasePrice')
_(u'cusImgL')
_(u'urgentCase')
_(u'laserTextL')
_(u'upDownR')
_(u'laserPriceL')
_(u'logoColorR')
_(u'surfaceL')
_(u'lineLength')
_(u'rotateL')
_(u'logoColorPriceR')
_(u'zoomR')
_(u'leftRightL')
_(u'leftRightR')
_(u'zoomL')
_(u'logoColorPriceL')
_(u'rotateR')
_(u'linePrice')
_(u'shell3D')
_(u'productName')
_(u'surfacePrice')
_(u'discount')
_(u'outBoxText')
_(u'extSer')
_(u'shell3DPrice')
_(u'service_person')
_(u'cusImgR')
_(u'pType')
_(u'totalSum')
_(u'basePrice')
_(u'sNumber')

# 耳塞參數 i18n
_(u'ep_colorRPrice')
_(u'laserPriceR')
_(u'laserTextR')
_(u'urgentCasePrice')
_(u'pType')
_(u'urgentCase')
_(u'ep_material')
_(u'laserPriceL')
_(u'ep_materialPrice')
_(u'laserTextL')
_(u'ep_typeNoPrice')
_(u'ep_colorR')
_(u'ep_typeNo')
_(u'productName')
_(u'discount')
_(u'ep_colorPrice')
_(u'extSer')
_(u'ep_colorL')
_(u'service_person')
_(u'earplugsAmount')
_(u'totalSum')
_(u'ep_colorLPrice')
_(u'basePrice')

# 狀態
_('waiting_pay')
_('payed')
_('waiting_ear')
_('processing')
_('processed')
_('shipping')
_('shipping_finished')
_('wait_30days')
_('reprocess')
_('finished')

# 其它補充
_(u'contact_custom')
