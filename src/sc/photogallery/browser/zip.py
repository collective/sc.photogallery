# -*- coding: utf-8 -*-
from plone import api
from sc.photogallery import _
from sc.photogallery.config import HAS_ZIPEXPORT
from sc.photogallery.utils import last_modified
from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserPage
from ZPublisher.Iterators import filestream_iterator

import os


if HAS_ZIPEXPORT:
    from ftw.zipexport.generation import ZipGenerator
    from ftw.zipexport.interfaces import IZipRepresentation


class ZipView(BrowserPage):

    """Export PhotoGallery as zip package."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._path = []

    @property
    def traverse_subpath(self):
        return self._path

    def publishTraverse(self, request, name):
        self._path.append(name)
        return self

    def _subpath(self):
        return getattr(self, 'traverse_subpath', [])

    @property
    def last_modified(self):
        return last_modified(self.context)

    @property
    def filename(self):
        base_url = self.context.absolute_url()
        subpath = self._subpath()
        last_modified = self.last_modified
        if not ((len(subpath) > 1) and (str(last_modified) == subpath[0])):
            url = '{0}/@@zip/{1}/{2}.zip'.format(
                base_url, str(last_modified), self.context.getId())
            return self.request.response.redirect(url)
        filename = subpath[1].encode('utf-8')
        return filename

    def zip_selected(self, objects):
        if not HAS_ZIPEXPORT:
            return None

        response = self.request.response
        with ZipGenerator() as generator:
            for obj in objects:
                repre = getMultiAdapter(
                    (obj, self.request), interface=IZipRepresentation)
                for path, pointer in repre.get_files():
                    generator.add_file(path, pointer)

            # check if zip has files
            if generator.is_empty:
                message = _(u'Zip export is not supported on the selected content.')
                api.portal.show_message(message, self.request, type=u'error')
                self.request.response.redirect(self.context.absolute_url())
                return

            zip_file = generator.generate()
            response.setHeader(
                'Content-Disposition', 'inline; filename="{0}"'.format(self.filename))
            response.setHeader('Content-type', 'application/zip')
            response.setHeader('Content-Length', os.stat(zip_file.name).st_size)

            return filestream_iterator(zip_file.name, 'rb')

    def __call__(self):
        if HAS_ZIPEXPORT and self.filename:
            return self.zip_selected([self.context])
        else:
            message = _(u'Operation not supported.')
            api.portal.show_message(message, self.request, type=u'error')
            self.request.response.redirect(self.context.absolute_url())
            return
