# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.directives import form
from sc.photogallery import _
from zope import schema
from zope.interface import Interface


class IBrowserLayer(Interface):

    """Add-on layer marker interface."""


class IPhotoGallery(form.Schema):

    """A Photo Gallery content type with a slideshow view."""

    text = RichText(
        title=_(u'Body text'),
        required=False,
    )


class IPhotoGallerySettings(form.Schema):

    """Schema for the control panel form."""

    download = schema.Bool(
        title=_(u'Enable download?'),
        description=_(
            u'Enable option to render download section of the image '
            u'(if ftw.zipexport present has option to download the entire gallery zipped).'
        ),
        default=False
    )
