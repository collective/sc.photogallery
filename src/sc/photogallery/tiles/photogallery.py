# -*- coding: utf-8 -*-
from sc.photogallery import _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class IPhotoGalleryTile(IPersistentCoverTile):

    """A tile that shows a photo gallery."""

    uuid = schema.TextLine(
        title=_(u'UUID'),
        required=False,
        readonly=True,
    )


class PhotoGalleryTile(PersistentCoverTile):

    """A tile that shows a photo gallery."""

    implements(IPhotoGalleryTile)

    index = ViewPageTemplateFile('photogallery.pt')
    is_configurable = True
    is_editable = False
    is_droppable = True

    short_name = _(u'msg_short_name_photogallery', u'Photo Gallery')

    def accepted_ct(self):
        """Accept only Photo Gallery objects."""
        return ['Photo Gallery']

    def populate_with_object(self, obj):
        super(PhotoGalleryTile, self).populate_with_object(obj)  # check permissions

        if obj.portal_type in self.accepted_ct():
            uuid = IUUID(obj)
            data_mgr = ITileDataManager(self)
            data_mgr.set(dict(uuid=uuid))
