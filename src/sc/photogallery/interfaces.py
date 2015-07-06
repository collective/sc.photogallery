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

    enable_download = schema.Bool(
        title=_(u'Enable download?'),
        description=_(
            u'Enable download of original images in the Photo Gallery by using an explicit link. '
            u'If ftw.zipexport is installed, enable also downloading of a ZIP file with all the images.'
        ),
        default=False
    )
