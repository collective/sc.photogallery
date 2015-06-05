# -*- coding: utf-8 -*-
from plone import api
from sc.photogallery.config import JS_RESOURCES


class PhotoGalleryMixin:

    """Common methods and functions used by views and and tiles."""

    def js_resources(self):
        """Return a list of JS resources that are not available in the
        registry, but need to be loaded anyway. This way the slideshow
        could use resources registered locally or globally.

        :returns: list of ids
        :rtype: list
        """
        js_registry = api.portal.get_tool('portal_javascripts')
        global_resources = js_registry.getResourceIds()
        return [r for r in JS_RESOURCES if r not in global_resources]
