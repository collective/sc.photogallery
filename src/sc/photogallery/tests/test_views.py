# -*- coding: utf-8 -*-
from plone import api
from sc.photogallery.interfaces import IPhotoGallery
from sc.photogallery.testing import INTEGRATION_TESTING
from zope.interface import alsoProvides

import unittest


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IPhotoGallery)

        with api.env.adopt_roles(['Manager']):
            self.gallery = api.content.create(
                self.portal, 'Photo Gallery', 'gallery')

    def test_render_js_resources(self):
        from sc.photogallery.config import JS_RESOURCES
        view = api.content.get_view('view', self.gallery, self.request)
        rendered = view()
        for js in JS_RESOURCES:
            self.assertIn(js, rendered)
