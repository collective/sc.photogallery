# -*- coding: utf-8 -*-
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.tests.test_image import zptlogo
from sc.photogallery.interfaces import IPhotoGallery
from sc.photogallery.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import unittest


class PhotoGalleryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'test')

        self.gallery = api.content.create(self.folder, 'Photo Gallery', 'gallery')

    def test_adding(self):
        self.assertTrue(IPhotoGallery.providedBy(self.gallery))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        schema = fti.lookupSchema()
        self.assertEqual(IPhotoGallery, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPhotoGallery.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.gallery))

    def test_allowed_content_types(self):
        allowed_types = [t.getId() for t in self.gallery.allowedContentTypes()]
        expected = ['Image']
        self.assertListEqual(allowed_types, expected)

    def test_selectable_as_folder_default_page(self):
        self.folder.setDefaultPage('gallery')
        self.assertEqual(self.folder.getDefaultPage(), 'gallery')

    def test_no_image(self):
        self.assertIsNone(self.gallery.image())
        self.assertIsNone(self.gallery.tag())

    def test_image_caption(self):
        self.assertEqual(self.gallery.image_caption(), u'')
        api.content.create(
            self.gallery, 'Image', 'foo', description=u'Foo')
        self.assertEqual(self.gallery.image_caption(), u'Foo')

    def test_image(self):
        from sc.photogallery.tests.api_hacks import set_image_field
        image = api.content.create(self.gallery, 'Image', 'foo')
        set_image_field(image, zptlogo, 'image/gif')
        try:
            data = self.gallery.image().image.data  # Dexterity
        except AttributeError:
            data = self.gallery.image().data  # Archetypes
        self.assertEqual(data, zptlogo)
        self.assertIn(u'height="16" width="16"', self.gallery.tag())
