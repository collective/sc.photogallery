# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from sc.photogallery.config import HAS_ZIPEXPORT
from sc.photogallery.interfaces import IPhotoGallerySettings
from sc.photogallery.testing import HAS_DEXTERITY
from sc.photogallery.testing import IMAGES
from sc.photogallery.testing import INTEGRATION_TESTING
from sc.photogallery.tests.api_hacks import set_image_field

import unittest


def load_file(name, size=0):
    """Load file from testing directory"""
    path = '/tmp/{0}'.format(name)
    with open(path, 'rb') as f:
        data = f.read()
    return data


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.gallery = api.content.create(
                container=self.portal,
                type='Photo Gallery',
                title='My Photo Gallery',
            )

        for i, name in enumerate(IMAGES):
            obj = api.content.create(
                container=self.gallery,
                type='Image',
                title='My Image {0}'.format(i + 1),
            )
            set_image_field(obj, load_file(name), 'image/jpeg')
            setattr(self, 'image_{0}'.format(i + 1), obj)

        self.view = api.content.get_view('view', self.gallery, self.request)

    def _enable_download(self):
        record = IPhotoGallerySettings.__identifier__ + '.enable_download'
        api.portal.set_registry_record(record, True)

    def test_render_js_resources(self):
        from sc.photogallery.config import JS_RESOURCES
        rendered = self.view()
        for js in JS_RESOURCES:
            self.assertIn(js, rendered)

    def test_can_download(self):
        self.assertFalse(self.view.can_download)
        self._enable_download()
        self.assertTrue(self.view.can_download)
        self.gallery.allow_download = False
        self.assertFalse(self.view.can_download)

    def test_img_size(self):
        self.assertEqual(self.view.img_size(self.image_1), '28.0 kB')
        self.assertEqual(self.view.img_size(self.image_2), '79.3 kB')
        self.assertEqual(self.view.img_size(self.image_3), '79.2 kB')
        self.assertEqual(self.view.img_size(self.image_4), '134.5 kB')
        self.assertEqual(self.view.img_size(self.image_5), '88.0 kB')

    def test_can_zipexport(self):
        self.assertFalse(self.view.can_zipexport)
        self._enable_download()
        self.assertTrue(self.view.can_zipexport)
        self.gallery.allow_download = False
        self.assertFalse(self.view.can_zipexport)

    def test_last_modified(self):
        now = int(DateTime().strftime('%s'))
        for i in range(1, 6):
            image = getattr(self, 'image_{0}'.format(i))
            int_future_date = now + (60 * i)  # Some minutes after now
            image.modification_date = DateTime(int_future_date)
            self.assertEqual(self.view.last_modified, int_future_date)

    def test_zip_url(self):
        url = 'http://nohost/plone/my-photo-gallery/@@zip/{0}/my-photo-gallery.zip'
        self.assertEqual(
            self.view.zip_url(),
            url.format(self.view.last_modified),
        )

    # FIXME: https://github.com/collective/sc.photogallery/issues/37
    @unittest.skipUnless(
        HAS_ZIPEXPORT and not HAS_DEXTERITY, 'requires ftw.zipexport')
    def test_zip_size(self):
        self.assertEqual(self.view._zip_size(), '409.5 kB')


class ZipViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.gallery = api.content.create(
                container=self.portal,
                type='Photo Gallery',
                title='My Photo Gallery',
            )

        for i, name in enumerate(IMAGES):
            obj = api.content.create(
                container=self.gallery,
                type='Image',
                title='My Image {0}'.format(i + 1),
            )
            set_image_field(obj, load_file(name), 'image/jpeg')
            setattr(self, 'image_{0}'.format(i + 1), obj)

        self.view = api.content.get_view('zip', self.gallery, self.request)

    def test_traverse_subpath(self):
        self.assertEqual(self.view.traverse_subpath, [])
        self.view.publishTraverse(self.request, 'test')
        self.assertEqual(self.view.traverse_subpath, ['test'])

    def test_last_modified(self):
        now = int(DateTime().strftime('%s'))
        for i in range(1, 6):
            image = getattr(self, 'image_{0}'.format(i))
            int_future_date = now + (60 * i)  # Some minutes after now
            image.modification_date = DateTime(int_future_date)
            self.assertEqual(self.view.last_modified, int_future_date)

    def test_filename(self):
        filename = 'http://nohost/plone/my-photo-gallery/@@zip/{0}/my-photo-gallery.zip'
        self.assertEqual(
            self.view.filename,
            filename.format(self.view.last_modified),
        )

    # FIXME: https://github.com/collective/sc.photogallery/issues/37
    @unittest.skipUnless(
        HAS_ZIPEXPORT and not HAS_DEXTERITY, 'requires ftw.zipexport')
    def test_zip_selected(self):
        self.view.zip_selected([self.gallery])
        response = self.request.response
        disposition = (
            'inline; filename="http://nohost/plone/'
            'my-photo-gallery/@@zip/{0}/my-photo-gallery.zip"'
        )
        self.assertEqual(
            response.getHeader('Content-Disposition'),
            disposition.format(self.view.last_modified),
        )
        self.assertEqual(response.getHeader('Content-type'), 'application/zip')
        self.assertEqual(response.getHeader('Content-Length'), '419321')

        self.view.zip_selected([self.gallery, self.gallery])
        self.assertEqual(response.getHeader('Content-Length'), '838660')
