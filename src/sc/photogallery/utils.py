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


def last_modified(context):
    """Return the date of the most recently modified object in a container."""
    # we don't care with recursion
    objects = context.objectValues()
    # take all modification dates in seconds since epoch
    modified = [int(obj.modified().strftime('%s')) for obj in objects]
    # XXX: do we really need to take care of the container itself?
    modified.append(int(context.modified().strftime('%s')))
    modified.sort()
    # return the most recent date
    return modified[-1]


def human_readable_size(size):
    """Return a number in human readable format."""
    if size < 0:
        raise ValueError

    if size < 1024:
        return str(size)
    else:
        for unit in ['kB', 'MB', 'GB']:
            size /= 1024.0
            if abs(size) < 1024.0:
                return '{size:3.1f} {unit}'.format(size=size, unit=unit)
        return '{size:.1f} GB'.format(size=size)
