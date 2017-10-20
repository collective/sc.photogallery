# -*- coding: utf-8 -*-
from mock import Mock
from plone import api
from sc.photogallery.testing import HAS_COVER
from sc.photogallery.testing import INTEGRATION_TESTING

import unittest


if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from sc.photogallery.tiles.photogallery import IPhotoGalleryTile
    from sc.photogallery.tiles.photogallery import PhotoGalleryTile
else:
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


class PhotoGalleryTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(PhotoGalleryTileTestCase, self).setUp()
        self.tile = PhotoGalleryTile(self.cover, self.request)
        self.tile.__name__ = u'sc.photogallery'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IPhotoGalleryTile
        self.klass = PhotoGalleryTile
        super(PhotoGalleryTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertFalse(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Photo Gallery'])

    def test_render_empty(self):
        msg = u'Drag&amp;drop a Photo Gallery here.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_render_photogallery(self):
        with api.env.adopt_roles(['Manager']):
            g1 = api.content.create(
                self.portal, 'Photo Gallery', 'g1')
        self.tile.populate_with_object(g1)
        self.assertIn(u'slideshow-player', self.tile())

    def test_render_js_resources(self):
        from sc.photogallery.config import JS_RESOURCES
        rendered = self.tile()
        for js in JS_RESOURCES:
            self.assertIn(js, rendered)
