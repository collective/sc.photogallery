# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from sc.photogallery.interfaces import IPhotoGallery
from zope.interface import implements

# BBB: for content created with version 1.0a1
import sys
sys.modules['sc.photogallery.content.photogallery'] = sys.modules[__name__]


class PhotoGallery(Container):

    """A Photo Gallery content type with a slideshow view."""

    implements(IPhotoGallery)
