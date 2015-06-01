# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize import view


class View(DefaultView):

    """Slideshow view for Photo Gallery content type."""

    @view.memoize
    def results(self):
        return self.context.listFolderContents()

    @property
    @view.memoize
    def is_empty(self):
        return len(self.results()) == 0

    def image(self, obj, scale='large'):
        """Return an image scale if the item has an image field.

        :param obj: [required]
        :type obj: content type object
        :param scale: the scale to be used
        :type scale: string
        """
        scales = obj.restrictedTraverse('@@images')
        return scales.scale('image', scale)

    def description(self, obj):
        """Return the description itens of the tile.

        :param obj: [required]
        :type obj: content type object
        """
        slide_num = self.results().index(obj) + 1
        slide_count = len(self.results())
        return {
            'slide_num': slide_num,
            'slide_count': slide_count,
            'description': obj.Description() or obj.Title()
        }

    def localized_time(self, obj, long_format=False):
        """Return the object time in a user-friendly way.

        :param item: [required]
        :type item: content type object
        :param long_format: show long date format if True
        :type scale: string
        """
        return api.portal.get_localized_time(obj.Date(), long_format)
