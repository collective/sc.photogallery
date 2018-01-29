# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize import forever
from plone.memoize.instance import memoizedproperty
from sc.photogallery.config import HAS_ZIPEXPORT
from sc.photogallery.interfaces import IPhotoGallerySettings
from sc.photogallery.utils import human_readable_size
from sc.photogallery.utils import last_modified
from sc.photogallery.utils import PhotoGalleryMixin
from zope.component import getMultiAdapter

import os


if HAS_ZIPEXPORT:
    from ftw.zipexport.generation import ZipGenerator
    from ftw.zipexport.interfaces import IZipRepresentation


class View(DefaultView, PhotoGalleryMixin):
    """Slideshow view for Photo Gallery content type."""

    def id(self):
        return id(self)

    @memoizedproperty
    def results(self):
        return self.context.listFolderContents()

    @property
    def is_empty(self):
        return len(self.results) == 0

    def image(self, obj, scale='large'):
        """Return an image scale if the item has an image field.

        :param obj: [required]
        :type obj: content type object
        :param scale: the scale to be used
        :type scale: string
        """
        scales = obj.restrictedTraverse('@@images')
        return scales.scale('image', scale)

    def localized_time(self, obj, long_format=False):
        """Return the object time in a user-friendly way.

        :param item: [required]
        :type item: content type object
        :param long_format: show long date format if True
        :type scale: string
        """
        return api.portal.get_localized_time(obj.Date(), long_format)

    @property
    def can_download(self):
        """Check if original images can be explicitly downloaded, that is,
        if downloading is enabled globally and the current object allows it.
        """
        record = IPhotoGallerySettings.__identifier__ + '.enable_download'
        enabled_globally = api.portal.get_registry_record(record)
        allow_download = self.context.allow_download
        return enabled_globally and allow_download

    def img_size(self, item):
        try:
            size = item.size()  # Archetypes
        except AttributeError:
            size = item.image.size  # Dexterity
        return human_readable_size(size)

    @property
    def can_zipexport(self):
        """Check if original images can be downloaded as a ZIP file,
        that is, if ftw.zipexport is installed and downloading is
        allowed in the current object.
        """
        return HAS_ZIPEXPORT and self.can_download

    @property
    def last_modified(self):
        return last_modified(self.context)

    def zip_url(self):
        base_url = self.context.absolute_url()
        url = '{0}/@@zip/{1}/{2}.zip'.format(
            base_url, str(self.last_modified), self.context.getId())
        return url

    @forever.memoize
    def _zip_size(self, last_modified=None):
        if not HAS_ZIPEXPORT:
            return

        with ZipGenerator() as generator:
            for obj in [self.context]:
                repre = getMultiAdapter(
                    (obj, self.request), interface=IZipRepresentation)
                for path, pointer in repre.get_files():
                    generator.add_file(path, pointer)
            zip_file = generator.generate()
            size = os.stat(zip_file.name).st_size
            return human_readable_size(size)

    def zip_size(self):
        return self._zip_size(self.last_modified)
