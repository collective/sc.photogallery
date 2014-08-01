# -*- coding: utf-8 -*-
from five import grok
from plone import api
from plone.memoize import view
from sc.photogallery.interfaces import IPhotoGallery

grok.templatedir('templates')


class View(grok.View):

    """Slideshow view for Photo Gallery content type."""

    grok.context(IPhotoGallery)

    @view.memoize
    def results(self):
        return self.context.listFolderContents()

    @property
    @view.memoize
    def is_empty(self):
        return len(self.results()) == 0

    def image(self, obj, scale='preview'):
        """Return an image scale if the item has an image field.

        :param item: [required]
        :type item: content type object
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
