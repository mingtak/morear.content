# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from morear.content.testing import MOREAR_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that morear.content is properly installed."""

    layer = MOREAR_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if morear.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'morear.content'))

    def test_browserlayer(self):
        """Test that IMorearContentLayer is registered."""
        from morear.content.interfaces import (
            IMorearContentLayer)
        from plone.browserlayer import utils
        self.assertIn(IMorearContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MOREAR_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['morear.content'])

    def test_product_uninstalled(self):
        """Test if morear.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'morear.content'))

    def test_browserlayer_removed(self):
        """Test that IMorearContentLayer is removed."""
        from morear.content.interfaces import \
            IMorearContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMorearContentLayer, utils.registered_layers())
