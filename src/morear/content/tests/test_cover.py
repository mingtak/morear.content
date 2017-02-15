# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from morear.content.interfaces import ICover
from morear.content.testing import MOREAR_CONTENT_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class CoverIntegrationTest(unittest.TestCase):

    layer = MOREAR_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Cover')
        schema = fti.lookupSchema()
        self.assertEqual(ICover, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Cover')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Cover')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ICover.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Cover',
            id='Cover',
        )
        self.assertTrue(ICover.providedBy(obj))
