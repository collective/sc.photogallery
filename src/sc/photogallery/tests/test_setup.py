# -*- coding: utf-8 -*-
from sc.photogallery.config import PROJECTNAME
from sc.photogallery.interfaces import IBrowserLayer
from sc.photogallery.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest

CSS = '++resource++sc.photogallery/photogallery.css'


class BaseTestCase(unittest.TestCase):

    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'sc.photogallery:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']
        self.sprops = self.portal['portal_properties'].site_properties


class TestInstall(BaseTestCase):

    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    def test_default_page_types(self):
        self.assertIn('Photo Gallery', self.sprops.default_page_types)

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile), (u'1000',))


class TestUninstall(BaseTestCase):

    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed_uninstalled(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)

    def test_default_page_types_removed(self):
        self.assertNotIn('Photo Gallery', self.sprops.default_page_types)


class TestUpgrade(BaseTestCase):

    """Ensure product upgrades work."""

    @unittest.expectedFailure  # XXX: upgrade step is not registered yet
    def test_to1010_available(self):
        upgrades = listUpgradeSteps(self.st, self.profile, '1000')
        self.assertEqual(len(upgrades), 1)
