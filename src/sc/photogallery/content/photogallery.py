# -*- coding: utf-8 -*-
from five import grok
from plone.dexterity.content import Container
from sc.photogallery.interfaces import IPhotoGallery


class PhotoGallery(Container):

    """A Photo Gallery content type with a slideshow view."""

    grok.implements(IPhotoGallery)
