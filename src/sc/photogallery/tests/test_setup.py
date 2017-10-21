# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer.utils import registered_layers
from sc.photogallery.config import PROJECTNAME
from sc.photogallery.interfaces import IBrowserLayer
from sc.photogallery.testing import HAS_COVER
from sc.photogallery.testing import INTEGRATION_TESTING
from sc.photogallery.testing import IS_PLONE_5

import unittest


JS = '++resource++sc.photogallery/photogallery.js'
CSS = '++resource++sc.photogallery/photogallery.css'


class InstallTestCase(unittest.TestCase):
    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    def test_setup_permission(self):
        permission = 'sc.photogallery: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_default_page_types(self):
        sprops = self.portal['portal_properties'].site_properties
        self.assertIn('Photo Gallery', sprops.default_page_types)

    def test_version(self):
        setup = self.portal['portal_setup']
        profile = 'sc.photogallery:default'
        self.assertEqual(
            setup.getLastVersionForProfile(profile), (u'1001',))

    @unittest.skipUnless(HAS_COVER, 'requires plone.app.tiles')
    def test_tile(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'sc.photogallery', tiles)


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed_uninstalled(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertNotIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)

    def test_tile_removed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'sc.photogallery', tiles)

    def test_default_page_types_removed(self):
        sprops = self.portal['portal_properties'].site_properties
        self.assertNotIn('Photo Gallery', sprops.default_page_types)
