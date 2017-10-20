# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from sc.photogallery.interfaces import IPhotoGallery
from zope.interface import implementer

# BBB: for content created with version 1.0a1
import sys
sys.modules['sc.photogallery.content.photogallery'] = sys.modules[__name__]  # noqa: I003


@implementer(IPhotoGallery)
class PhotoGallery(Container):

    """A Photo Gallery content type with a slideshow view."""

    # FIXME: @property
    def image(self):
        """Return the first image on a Photo Gallery."""
        # photo gallery contain only images; we don't need to filter the list
        images = self.listFolderContents()
        return images[0] if len(images) > 0 else None

    # FIXME: @property
    def image_caption(self):
        """Return the description of the first image in a Photo Gallery."""
        try:
            return self.image().Description()
        except AttributeError:
            return u''

    # XXX: compatibility with folder_summary_view in folders
    image_thumb = image

    # XXX: this probably should not be necessary if we can define the
    #      image method of the class as a property
    def tag(self, **kwargs):
        """Return a tag for the first image in a Photo Gallery."""
        try:
            scales = self.image().restrictedTraverse('@@images')
            return scales.tag('image', **kwargs)
        except AttributeError:
            return None
