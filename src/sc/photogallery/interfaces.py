# -*- coding: utf-8 -*-
from sc.photogallery import _
from plone.app.textfield import RichText
from plone.directives import form
from zope.interface import Interface


class IBrowserLayer(Interface):

    """Add-on layer marker interface."""


class IPhotoGallery(form.Schema):

    """A Photo Gallery content type with a slideshow view."""

    text = RichText(
        title=_(u'Body text'),
        required=False,
    )
