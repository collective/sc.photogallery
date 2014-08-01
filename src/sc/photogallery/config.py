# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'sc.photogallery'


class HiddenProfiles(object):

    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'sc.photogallery:uninstall',
            u'sc.photogallery.upgrades.v1010:default'
        ]
