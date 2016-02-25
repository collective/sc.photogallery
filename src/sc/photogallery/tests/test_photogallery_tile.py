# -*- coding: utf-8 -*-
from collective.cover.tests.base import TestTileMixin
from mock import Mock
from plone import api
from sc.photogallery.testing import INTEGRATION_TESTING
from sc.photogallery.tiles.photogallery import IPhotoGalleryTile
from sc.photogallery.tiles.photogallery import PhotoGalleryTile

import unittest


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


def test_suite():
    """Load tile tests only in Plone < 5.0."""
    from sc.photogallery.testing import PLONE_VERSION
    if PLONE_VERSION < '5.0':
        return unittest.defaultTestLoader.loadTestsFromName(__name__)
    else:
        return unittest.TestSuite()
