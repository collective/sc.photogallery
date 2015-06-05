# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize.instance import memoizedproperty
from sc.photogallery.utils import PhotoGalleryMixin


class View(DefaultView, PhotoGalleryMixin):

    """Slideshow view for Photo Gallery content type."""

    @memoizedproperty
    def results(self):
        return self.context.listFolderContents()

    @memoizedproperty
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
