# -*- coding: utf-8 -*-
from sc.photogallery.config import PROJECTNAME
from sc.photogallery.interfaces import IBrowserLayer
from sc.photogallery.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest

JS = (
    '++resource++collective.js.cycle2/jquery.cycle2.js',
    '++resource++collective.js.cycle2/jquery.cycle2.carousel.js',
    '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js',
    '++resource++sc.photogallery/photogallery.js',
)

CSS = (
    '++resource++sc.photogallery/photogallery.css',
)


class TestInstall(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_jsregistry(self):
        js_resources = self.portal['portal_javascripts'].getResourceIds()
        for id in JS:
            self.assertIn(id, js_resources)

    def test_cssregistry(self):
        css_resources = self.portal['portal_css'].getResourceIds()
        for id in CSS:
            self.assertIn(id, css_resources)

    def test_default_page_types(self):
        sprops = self.portal['portal_properties'].site_properties
        self.assertIn('Photo Gallery', sprops.default_page_types)

    def test_version(self):
        setup = self.portal['portal_setup']
        profile = 'sc.photogallery:default'
        self.assertEqual(
            setup.getLastVersionForProfile(profile), (u'1001',))


class TestUninstall(unittest.TestCase):

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

    def test_jsregistry(self):
        js_resources = self.portal['portal_javascripts'].getResourceIds()
        for id in JS:
            self.assertNotIn(id, js_resources)

    def test_cssregistry(self):
        css_resources = self.portal['portal_css'].getResourceIds()
        for id in CSS:
            self.assertNotIn(id, css_resources)

    def test_default_page_types_removed(self):
        sprops = self.portal['portal_properties'].site_properties
        self.assertNotIn('Photo Gallery', sprops.default_page_types)
