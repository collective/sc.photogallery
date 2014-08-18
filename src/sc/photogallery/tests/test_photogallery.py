# -*- coding: utf-8 -*-
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from sc.photogallery.interfaces import IPhotoGallery
from sc.photogallery.testing import INTEGRATION_TESTING
from sc.photogallery.testing import PLONE_VERSION
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

    @unittest.skipIf(PLONE_VERSION >= '5.0', 'FIXME')
    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.gallery))
        self.assertTrue(IAttributeUUID.providedBy(self.gallery))

    def test_allowed_content_types(self):
        allowed_types = [t.getId() for t in self.gallery.allowedContentTypes()]
        expected = ['Image']
        self.assertListEqual(allowed_types, expected)

    def test_selectable_as_folder_default_page(self):
        self.folder.setDefaultPage('gallery')
        self.assertEqual(self.folder.getDefaultPage(), 'gallery')
