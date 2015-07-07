# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from sc.photogallery import _
from sc.photogallery.interfaces import IPhotoGallerySettings


class PhotoGallerySettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IPhotoGallerySettings
    label = _(u'Photo Gallery')
    description = _(u'Settings for the sc.photogallery package')


class PhotoGallerySettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = PhotoGallerySettingsEditForm
